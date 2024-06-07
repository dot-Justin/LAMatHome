import os
import json
import logging
import coloredlogs
from datetime import datetime
from collections import deque
from utils.ui import create_ui
from utils.llm_parse import LLMParse, CombinedParse
from utils.journals import journal_entries_generator
from utils.splashscreen import colored_splash
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def main():
    # Check if .env exists, if not run ui.py to create it
    if not os.path.exists(".env"):
        create_ui()
    print(colored_splash)
    logging.info("LAMAtHome has started!")

    # Ensure state.json exists and is valid
    state_file = "state/state.json"
    state_dir = os.path.dirname(state_file)
    
    # Ensure the directory exists
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)
    
    if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
        with open(state_file, 'w') as f:
            json.dump({}, f)

    # Initialize queue for storing rolling transcript
    transcript = deque(maxlen=5)

    with sync_playwright() as p:
        # Use firefox for full headless
        browser = p.firefox.launch(headless=False) 
        
        for journal in journal_entries_generator(datetime.utcnow().isoformat() + 'Z'):
            # grab prompt from journal
            prompt = journal['utterance']['prompt']
            logging.info(f"Prompt: {prompt}")

            # split prompt into tasks
            promptParsed = LLMParse(prompt, transcript)
            tasks = promptParsed.split("&&")
            
            # iterate through tasks and execute each sequentially
            for task in tasks:
                logging.info(f"Task: {task}")
                CombinedParse(browser, task)

                # Append the completed interaction to the transcript
                chat = {
                    "user prompt": prompt,
                    "LLM response": promptParsed
                }
                transcript.append(chat)

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
