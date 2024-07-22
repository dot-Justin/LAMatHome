import os
import sys
import logging
from utils import splash_screen, config, journal


def save(user_journal: journal.Journal, entry: journal.Entry) -> None:
    '''
    Save the given entry's resources to disk.
    '''
    if entry:
        # Save resources if enabled in config
        if config.config['lamathomesave_isenabled']:
            # resolve save path
            save_path = config.config['lamathomesave_path']
            save_path = os.path.expanduser(save_path)
            
            # Split the path into components using os.path.split
            path_components = []
            while True:
                save_path, tail = os.path.split(save_path)
                if tail:
                    path_components.insert(0, tail)
                else:
                    if save_path:
                        path_components.insert(0, save_path)
                    break
            
            # Join the path components using os.path.join
            save_path = os.path.join(*path_components)
            
            # Ensure the directory exists
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path)
                except OSError as error:
                    logging.error(f"Error creating directory: {error}")
                    # Fallback to cache directory if creation fails
                    save_path = os.path.expandvars(config.config['cache_dir'])
            
            user_journal.save_resources(entry, save_path)


def terminate() -> None:
    '''
    Terminate the LAMatHome application.
    '''
    if not config.config["lamathometerminate_isenabled"]:
        logging.error("LAMatHome termination is not enabled.")
        return
    print(splash_screen.colored_splash_goodbye)
    sys.exit()