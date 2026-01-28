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
                "short of breath", "cant breathe", "can't breathe", "difficulty breathing", "dyspnea", "gasping",
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
                "dizzy", "faint", "passed out", "seizure", "stroke", "numbness", "weakness",
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
                if re.search(r'\b' + re.escape(kw), text):
                    detected.append(category)
                    break
        
        return detected

    def detect_danger_keywords(self, text: str) -> List[str]:
        """
        Specific check for Life-Threatening keywords (Level 1).
        """
        danger_terms = [
            # English - Critical/Life-threatening
            "cardiac arrest", "unresponsive", "unconscious", "not conscious", 
            "blue", "cyanotic", "not breathing", "stopped breathing", "apnea",
            "gunshot", "stab", "choking", "drowning", "hanging", "overdose",
            "seizure", "fitting", "convulsion", "anaphylaxis", "severe bleeding",
            "pulseless", "no pulse", "collapsed", "found down",
            # Arabic - Critical
            "توقف القلب", "غير مستجيب", "فاقد الوعي", "مغمى عليه", "إغماء",
            "أزرق", "قاطع نفس", "مش بيتنفس", "رصاص", "طعن", "سكينة",
            "تشنج", "شرقان", "غرق", "جرعة زيادة", "نزيف شديد"
        ]
        
        matches = []
        text = text.lower()
        for term in danger_terms:
            if re.search(r'\b' + re.escape(term), text):
                matches.append(term)
                
        return matches
