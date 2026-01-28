from typing import List, Dict
import re

class NLPProcessor:
    def __init__(self):
        # Arabic and English keywords mapping to clinical concepts
        self.concepts = {
            "chest_pain": [
                "chest pain", "pain in chest", "tightness in chest", "chest tightness",
                "angina", "heart pain",
                "ألم صدر", "وجع في صدري", "نغزة في صدري", "طبقة على صدري", "ذبحة", "حرقان في الصدر"
            ],
            "sob": [
                "short of breath", "shortness of breath", "cant breathe", "can't breathe", 
                "difficulty breathing", "dyspnea", "gasping", "breathless",
                "ضيق تنفس", "مش عارف آخد نفسي", "مش عارفة آخد نفسي", "كرشة نفس", "مخنوق", "نهجان", "مش قادر اتنفس"
            ],
            "stroke": [
                "stroke", "face droop", "face drooping", "facial droop", "arm weakness", 
                "leg weakness", "slurred speech", "speech difficulty", "can't speak",
                "one side weak", "hemiparesis", "hemiplegia",
                "جلطة", "شلل", "وشي مايل", "مش قادر اتكلم"
            ],
            "trauma": [
                "fall", "fell", "hit", "accident", "crash", "fracture", "broken", 
                "wound", "injury", "swollen", "sprain",
                "سقوط", "وقعت", "خبطت", "حادث", "كسر", "نزيف", "تعويرة", "ورم"
            ],
            "abdominal": [
                "stomach pain", "abdominal pain", "belly ache", "belly pain",
                "vomiting", "diarrhea", "nausea",
                "وجع بطن", "مغص", "قيء", "ترجيع", "إسهال", "ألم في معدتي"
            ],
            "neuro": [
                "dizzy", "dizziness", "faint", "passed out", "seizure", 
                "numbness", "tingling", "weakness", "headache", "severe headache",
                "دوخة", "إغماء", "تشنجات", "تنميل", "ضعف", "صداع شديد"
            ],
            "fever": [
                "fever", "febrile", "temperature", "chills", "shivering",
                "حرارة", "سخونية", "رعشة", "حمى"
            ],
            "psych": [
                "suicidal", "kill myself", "hopeless", "voices", "hallucination", 
                "aggressive", "self harm", "want to die",
                "انتحار", "هاقتل نفسي", "أصوات", "هلاوس", "عدواني", "مجنون"
            ],
            "allergy": [
                "allergy", "allergic", "rash", "hives", "swelling face", 
                "swelling lips", "peanut", "bee sting",
                "حساسية", "طفح", "تورم", "حبوب", "قرصة نحل"
            ],
            "laceration": [
                "cut", "laceration", "wound", "bleeding", "stitches",
                "جرح", "قطع", "نزيف"
            ]
        }
        
        # Negation terms (simple check)
        self.negations = ["no ", "not ", "denies ", "without ", "لا ", "بدون ", "مافيش "]

    def extract_symptoms(self, text: str) -> List[str]:
        """
        Analyze text and return a list of identified symptom keys.
        """
        text_lower = text.lower()
        detected = []
        
        for category, keywords in self.concepts.items():
            for kw in keywords:
                # Use word boundary for English, direct search for Arabic
                if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower) or kw in text:
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
        text_lower = text.lower()
        for term in danger_terms:
            if re.search(r'\b' + re.escape(term.lower()) + r'\b', text_lower) or term in text:
                matches.append(term)
                
        return matches
