import re
import logging
import os
import urllib.parse
import webbrowser
import ctypes
import time
from utils.helpers import log_disabled_integration
from integrations.telegram import telegram_isenabled, telegramtext_isenabled, TelegramText
from integrations.computer import (
    computer_isenabled, computergoogle_isenabled, computeryoutube_isenabled,
    computergmail_isenabled, computeramazon_isenabled, computervolume_isenabled,
    computerrun_isenabled, ComputerGoogle, ComputerYoutube, ComputerGmail,
    ComputerAmazon, ComputerVolume, ComputerRun
)
from integrations.discord import login_discord, send_discord_message
from integrations.facebook import open_facebook_messenger

def CombinedParse(browser, page, text):
    """Parses the message and executes the appropriate command for Google, Telegram, Discord, or Facebook."""
    recipient = None
    message = None
    platform = None

    # Improved regex to capture platform, recipient, and message
    match = re.search(r"message on (discord|facebook)\.?\s*to\s+([\w\s]+)\s+saying,?\s+(.*)", text, re.IGNORECASE)
    if match:
        platform = match.group(1).lower()
        recipient = match.group(2).strip()
        message = match.group(3).strip()
    else:
        logging.error("Could not parse message details.")
        return

    logging.info(f"Recipient: {recipient}")
    logging.info(f"Platform: {platform}")
    logging.info(f"Message: {message}")

    words = text.split()
    if len(words) < 3:
        logging.error("Invalid prompt format.")
        return

    first_word = words[0].strip('.,!?:;').lower()
    second_word = words[1].strip('.,!?:;').lower()

    if first_word == "telegram":
        if telegram_isenabled:
            if telegramtext_isenabled:
                TelegramText(browser, text)
            else:
                log_disabled_integration("TelegramText")
        else:
            log_disabled_integration("Telegram")
    elif first_word == "computer":
        if not computer_isenabled:
            log_disabled_integration("Computer")
            return

        if second_word in ["google", "youtube", "gmail", "amazon", "volume", "run", "launch", "open"]:
            if second_word == "google":
                if computergoogle_isenabled:
                    ComputerGoogle(text)
                else:
                    log_disabled_integration("ComputerGoogle")
            elif second_word == "youtube":
                if computeryoutube_isenabled:
                    ComputerYoutube(text)
                else:
                    log_disabled_integration("ComputerYoutube")
            elif second_word == "gmail":
                if computergmail_isenabled:
                    ComputerGmail(text)
                else:
                    log_disabled_integration("ComputerGmail")
            elif second_word == "amazon":
                if computeramazon_isenabled:
                    ComputerAmazon(text)
                else:
                    log_disabled_integration("ComputerAmazon")
            elif second_word == "volume":
                if computervolume_isenabled:
                    ComputerVolume(text)
                else:
                    log_disabled_integration("ComputerVolume")
            elif second_word in ["run", "launch", "open"]:
                if computerrun_isenabled:
                    ComputerRun(text)
                else:
                    log_disabled_integration("ComputerRun")
        else:
            logging.error("Unknown Computer command or the integration is not enabled.")
    elif platform == "discord":
        login_discord(page)
        if recipient == 'r':
            recipient = 'r1-general'
        logging.info(f"Recipient after check: {recipient}")
        send_discord_message(page, recipient, message)
    elif platform == "facebook":
        open_facebook_messenger(page, recipient, message)
    else:
        logging.error("Unknown command type.")

