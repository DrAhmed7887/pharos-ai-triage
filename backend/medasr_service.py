from gradio_client import Client

class MedASRService:
    def __init__(self):
        self.available = True
        self.client = None
    
    def get_client(self):
        if self.client is None:
            self.client = Client("DrZayed/medasr-api")
        return self.client
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            client = self.get_client()
            result = client.predict(audio=audio_path, api_name="/transcribe")
            return {"success": True, "transcription": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
