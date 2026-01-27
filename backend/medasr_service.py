import google.generativeai as genai
import os

class MedASRService:
    def __init__(self):
        self.available = True
        self.model = None
    
    def get_model(self):
        if self.model is None:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        return self.model
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            print(f"[Gemini] Transcribing: {audio_path}")
            
            audio_file = genai.upload_file(audio_path, mime_type="audio/wav")
            
            response = self.get_model().generate_content([
                audio_file,
                """Transcribe this audio exactly as spoken.
                - If Arabic, write in Arabic.
                - If English medical terms, write in English.
                - Handle mixed Arabic/English naturally.
                - Return ONLY the transcription."""
            ])
            
            print(f"[Gemini] Result: {response.text}")
            return {"success": True, "transcription": response.text}
        except Exception as e:
            print(f"[Gemini] ERROR: {str(e)}")
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
