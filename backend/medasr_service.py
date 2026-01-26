import traceback

class MedASRService:
    def __init__(self):
        self.available = True
        self.client = None
    
    def get_client(self):
        if self.client is None:
            from gradio_client import Client
            self.client = Client("DrZayed/medasr-api")
        return self.client
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            print(f"[MedASR] Transcribing: {audio_path}")
            client = self.get_client()
            print(f"[MedASR] Client connected")
            result = client.predict(audio=audio_path, api_name="/transcribe")
            print(f"[MedASR] Result: {result}")
            return {"success": True, "transcription": result}
        except Exception as e:
            print(f"[MedASR] ERROR: {str(e)}")
            print(traceback.format_exc())
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
