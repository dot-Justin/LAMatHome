import logging
from utils.get_env import RH_EMAIL, RH_PASS

def login_hole_rabbit(page):
    
    """Logs into hole.rabbit.tech and saves authentication cookies."""
    page.goto("https://hole.rabbit.tech")
    if not page.url.startswith("https://hole.rabbit.tech/journal"):
        page.fill('input#username', RH_EMAIL)
        page.fill('input#password', RH_PASS)
        page.click('button[type="submit"][data-action-button-primary="true"]')
        page.wait_for_load_state('load')
        logging.info("Logged into hole.rabbit.tech")