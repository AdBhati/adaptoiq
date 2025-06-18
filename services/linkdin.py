import requests
from config import settings
import logging

logger = logging.getLogger(__name__)

class PDLService:
    def __init__(self):
        self.api_url = "https://api.peopledatalabs.com/v5/person/enrich"
        self.api_key = settings.PDL_API_KEY  

    def fetch_profile_data(self, linkedin_url: str) -> dict:
        try:
            params = {
                "api_key": self.api_key,
                "profile": linkedin_url
            }

            response = requests.get(self.api_url, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"PDL API error {response.status_code}: {response.text}")
                return {"error": f"PDL API error: {response.status_code}"}

        except Exception as e:
            logger.exception("PDL scraping failed")
            return {"error": str(e)}
