import logging


def TelegramText(page, recipient, message):

    session_file = "cache/state.json"
    context = page.context
    page = context.new_page()
    page.goto("https://web.telegram.org/k/")

    if page.is_visible('text=Chats'):
        logging.info("Already logged in to Telegram.")
    else:
        logging.info("Telegram session expired, logging in again.")

    logging.info(f"User to search: {recipient}")
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

        page.fill('[placeholder=" "]', recipient)
        page.press('[placeholder=" "]', 'Enter')
        page.wait_for_timeout(1000)

        if page.is_visible('.search-super-content-chats a'):
            page.click('.search-super-content-chats a')
            page.wait_for_timeout(1000)

            page.fill('.input-message-input:nth-child(1)', message)
            page.click('.btn-send > .c-ripple')

            logging.info(f"Sent message to {recipient}: {message}")
        else:
            logging.error("No users found, aborting.")
            context.close()
            return
    else:
        logging.error("Failed to log in to Telegram after multiple attempts")
        context.close()
        return

    context.storage_state(path=session_file)
    # Close the telegram page, but keep context open for other integrations
    page.close()
    