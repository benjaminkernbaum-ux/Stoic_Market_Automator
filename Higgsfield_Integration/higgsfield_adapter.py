import requests
import os
import json
import time

class HiggsfieldSpecialist:
    """
    Higgsfield AI Integration Specialist for Stoic Market.
    Handles high-quality animation and cinematic video generation.
    """
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("HIGGSFIELD_API_KEY")
        self.api_secret = api_secret or os.getenv("HIGGSFIELD_API_SECRET")
        self.base_url = "https://platform.higgsfield.ai"
        
    def generate_animation(self, image_url, motion_prompt, model="dop-standard", duration=5):
        """
        Transforms a static Stoic Market post into a cinematic video.
        """
        endpoint = f"{self.base_url}/higgsfield-ai/dop/standard"
        
        headers = {
            "Authorization": f"Key {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "image_url": image_url,
            "prompt": f"Cinematic lighting, high quality, 4k, stoic atmosphere. {motion_prompt}",
            "duration": duration
        }
        
        print(f"🎬 Iniciando animação Higgsfield (Modelo: {model})...")
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            request_id = data.get("request_id")
            print(f"✅ Solicitação enviada! Request ID: {request_id}")
            return request_id
        except Exception as e:
            print(f"❌ Erro ao conectar com Higgsfield: {e}")
            return None

    def poll_result(self, request_id):
        """
        Checks if the video is ready.
        """
        # Note: Actual polling endpoint should be verified in docs
        # Standard pattern is /status/{request_id}
        check_url = f"{self.base_url}/status/{request_id}"
        headers = {"Authorization": f"Key {self.api_key}:{self.api_secret}"}
        
        while True:
            res = requests.get(check_url, headers=headers).json()
            status = res.get("status")
            if status == "completed":
                return res.get("video_url")
            elif status == "failed":
                return "Error"
            print("⏳ Renderizando vídeo no Higgsfield...")
            time.sleep(10)

if __name__ == "__main__":
    # Test block
    print("Higgsfield Specialist Module Ready.")
