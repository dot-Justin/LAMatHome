import os
import sys
import pytextnow
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from LAH_HOME_APP_MAIN.utils.get_env import TEXT_CSRF, TEXT_USERNAME, TEXT_SID
from LAH_HOME_APP_MAIN.utils.determine_contact import *

client = pytextnow.Client(TEXT_USERNAME, sid_cookie=TEXT_SID, csrf_cookie=TEXT_CSRF)


def send_sms(recipient, message):
    
    closest_match = find_closest_match(recipient, 'utils\contacts.json')

    if closest_match:
        print(f"Closest match: {closest_match['name']}")
        if closest_match['numbers']:
            first_number = closest_match['numbers'][0]
            print(f"Sending message to: {first_number}")
            client.send_sms(first_number, message)
        else:
            print("No numbers found for the closest match.")
    else:
        print("No match found.")

def send_mms(recipient, pic):
    client.send_mms(recipient, pic)