import sys
from utils.splashscreen import colored_splash_goodbye


# Function to sys.exit to terminate LAH
def terminate():
    print(colored_splash_goodbye)
    sys.exit()