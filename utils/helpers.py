import logging

async def log_disabled_integration(integration_name):
    logging.info(f"Attempted to call {integration_name}, but it is disabled.")
