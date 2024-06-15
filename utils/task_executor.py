import logging
import shlex
from utils import config
from integrations import browser_int, computer_int, discord_int, facebook_int, google_int, lam_at_home_int, open_interpreter_int, telegram_int

def parse_flags(command_text):
    parts = shlex.split(command_text)
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

def execute_single_command(command_text):
    if config.config["debug"]:
        logging.info(f"Executing command: {command_text}")

    flags = parse_flags(command_text)
    utterance = flags.get('--utterance')
    log_message = flags.get('--log')

    if not utterance:
        logging.error("Command did not provide enough parameters.")
        return

    command = command_text.split()[0]
    logging.info(f"Command: {command}")

    if log_message:
        logging.info(log_message)

    if command == "browser_int":
        browser_int.handle_command(command_text)
    elif command == "computer_int":
        computer_int.handle_command(command_text)
    elif command == "discord_int":
        discord_int.handle_command(command_text)
    elif command == "facebook_int":
        facebook_int.handle_command(command_text)
    elif command == "google_int":
        google_int.handle_command(command_text)
    elif command == "lam_at_home_int":
        lam_at_home_int.handle_command(command_text)
    elif command == "open_interpreter_int":
        open_interpreter_int.handle_command(command_text)
    elif command == "telegram_int":
        telegram_int.handle_command(command_text)
    else:
        logging.error(f"Unknown command type: {command}")

def execute_command(command_text):
    commands = command_text.split('&&')
    for command in commands:
        execute_single_command(command.strip())