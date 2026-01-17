from typing import List, Dict
import re

class NLPProcessor:
    def __init__(self):
        # Arabic and English keywords mapping to clinical concepts
        self.concepts = {
            "chest_pain": [
                "chest pain", "pain in chest", "tightness", "pressure", "angina",
                "ألم صدر", "وجع في صدري", "نغزة", "طبقة على صدري", "ذبحة", "حرقان في الصدر"
            ],
            "sob": [
                "short of breath", "cant breathe", "difficulty breathing", "dyspnea", "gasping",
                "ضيق تنفس", "مش عارف آخد نفسي", "كرشة نفس", "مخنوق", "نهجان"
            ],
            "trauma": [
                "fall", "hit", "accident", "crash", "fracture", "broken", "cut", "wound",
                "سقوط", "وقعت", "خبطت", "حادث", "كسر", "جرح", "نزيف", "تعويرة"
            ],
            "abdominal": [
                "stomach pain", "abdominal pain", "belly ache", "vomiting", "diarrhea",
                "وجع بطن", "مغص", "قيء", "ترجيع", "إسهال", "ألم في معدتي"
            ],
            "neuro": [
                "dindsy", "faint", "passed out", "seizure", "stroke", "numbness", "weakness",
                "دوخة", "إغماء", "تشنجات", "جلطة", "تنميل", "ضعف", "صداع شديد"
            ],
            "fever": [
                "fever", "hot", "temperature", "chills", "shivering",
                "حرارة", "سخونية", "رعشة", "حمى"
            ],
            "psych": [
                "suicidal", "kill myself", "hopeless", "voices", "hallucination", "aggressive",
                "انتحار", "هاقتل نفسي", "أصوات", "هلاوس", "عدواني", "مجنون"
            ],
            "allergy": [
                "allergy", "allergic", "rash", "hives", "swelling", "peanut", "bee",
                "حساسية", "طفح", "تورم", "حبوب", "قرصة", "نحل"
            ]
        }
        
        # Negation terms (simple check)
        self.negations = ["no ", "not ", "denies ", "without ", "لا ", "بدون ", "مافيش "]

    def extract_symptoms(self, text: str) -> List[str]:
        """
        Analyze text and return a list of identified symptom keys.
        """
        text = text.lower()
        detected = []
        
        for category, keywords in self.concepts.items():
            for kw in keywords:
                # Use regex with word boundary at the start to avoid partial matches
                # e.g. "instability" should not match "stab"
                if re.search(r'\b' + re.escape(kw), text):
                    detected.append(category)
                    break
        
        return detected

    def detect_danger_keywords(self, text: str) -> List[str]:
        """
        Specific check for Life-Threatening keywords (Level 1).
        """
        danger_terms = [
            "cardiac arrest", "unresponsive", "blue", "not breathing", "gunshot", "stab",
            "توقف القلب", "غير مستجيب", "أزرق", "قاطع نفس", "رصاص", "طعن", "سكينة"
        ]
        
        matches = []
        text = text.lower()
        for term in danger_terms:
            if re.search(r'\b' + re.escape(term), text):
                matches.append(term)
                
        return matches
