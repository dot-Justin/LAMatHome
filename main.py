import os
import json
import logging
import coloredlogs
from datetime import datetime, timezone
from collections import deque
from utils import config, ui, llm_parse, rabbithole, splashscreen, get_env
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def process_utterance(utterance, transcript, playwright_context):
    logging.info(f"Prompt: {utterance}")

    # split prompt into tasks
    promptParsed = llm_parse.LLMParse(utterance, transcript)
    tasks = promptParsed.split("&&")
    
    # iterate through tasks and execute each sequentially
    for task in tasks:
        logging.info(f"Task: {task}")
        llm_parse.CombinedParse(playwright_context, task)

        # Append the completed interaction to the transcript
        chat = {
            "user prompt": utterance,
            "LLM response": promptParsed
        }
        transcript.append(chat)


def main():
    try:
        # Check if env file exists, if not run ui.py to create it
        if not os.path.exists(config.config["env_file"]):
            ui.create_ui()
        print(splashscreen.colored_splash)
        logging.info("LAMatHome has started!")

        # create cache directory if it doesn't exist
        if not os.path.exists(config.config['cache_dir']):
            os.makedirs(config.config['cache_dir'])

        # Ensure state.json exists and is valid
        state_file = os.path.join(config.config['cache_dir'], config.config['state_file'])
        if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
            with open(state_file, 'w') as f:
                json.dump({}, f)

        # Initialize queue for storing rolling transcript
        transcript = deque(maxlen=config.config['rolling_transcript_size'])

        with sync_playwright() as p:
            # Use firefox for full headless
            browser = p.firefox.launch(headless=False)
            context = browser.new_context(storage_state=state_file)  # Use state to stay logged in

            user, assistant = None, None
            if get_env.RH_ACCESS_TOKEN:
                # fetch rabbit hole user profile
                profile = rabbithole.fetch_user_profile()
                user = profile.get('name')
                assistant = profile.get('assistantName')
            
            if config.config["mode"] == "rabbit":
                currentTimeIso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                logging.info(f"Welcome {user}! LAMatHome is now listening for journals posted by {assistant}")
                for journal in rabbithole.journal_entries_generator(currentTimeIso):
                    prompt = journal['utterance']['prompt']
                    process_utterance(prompt, transcript, context)
            
            elif config.config["mode"] == "cli":
                logging.info("Entering interactive mode...")
                while True:
                    try:
                        user_input = input(f"{user}@LAMatHome> " if user else "LAMatHome> ")
                        process_utterance(user_input, transcript, context)
                    except PlaywrightTimeoutError:
                        logging.error("Playwright timed out while waiting for response.")

    except KeyboardInterrupt:
        logging.info("Program terminated by user.")
    finally:
        context.close()
        logging.info("Cleaning up and exiting...")


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
