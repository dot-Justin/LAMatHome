import json
import os

def load_config():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_file = os.path.join(project_root, 'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

config = load_config()
