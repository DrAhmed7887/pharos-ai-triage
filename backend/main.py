from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .models import PatientInput, TriageResult
from .logic.triage_engine import TriageEngine
from .database import engine, Base, get_db
from .sql_models import Patient
import uvicorn
from .ai_service import AIService

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Egypt AI Triage System", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine_logic = TriageEngine()
ai_service = AIService()

@app.get("/")
def read_root():
    return {"message": "AI Triage System API Active"}

@app.post("/triage", response_model=TriageResult)
def triage_patient(patient: PatientInput, db: Session = Depends(get_db)):
    try:
        # 1. Run Logic
        result = engine_logic.evaluate(patient)
        
        # 2. Persist to DB
        db_patient = Patient(
            name="Anonymous", # Update if name field added to input
            age=patient.age,
            gender=patient.gender.value,
            vitals=patient.vitals.model_dump(),
            chief_complaint=patient.chief_complaint_text,
            triage_level=result.level,
            triage_color=result.color_code,
            triage_label_en=result.label_en,
            triage_label_ar=result.label_ar,
            triage_reasoning=result.reasoning,
            triage_red_flags=result.red_flags
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai-triage")
def ai_triage_patient(patient: PatientInput, db: Session = Depends(get_db)):
    try:
        # 1. AI Analysis
        ai_result = ai_service.analyze_triage(patient.model_dump())
        
        # Fallback if AI fails
        if "error" in ai_result:
             # Fallback to standard logic if AI fails
             std_result = engine_logic.evaluate(patient)
             return {
                 "level": std_result.level,
                 "color_code": std_result.color_code,
                 "label_en": std_result.label_en,
                 "label_ar": std_result.label_ar,
                 "reasoning": [ai_result.get("reasoning"), "Fallback to Standard Protocol"],
                 "red_flags": std_result.red_flags,
                 "ai_data": None
             }

        # Map AI Level to Color/Label
        level = ai_result.get("triage_level", 3)
        colors = {1:"#ef4444", 2:"#f97316", 3:"#eab308", 4:"#22c55e", 5:"#3b82f6"}
        labels_en = {1:"Resuscitation", 2:"Emergent", 3:"Urgent", 4:"Less Urgent", 5:"Non-Urgent"}
        labels_ar = {1:"إنعاش", 2:"طوارئ", 3:"عاجل", 4:"أقل إلحاحاً", 5:"غير عاجل"}

        final_response = {
            "level": level,
            "color_code": colors.get(level, "#eab308"),
            "label_en": f"{labels_en.get(level)} (Level {level})",
            "label_ar": f"{labels_ar.get(level)} (مستوى {level})",
            "description": "AI-Assisted Assessment",
            "recommended_action": "Review AI suggestions below",
            "time_to_physician": "Based on acuity",
            "red_flags": ai_result.get("red_flags", []),
            "reasoning": [ai_result.get("reasoning")],
            "ai_data": {
                "reasoning_ar": ai_result.get("reasoning_ar"),
                "followup_question": ai_result.get("followup_question"),
                "followup_question_ar": ai_result.get("followup_question_ar"),
                "severity": ai_result.get("severity")
            },
            "confidence": "AI-Generated"
        }

        # Persist (marking as AI)
        db_patient = Patient(
            name="Anonymous (AI)", 
            age=patient.age,
            gender=patient.gender.value,
            vitals=patient.vitals.model_dump(),
            chief_complaint=patient.chief_complaint_text,
            triage_level=level,
            triage_color=final_response["color_code"],
            triage_label_en=final_response["label_en"],
            triage_label_ar=final_response["label_ar"],
            triage_reasoning=final_response["reasoning"],
            triage_red_flags=final_response["red_flags"]
        )
        db.add(db_patient)
        db.commit()
        
        return final_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients")
def get_patients(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    patients = db.query(Patient).order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
         raise HTTPException(status_code=404, detail="Patient not found")
    return patient

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
