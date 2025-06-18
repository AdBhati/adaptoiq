from openai import OpenAI
from config import settings
import logging
import json
import re

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # Correct way to initialize the client
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def ask(self, prompt: str, temperature: float = 0.2, model: str = "gpt-3.5-turbo") -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise Exception("OpenAI service error")
        

class ResumeSkillExtractor:
    def __init__(self):
        self.openai_service = OpenAIService()

    def extract_info_from_resume(self, resume_text: str) -> dict:
        prompt = (
            "You are an intelligent HR assistant. Extract the following details from the resume text:\n"
            "- Skills\n"
            "- Interests\n"
            "- Education\n"
            "- Degree(s)\n\n"
            f"Resume:\n{resume_text}\n\n"
            "Respond in JSON format like:\n"
            "{\n"
            "  \"skills\": [...],\n"
            "  \"interests\": [...],\n"
            "  \"education\": [...],\n"
            "  \"degrees\": [...]\n"
            "}"
        )

        try:
            openai_service = OpenAIService()
            response = openai_service.ask(prompt)

            # print("Raw OpenAI response:\n", response)

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            return {"error": "Invalid AI response format", "raw_response": response}

        except Exception as e:
            return {"error": str(e)}
        

def classify_skill_type(skill_name: str) -> str:
    prompt = (
        f"You are an expert HR analyst. Categorize the following skill into either 'Technical' or 'Core':\n"
        f"Skill: {skill_name}\n\n"
        "Respond with only one word: 'Technical' or 'Core'."
    )

    try:
        openai_service = OpenAIService()
        response = openai_service.ask(prompt)
        response = response.strip().capitalize()

        if response in ["Technical", "Core"]:
            return response
        return "Technical"  # Default fallback
    except Exception:
        return "Technical"

