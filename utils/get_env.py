from dotenv import load_dotenv
import os

load_dotenv()

RH_EMAIL = os.getenv("RABBITHOLE_EMAIL")
RH_PASS = os.getenv("RABBITHOLE_PASSWORD")

if not RH_EMAIL or not RH_PASS:
    raise ValueError("Failed to load environment variables. Please check the .env file.")
