import os
import sqlite3
import json
import re
import logging
import coloredlogs
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import webbrowser
import urllib.parse

#############################################################
#                                                           #
#                          Computer:                        #
#                                                           #
#############################################################
# Computer Integration                                      #
# Syntax: "Computer [Function] [query]"                     #
# Example: "Computer Google What is the meaning of life"    #
#############################################################

computer_isenabled = True

def ComputerParse(browser, title):
    if not computer_isenabled:
        log_disabled_integration("Computer")
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer command.")
        return

    second_word = words[1].strip('.,!?:;').lower()
    if second_word == "google":
        if computergoogle_isenabled:
            ComputerGoogle(title)
        else:
            log_disabled_integration("ComputerGoogle")
    elif second_word == "youtube":
        if computeryoutube_isenabled:
            ComputerYoutube(title)
        else:
            log_disabled_integration("ComputerYoutube")
    elif second_word == "gmail":
        if computergmail_isenabled:
            ComputerGmail(title)
        else:
            log_disabled_integration("ComputerGmail")
    elif second_word == "amazon":
        if computeramazon_isenabled:
            ComputerAmazon(title)
        else:
            log_disabled_integration("ComputerAmazon")
    elif second_word == "volume":
        if computervolume_isenabled:
            ComputerVolume(title)
        else:
            log_disabled_integration("ComputerVolume")
    else:
        logging.error("Unknown Computer command or the integration is not enabled.")


############################
#      ComputerGoogle      #
############################

computergoogle_isenabled = True

def ComputerGoogle(title):
    if not computergoogle_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Google command.")
        return

    # Strip punctuation from the first and second words
    first_word = words[0].strip('.,!?:;')
    second_word = words[1].strip('.,!?:;')

    # Join the remaining words to form the query
    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"

    # Open the URL in the default web browser
    webbrowser.open(url)
    logging.info(f"Opened Google search for query: {query}")

############################
#      ComputerYoutube     #
############################

computeryoutube_isenabled = True

def ComputerYoutube(title):
    if not computeryoutube_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Youtube command.")
        return

    # Strip punctuation from the first and second words
    first_word = words[0].strip('.,!?:;')
    second_word = words[1].strip('.,!?:;')

    # Join the remaining words to form the query
    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # Open the URL in the default web browser
    webbrowser.open(url)
    logging.info(f"Opened YouTube search for query: {query}")

##########################
#      ComputerGmail     #
##########################

computergmail_isenabled = True

def ComputerGmail(title):
    if not computergmail_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Gmail command.")
        return

    # Strip punctuation from the first and second words
    first_word = words[0].strip('.,!?:;')
    second_word = words[1].strip('.,!?:;')

    # Join the remaining words to form the query
    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"

    # Open the URL in the default web browser
    webbrowser.open(url)
    logging.info(f"Opened Gmail search for query: {query}")

###########################
#      ComputerAmazon     #
###########################

computeramazon_isenabled = True

def ComputerAmazon(title):
    if not computeramazon_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Amazon command.")
        return

    # Strip punctuation from the first and second words
    first_word = words[0].strip('.,!?:;')
    second_word = words[1].strip('.,!?:;')

    # Join the remaining words to form the query
    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.amazon.com/s?k={encoded_query}"

    # Open the URL in the default web browser
    webbrowser.open(url)
    logging.info(f"Opened Amazon search for query: {query}")

# Computer Searches ^
# ----------------------------------------------------------#
# Computer Settings v

############################
#      ComputerVolume      #
############################

computervolume_isenabled = True

# These control how much audio gets turned up or down on "computer volume up/down".
vol_up_step_value = 4
vol_down_step_value = 4

def ComputerVolume(title):
    if not computervolume_isenabled:
        log_disabled_integration("ComputerVolume")
        return

    import re
    import ctypes

    # Remove punctuation and convert words to lowercase
    title_cleaned = re.sub(r'[^\w\s]', '', title).lower()

    words = title_cleaned.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Volume command.")
        return

    # Try to interpret the volume value
    volume_word = words[2]
    
    if volume_word == "mute":
        try:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)  # Mute the volume
            logging.info("Muted the volume")
        except Exception as e:
            logging.error(f"Failed to mute volume: {e}")
        return

    if volume_word == "unmute":
        try:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)  # Unmute the volume
            logging.info("Unmuted the volume")
        except Exception as e:
            logging.error(f"Failed to unmute volume: {e}")
        return

    if volume_word == "up":
        try:
            for _ in range(vol_up_step_value):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            logging.info(f"Increased volume by {vol_up_step_value} steps")
        except Exception as e:
            logging.error(f"Failed to increase volume: {e}")
        return

    if volume_word == "down":
        try:
            for _ in range(vol_down_step_value):
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            logging.info(f"Decreased volume by {vol_down_step_value} steps")
        except Exception as e:
            logging.error(f"Failed to decrease volume: {e}")
        return

    try:
        volume_value = int(volume_word)
        if volume_value < 0 or volume_value > 100:
            raise ValueError
    except ValueError:
        logging.error(f"Invalid volume value: {volume_word}. Must be an integer between 0 and 100.")
        return

    # Set the volume (looking for other ways, emulates a keybind for volume down (all the way) then up to specified percent.)
    try:
        for _ in range(50):  # Set volume to 0
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
        for _ in range(volume_value // 2):  # Increase to desired volume
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
        logging.info(f"Set volume to {volume_value}%")
    except Exception as e:
        logging.error(f"Failed to set volume: {e}")



#############################################################
#                                                           #
#                          Telegram:                        #
#                                                           #
#############################################################
# Telegram Integration                                      #
# Syntax: "Telegram [user] [rest of prompt is message]"     #
# Example: "Telegram Justin Why are you so cool?"           #
#############################################################

telegram_isenabled = True

def TelegramParse(browser, title):
    if not telegram_isenabled:
        log_disabled_integration("Telegram")
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Telegram command.")
        return

    if telegramtext_isenabled:
        TelegramText(browser, title)
    else:
        log_disabled_integration("TelegramText")

##########################
#      TelegramText      #
##########################

telegramtext_isenabled = True

def TelegramText(browser, title):
    if not telegramtext_isenabled:
        return

    session_file = "sessions/telegram_state.json"
    os.makedirs("sessions", exist_ok=True)

    context = browser.new_context(storage_state=session_file if os.path.exists(session_file) else None)
    page = context.new_page()
    page.goto("https://web.telegram.org/k/")

    # Check if already logged in
    if page.is_visible('text=Chats'):
        logging.info("Already logged in to Telegram.")
    else:
        logging.info("Telegram session expired, logging in again.")

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Telegram message.")
        return

    user_search = words[1]  # The second word is the user search term
    message = " ".join(words[2:])  # Everything after the first two words is the message content

    logging.info(f"User to search: {user_search}")
    logging.info(f"Message to send: {message}")

    login_successful = False
    for _ in range(3):  # Try 3 times to log in
        try:
            page.wait_for_selector('[placeholder=" "]', timeout=30000)  # Wait for the search bar to appear
            login_successful = True
            break
        except:
            page.reload()  # Reload the page if login fails

    if login_successful:
        context.storage_state(path=session_file)  # Save session

        # Search for the user or group
        page.fill('[placeholder=" "]', user_search)
        page.press('[placeholder=" "]', 'Enter')
        page.wait_for_timeout(1000)  # Wait for search results to load

        # Click on the first user or group under "Chats"
        if page.is_visible('.search-super-content-chats a'):
            page.click('.search-super-content-chats a')
            page.wait_for_timeout(1000)  # Ensure the chat is loaded

            # Send the message
            page.fill('.input-message-input:nth-child(1)', message)
            page.click('.btn-send > .c-ripple')

            logging.info(f"Sent message to {user_search}: {message}")
        else:
            logging.error("No users found, aborting.")
            context.close()
            return
    else:
        logging.error("Failed to log in to Telegram after multiple attempts")
        context.close()
        return

    context.storage_state(path=session_file)  # Save session at the end
    context.close()


#----------------------------------------------------------------------------------------------------------------------------------#


################################
#            Logging           #
#         Env Variables        #
################################

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
coloredlogs.install(level='INFO', fmt='%(asctime)s - %(levelname)s - %(message)s')

def log_disabled_integration(integration_name):
    logging.info(f"Attempted to call {integration_name}, but it is disabled.")

# Load environment variables
load_dotenv()
RH_EMAIL = os.getenv("RABBITHOLE_EMAIL")
RH_PASS = os.getenv("RABBITHOLE_PASSWORD")

# Check if the environment variables are loaded correctly
if not RH_EMAIL or not RH_PASS:
    logging.error("Failed to load environment variables. Please check the .env file.")
    exit(1)

##############################
#         Database           #
##############################

def init_db():
    conn = sqlite3.connect('journal_entries.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, time TEXT)''')
    conn.commit()
    conn.close()

def entry_exists(title, date, time):
    conn = sqlite3.connect('journal_entries.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries WHERE title = ? AND date = ? AND time = ?", (title, date, time))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def save_entry(title, date, time):
    conn = sqlite3.connect('journal_entries.db')
    c = conn.cursor()
    c.execute("INSERT INTO entries (title, date, time) VALUES (?, ?, ?)", (title, date, time))
    conn.commit()
    conn.close()

#########################################################
#                                                       #
#                          Main:                        #
#                                                       #
#########################################################

def main():
    init_db() #initialize database

    state_file = "sessions/rabbithole_state.json"
    os.makedirs("sessions", exist_ok=True)
    
    # Ensure state.json exists and is valid
    if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
        with open(state_file, 'w') as f:
            json.dump({}, f)

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # No longer breaks script! If you want to see LAMAtHome work through GUI's, set to False.
        context = browser.new_context(storage_state=state_file)
        page = context.new_page()

        page.goto("https://hole.rabbit.tech")
        if not page.is_visible('input#username'):
            logging.info("Already logged in.")
        else:
            page.wait_for_selector('input#username', timeout=30000)
            page.fill('input#username', RH_EMAIL)
            page.wait_for_selector('input#password', timeout=30000)
            page.fill('input#password', RH_PASS)
            page.click('button[type="submit"][data-action-button-primary="true"]')
            page.wait_for_load_state('load')
            context.storage_state(path=state_file)

        while True:
            page.goto("https://hole.rabbit.tech/journal/details")
            page.wait_for_load_state('load')

            logging.info("Waiting for journal entries to appear...")
            try:
                page.wait_for_selector('.w-full:nth-child(2) > .mb-8 li', timeout=15000)
            except Exception as e:
                logging.error(f"Error waiting for journal entries: {e}")
                continue

            # Check for entries without SVG (svg found means it's an entry other than plain text which we don't want)
            entries = page.locator('.w-full:nth-child(2) > .mb-8 li')
            found_valid_entry = False

            for i in range(entries.count()):
                entry = entries.nth(i)
                if entry.locator('svg').count() == 0:
                    entry.click()
                    found_valid_entry = True
                    break

            if not found_valid_entry:
                logging.info("No valid entries without SVG found, reloading...")
                continue

            # Extracting info to put in database
            title = page.locator('.text-white-400').text_content()
            date = page.locator('.text-sm > div:nth-child(1)').text_content()
            time = page.locator('.text-sm > div:nth-child(2)').text_content()

            if entry_exists(title, date, time):
                logging.info("DB entry already exists, reloading to check for new entries...")
            else:
                save_entry(title, date, time)
                logging.info(f"Saved entry: {title}, {date}, {time}")
                # New entry detected, so below regex check the new entry's context and see if we want to do anything with it
                first_word = title.split()[0].strip().lower().strip('.,!?:;')

                logging.info(f"First word of title: {first_word}") # log first word (potential action) to terminal

                # First word = 'telegram', call TelegramParse function
                if re.match(r'^[a-z]+$', first_word) and first_word == "telegram":
                    if telegram_isenabled:
                        logging.info(f"Calling Telegram function with title: {title}")
                        TelegramParse(browser, title)
                    else:
                        log_disabled_integration("Telegram")
                # First word = 'computer', call ComputerParse function
                elif re.match(r'^[a-z]+$', first_word) and first_word == "computer":
                    if computer_isenabled:
                        logging.info(f"Calling Computer function with title: {title}")
                        ComputerParse(browser, title)
                    else:
                        log_disabled_integration("Computer")

if __name__ == "__main__":
    main()