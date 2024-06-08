import re
import time
import ctypes
import logging
from utils.helpers import log_disabled_integration


############################
#      ComputerVolume      #
############################

vol_up_step_value = 4
vol_down_step_value = 4

def ComputerVolume(title):

    title_cleaned = re.sub(r'[^\w\s]', '', title).lower()

    words = title_cleaned.split()
    if len(words) < 3:
        logging.error(f"Invalid prompt format '{title_cleaned}' for Computer Volume command.")
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


#################################
#         ComputerMedia         #
#################################

computermedia_isenabled = True

def ComputerMedia(title):
    if not computermedia_isenabled:
        log_disabled_integration("ComputerMedia")
        return
    
    words = title.split()

    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Skip command.")
        return

    if words[2] == "next": # words[2] is the action
        try:
            ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0) # key up event
            logging.info("Skipped to the next song")
        except Exception as e:
            logging.error(f"Failed to skip to the next song: {e}")
            return
    elif words[2] == "back":
        try:
            ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0) # key up event
            logging.info("Skipped to the previous song")
            return
        except:
            logging.error(f"Failed to skip to the previous song: {e}")
            return
    elif words[2] == "play":
        try:
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0) # key up event
            logging.info("Play the current song")
            return
        except:
            logging.error(f"Failed to play/pause the current song: {e}")
            return
    elif words[2] == "pause":
        try:
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0) # key up event
            logging.info("Pause the current song")
            return
        except:
            logging.error(f"Failed to pause the current song: {e}")
            return
    else:
        logging.error("Invalid prompt format for Computer Skip command.")
        return