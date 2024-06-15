import logging
import shlex
from utils import config
from integrations import browser_int, computer_int, discord_int, facebook_int, google_int, lam_at_home_int, open_interpreter_int, telegram_int

def log_disabled_integration(integration):
    if config.config["debug"]:
        logging.info(f"Attempted integration call, but {integration} is disabled.")

def parse_flags(utterance):
    """
    Parse the command flags from the utterance.
    """
    parts = shlex.split(utterance)
    flags = {
        '--utterance': None,
        '--log': None
    }
    current_flag = None
    for part in parts:
        if part.startswith('--'):
            current_flag = part
        elif current_flag:
            flags[current_flag] = part
            current_flag = None
    return flags

def execute_command(command_text):
    if config.config["debug"]:
        logging.info(f"Executing command: {command_text}")
    
    flags = parse_flags(command_text)
    utterance = flags.get('--utterance')
    log_message = flags.get('--log')

    if not utterance:
        logging.error("Command did not provide enough parameters.")
        return

    # words = utterance.split()
    # if len(words) < 1:
    #     logging.error("Command did not provide enough parameters.")
    #     return

    command = command_text.split()[0]  # Fix the command extraction
    logging.info(command)
    message = flags.get('--utterance')  # Send the entire utterance to the integration module

    if log_message:
        logging.info(log_message)

    if command == "browser_int":
        browser_int.handle_command(utterance)
    elif command == "computer_int":
        computer_int.handle_command(utterance)
    elif command == "discord_int":
        discord_int.handle_command(utterance)
    elif command == "facebook_int":
        facebook_int.handle_command(utterance)
    elif command == "google_int":
        google_int.handle_command(utterance)
    elif command == "lam_at_home_int":
        lam_at_home_int.handle_command(utterance)
    elif command == "open_interpreter_int":
        open_interpreter_int.handle_command(utterance)
    elif command == "telegram_int":
        telegram_int.handle_command(utterance)
    else:
        logging.error(f"Unknown command type: {command}")

def execute_task(context, utterance):
    if config.config["debug"]:
        logging.info(f"Received task: {utterance}")
    
    commands = utterance.split('&&')
    
    if config.config["debug"]:
        logging.info(f"Parsed commands: {commands}")
    
    for command in commands:
        if command:
            execute_command(command)

    if config.config["debug"]:
        logging.info("Task execution completed.")
