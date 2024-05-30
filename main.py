from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os
import json
import logging
import re
from datetime import datetime
import coloredlogs
from integrations.computer import ComputerParse, computer_isenabled
from integrations.telegram import TelegramParse, telegram_isenabled
from utils.database import init_db, entry_exists, save_entry
from utils.helpers import log_disabled_integration
from utils.get_env import RH_EMAIL, RH_PASS
from integrations.discord import login_discord, send_discord_message
from integrations.facebook import open_facebook_messenger
from integrations.rabbithole import login_hole_rabbit
from integrations.parse import CombinedParse
from dotenv import load_dotenv

# --- Main execution ---
def main():
    init_db()  # Initialize database

    state_file = "sessions/rabbithole_state.json"
    os.makedirs("sessions", exist_ok=True)

    # Ensure state.json exists and is valid
    if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
        with open(state_file, 'w') as f:
            json.dump({}, f)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Launch Firefox
        context = browser.new_context(storage_state=state_file)  # Use state to stay logged in
        page = context.new_page()  # Open a new page

        # Block unnecessary resources but allow CSS
        page.route("**/*", lambda route, request: route.continue_() if request.resource_type in ["document", "script", "xhr", "fetch", "stylesheet"] else route.abort())

        # --- Login to hole.rabbit.tech ---
        login_hole_rabbit(page)

        previous_text_content = ''
        while True:
            if not page.is_closed():
                # try:
                page.goto('https://hole.rabbit.tech/journal/details')
                page.wait_for_load_state('load')
                first_item = page.locator('ul li div.line-clamp-1').first
                first_item.click(timeout=60000)
                page.wait_for_timeout(5000)
                texts = page.locator('div.text-white-400.w-full.text-wrap.text-3xl.md\\:w-\\[70\\%\\]').inner_text()
                logging.info(f"Text content: {texts}")

                CombinedParse(browser, page, texts.lower())

                if texts != previous_text_content:
                    previous_text_content = texts
                    logging.info(f"Previous Text content: {previous_text_content}")
                    
                    # --- Integrations from main.py ---
                    title = texts.lower()  # Assuming 'texts' is the title from the journal entry
                    print('title after texts:', title)
                    current_datetime = datetime.now()
                    date = current_datetime.strftime('%Y-%m-%d')
                    time = current_datetime.strftime('%H:%M:%S')
                    
                    if entry_exists(title, date, time):
                        logging.info("DB entry already exists, reloading to check for new entries...")
                    else:
                        save_entry(title, date, time)
                        logging.info(f"Saved entry: {title}, {date}, {time}")

                        first_word = title.split()[0].strip().lower().strip('.,!?:;')
                        logging.info(f"First word of title: {first_word}")

                        if re.match(r'^[a-z]+$', first_word) and first_word == "telegram":
                            if telegram_isenabled:
                                logging.info(f"Calling Telegram function with title: {title}")
                                TelegramParse(browser, title)
                            else:
                                log_disabled_integration("Telegram")
                        elif re.match(r'^[a-z]+$', first_word) and first_word == "computer":
                            if computer_isenabled:
                                logging.info(f"Calling Computer function with title: {title}")
                                ComputerParse(browser, title)
                            else:
                                log_disabled_integration("Computer")
                else:
                    logging.info(f"Couldn't parse: {texts}")
                # except Exception as e:
                #     logging.error(f"An error occurred: {e}")
            else:
                logging.error("The page has been closed. Exiting...")
                break
            logging.info("Timing out for 45 seconds... Checking again in 45 seconds...")
            page.wait_for_timeout(45000)

if __name__ == "__main__":
    # --- Load .env and Start Application ---
    load_dotenv()

    if not RH_EMAIL or not RH_PASS:
        logging.error("Failed to load environment variables. Please check the .env file.")
        exit(1)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s')

    main()
