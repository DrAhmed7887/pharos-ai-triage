import requests
import os

MEDASR_API_URL = "https://drzayed-medasr-api.hf.space/api/predict"

class MedASRService:
    def __init__(self):
        self.available = True
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            with open(audio_path, 'rb') as f:
                # Call Hugging Face Space API
                response = requests.post(
                    "https://drzayed-medasr-api.hf.space/call/transcribe",
                    files={"audio": f}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Gradio returns data in specific format
                    if "data" in result:
                        return {"success": True, "transcription": result["data"][0]}
                    return {"success": True, "transcription": result.get("transcription", "")}
                else:
                    return {"success": False, "error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
