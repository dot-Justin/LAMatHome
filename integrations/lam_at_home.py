import os
import sys
import logging
from utils import splash_screen, config, journal


def save(entry: journal.Entry) -> None:
    '''
    Save the given entry's resources to disk.
    '''
    if entry:
        # Save resources if enabled in config
        if config.config['lamathomesave_isenabled']:
            # resolve save path
            save_path = config.config['lamathomesave_path']
            save_path = os.path.expanduser(save_path)
            save_path = os.path.expandvars(save_path)
            
            # Ensure the directory exists
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path)
                except OSError as error:
                    logging.error(f"Error creating directory: {error}")
                    # Fallback to cache directory if creation fails
                    save_path = os.path.expandvars(config.config['cache_dir'])
            
            entry.save_resources(save_path)


def terminate() -> None:
    '''
    Terminate the LAMatHome application.
    '''
    if not config.config["lamathometerminate_isenabled"]:
        logging.error("LAMatHome termination is not enabled.")
        return
    print(splash_screen.colored_splash_goodbye)
    sys.exit()