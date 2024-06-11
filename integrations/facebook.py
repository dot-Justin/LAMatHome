import logging
from utils.get_env import FB_EMAIL, FB_PASS

logged_in = False

def login_facebook(page):
    """Logs into Facebook Messenger and handles initial pop-ups."""
    global logged_in
    if not logged_in:
        page.goto("https://www.messenger.com/")
        page.wait_for_load_state("load")
        page.fill('input[name="email"]', FB_EMAIL)
        page.fill('input[name="pass"]', FB_PASS)
        page.click('button[name="login"]')
        page.wait_for_load_state('load')
        
        # Close any initial pop-up
        try:
            if page.wait_for_selector('div[aria-label="Close"]', state='visible', timeout=5000):
                page.click('div[aria-label="Close"]', force=True)
        except Exception as e:
            logging.error(f"Error closing initial pop-up: {e}")
        
        page.click('text="Don\'t sync"')
        logged_in = True
        logging.info("Logged into Facebook Messenger")
    else:
        logging.info("Already logged into Facebook Messenger.")

def FacebookText(page, recipient, message):
    """Sends a message to a specific recipient on Facebook Messenger."""
    global logged_in
    if not logged_in:
        login_facebook(page)

    # Handle second popup if necessary
    try:
        if page.wait_for_selector('div[aria-label="Close"]', state='visible', timeout=5000):
            page.wait_for_timeout(500)
            page.wait_for_load_state('load')
            page.click('div[aria-label="Close"]', force=True)
            page.click('text="Don\'t sync"')
    except Exception as e:
        logging.error(f"Error closing second pop-up: {e}")

    # Search for the recipient and open the conversation
    search_box = page.locator('input[aria-label="Search Messenger"]')
    search_box.click()
    search_box.fill(recipient)

    # Use a more specific selector to find the recipient
    recipient_selector = 'a[role="presentation"][tabindex="-1"]'
    page.wait_for_timeout(5000)
    while True:
        recipient_elements = page.locator(recipient_selector).all()
        if recipient_elements:
            break

    # Filter the elements to find the one that matches the recipient's name
    for element in recipient_elements[1:]:
        element_text = element.inner_text()
        if recipient.lower() in element_text.lower():
            element.click()
            logging.info(f"Recipient {recipient} found.")
            break
    else:
        logging.error(f"Recipient {recipient} not found.")
        return False  # Exit the function if the recipient is not found

    # Wait for the message input box to be visible and focused
    page.wait_for_timeout(5000)
    message_box_selector = 'div[aria-label="Message"]'
    message_box = page.wait_for_selector(message_box_selector, state='visible')
    message_box.click()

    # Send the message
    message_box.fill(message)
    page.keyboard.press('Enter')
    page.wait_for_timeout(5000)
    page.close()
    logging.info(f"Message '{message}' sent to '{recipient}' on Facebook Messenger!")
    return True
