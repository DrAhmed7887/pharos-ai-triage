from ..models import PatientInput, TriageResult, TriageLevel, Vitals
from ..nlp.processor import NLPProcessor
from typing import List, Tuple

class TriageEngine:
    def __init__(self):
        self.nlp = NLPProcessor()
        
    def _check_vitals_danger_zone(self, age: int, vitals: Vitals) -> bool:
        """
        Check if vitals are in the danger zone based on age (ESI v5 Table).
        Returns True if upgrading to Level 2 is recommended.
        """
        hr = vitals.hr
        rr = vitals.rr
        spo2 = vitals.spo2
        
        if not hr or not rr or not spo2:
            return False

        # Pediatric Adjustments (Simplified for MVP based on ESI table)
        if age < 3/12: # < 3 months
             if hr > 180 or rr > 50 or spo2 < 92: return True
        elif age < 3: # 3 months to 3 years
             if hr > 160 or rr > 40 or spo2 < 92: return True
        elif age < 8: # 3-8 years
             if hr > 140 or rr > 30 or spo2 < 92: return True
        else: # > 8 years and adults
             if hr > 100 or rr > 20 or spo2 < 92: return True
        
        return False

    def _calculate_resources(self, patient: PatientInput, symptoms: List[str]) -> int:
        """
        Estimate resources needed based on complaint and vitals.
        Resources: Labs, ECG, X-Ray, CT/MRI, IV Fluids, IV Meds, Consult.
        Not Resources: History, Exam, PO Meds, Tetanus, Refill.
        """
        resources = 0
        
        # Symptom-based resource prediction
        if "abdominal" in symptoms or "fever" in symptoms:
            resources += 1 # Likely labs
        
        if "chest_pain" in symptoms or "sob" in symptoms:
            resources += 2 # ECG + Labs/CXR
            
        if "trauma" in symptoms or "neuro" in symptoms:
            resources += 1 # Imaging (X-ray/CT)
            
        if "abdominal" in symptoms: # Vomiting/Diarrhea implied
            resources += 1 # IV fluids potential

        if "allergy" in symptoms:
            resources += 1 # IV/IM Meds (Benadryl/Epi/Steroids)

        if patient.vitals.temp and patient.vitals.temp > 38.0:
            if "fever" not in symptoms: # Don't double count if fever already triggered labs
                 resources += 1 # Workup
            
        return resources

    def evaluate(self, patient: PatientInput) -> TriageResult:
        reasoning = []
        red_flags = []
        
        # NLP Analysis
        symptoms = self.nlp.extract_symptoms(patient.chief_complaint_text)
        danger_keywords = self.nlp.detect_danger_keywords(patient.chief_complaint_text)
        
        # --- Decision Point A: Resuscitation (Level 1) ---
        # Immediate life-saving intervention required?
        is_level_1 = False
        if patient.vitals.spo2 and patient.vitals.spo2 < 90:
            is_level_1 = True
            reasoning.append("SpO2 < 90% indicates severe hypoxia.")
        
        if patient.vitals.gcs and patient.vitals.gcs < 9: # Unresponsive
            is_level_1 = True
            reasoning.append("GCS < 9 indicates severe altered mental status.")

        if danger_keywords:
            is_level_1 = True
            reasoning.append(f"Critical keywords detected: {', '.join(danger_keywords)}")

        if is_level_1:
            return TriageResult(
                level=TriageLevel.RESUSCITATION,
                color_code="#ef4444", # Red
                label_ar="إنعاش (مستوى ١)",
                label_en="Resuscitation (Level 1)",
                description="Requires immediate life-saving intervention.",
                recommended_action="Activate resuscitation team immediately.",
                time_to_physician="Immediate",
                red_flags=red_flags,
                reasoning=reasoning
            )

        # --- Decision Point B: Emergent (Level 2) ---
        # High risk, confused, lethargic, severe pain/distress
        is_level_2 = False
        
        # Pain
        if patient.vitals.pain_score >= 7:
            is_level_2 = True
            reasoning.append("Severe pain score reported (>=7).")
            
        # Confusion
        if patient.vitals.gcs and patient.vitals.gcs < 15:
            is_level_2 = True
            reasoning.append("Altered mental status (GCS < 15).")
            
        # Danger Zone Vitals
        if self._check_vitals_danger_zone(patient.age, patient.vitals):
            is_level_2 = True
            reasoning.append("Vital signs in danger zone for age.")
            red_flags.append("Abnormal Vital Signs")
            
        # High Risk Symptoms
        # Dynamic check to provide specific reasoning
        high_risk_triggers = []
        if "chest_pain" in symptoms: high_risk_triggers.append("Chest Pain")
        if "stroke" in symptoms: high_risk_triggers.append("Stroke Symptoms")
        if "neuro" in symptoms: high_risk_triggers.append("Neurological Deficit")
        if "psych" in symptoms: high_risk_triggers.append("Psychiatric Emergency")
        
        if high_risk_triggers:
             is_level_2 = True
             reasoning.append(f"High-risk symptom(s) detected: {', '.join(high_risk_triggers)}")

        # Allergy Check
        if "allergy" in symptoms:
            # If respiratory distress or shock was found, Level 1 would already trigger above via keywords/vitals
            reasoning.append("Allergic reaction flagged - monitoring for anaphylaxis risk.")
            if not is_level_1 and (patient.vitals.rr and patient.vitals.rr > 22):
                 is_level_2 = True
                 reasoning.append("Allergy with elevated RR indicates potential airway compromise.")
            # If just stable allergy, might be Level 3 (meds) or 4.
            # ESI usually treats significant allergic reactions as Level 2/3. 
            # We'll default to checking resources later if stable, but flag it here.

        if is_level_2:
            return TriageResult(
                level=TriageLevel.EMERGENT,
                color_code="#f97316", # Orange
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
        
        # Vital sign check for Level 3 (if danger zone, already moved to 2)
        # But if vitals are dangerous, we already caught it.
        # If vitals are just 'abnormal' but not dangerous? ESI usually up-triage to 2 if danger zone.
        
        if resource_count >= 2:
            # Check vitals again just in case (Danger zone) - Done above.
            return TriageResult(
                level=TriageLevel.URGENT,
                color_code="#eab308", # Yellow
                label_ar="عاجل (مستوى ٣)",
                label_en="Urgent (Level 3)",
                description="Stable, requires multiple resources.",
                recommended_action="Room patient, order labs/imaging.",
                time_to_physician="< 60 mins",
                red_flags=red_flags,
                reasoning=[f"Predicted {resource_count} resources needed (Labs, Imaging, etc)."]  
            )
            
        elif resource_count == 1:
            return TriageResult(
                level=TriageLevel.LESS_URGENT,
                color_code="#22c55e", # Green
                label_ar="أقل إلحاحاً (مستوى ٤)",
                label_en="Less Urgent (Level 4)",
                description="Stable, requires one resource.",
                recommended_action="Fast track or clinic area.",
                time_to_physician="Can wait",
                red_flags=red_flags,
                reasoning=["Predicted only 1 resource needed."]
            )
            
        else: # 0 resources
            return TriageResult(
                level=TriageLevel.NON_URGENT,
                color_code="#3b82f6", # Blue
                label_ar="غير عاجل (مستوى ٥)",
                label_en="Non-Urgent (Level 5)",
                description="No resources needed.",
                recommended_action="Prescription refill or reassurance.",
                time_to_physician="Can wait / Refer to PCP",
                red_flags=red_flags,
                reasoning=["No acute resources predicted."]
            )
