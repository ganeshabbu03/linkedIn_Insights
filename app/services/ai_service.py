from app.models.page import Page
from app.core.config import get_settings
from huggingface_hub import AsyncInferenceClient
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.HUGGINGFACE_API_KEY
        
        # Default to a reliable free model if key is present
        # Qwen 2.5 7B is versatile and widely endorsed on the Hub
        self.model_id = "Qwen/Qwen2.5-7B-Instruct" 
        
        if self.api_key:
            self.client = AsyncInferenceClient(token=self.api_key)
        else:
            logger.warning("HUGGINGFACE_API_KEY not found. AI Service will return mock data.")
            self.client = None

    async def generate_summary(self, page: Page) -> str:
        if not self.client:
            return f"AI Summary (Mock): {page.name} is a company in {page.industry} with {page.followers_count} followers. (Configure HUGGINGFACE_API_KEY for real AI)"
        
        try:
            # Mistral/Llama instruct format
            messages = [
                {
                    "role": "system",
                    "content": "You are a professional business analyst. Analyze the provided LinkedIn page data and write a concise 3-sentence summary highlighting key focus, scale, and industry presence."
                },
                {
                    "role": "user", 
                    "content": f"""Data:
Name: {page.name}
Description: {page.description}
Industry: {page.industry}
Followers: {page.followers_count}
Headcount: {page.head_count}
Location: {page.location}

Please provide the summary."""
                }
            ]

            # Call chat_completion
            response = await self.client.chat_completion(
                messages=messages,
                model=self.model_id,
                max_tokens=250,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"AI Generation failed: {e}")
            return f"Could not generate AI summary. Error: {str(e)}"
