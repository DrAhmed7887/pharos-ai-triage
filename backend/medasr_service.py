import google.generativeai as genai
import os

# Configure API key at module load
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    print("[Gemini] API configured")
else:
    print("[Gemini] WARNING: No API key found")

class MedASRService:
    def __init__(self):
        self.available = True
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("[Gemini] Transcription service ready")
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            print(f"[Gemini] Transcribing: {audio_path}")
            
            # Upload file to Gemini
            audio_file = genai.upload_file(audio_path, mime_type="audio/wav")
            print(f"[Gemini] File uploaded: {audio_file.name}")
            
            # Generate transcription
            response = self.model.generate_content([
                audio_file,
                "Transcribe this audio exactly. If Arabic, write Arabic. If English, write English. Return ONLY the transcription."
            ])
            
            transcription = response.text.strip()
            print(f"[Gemini] Result: {transcription}")
            return {"success": True, "transcription": transcription}
            
        except Exception as e:
            print(f"[Gemini] ERROR: {str(e)}")
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
