import urllib.parse
import webbrowser
import logging
from utils.helpers import log_disabled_integration

browser_isenabled=True

###############################
#         BrowserSite         #
###############################

browsersite_isenabled = True

def BrowserSite(title):
    try:
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

    # words = title.split()
    encoded_query = urllib.parse.quote(title)
    url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened Google search for query: {title}")

###########################
#      BrowserYoutube     #
###########################

browseryoutube_isenabled = True

def BrowserYoutube(title):
    if not browseryoutube_isenabled:
        return

    query = title
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened YouTube search for query: {query}")

#########################
#      BrowserGmail     #
#########################

browsergmail_isenabled = True

def BrowserGmail(title):
    if not browsergmail_isenabled:
        return
    encoded_query = urllib.parse.quote(title)
    url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened Gmail search for query: {title}")

##########################
#      BrowserAmazon     #
##########################

browseramazon_isenabled = True

def BrowserAmazon(title):
    if not browseramazon_isenabled:
        return

    encoded_query = urllib.parse.quote(title)
    url = f"https://www.amazon.com/s?k={encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened Amazon search for query: {title}")