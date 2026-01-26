class MedASRService:
    def __init__(self):
        self.available = True
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            from gradio_client import Client
            print("[MedASR] Connecting to Hugging Face...")
            self._client = Client("DrZayed/medasr-api")
            print("[MedASR] Connected!")
        return self._client
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            print(f"[MedASR] Transcribing: {audio_path}")
            result = self.client.predict(audio_path, api_name="/transcribe")
            print(f"[MedASR] Result: {result}")
            return {"success": True, "transcription": result}
        except Exception as e:
            print(f"[MedASR] ERROR: {str(e)}")
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
