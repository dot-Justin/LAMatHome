import logging
from utils.contacts import contacts

def get_contact_name(integration, recipient):
    """Get the actual name from the recipient or its nickname for the given integration."""
    if integration not in contacts:
        logging.error(f"Integration {integration} not found.")
        return None

    for contact in contacts[integration]:
        if recipient.lower() == contact["name"].lower():
            return contact["name"]
        if recipient.lower() in [nickname.lower() for nickname in contact["nicknames"]]:
            return contact["name"]
    return None