import os
import json
import logging
import coloredlogs
from datetime import datetime, timezone
from integrations import lam_at_home_int
from utils import config, get_env, rabbit_hole, splash_screen, ui, llm_parse, task_executor, journal
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def process_utterance(journal_entry, journal: journal.Journal, playwright_context):
    if isinstance(journal_entry, str):
        utterance = journal_entry
    else: 
        utterance = journal_entry['utterance']['prompt']
    logging.info(f"Prompt: {utterance}")

    try:
        # Send the utterance to the Groq API for parsing
        parsed_command = llm_parse.LLMParse(utterance, journal.get_interactions())

        # Execute the parsed command
        task_executor.execute_command(parsed_command)

        # Append the completed interaction to the journal
        journal.add_entry(journal_entry, llm_response=parsed_command)

    except PlaywrightTimeoutError:
        logging.error("Playwright timed out while waiting for response.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    try:
        # Check if env file exists, if not run ui.py to create it
        if not os.path.exists(config.config["env_file"]):
            ui.create_ui()
        print(splash_screen.colored_splash)
        logging.info("LAMatHome is starting...")

        # create cache directory if it doesn't exist
        if not os.path.exists(config.config['cache_dir']):
            os.makedirs(config.config['cache_dir'])

        # Ensure state.json exists and is valid
        state_file = os.path.join(config.config['cache_dir'], config.config['state_file'])
        if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
            with open(state_file, 'w') as f:
                json.dump({}, f)

        # Initialize journal for storing rolling transcript
        userJournal = journal.Journal(max_entries=config.config['rolling_transcript_size'])

        with sync_playwright() as p:
            # Use firefox for full headless
            browser = p.firefox.launch(headless=False)
            context = browser.new_context(storage_state=state_file)  # Use state to stay logged in

            user, assistant = None, None
            if get_env.RH_ACCESS_TOKEN:
                # fetch rabbit hole user profile
                profile = rabbit_hole.fetch_user_profile()
                user = profile.get('name')
                assistant = profile.get('assistantName')
            
            if config.config["mode"] == "rabbit":
                currentTimeIso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                logging.info(f"Welcome {user}! LAMatHome is now listening for journal entries posted by {assistant}")
                for journal_entry in rabbit_hole.journal_entries_generator(currentTimeIso):
                    process_utterance(journal_entry, userJournal, context)
            
            elif config.config["mode"] == "cli":
                logging.info("Entering interactive mode...")
                while True:
                    user_input = input(f"{user}@LAMatHome> " if user else "LAMatHome> ")
                    process_utterance(user_input, userJournal, context)

            else:
                logging.error("Invalid mode specified in config.json")

    except KeyboardInterrupt:
        print("\n")
        logging.info("Program terminated by user")
    finally:
        lam_at_home_int.terminate()


if __name__ == "__main__":
    # configure logging and run LAMatHome
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    coloredlogs.install(
        level='INFO', 
        fmt='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S', 
        field_styles={'asctime': {'color': 'white'}}
    )
    main()