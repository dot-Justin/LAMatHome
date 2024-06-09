import logging
import urllib.parse
import webbrowser
import subprocess
import platform

###############################
#         BrowserSite         #
###############################

def BrowserSite(title):
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

browsergoogle_isenabled = True

def BrowserGoogle(title):
    if not browsergoogle_isenabled:
        return

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

browseryoutube_isenabled = True

def BrowserYoutube(title):
    if not browseryoutube_isenabled:
        return

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

browsergmail_isenabled = True

def BrowserGmail(title):
    if not browsergmail_isenabled:
        return

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

browseramazon_isenabled = True

def BrowserAmazon(title):
    if not browseramazon_isenabled:
        return

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
