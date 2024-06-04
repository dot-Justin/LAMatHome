import sys
from utils.splashscreen import colored_splash_goodbye

lamathome_isenabled = True
lamathometerminate_isenabled = True

# Function to sys.exit to terminate LAH
def terminate():
    print(colored_splash_goodbye)
    sys.exit()

# if __name__ == "__main__":
#     print(colored_splash_goodbye)