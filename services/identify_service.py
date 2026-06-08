import httpx
import os

COLAB_URL = os.getenv("COLAB_IDENTIFY_URL", "http://211.105.65.14:8080")

class IdentifyService:
    async def identify_pill(self, image_bytes: bytes, filename: str, content_type: str, question: str):
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{COLAB_URL}/identify",
                files={"image": (filename, image_bytes, content_type)},
                data={"question": question},
            )
            return response.json()
