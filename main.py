import os
import re
import json
import logging
import coloredlogs
from datetime import datetime
from ui import create_ui
from utils.get_env import RH_EMAIL, RH_PASS
from utils.llm_parse import LLMParse, CombinedParse
from utils.helpers import log_disabled_integration
from utils.journals import journal_entries_generator
from utils.splashscreen import colored_splash
from integrations.computer import computer_isenabled
from integrations.telegram import telegram_isenabled
from integrations.discord import login_discord, DiscordText
from integrations.facebook import FacebookText
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# --- Main execution ---
def main():

    # Check if .env exists, if not run ui.py to create it
    first_run=False
    if not os.path.exists(".env"):
        create_ui()
        first_run=True

    if not first_run:
        print(colored_splash)
        state_file = "state.json"

    # Ensure state.json exists and is valid
    if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
        with open(state_file, 'w') as f:
            json.dump({}, f)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True) # Use firefox for full headless. If this gets stuck at any point, set to True, and try again.
        context = browser.new_context(storage_state=state_file)  # Use state to stay logged in
        page = context.new_page()  # Open a new page

        if not page.is_closed():
            for journal in journal_entries_generator(datetime.utcnow().isoformat() + 'Z'):
                # --- Parse the journal entry ---
                prompt = journal['utterance']['prompt']
                logging.info(f"Prompt: {prompt}")
                promptParsed = LLMParse(prompt)
                CombinedParse(page, promptParsed)
        else:
            logging.error("The page has been closed. Exiting...")

if __name__ == "__main__":
    # --- Start Application ---
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', field_styles={
        'asctime': {'color': 'cyan'}
    })
    main()
