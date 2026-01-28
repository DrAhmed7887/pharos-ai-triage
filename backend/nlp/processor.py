from typing import List, Dict
import re

class NLPProcessor:
    """
    NLP Processor for Egyptian Emergency Triage
    Includes Egyptian Arabic (Masri) slang and medical terms
    """
    def __init__(self):
        # Arabic and English keywords mapping to clinical concepts
        # Egyptian Arabic (عامية مصرية) included
        self.concepts = {
            "chest_pain": [
                # English
                "chest pain", "pain in chest", "tightness in chest", "chest tightness",
                "angina", "heart pain", "heart attack", "mi", "acs",
                # Arabic - Standard
                "ألم صدر", "ألم في الصدر", "ذبحة صدرية",
                # Egyptian Slang
                "وجع في صدري", "صدري بيوجعني", "نغزة في صدري", "نغز في قلبي",
                "طبقة على صدري", "حاسس بضغط على صدري", "قلبي بيوجعني",
                "حرقان في صدري", "صدري تقيل", "مش قادر اتنفس من صدري"
            ],
            "sob": [
                # English
                "short of breath", "shortness of breath", "cant breathe", "can't breathe", 
                "difficulty breathing", "dyspnea", "gasping", "breathless", "wheezing",
                "asthma", "asthma attack", "copd", "respiratory distress",
                # Arabic - Standard
                "ضيق تنفس", "صعوبة في التنفس",
                # Egyptian Slang
                "مش عارف آخد نفسي", "مش عارفة آخد نفسي", "مش قادر اتنفس",
                "نفسي ضيق", "كرشة نفس", "مخنوق", "مخنوقة", "نهجان", "نهجانة",
                "بلهث", "مش لاقي نفسي", "نفسي واقف", "بتنهج", "ربو", "ازمة ربو"
            ],
            "stroke": [
                # English
                "stroke", "cva", "face droop", "face drooping", "facial droop", 
                "arm weakness", "leg weakness", "slurred speech", "speech difficulty", 
                "can't speak", "one side weak", "hemiparesis", "hemiplegia", "tia",
                # Arabic - Standard
                "جلطة", "جلطة دماغية", "سكتة دماغية",
                # Egyptian Slang
                "وشه مايل", "وشي مايل", "بقه اتلوى", "ايده مش بتتحرك",
                "رجله مش بتتحرك", "نص جسمه مش بيتحرك", "مش قادر يتكلم",
                "بيرطن", "لسانه اتلت", "كلامه مش مفهوم"
            ],
            "trauma": [
                # English
                "fall", "fell", "hit", "accident", "crash", "fracture", "broken", 
                "wound", "injury", "swollen", "sprain", "motorcycle", "car accident",
                "rta", "road traffic", "head injury", "blunt trauma",
                # Arabic - Standard
                "سقوط", "كسر", "إصابة", "حادث",
                # Egyptian Slang
                "وقعت", "وقع", "طاحت", "خبطت", "خبط", "اتخبط", "اتخبطت",
                "حادثة", "حادثة عربية", "موتوسيكل", "عربية خبطته",
                "اتكسر", "رجلي اتكسرت", "ايدي اتكسرت", "ورم", "وارم", "وارمة",
                "التوا", "رجلي اتلوت", "سقالة", "من فوق", "اتضرب"
            ],
            "abdominal": [
                # English
                "stomach pain", "abdominal pain", "belly ache", "belly pain",
                "vomiting", "diarrhea", "nausea", "food poisoning", "appendix",
                "appendicitis", "gastro", "gi bleed",
                # Arabic - Standard
                "ألم بطن", "ألم في البطن", "قيء", "إسهال",
                # Egyptian Slang
                "وجع بطن", "بطني بتوجعني", "مغص", "مغص شديد",
                "بترجع", "برجع", "ترجيع", "استفراغ", "اسهال", "بطني ماشية",
                "معدتي وجعاني", "تسمم", "أكل باظ", "فسيخ", "رنجة",
                "الاكل مش طالع", "بطني منفوخة", "الزايدة"
            ],
            "neuro": [
                # English
                "dizzy", "dizziness", "faint", "fainting", "vertigo",
                "numbness", "tingling", "weakness", "headache", "severe headache",
                "migraine", "worst headache",
                # Arabic - Standard
                "دوخة", "صداع", "تنميل",
                # Egyptian Slang
                "دايخ", "دايخة", "راسي بيدور", "الدنيا بتلف",
                "صداع جامد", "راسي بتوجعني", "راسي هتنفجر",
                "ايدي بتنمل", "رجلي بتنمل", "حاسس بتنميل",
                "ضعف", "جسمي تعبان", "مش قادر اقف"
            ],
            "fever": [
                # English
                "fever", "febrile", "temperature", "chills", "shivering", "hot",
                "high temperature", "pyrexia",
                # Arabic - Standard
                "حرارة", "حمى",
                # Egyptian Slang
                "سخونية", "سخونيته عالية", "جسمه حر", "جسمي ولع",
                "رعشة", "بيرعش", "برد ورعشة", "حرارته مرتفعة",
                "الحرارة عالية", "نار", "جسمه نار"
            ],
            "psych": [
                # English
                "suicidal", "kill myself", "hopeless", "voices", "hallucination", 
                "aggressive", "self harm", "want to die", "cutting myself",
                "psychosis", "manic", "depressed", "anxiety attack", "panic attack",
                # Arabic - Standard
                "انتحار", "اكتئاب", "هلاوس",
                # Egyptian Slang
                "عايز اموت", "عايزة اموت", "هاقتل نفسي", "مش عايز اعيش",
                "بسمع أصوات", "شايف حاجات", "عدواني", "بيضرب", "هايج",
                "مجنون", "اعصابي تعبتني", "قلقان جدا", "خايف جدا"
            ],
            "allergy": [
                # English
                "allergy", "allergic", "rash", "hives", "swelling face", 
                "swelling lips", "peanut", "bee sting", "anaphylaxis", "epipen",
                # Arabic - Standard
                "حساسية", "طفح جلدي",
                # Egyptian Slang
                "عندي حساسية", "جسمي طلع حبوب", "وشي ورم",
                "شفايفي ورمت", "قرصة نحل", "النحل قرصني",
                "حكة", "جسمي بيحكني", "جلدي احمر"
            ],
            "laceration": [
                # English
                "cut", "laceration", "wound", "stitches", "bleeding", "gash",
                "sliced", "knife cut",
                # Arabic - Standard
                "جرح", "نزيف",
                # Egyptian Slang
                "اتقطعت", "ايدي اتقطعت", "جرح عميق", "بينزف",
                "محتاج غرز", "سكينة جرحتني", "زجاج قطعني"
            ],
            "burn": [
                # English
                "burn", "burned", "burnt", "boiling water", "scald", "fire burn",
                "chemical burn", "electrical burn",
                # Arabic - Standard
                "حرق", "حروق",
                # Egyptian Slang
                "اتحرقت", "اتحرق", "ميه سخنة", "الميه السخنة حرقتني",
                "النار حرقتني", "الزيت حرقني", "كهربا"
            ],
            "bite_sting": [
                # English
                "scorpion", "snake bite", "snake", "venom", "scorpion sting",
                "dog bite", "cat bite", "animal bite", "spider bite",
                # Arabic - Standard
                "عقرب", "ثعبان", "لدغة",
                # Egyptian Slang
                "العقرب قرصني", "قرصة عقرب", "تعبان عضني", "عضة تعبان",
                "كلب عضني", "قطة عضتني", "حيوان عضني"
            ],
            "pregnancy": [
                # English
                "pregnant", "pregnancy", "labor", "contractions", "water broke",
                "bleeding pregnant", "miscarriage", "ectopic", "delivery",
                # Arabic - Standard
                "حامل", "حمل", "ولادة",
                # Egyptian Slang
                "انا حامل", "الطلق جالي", "طلق", "الميه نزلت",
                "بنزف وانا حامل", "البيبي جاي", "مغص ولادة"
            ],
            "diabetic": [
                # English
                "diabetic", "diabetes", "hypoglycemia", "hyperglycemia", 
                "sugar low", "sugar high", "dka", "ketoacidosis",
                "shaking sweating confused",
                # Arabic - Standard
                "سكري", "السكر",
                # Egyptian Slang
                "السكر واطي", "سكري واطي", "السكر عالي", "سكري عالي",
                "السكر نزل", "حاسس بدوخة وعرق", "السكر طالع"
            ],
            "cardiac": [
                # English
                "palpitations", "heart racing", "irregular heartbeat", "arrhythmia",
                "afib", "heart flutter", "skipped beat",
                # Arabic - Standard
                "خفقان", "عدم انتظام ضربات القلب",
                # Egyptian Slang
                "قلبي بيدق جامد", "قلبي بيخبط", "قلبي بيرفرف",
                "حاسس بدقات قلبي", "قلبي واقف"
            ],
            "hypertension": [
                # English
                "bp high", "bp very high", "high blood pressure", 
                "hypertensive crisis", "hypertension",
                # Arabic - Standard
                "ضغط عالي", "ارتفاع ضغط الدم",
                # Egyptian Slang
                "الضغط عالي", "ضغطي عالي", "الضغط طالع"
            ],
            "hypotension": [
                # English
                "bp low", "low blood pressure", "feeling faint", "lightheaded",
                # Arabic - Standard
                "ضغط واطي",
                # Egyptian Slang  
                "الضغط واطي", "ضغطي واطي", "الضغط نازل"
            ],
            "eye": [
                # English
                "chemical in eye", "metal in eye", "eye injury", "chemical splash",
                "can't see", "vision loss", "eye pain",
                # Arabic - Standard
                "إصابة العين",
                # Egyptian Slang
                "حاجة دخلت عيني", "عيني بتوجعني", "مش شايف",
                "كيماوي في عيني", "حديدة في عيني"
            ],
            "uti": [
                # English
                "uti", "urinary", "burning urination", "blood in urine",
                "kidney pain", "flank pain",
                # Arabic - Standard
                "التهاب مجرى البول",
                # Egyptian Slang
                "حرقان في البول", "بول بدم", "وجع في الكلى",
                "ضهري بيوجعني", "مش قادر ابول"
            ],
            "respiratory_infection": [
                # English
                "cough", "pneumonia", "bronchitis", "sputum", "cold", "flu",
                "covid", "corona",
                # Arabic - Standard
                "كحة", "التهاب رئوي",
                # Egyptian Slang
                "كحة جامدة", "بكح دم", "صدري تعبني", "برد", "انفلونزا",
                "كورونا", "بلغم"
            ],
            "pediatric": [
                # English
                "child", "baby", "infant", "not eating", "dry mouth",
                "not drinking", "lethargic baby", "floppy baby",
                # Arabic - Standard
                "طفل", "رضيع",
                # Egyptian Slang
                "الطفل", "البيبي", "الواد", "البنت",
                "مش بياكل", "مش بيشرب", "العيل تعبان",
                "البيبي نايم كتير", "مش بيرضع"
            ],
            "heat": [
                # English
                "heat stroke", "sunstroke", "collapsed in sun", "heat exhaustion",
                # Arabic - Standard
                "ضربة شمس", "ضربة الشمس",
                # Egyptian Slang
                "ضربته الشمس", "ضربتها الشمس", "الشمس ضربته", "الشمس ضربتها",
                "قعد في الشمس كتير", "الحر جابله"
            ],
            "ear": [
                # English
                "ear pain", "earache", "ear infection", "otitis",
                # Arabic - Standard
                "ألم الأذن",
                # Egyptian Slang
                "ودني بتوجعني", "التهاب في ودني"
            ],
            "dental": [
                # English
                "tooth pain", "toothache", "dental", "abscess",
                # Arabic - Standard
                "ألم الأسنان",
                # Egyptian Slang
                "سناني بتوجعني", "ضرسي بيوجعني", "خراج في سناني"
            ],
            "back_pain": [
                # English
                "back pain", "lower back", "sciatica", "spine",
                # Arabic - Standard
                "ألم الظهر",
                # Egyptian Slang
                "ضهري بيوجعني", "وجع في ضهري", "الديسك"
            ]
        }
        
        # Negation terms
        self.negations = [
            "no ", "not ", "denies ", "without ", "never ",
            "لا ", "بدون ", "مافيش ", "مش ", "ما عنديش "
        ]

    def extract_symptoms(self, text: str) -> List[str]:
        """
        Analyze text and return a list of identified symptom keys.
        """
        text_lower = text.lower()
        detected = []
        
        for category, keywords in self.concepts.items():
            for kw in keywords:
                # Check both lowercase match and original (for Arabic)
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
            "gunshot", "stab", "stabbed", "choking", "drowning", "hanging", 
            "overdose", "seizure", "fitting", "convulsion", "convulsing", 
            "anaphylaxis", "severe bleeding", "massive bleeding",
            "pulseless", "no pulse", "collapsed", "found down", "found unresponsive",
            "heat stroke", "sunstroke", "electrocution", "drowning",
            # Trauma - severe
            "amputation", "evisceration", "impaled",
            # Pregnancy emergencies
            "cord prolapse", "placenta abruption",
            
            # Arabic - Standard Critical
            "توقف القلب", "غير مستجيب", "فاقد الوعي", 
            
            # Egyptian Slang - Critical
            "مغمى عليه", "مغمى عليها", "مش بيرد", "مش بترد",
            "إغماء", "اغمى عليه", "وقع مغمى عليه",
            "أزرق", "لونه ازرق", "شفايفه زرقا",
            "قاطع نفس", "مش بيتنفس", "نفسه واقف",
            "رصاص", "اتضرب بالنار", "طلق ناري",
            "طعن", "سكينة", "اتطعن",
            "تشنج", "بيتشنج", "تشنجات",
            "شرقان", "الاكل وقف في زوره", "مش قادر يبلع",
            "غرق", "كان هيغرق",
            "جرعة زيادة", "اخد حبوب كتير", "بلع دوا كتير",
            "نزيف شديد", "بينزف جامد", "الدم مش واقف",
            "ضربة شمس", "ضربته الشمس", "ضربتها الشمس", "الشمس ضربته",
            "كهربا كهربته", "اتكهرب",
            "حامل وبتنزف", "حامل ونزيف"
        ]
        
        matches = []
        text_lower = text.lower()
        for term in danger_terms:
            if re.search(r'\b' + re.escape(term.lower()) + r'\b', text_lower) or term in text:
                matches.append(term)
                
        return matches
