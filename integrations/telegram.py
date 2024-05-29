import logging
import os
from utils.helpers import log_disabled_integration

#############################################################
#                                                           #
#                          Telegram:                        #
#                                                           #
#############################################################

# Set False to disable Computer integration altogether
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

    if page.is_visible('text=Chats'):
        logging.info("Already logged in to Telegram.")
    else:
        logging.info("Telegram session expired, logging in again.")

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Telegram message.")
        return

    user_search = words[1]
    message = " ".join(words[2:])

    logging.info(f"User to search: {user_search}")
    logging.info(f"Message to send: {message}")

    login_successful = False
    for _ in range(3):
        try:
            page.wait_for_selector('[placeholder=" "]', timeout=30000)
            login_successful = True
            break
        except:
            page.reload()

    if login_successful:
        context.storage_state(path=session_file)

        page.fill('[placeholder=" "]', user_search)
        page.press('[placeholder=" "]', 'Enter')
        page.wait_for_timeout(1000)

        if page.is_visible('.search-super-content-chats a'):
            page.click('.search-super-content-chats a')
            page.wait_for_timeout(1000)

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

    context.storage_state(path=session_file)
    context.close()
