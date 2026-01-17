import requests
import json
import time

BASE_URL = "http://localhost:8000/triage"

def run_test(name, data, expected_level_range):
    print(f"\n--- Testing: {name} ---")
    try:
        response = requests.post(BASE_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            level = result['level']
            print(f"Result Level: {level}")
            
            # DB Persistence check skipped (Client-Side Storage)
            
            if level in expected_level_range:
                print("✅ PASS")
            else:
                print(f"❌ FAIL (Expected {expected_level_range}, got {level})")
        else:
            print(f"❌ FAIL (API Error: {response.status_code})")
            print(response.text)
    except Exception as e:
        print(f"❌ FAIL (Exception: {str(e)})")

scenarios = [
    {
        "name": "STEMI Chest Pain (Level 1/2)",
        "data": {
            "age": 55, "gender": "male",
            "chief_complaint_text": "Severe chest pain radiating to left arm, sweating",
            "vitals": { "hr": 110, "rr": 24, "spo2": 94, "sbp": 160, "pain_score": 9 },
            "history_cardiac": True
        },
        "expected": [1, 2] # Likely 2 unless shock
    },
    {
        "name": "Abdominal Pain (Level 3)",
        "data": {
            "age": 30, "gender": "female",
            "chief_complaint_text": "Stomach pain and vomiting since morning",
            "vitals": { "hr": 90, "rr": 18, "spo2": 99, "sbp": 120, "pain_score": 5 }
        },
        "expected": [3] # Needs labs/fluids (2 resources)
    },
    {
        "name": "Pediatric Fever - High Risk (Level 2)",
        "data": {
            "age": 0.2, "gender": "male", # 2 months old (0.2 years)
            "chief_complaint_text": "High fever and not feeding well",
            "vitals": { "hr": 190, "rr": 60, "spo2": 95, "temp": 39.0 }
        },
        "expected": [2] # HR > 180 for < 3mo is danger zone
    },
    {
        "name": "Ankle Sprain (Level 4/5)",
        "data": {
            "age": 20, "gender": "male",
            "chief_complaint_text": "Twisted ankle while playing football",
            "vitals": { "hr": 70, "rr": 16, "spo2": 100, "pain_score": 3, "temp": 37.0 }
        },
        "expected": [4, 5] # X-ray only -> Level 4. If no x-ray needed -> Level 5.
    },
    {
        "name": "Psychiatric - Suicidal (Level 2)",
        "data": {
            "age": 25, "gender": "female",
            "chief_complaint_text": "Feeling suicidal and hopeless",
            "vitals": { "hr": 80, "rr": 16, "spo2": 99, "gcs": 15 }
        },
        "expected": [2] # High risk
    },
    {
        "name": "Allergy - Stable (Level 3/4)",
        "data": {
            "age": 30, "gender": "male",
            "chief_complaint_text": "I ate peanuts and have a rash",
            "vitals": { "hr": 90, "rr": 18, "spo2": 98 }
        },
        "expected": [3, 4] # Needs meds (1 resource) -> 4, or 2 resources -> 3
    },
     {
        "name": "Arabic: Severe SOB (Level 1/2)",
        "data": {
            "age": 60, "gender": "male",
            "chief_complaint_text": "عندي ضيق تنفس شديد ومش قادر اتكلم",
            "vitals": { "hr": 120, "rr": 35, "spo2": 88 } # SpO2 < 90 -> Level 1
        },
        "expected": [1]
    }
]

if __name__ == "__main__":
    for s in scenarios:
        run_test(s['name'], s['data'], s['expected'])
