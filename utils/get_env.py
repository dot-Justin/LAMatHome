from dotenv import load_dotenv
import os

load_dotenv()

RH_EMAIL = os.getenv("RH_EMAIL")
RH_PASS = os.getenv("RH_PASS")
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASS = os.getenv("FB_PASS")
DC_EMAIL = os.getenv("DC_EMAIL")
DC_PASS = os.getenv("DC_PASS")

if not RH_EMAIL or not RH_PASS or not FB_EMAIL or not FB_PASS or not DC_EMAIL or not DC_PASS:
    raise ValueError("Failed to load environment variables. Please check the .env file.")
