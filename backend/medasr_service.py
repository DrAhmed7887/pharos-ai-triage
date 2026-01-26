from transformers import AutoModelForCTC, AutoProcessor
import torch
import librosa
import re

class MedASRService:
    def __init__(self):
        self.model = None
        self.processor = None
        self.loaded = False
    
    def load_model(self):
        if not self.loaded:
            print("Loading MedASR model...")
            self.processor = AutoProcessor.from_pretrained("google/medasr", trust_remote_code=True)
            self.model = AutoModelForCTC.from_pretrained("google/medasr", trust_remote_code=True)
            self.loaded = True
            print("✅ MedASR loaded!")
    
    def transcribe(self, audio_path: str) -> dict:
        try:
            self.load_model()
            speech, sample_rate = librosa.load(audio_path, sr=16000)
            inputs = self.processor(speech, sampling_rate=sample_rate, return_tensors="pt", padding=True)
            
            with torch.no_grad():
                logits = self.model(**inputs).logits
                predicted_ids = torch.argmax(logits, dim=-1)
                raw_text = self.processor.batch_decode(predicted_ids)[0]
            
            clean_text = self._clean_transcription(raw_text)
            return {"success": True, "transcription": clean_text}
        except Exception as e:
            return {"success": False, "error": str(e), "transcription": ""}
    
    def _clean_transcription(self, text: str) -> str:
        text = re.sub(r'<epsilon>', '', text)
        text = re.sub(r'\{[^}]*\}', ' ', text)
        text = re.sub(r'\[+', '[', text)
        text = re.sub(r'\]+', ']', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.replace('</s>', '')
        return text

medasr_service = MedASRService()
