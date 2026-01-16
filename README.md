# 🏥 PHAROS-AI: Emergency Triage System

**AI-powered Emergency Department Triage System for Egyptian Hospitals**

[![Made with Gemini](https://img.shields.io/badge/AI-Google%20Gemini-blue)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB)](https://reactjs.org/)

## 🌟 Overview

PHAROS-AI (Patient Health Assessment & Risk-Ordered Sorting) is a clinical decision support tool that uses AI to assist emergency department triage. Built for Egyptian hospitals, it supports both Arabic and English input.

## ✨ Features

- **🤖 AI-Powered Analysis**: Google Gemini integration for intelligent symptom analysis
- **🔄 Dual Mode**: Toggle between AI and rule-based (ESI v5) triage
- **🌍 Bilingual**: Full Arabic/English support (Egyptian dialect)
- **📊 5-Level ESI Triage**: Standard emergency severity classification
- **🚨 Red Flag Detection**: Automatic identification of critical symptoms
- **📱 Responsive UI**: Works on desktop and mobile

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | Python + FastAPI |
| AI | Google Gemini 2.5 Flash |
| Triage Logic | ESI v5 Algorithm |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key ([Get one free](https://aistudio.google.com/apikey))

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your API key
echo 'GEMINI_API_KEY=your_key_here' > .env

# Run
uvicorn backend.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**

## 📋 Triage Levels

| Level | Color | Name | Time to Physician |
|-------|-------|------|-------------------|
| 1 | 🔴 Red | Resuscitation | Immediate |
| 2 | 🟠 Orange | Emergent | < 15 min |
| 3 | 🟡 Yellow | Urgent | < 30 min |
| 4 | 🟢 Green | Less Urgent | < 60 min |
| 5 | 🔵 Blue | Non-Urgent | < 120 min |

## 🧪 Validation

Run test scenarios:
```bash
python validate_scenarios.py
```

## ⚠️ Disclaimer

This is a **clinical decision support tool**, not a replacement for professional medical judgment. Always defer to qualified healthcare providers for patient care decisions.

## 👨‍⚕️ Author

**Dr. Ahmed Helmy**  
Clinical AI Specialist | AUC AI in Healthcare Program

## 📄 License

MIT License - See LICENSE file for details
