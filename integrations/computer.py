import re
import urllib.parse
import webbrowser
import ctypes
import logging
import time
from utils.helpers import log_disabled_integration

#############################################################
#                                                           #
#                          Computer:                        #
#                                                           #
#############################################################

computer_isenabled = True

def ComputerParse(browser, title):
    if not computer_isenabled:
        log_disabled_integration("Computer")
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer command.")
        return

    second_word = words[1].strip('.,!?:;').lower()
    if second_word in ["google", "youtube", "gmail", "amazon", "volume", "run", "launch", "open"]:
        if second_word == "google":
            if computergoogle_isenabled:
                ComputerGoogle(title)
            else:
                log_disabled_integration("ComputerGoogle")
        elif second_word == "youtube":
            if computeryoutube_isenabled:
                ComputerYoutube(title)
            else:
                log_disabled_integration("ComputerYoutube")
        elif second_word == "gmail":
            if computergmail_isenabled:
                ComputerGmail(title)
            else:
                log_disabled_integration("ComputerGmail")
        elif second_word == "amazon":
            if computeramazon_isenabled:
                ComputerAmazon(title)
            else:
                log_disabled_integration("ComputerAmazon")
        elif second_word == "volume":
            if computervolume_isenabled:
                ComputerVolume(title)
            else:
                log_disabled_integration("ComputerVolume")
        elif second_word in ["run", "launch", "open"]:
            if computerrun_isenabled:
                ComputerRun(title)
            else:
                log_disabled_integration("ComputerRun")
    else:
        logging.error("Unknown Computer command or the integration is not enabled.")

############################
#      ComputerGoogle      #
############################

computergoogle_isenabled = True

def ComputerGoogle(title):
    if not computergoogle_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Google command.")
        return

    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened Google search for query: {query}")

############################
#      ComputerYoutube     #
############################

computeryoutube_isenabled = True

def ComputerYoutube(title):
    if not computeryoutube_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Youtube command.")
        return

    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened YouTube search for query: {query}")

##########################
#      ComputerGmail     #
##########################

computergmail_isenabled = True

def ComputerGmail(title):
    if not computergmail_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Gmail command.")
        return

    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://mail.google.com/mail/u/0/#search/{encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened Gmail search for query: {query}")

###########################
#      ComputerAmazon     #
###########################

computeramazon_isenabled = True

def ComputerAmazon(title):
    if not computeramazon_isenabled:
        return

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Amazon command.")
        return

    query = " ".join(words[2:])
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.amazon.com/s?k={encoded_query}"

    webbrowser.open(url)
    logging.info(f"Opened Amazon search for query: {query}")

############################
#      ComputerVolume      #
############################

computervolume_isenabled = True

vol_up_step_value = 4
vol_down_step_value = 4

def ComputerVolume(title):
    if not computervolume_isenabled:
        log_disabled_integration("ComputerVolume")
        return

    title_cleaned = re.sub(r'[^\w\s]', '', title).lower()

    words = title_cleaned.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Volume command.")
        return

    volume_word = words[2]
    
    if volume_word == "mute":
        try:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            logging.info("Muted the volume")
        except Exception as e:
            logging.error(f"Failed to mute volume: {e}")
        return

    if volume_word == "unmute":
        try:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            logging.info("Unmuted the volume")
        except Exception as e:
            logging.error(f"Failed to unmute volume: {e}")
        return

    if volume_word == "up":
        try:
            for _ in range(vol_up_step_value):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            logging.info(f"Increased volume by {vol_up_step_value} steps")
        except Exception as e:
            logging.error(f"Failed to increase volume: {e}")
        return

    if volume_word == "down":
        try:
            for _ in range(vol_down_step_value):
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            logging.info(f"Decreased volume by {vol_down_step_value} steps")
        except Exception as e:
            logging.error(f"Failed to decrease volume: {e}")
        return

    try:
        volume_value = int(volume_word)
        if volume_value < 0 or volume_value > 100:
            raise ValueError
    except ValueError:
        logging.error(f"Invalid volume value: {volume_word}. Must be an integer between 0 and 100.")
        return

    try:
        for _ in range(50):
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
        for _ in range(volume_value // 2):
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
        logging.info(f"Set volume to {volume_value}%")
    except Exception as e:
        logging.error(f"Failed to set volume: {e}")

###############################
#         ComputerRun         #
###############################

computerrun_isenabled = True

def ComputerRun(title):
    if not computerrun_isenabled:
        log_disabled_integration("ComputerRun")
        return

    title_cleaned = re.sub(r'[^\w\s]', '', title).lower()
    words = title_cleaned.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Run command.")
        return

    command = " ".join(words[2:])

    try:
        # Press Windows key
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)
        time.sleep(0.1)

        # Type the command
        for char in command:
            vk = ctypes.windll.user32.VkKeyScanW(ord(char))
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)
            time.sleep(0.05)

        # Press Enter
        ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)
        
        logging.info(f"Executed command: {command}")
    except Exception as e:
        logging.error(f"Failed to execute command: {e}")
