import requests
import base64
import os

class MedASRService:
    def __init__(self):
        self.available = True
        self.api_url = "https://drzayed-medasr-api.hf.space/call/transcribe"
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            # Read and encode audio as base64
            with open(audio_path, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Get file extension
            ext = os.path.splitext(audio_path)[1].lower()
            mime_types = {'.wav': 'audio/wav', '.webm': 'audio/webm', '.mp3': 'audio/mpeg'}
            mime_type = mime_types.get(ext, 'audio/wav')
            
            # Gradio API format
            payload = {
                "data": [{"name": "audio.wav", "data": f"data:{mime_type};base64,{audio_data}"}]
            }
            
            # Step 1: Submit the job
            response = requests.post(self.api_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                event_id = result.get("event_id")
                
                # Step 2: Get the result
                result_response = requests.get(
                    f"https://drzayed-medasr-api.hf.space/call/transcribe/{event_id}",
                    timeout=60
                )
                
                if result_response.status_code == 200:
                    # Parse SSE response
                    for line in result_response.text.split('\n'):
                        if line.startswith('data:'):
                            import json
                            data = json.loads(line[5:].strip())
                            if isinstance(data, list) and len(data) > 0:
                                return {"success": True, "transcription": data[0]}
                
                return {"success": False, "error": "Failed to get transcription result"}
            else:
                return {"success": False, "error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

medasr_service = MedASRService()
