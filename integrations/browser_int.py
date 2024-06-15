import logging
import urllib.parse
import webbrowser
import subprocess
import platform
import shlex
import re
from groq import Groq
from utils import config, get_env

integration_name = "browser_int"

def get_api_configuration():
    GROQ_API_KEY = get_env.GROQ_API_KEY
    if GROQ_API_KEY:
        return GROQ_API_KEY
    else:
        raise ValueError("No valid API key found. Please set GROQ_API_KEY in your environment variables.")

def handle_command(command_text, temperature=0.1, top_p=1):
    api_key = get_api_configuration()
    client = Groq(api_key=api_key)

    flags = parse_flags(command_text)
    log_message = flags.get('--log')

    if log_message:
        logging.info(log_message)

    # Check for presence of any actionable flag
    actionable_flags = {flag: value for flag, value in flags.items() if value is not None}
    if not actionable_flags:
        logging.error("No actionable flag provided in the command.")
        return

    messages = [
        {
            "role": "system",
            "content": """
            You are an advanced LLM specializing in intention triage and data parsing. You will receive a message from the user and need to respond with a relevant action in the form of a precise command based on the message. The commands you can use are:
            You NEVER conversate with the user, you are strictly the backend converting the user message into a command.

            browser_int --site "https://site"
            Opens a specified website in the default browser.

            browser_int --google "search query"
            Opens a Google search for the specified query in the default browser.

            browser_int --youtube "search query"
            Opens a YouTube search for the specified query in the default browser.

            browser_int --gmail "search query"
            Opens a Gmail search.

            browser_int --amazon "search query"
            Opens an Amazon search for the specified query in the default browser.

            Command flags:
            You also have access to the following command flags:

            --log "message"
            Logs a message to the user.
            Ensure that each command is clearly formatted and precisely executed based on the user's message.

            ### Examples:
            Utterance: "Open Google for cute corgis"
            Command: browser_int --google "cute corgis"

            Utterance: "Search amazon for sunglasses"
            Command: browser_int --amazon "sunglasses"

            Utterance: "Open the link for wikipedia."
            Command: browser_int --site "https://wikipedia.org"

            Utterance: "Search on youtube for reviews about the rabbit r1"
            Command: browser_int --youtube "rabbit r1 review"

            Utterance: "Open a search on google for, I don't know, some random weird thing."
            Command: browser_int --google "purple watermelon"
            Note: Be creative with some commands that are ambiguous like this.

            ### Other things to note:
            Open links: You have the ability to open links in your default browser. If the user asks to open a link, open it. If the user asks to open a search on a specific website, attempt to do so. If you do not know the url structure for a site, cancel the command by simply outputting ""
            """
        },
        {
            "role": "user",
            "content": f"""
            PROMPT TO RESPOND TO: {command_text}
            """
        }
    ]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
            temperature=temperature,
            top_p=top_p
        )

        logging.info(f"Full response from Groq API: {chat_completion}") if config.config["debug"] else None

        if chat_completion.choices and chat_completion.choices[0].message and chat_completion.choices[0].message.content:
            response_text = chat_completion.choices[0].message.content.strip()
            logging.info(f"Response text: {response_text}")

            match = re.search(r'`([^`]+)`', response_text)
            if match:
                response_text = match.group(1)

            execute_parsed_command(response_text)
        else:
            logging.error(f"Unexpected response structure: {chat_completion}")
            raise ValueError("Invalid response structure")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise ValueError(f"Failed to get response from API: {e}")

def parse_flags(command_text):
    """Parse command flags from the command text."""
    parts = shlex.split(command_text)
    flags = {
        '--site': None,
        '--google': None,
        '--youtube': None,
        '--gmail': None,
        '--amazon': None,
        '--log': None
    }
    current_flag = None
    for part in parts:
        if part.startswith('--'):
            current_flag = part
        elif current_flag:
            flags[current_flag] = part
            current_flag = None
    return flags

def execute_parsed_command(parsed_command):
    flags = parse_flags(parsed_command)
    
    for flag, value in flags.items():
        if value:
            command = flag[2:].strip().lower()
            if command == "site":
                BrowserSite(value)
            elif command == "google":
                BrowserGoogle(value)
            elif command == "youtube":
                BrowserYoutube(value)
            elif command == "gmail":
                BrowserGmail(value)
            elif command == "amazon":
                BrowserAmazon(value)
            else:
                logging.error(f"Unknown {integration_name} command: {command}")

###############################
#         BrowserSite         #
###############################

def BrowserSite(title):
    if not config.config["browsersite_isenabled"]:
        logging.error("BrowserSite is not enabled in the config file.")
    else:
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', 'Safari', title])
            else:  # Windows or other OS
                webbrowser.open(title)
            logging.info(f"Opened website: {title}")
        except Exception as e:
            logging.error(f"Failed to open website: {e}")

###########################
#      BrowserGoogle      #
###########################

def BrowserGoogle(title):
    if not config.config["browsergoogle_isenabled"]:
        logging.error("BrowserGoogle is not enabled in the config file.")
    else:
        encoded_query = urllib.parse.quote(title)
        url = f"https://www.google.com/search?q={encoded_query}"
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', 'Safari', url])
            else:  # Windows or other OS
                webbrowser.open(url)
            logging.info(f"Opened Google search for query: {title}")
        except Exception as e:
            logging.error(f"Failed to open Google search: {e}")

###########################
#      BrowserYoutube     #
###########################

def BrowserYoutube(title):
    if not config.config["browseryoutube_isenabled"]:
        logging.error("BrowserYoutube is not enabled in the config file.")
    else:
        encoded_query = urllib.parse.quote(title)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"

        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', 'Safari', url])
            else:  # Windows or other OS
                webbrowser.open(url)
            logging.info(f"Opened YouTube search for query: {title}")
        except Exception as e:
            logging.error(f"Failed to open YouTube search: {e}")

#########################
#      BrowserGmail     #
#########################

def BrowserGmail(title):
    if not config.config["browsergmail_isenabled"]:
        logging.error("BrowserGmail is not enabled in the config file.")
    else:
        encoded_query = urllib.parse.quote(title)
        url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"

        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', 'Safari', url])
            else:  # Windows or other OS
                webbrowser.open(url)
            logging.info(f"Opened Gmail search for query: {title}")
        except Exception as e:
            logging.error(f"Failed to open Gmail search: {e}")

##########################
#      BrowserAmazon     #
##########################

def BrowserAmazon(title):
    if not config.config["browseramazon_isenabled"]:
        logging.error("BrowserAmazon is not enabled in the config file.")
    else:
        encoded_query = urllib.parse.quote(title)
        url = f"https://www.amazon.com/s?k={encoded_query}"

        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', 'Safari', url])
            else:  # Windows or other OS
                webbrowser.open(url)
            logging.info(f"Opened Amazon search for query: {title}")
        except Exception as e:
            logging.error(f"Failed to open Amazon search: {e}")
