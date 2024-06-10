import logging
from utils.get_env import G_HOME_EMAIL, G_HOME_PASS

def GoogleHome(page, automation):
    """Opens Google home, logs in if necessary, and runs the automation."""
    session_file = "cache/state.json"
    context = page.context

    page.goto("https://home.google.com")
    logging.info(f"Opening Google Home page: {page.url}")
    logging.info(f"Automation to run: {automation}")

    # If not logged in
    if page.url == "https://home.google.com/welcome/" or page.is_visible("text=From smart lights to smart locks"):
        logging.info("Not logged in, proceeding with login steps")
        page.wait_for_load_state('load')
        page.click("text=Go to Google Home")
        logging.info("Clicked 'Go to Google Home'")

        page.fill("input[type=email]", G_HOME_EMAIL)
        logging.info(f"Filled in email: {G_HOME_EMAIL}")

        page.click("text=Next")
        logging.info("Clicked 'Next' after email")

        page.fill("input[type=password]", G_HOME_PASS)
        logging.info("Filled in password")

        page.click("text=Next")
        logging.info("Clicked 'Next' after password")

        if page.is_visible("text=Simplify your sign-in"):
            page.click("text=Not now")
            logging.info("Clicked 'Not now' for simplify sign-in prompt")

        page.click("text=OK")
        logging.info("Clicked 'OK' after logging in")
        page.wait_for_load_state('load')

    logging.info("Page is visible with 'OK' button")
    page.wait_for_load_state('load')
    page.click("text=OK")
    logging.info("Clicked 'OK' button")

    # Locate the automation div and click the play button
    automation_div = page.locator(f"//div[contains(@class, 'automation-name') and normalize-space(text())='{automation}']").first
    if automation_div.is_visible():
        logging.info(f'Google Home "{automation}" was found')
        play_button = automation_div.locator("xpath=ancestor::mat-card//button[@aria-label='Start automation']").first
        if play_button.is_visible():
            play_button.click()
            logging.info(f'Google Home "{automation}" play button was clicked')
        else:
            logging.error(f'Play button for "{automation}" is not visible')
    else:
        logging.error(f'Google Home "{automation}" is not available')
    
    context.storage_state(path=session_file)
    logging.info(f"Saved browser state to {session_file}")
    page.close()
    logging.info("Browser closed")
