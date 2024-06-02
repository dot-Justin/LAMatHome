from dotenv import load_dotenv
import os

load_dotenv()

RH_EMAIL = os.getenv("RH_EMAIL")
RH_PASS = os.getenv("RH_PASS")
RH_ACCESS_TOKEN = os.getenv("RH_ACCESS_TOKEN")
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASS = os.getenv("FB_PASS")
DC_EMAIL = os.getenv("DC_EMAIL")
DC_PASS = os.getenv("DC_PASS")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
