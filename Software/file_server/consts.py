import os
from dotenv import load_dotenv

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:rootroot@127.0.0.1:5434/cubbysense"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "your_key_here"
