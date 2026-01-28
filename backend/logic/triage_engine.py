from ..models import PatientInput, TriageResult, TriageLevel, Vitals
from ..nlp.processor import NLPProcessor
from typing import List, Tuple

class TriageEngine:
    def __init__(self):
        self.nlp = NLPProcessor()
        
    def _check_critical_vitals(self, vitals: Vitals) -> Tuple[bool, List[str]]:
        """
        Check for immediately life-threatening vital signs (Level 1).
        Returns (is_critical, list of reasons)
        """
        reasons = []
        
        # Respiratory Rate - Critical
        if vitals.rr is not None:
            if vitals.rr < 8:
                reasons.append(f"Critical: RR {vitals.rr} (< 8 = respiratory failure)")
            elif vitals.rr > 36:
                reasons.append(f"Critical: RR {vitals.rr} (> 36 = severe respiratory distress)")
        
        # Heart Rate - Critical
        if vitals.hr is not None:
            if vitals.hr < 40:
                reasons.append(f"Critical: HR {vitals.hr} (< 40 = severe bradycardia)")
            elif vitals.hr > 150:
                reasons.append(f"Critical: HR {vitals.hr} (> 150 = unstable tachycardia)")
        
        # SpO2 - Critical
        if vitals.spo2 is not None and vitals.spo2 < 90:
            reasons.append(f"Critical: SpO2 {vitals.spo2}% (< 90% = severe hypoxia)")
        
        # GCS - Critical
        if vitals.gcs is not None and vitals.gcs < 9:
            reasons.append(f"Critical: GCS {vitals.gcs} (< 9 = comatose)")
        
        # Blood Pressure - Critical
        if vitals.sbp is not None:
            if vitals.sbp < 80:
                reasons.append(f"Critical: SBP {vitals.sbp} (< 80 = shock)")
            elif vitals.sbp > 220:
                reasons.append(f"Critical: SBP {vitals.sbp} (> 220 = hypertensive emergency)")
        
        return (len(reasons) > 0, reasons)
        
    def _check_vitals_danger_zone(self, age: int, vitals: Vitals) -> Tuple[bool, List[str]]:
        """
        Check if vitals are in the danger zone based on age (ESI v5 Table).
        Returns (is_danger, list of reasons) for Level 2.
        """
        reasons = []
        hr = vitals.hr
        rr = vitals.rr
        spo2 = vitals.spo2
        
        # Adults
        if age >= 8:
            if hr and (hr > 100 or hr < 50):
                reasons.append(f"Abnormal HR: {hr}")
            if rr and (rr > 20 or rr < 10):
                reasons.append(f"Abnormal RR: {rr}")
            if spo2 and spo2 < 94:
                reasons.append(f"Low SpO2: {spo2}%")
        # Pediatric (simplified)
        elif age < 3:
            if hr and hr > 160:
                reasons.append(f"Pediatric tachycardia: HR {hr}")
            if rr and rr > 40:
                reasons.append(f"Pediatric tachypnea: RR {rr}")
        
        return (len(reasons) > 0, reasons)

    def _calculate_resources(self, patient: PatientInput, symptoms: List[str]) -> int:
        """
        Estimate resources needed based on complaint and vitals.
        """
        resources = 0
        
        if "abdominal" in symptoms:
            resources += 2  # Labs + possible imaging
        
        if "chest_pain" in symptoms or "sob" in symptoms:
            resources += 2  # ECG + Labs/CXR
            
        if "trauma" in symptoms:
            resources += 2  # X-ray + possible labs
            
        if "fever" in symptoms:
            resources += 1  # Labs
            
        if "laceration" in symptoms:
            resources += 1  # Suture supplies

        if "allergy" in symptoms:
            resources += 1  # IV/IM Meds
            
        return resources

    def evaluate(self, patient: PatientInput) -> TriageResult:
        reasoning = []
        red_flags = []
        
        # NLP Analysis
        symptoms = self.nlp.extract_symptoms(patient.chief_complaint_text)
        danger_keywords = self.nlp.detect_danger_keywords(patient.chief_complaint_text)
        
        # --- Decision Point A: Resuscitation (Level 1) ---
        is_level_1 = False
        
        # Check critical vital signs FIRST
        vitals_critical, vitals_reasons = self._check_critical_vitals(patient.vitals)
        if vitals_critical:
            is_level_1 = True
            reasoning.extend(vitals_reasons)
            red_flags.extend(vitals_reasons)

        # Check danger keywords (unconscious, unresponsive, etc.)
        if danger_keywords:
            is_level_1 = True
            reasoning.append(f"Critical keywords: {', '.join(danger_keywords)}")
            red_flags.append(f"Critical: {', '.join(danger_keywords)}")

        if is_level_1:
            return TriageResult(
                level=TriageLevel.RESUSCITATION,
                color_code="#ef4444",
                label_ar="إنعاش (مستوى ١)",
                label_en="Resuscitation (Level 1)",
                description="Requires immediate life-saving intervention.",
                recommended_action="Activate resuscitation team immediately.",
                time_to_physician="Immediate",
                red_flags=red_flags,
                reasoning=reasoning
            )

        # --- Decision Point B: Emergent (Level 2) ---
        is_level_2 = False
        
        # Severe Pain
        if patient.vitals.pain_score and patient.vitals.pain_score >= 7:
            is_level_2 = True
            reasoning.append(f"Severe pain: {patient.vitals.pain_score}/10")
            
        # Altered mental status (GCS 9-14)
        if patient.vitals.gcs and 9 <= patient.vitals.gcs < 15:
            is_level_2 = True
            reasoning.append(f"Altered mental status: GCS {patient.vitals.gcs}")
            
        # Danger Zone Vitals (not critical but concerning)
        danger_zone, danger_reasons = self._check_vitals_danger_zone(patient.age, patient.vitals)
        if danger_zone:
            is_level_2 = True
            reasoning.extend(danger_reasons)
            red_flags.append("Abnormal Vital Signs")
            
        # High Risk Symptoms
        high_risk_triggers = []
        if "chest_pain" in symptoms: high_risk_triggers.append("Chest Pain")
        if "stroke" in symptoms: high_risk_triggers.append("Stroke Symptoms")
        if "psych" in symptoms: high_risk_triggers.append("Psychiatric Emergency")
        if "sob" in symptoms: high_risk_triggers.append("Shortness of Breath")
        
        if high_risk_triggers:
            is_level_2 = True
            reasoning.append(f"High-risk: {', '.join(high_risk_triggers)}")

        if is_level_2:
            return TriageResult(
                level=TriageLevel.EMERGENT,
                color_code="#f97316",
                label_ar="طوارئ (مستوى ٢)",
                label_en="Emergent (Level 2)",
                description="High risk, potential for rapid deterioration.",
                recommended_action="Place in acute care bed, continuous monitoring.",
                time_to_physician="< 15 mins",
                red_flags=red_flags,
                reasoning=reasoning
            )

        # --- Decision Point C: Resources (Level 3, 4, 5) ---
        resource_count = self._calculate_resources(patient, symptoms)
        
        if resource_count >= 2:
            return TriageResult(
                level=TriageLevel.URGENT,
                color_code="#eab308",
                label_ar="عاجل (مستوى ٣)",
                label_en="Urgent (Level 3)",
                description="Stable, requires multiple resources.",
                recommended_action="Room patient, order labs/imaging.",
                time_to_physician="< 60 mins",
                red_flags=red_flags,
                reasoning=[f"Estimated {resource_count} resources needed."]  
            )
            
        elif resource_count == 1:
            return TriageResult(
                level=TriageLevel.LESS_URGENT,
                color_code="#22c55e",
                label_ar="أقل إلحاحاً (مستوى ٤)",
                label_en="Less Urgent (Level 4)",
                description="Stable, requires one resource.",
                recommended_action="Fast track or clinic area.",
                time_to_physician="Can wait",
                red_flags=red_flags,
                reasoning=["Estimated 1 resource needed."]
            )
            
        else:
            return TriageResult(
                level=TriageLevel.NON_URGENT,
                color_code="#3b82f6",
                label_ar="غير عاجل (مستوى ٥)",
                label_en="Non-Urgent (Level 5)",
                description="No resources needed.",
                recommended_action="Prescription refill or reassurance.",
                time_to_physician="Can wait / Refer to PCP",
                red_flags=red_flags,
                reasoning=["No acute resources predicted."]
            )
