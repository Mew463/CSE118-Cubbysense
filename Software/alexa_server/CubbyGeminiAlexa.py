#python3 -m uvicorn CubbyGeminiAlexa:app --reload  --host 0.0.0.0 --port 8080
#ngrok http 8080 #
#ngrok http --url=complete-primate-simply.ngrok-free.app 8080
from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests  # Add the HTTP client import

# Configure the Gemini API with the API key
# Load environment variables from .env file
load_dotenv()
# Access the API key
api_key_str = os.getenv("API_KEY")
genai.configure(api_key=api_key_str) #DO NOT SHARE THIS API KEY

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

class AlexaRequest(BaseModel):
    version: str
    session: dict
    request: dict
    context: dict

# Replace the hardcoded itemslist with a function to fetch items
def fetch_items():
    try:
        response = requests.get("http://localhost:8081/items")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the API returns a JSON array
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        return []  # Return an empty list if the fetch fails

def build_alexa_response(message):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": message
            },
            "shouldEndSession": True
        }
    }

@app.post("/alexa_skill")
async def handle_alexa_request(request: Request):
    try:
        alexa_request = await request.json()
        request_type = alexa_request["request"]["type"]

        print(alexa_request["request"]["intent"])

        # Handle LaunchRequest separately
        if request_type == "LaunchRequest":
            return build_alexa_response("Welcome to the Gemini Flash skill. You can ask me to forward a request to Gemini.")

        # Handle IntentRequest
        elif request_type == "IntentRequest":
            intent_name = alexa_request["request"]["intent"]["name"] #welcome back dialogue

            # Handle GetGeminiFlashIntent
            if intent_name == "SendCubbyEvent":
                try:
                    # Generate content using the Gemini model

                    # Extract the user's message from the Alexa request
                    try:
                        user_location = alexa_request["request"]["intent"]["slots"]["location"]["value"]
                    except KeyError:
                        user_location = ""  # or set a default value

                    try:
                        user_direction = alexa_request["request"]["intent"]["slots"]["direction"]["value"]
                    except KeyError:
                        user_direction = ""  # or set a default value

                    try:
                        user_actor = alexa_request["request"]["intent"]["slots"]["actor"]["value"]
                    except KeyError:
                        user_actor = ""  # or set a default value
                    
                    try: 
                        itemslist = fetch_items()
                    except Exception as e:
                        itemslist = ["Default list", "scissors", "pencil", "laptop", "pots", "pans", "starbucks card", "car keys", "credit card", "home keys", "passport", "cheatsheet"]
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    intial_prompt = "Your name is Cubby aka Flash Drive and you are an assistant at home tracking my items. A list of items will be provided."
                    prompt = intial_prompt + ". This is context from Alexa Services: Actor: " + user_actor + ", Direction:" + user_direction + ", Location:" + user_location + ". As an assistant, give suggestions in under 2 sentences. Here is the list of items available:" + str(itemslist)
                    response = model.generate_content(prompt)
                    
                    # Extract text from the response
                    message = response.text if response.text else "Cubby did not provide a response."
                    return build_alexa_response(f"{message}")
                

                except Exception as e:
                    logger.error(f"Error contacting Gemini API: {e}")
                    return build_alexa_response("Sorry, I had an error processing your request with Gemini Flash at the moment.")
                
            elif intent_name == "GetGeminiFlashEvent":
                try:
                    # Generate content using the Gemini model

                    # Extract the user's message from the Alexa request
                    user_message = str(alexa_request["request"]["intent"])
                    
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content("You are a personal assistant, Alexa, that responds in two lines or less. Respond to this user event:" + user_message)
                    
                    # Extract text from the response
                    message = response.text if response.text else "Gemini Flash did not provide a response."
                    return build_alexa_response(f"Gemini Flash says: {message}")
                

                except Exception as e:
                    logger.error(f"Error contacting Gemini API: {e}")
                    return build_alexa_response("Sorry, I couldn't reach Gemini Flash at the moment.")

            # Handle HelpIntent
            elif intent_name == "AMAZON.HelpIntent":
                return build_alexa_response("You can ask me to forward a request to Gemini Flash by saying, 'ask Gemini Flash.'")

            else:
                return build_alexa_response("Sorry, I didn't understand that request.")

        # Handle unexpected request types
        else:
            return build_alexa_response("I'm not sure how to handle that request.")

    except Exception as e:
        logger.error(f"Error handling request: {e}")
        return build_alexa_response("Sorry, there was an error processing your request.")

@app.get("/gemini_status")
async def gemini_status():
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            "You are a personal assistant. Respond to this user event."
        )
        message = response.text if response.text else "Cubby did not provide a response."
        return {"status": "success", "message": message}
    except Exception as e:
        logger.error(f"Error handling Gemini request: {e}")
        return {"status": "error", "message": "Gemini service is currently unavailable."}
