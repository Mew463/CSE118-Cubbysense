import google.generativeai as genai
import logging
from typing import List

from models import Item
from consts import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

logger = logging.getLogger(__name__)
model = genai.GenerativeModel("gemini-1.5-flash")

def check_for_forgotten_items(location: str, items_in_cubby: List[Item]):
    items_in_cubby_as_string = ", ".join([item.name for item in items_in_cubby])
    try:
        response = model.generate_content(f"I am leaving to {location} now. I still have {items_in_cubby_as_string} in my cubbies. Can I leave without them?")
        return response
    except Exception as e:
        logger.error("Error generating response: %s", e)
        return None


