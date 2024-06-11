import time
import logging
from utils.get_env import DC_EMAIL, DC_PASS


dc_logged_in = False

def login_discord(page):
    """Logs into Discord and saves authentication cookies."""
    global dc_logged_in
    if not dc_logged_in:
        page.goto("https://discord.com/login")
        page.fill('input[name="email"]', DC_EMAIL)
        page.fill('input[name="password"]', DC_PASS)
        page.wait_for_timeout(3000)  # Adjust wait time if needed
        page.keyboard.press("Enter")
        page.wait_for_load_state('load')
        page.wait_for_selector('text=Friends', timeout=60000)
        logging.info("Logged into Discord")
        dc_logged_in = True
    else:
        logging.info("Already logged into Discord.")

def DiscordText(page, recipient, message):
    if not (page, recipient, message):
        logging.error(f'Missing one of the required parameters to complete the task ({page}, {recipient}, or {message})')
        pass
    else:
        """Sends a message to a specific recipient on Discord."""
        global dc_logged_in
        if not dc_logged_in:
            login_discord(page)
        page.goto("https://discord.com/channels/@me")
        page.wait_for_load_state('load')

        # Ensure the page is focused
        page.bring_to_front()
        # Wait for the quick switcher to be visible and then click on it
        search_Butt = page.wait_for_selector('button[class^="searchBarComponent__"]')
        search_Butt.click()
        quick_switcher = page.wait_for_selector('input[aria-label="Quick switcher"]')
        if recipient and message:
            quick_switcher.fill(recipient)
            time.sleep(5)
            quick_switcher.press("Enter")
            time.sleep(5)  # Give time for recipient to load
            
        # Wait for the message box to be ready
            page.fill('div[role="textbox"]', message)
            page.keyboard.press("Enter")
            logging.info(f"Message '{message}' sent to '{recipient}' on Discord!")
            time.sleep(5)
            page.close()
        else:
            page.close()
            logging.error(f"Message was not sent on Discord!")
        
        return True
