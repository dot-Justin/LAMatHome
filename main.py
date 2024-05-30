import os
import json
import logging
import re
import coloredlogs
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from integrations.computer import ComputerParse, computer_isenabled
from integrations.telegram import TelegramParse, telegram_isenabled
from utils.database import init_db, entry_exists, save_entry
from utils.helpers import log_disabled_integration
from utils.get_env import RH_EMAIL, RH_PASS

def main():
    init_db()  # Initialize database

    state_file = "sessions/rabbithole_state.json"
    os.makedirs("sessions", exist_ok=True)

    # Ensure state.json exists and is valid
    if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
        with open(state_file, 'w') as f:
            json.dump({}, f)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)  # Launch Firefox, because Chrome is too mainstream (jk, it helps stability.) After your initial run (and you get logged into telegram), this can be set to True and you won't see LAH working!
        context = browser.new_context(storage_state=state_file) # Use state to stay logged in
        page = context.new_page() # Open a new page

        # Block unnecessary resources but allow CSS
        page.route("**/*", lambda route, request: route.continue_() if request.resource_type in ["document", "script", "xhr", "fetch", "stylesheet"] else route.abort())

        page.goto("https://hole.rabbit.tech")
        if not page.is_visible('input#username'):
            logging.info("Already logged in.")  # we already logged in, life good
        else:
            page.wait_for_selector('input#username', timeout=30000)
            page.fill('input#username', RH_EMAIL)
            page.wait_for_selector('input#password', timeout=30000)
            page.fill('input#password', RH_PASS)
            page.click('button[type="submit"][data-action-button-primary="true"]')
            page.wait_for_load_state('networkidle')  # Wait until network is idle
            context.storage_state(path=state_file)

        while True:
            page.goto("https://hole.rabbit.tech/journal/details") # Go to the journal details page
            page.wait_for_selector('.w-full:nth-child(2) > .mb-8 li', timeout=15000)  # Wait for specific element

            logging.info("Waiting for journal entries to appear...")
            try:
                page.wait_for_selector('.w-full:nth-child(2) > .mb-8 li', timeout=15000)
            except PlaywrightTimeoutError as e:
                logging.error(f"Error waiting for journal entries: {e}") # Something went wrong, surprise!
                continue

            entries = page.locator('.w-full:nth-child(2) > .mb-8 li')
            found_valid_entry = False

            for i in range(entries.count()):
                entry = entries.nth(i)
                if entry.locator('svg').count() == 0:
                    logging.info(f"Attempting to click on entry {i}...")
                    try:
                        entry.click(timeout=15000)
                        found_valid_entry = True
                        break
                    except PlaywrightTimeoutError as e:
                        logging.error(f"Error clicking on entry {i}: {e}")
                        continue

            if not found_valid_entry:
                logging.info("No valid entries without SVG found, reloading...") # No good entries, try again
                continue

            title = page.locator('.text-white-400').text_content()
            date = page.locator('.text-sm > div:nth-child(1)').text_content()
            time = page.locator('.text-sm > div:nth-child(2)').text_content()

            if entry_exists(title, date, time): # Check if entry already exists in the DB
                logging.info("DB entry already exists, reloading to check for new entries...") # Already there, move on
            else:
                save_entry(title, date, time) # Save the new entry
                logging.info(f"Saved entry: {title}, {date}, {time}") # Let the world know we saved it

                first_word = title.split()[0].strip().lower().strip('.,!?:;') # Get the first word to determine if we need to do anything with it
                logging.info(f"First word of title: {first_word}") # Log the first word

                if re.match(r'^[a-z]+$', first_word) and first_word == "telegram": # Call Telegram function
                    if telegram_isenabled:
                        logging.info(f"Calling Telegram function with title: {title}")
                        TelegramParse(browser, title)
                    else:
                        log_disabled_integration("Telegram")
                elif re.match(r'^[a-z]+$', first_word) and first_word == "computer": # Call Computer function
                    if computer_isenabled:
                        logging.info(f"Calling Computer function with title: {title}")
                        ComputerParse(browser, title)
                    else:
                        log_disabled_integration("Computer")

if __name__ == "__main__":
    load_dotenv()

    if not RH_EMAIL or not RH_PASS:
        logging.error("Failed to load environment variables. Please check the .env file.")
        exit(1)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') # setup logging
    coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s')

    main() # run main!
