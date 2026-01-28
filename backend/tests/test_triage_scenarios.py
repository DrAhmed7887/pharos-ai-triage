"""
SAFE-Triage AI - Critical Scenario Testing
Tests common ER presentations against expected ESI levels
Includes Egyptian Arabic (عامية مصرية) scenarios
"""
import sys
sys.path.insert(0, '/Users/ahmedzayed/Downloads/safe-triage-project')

from backend.models import PatientInput, Vitals
from backend.logic.triage_engine import TriageEngine

engine = TriageEngine()

# Test scenarios: (description, patient_data, expected_level)
SCENARIOS = [
    # ========================================
    # LEVEL 1 - RESUSCITATION (إنعاش)
    # ========================================
    
    # English - Critical Keywords
    ("Unconscious patient", {
        "age": 55, "gender": "male",
        "chief_complaint_text": "unconscious, found on floor",
        "vitals": {}
    }, 1),
    
    ("Unresponsive patient", {
        "age": 40, "gender": "female",
        "chief_complaint_text": "unresponsive, not waking up",
        "vitals": {}
    }, 1),
    
    ("Cardiac arrest", {
        "age": 60, "gender": "male",
        "chief_complaint_text": "cardiac arrest, no pulse",
        "vitals": {}
    }, 1),
    
    ("Not breathing", {
        "age": 30, "gender": "male",
        "chief_complaint_text": "not breathing, blue lips",
        "vitals": {}
    }, 1),
    
    ("Active seizure", {
        "age": 25, "gender": "female",
        "chief_complaint_text": "seizure, convulsing now",
        "vitals": {}
    }, 1),
    
    ("Gunshot wound", {
        "age": 28, "gender": "male",
        "chief_complaint_text": "gunshot to abdomen",
        "vitals": {}
    }, 1),
    
    ("Stab wound", {
        "age": 32, "gender": "male",
        "chief_complaint_text": "stab wound to chest",
        "vitals": {}
    }, 1),
    
    ("Choking", {
        "age": 4, "gender": "male",
        "chief_complaint_text": "choking on food, can't breathe",
        "vitals": {}
    }, 1),
    
    ("Overdose", {
        "age": 22, "gender": "female",
        "chief_complaint_text": "overdose, took whole bottle of pills",
        "vitals": {}
    }, 1),
    
    ("Anaphylaxis", {
        "age": 30, "gender": "male",
        "chief_complaint_text": "anaphylaxis, throat swelling, ate peanuts",
        "vitals": {}
    }, 1),
    
    # Critical Vital Signs
    ("Severe bradycardia (HR < 40)", {
        "age": 70, "gender": "male",
        "chief_complaint_text": "feeling weak",
        "vitals": {"hr": 35, "rr": 16, "spo2": 95}
    }, 1),
    
    ("Respiratory failure (RR < 8)", {
        "age": 50, "gender": "female",
        "chief_complaint_text": "very sleepy after taking pills",
        "vitals": {"hr": 60, "rr": 4, "spo2": 88}
    }, 1),
    
    ("Severe hypoxia (SpO2 < 90)", {
        "age": 65, "gender": "male",
        "chief_complaint_text": "can't breathe",
        "vitals": {"hr": 110, "rr": 28, "spo2": 85}
    }, 1),
    
    ("Severe tachycardia (HR > 150)", {
        "age": 45, "gender": "male",
        "chief_complaint_text": "heart racing, dizzy",
        "vitals": {"hr": 180, "rr": 22, "spo2": 94}
    }, 1),
    
    ("Shock (SBP < 80)", {
        "age": 35, "gender": "female",
        "chief_complaint_text": "bleeding heavily",
        "vitals": {"hr": 130, "sbp": 70, "dbp": 40}
    }, 1),
    
    # Arabic - Critical (فاقد الوعي)
    ("Arabic - فاقد الوعي", {
        "age": 50, "gender": "male",
        "chief_complaint_text": "فاقد الوعي مش بيرد",
        "vitals": {}
    }, 1),
    
    ("Arabic - مغمى عليه", {
        "age": 45, "gender": "male",
        "chief_complaint_text": "مغمى عليه في الشارع",
        "vitals": {}
    }, 1),
    
    ("Arabic - مش بيتنفس", {
        "age": 60, "gender": "female",
        "chief_complaint_text": "نفسه واقف مش بيتنفس",
        "vitals": {}
    }, 1),
    
    ("Arabic - تشنجات", {
        "age": 30, "gender": "male",
        "chief_complaint_text": "بيتشنج على الأرض",
        "vitals": {}
    }, 1),
    
    ("Arabic - طعن", {
        "age": 25, "gender": "male",
        "chief_complaint_text": "اتطعن بسكينة في بطنه",
        "vitals": {}
    }, 1),
    
    ("Arabic - جرعة زيادة", {
        "age": 20, "gender": "female",
        "chief_complaint_text": "بلعت حبوب كتير جرعة زيادة",
        "vitals": {}
    }, 1),
    
    ("Arabic - شرقان", {
        "age": 3, "gender": "male",
        "chief_complaint_text": "الاكل وقف في زوره شرقان",
        "vitals": {}
    }, 1),
    
    ("Arabic - ضربة شمس", {
        "age": 40, "gender": "male",
        "chief_complaint_text": "ضربته الشمس وهو شغال",
        "vitals": {}
    }, 1),
    
    ("Arabic - نزيف شديد", {
        "age": 35, "gender": "female",
        "chief_complaint_text": "بتنزف جامد الدم مش واقف",
        "vitals": {}
    }, 1),
    
    # ========================================
    # LEVEL 2 - EMERGENT (طوارئ)
    # ========================================
    
    # English - High Risk
    ("Chest pain - adult", {
        "age": 55, "gender": "male",
        "chief_complaint_text": "severe chest pain radiating to arm",
        "vitals": {"hr": 90, "rr": 18, "spo2": 96, "pain_score": 8}
    }, 2),
    
    ("Stroke symptoms", {
        "age": 70, "gender": "female",
        "chief_complaint_text": "face drooping, can't move left arm, slurred speech",
        "vitals": {"hr": 88, "rr": 16, "spo2": 97}
    }, 2),
    
    ("Difficulty breathing (stable SpO2)", {
        "age": 45, "gender": "male",
        "chief_complaint_text": "short of breath, getting worse",
        "vitals": {"hr": 100, "rr": 24, "spo2": 93}
    }, 2),
    
    ("Severe abdominal pain", {
        "age": 60, "gender": "female",
        "chief_complaint_text": "severe stomach pain, worst of my life",
        "vitals": {"hr": 95, "rr": 20, "pain_score": 9}
    }, 2),
    
    ("Suicidal ideation", {
        "age": 25, "gender": "male",
        "chief_complaint_text": "suicidal, wants to kill myself",
        "vitals": {}
    }, 2),
    
    ("High pain score (>=7)", {
        "age": 40, "gender": "female",
        "chief_complaint_text": "severe back pain",
        "vitals": {"pain_score": 8}
    }, 2),
    
    ("Altered mental status (GCS 12)", {
        "age": 75, "gender": "male",
        "chief_complaint_text": "confused, not making sense",
        "vitals": {"gcs": 12}
    }, 2),
    
    # Arabic - High Risk
    ("Arabic - ألم صدر شديد", {
        "age": 60, "gender": "male",
        "chief_complaint_text": "صدري بيوجعني جامد حاسس بضغط",
        "vitals": {"pain_score": 8}
    }, 2),
    
    ("Arabic - مش عارف آخد نفسي", {
        "age": 40, "gender": "female",
        "chief_complaint_text": "مش عارفة آخد نفسي مخنوقة",
        "vitals": {}
    }, 2),
    
    ("Arabic - جلطة", {
        "age": 65, "gender": "male",
        "chief_complaint_text": "وشه مايل ومش قادر يتكلم",
        "vitals": {}
    }, 2),
    
    ("Arabic - عايز يموت", {
        "age": 22, "gender": "male",
        "chief_complaint_text": "عايز اموت مش عايز اعيش",
        "vitals": {}
    }, 2),
    
    ("Arabic - حامل وبتنزف", {
        "age": 28, "gender": "female",
        "chief_complaint_text": "انا حامل وبنزف",
        "vitals": {}
    }, 2),
    
    ("Arabic - السكر واطي", {
        "age": 55, "gender": "male",
        "chief_complaint_text": "السكر واطي وبيرعش",
        "vitals": {}
    }, 2),
    
    ("Arabic - قلبي بيدق جامد", {
        "age": 45, "gender": "female",
        "chief_complaint_text": "قلبي بيدق جامد وحاسة بدوخة",
        "vitals": {}
    }, 2),
    
    # ========================================
    # LEVEL 3 - URGENT (عاجل)
    # ========================================
    
    ("Abdominal pain with fever", {
        "age": 35, "gender": "female",
        "chief_complaint_text": "stomach pain and fever for 2 days",
        "vitals": {"hr": 85, "rr": 16, "temp": 38.5, "pain_score": 5}
    }, 3),
    
    ("Minor trauma with pain", {
        "age": 28, "gender": "male",
        "chief_complaint_text": "fell off bike, ankle swollen",
        "vitals": {"pain_score": 5}
    }, 3),
    
    # Arabic - Urgent
    ("Arabic - وجع بطن ومغص", {
        "age": 30, "gender": "female",
        "chief_complaint_text": "بطني بتوجعني ومغص شديد",
        "vitals": {}
    }, 3),
    
    ("Arabic - وقعت وايدي وارمة", {
        "age": 40, "gender": "male",
        "chief_complaint_text": "وقعت من السلم وايدي وارمة",
        "vitals": {}
    }, 3),
    
    # ========================================
    # LEVEL 4 - LESS URGENT (أقل إلحاحاً)
    # ========================================
    
    ("Simple laceration", {
        "age": 30, "gender": "male",
        "chief_complaint_text": "cut on hand, needs stitches",
        "vitals": {}
    }, 4),
    
    ("Mild fever", {
        "age": 25, "gender": "female",
        "chief_complaint_text": "fever and sore throat",
        "vitals": {"temp": 38.2}
    }, 4),
    
    # Arabic - Less Urgent
    ("Arabic - جرح محتاج غرز", {
        "age": 35, "gender": "male",
        "chief_complaint_text": "ايدي اتقطعت محتاج غرز",
        "vitals": {}
    }, 4),
    
    ("Arabic - سخونية", {
        "age": 20, "gender": "female",
        "chief_complaint_text": "عندي سخونية وزوري بيوجعني",
        "vitals": {}
    }, 4),
    
    # ========================================
    # LEVEL 5 - NON-URGENT (غير عاجل)
    # ========================================
    
    ("Prescription refill", {
        "age": 45, "gender": "male",
        "chief_complaint_text": "need refill of blood pressure medication",
        "vitals": {}
    }, 5),
    
    ("Minor complaint", {
        "age": 30, "gender": "female",
        "chief_complaint_text": "runny nose for 3 days",
        "vitals": {}
    }, 5),
    
    # Arabic - Non-Urgent
    ("Arabic - عايز روشتة", {
        "age": 50, "gender": "male",
        "chief_complaint_text": "عايز اجدد روشتة الضغط",
        "vitals": {}
    }, 5),
    
    ("Arabic - برد خفيف", {
        "age": 25, "gender": "female",
        "chief_complaint_text": "عندي برد خفيف ورشح",
        "vitals": {}
    }, 5),
]

def run_tests():
    print("=" * 70)
    print("SAFE-Triage AI - Scenario Testing (اختبار السيناريوهات)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    failures = []
    
    for description, data, expected_level in SCENARIOS:
        # Build PatientInput
        vitals_data = data.get("vitals", {})
        vitals = Vitals(
            hr=vitals_data.get("hr"),
            rr=vitals_data.get("rr"),
            spo2=vitals_data.get("spo2"),
            sbp=vitals_data.get("sbp"),
            dbp=vitals_data.get("dbp"),
            temp=vitals_data.get("temp"),
            gcs=vitals_data.get("gcs"),
            pain_score=vitals_data.get("pain_score", 0)
        )
        
        patient = PatientInput(
            age=data["age"],
            gender=data["gender"],
            chief_complaint_text=data["chief_complaint_text"],
            vitals=vitals
        )
        
        # Run triage
        result = engine.evaluate(patient)
        actual_level = result.level.value
        
        # Check result
        if actual_level == expected_level:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
            failures.append({
                "description": description,
                "complaint": data["chief_complaint_text"],
                "expected": expected_level,
                "actual": actual_level,
                "reasoning": result.reasoning
            })
        
        print(f"{status} | {description}")
        print(f"       Expected: Level {expected_level} | Got: Level {actual_level}")
        if actual_level != expected_level:
            print(f"       Reasoning: {result.reasoning}")
        print()
    
    # Summary
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(SCENARIOS)} tests")
    print(f"النتائج: {passed} نجح، {failed} فشل من {len(SCENARIOS)} اختبار")
    print("=" * 70)
    
    if failures:
        print("\n❌ FAILED SCENARIOS (السيناريوهات الفاشلة):")
        for f in failures:
            print(f"\n  {f['description']}")
            print(f"    Complaint: {f['complaint']}")
            print(f"    Expected Level {f['expected']}, Got Level {f['actual']}")
            print(f"    Reasoning: {f['reasoning']}")
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
