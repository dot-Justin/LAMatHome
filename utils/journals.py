import requests
import time
from datetime import datetime, timedelta
from get_env import RH_ACCESS_TOKEN


def get_all_journals():
    '''
    Fetches all journal entries for the given user.
    TODO: Add pagination support when rabbit hole API supports it.
    '''
    fetchJournalEndpoint = f"https://hole.rabbit.tech/apis/fetchUserJournal"
    headers = {
        "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
        "content-type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
    }
    body = {
        "accessToken": RH_ACCESS_TOKEN,
    }

    try:
        response = requests.post(fetchJournalEndpoint, headers=headers, json=body)
        response.raise_for_status()  # Raise an error for bad status codes
        responseDict = response.json()
        return responseDict
    except requests.exceptions.RequestException as e:
        print(f"Error fetching journals: {e}")
        return None


def is_valid_iso_format(timestamp):
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def get_journals(before=None, after=None):
    # Validate timestamps
    if before and not is_valid_iso_format(before):
        raise ValueError("Invalid 'before' timestamp format")
    if after and not is_valid_iso_format(after):
        raise ValueError("Invalid 'after' timestamp format")

    # Check timestamp logic
    if before and after and before <= after:
        raise ValueError("'before' timestamp must be after 'after' timestamp")

    responseDict = get_all_journals()
    if not responseDict:
        return []

    journalEntries = responseDict.get('journal', {}).get('entries', [])

    # Filter journals based on before and after timestamps
    if before is not None:
        journalEntries = list(filter(lambda x: x["createdOn"] < before, journalEntries))
    if after is not None:
        journalEntries = list(filter(lambda x: x["createdOn"] > after, journalEntries))

    return journalEntries


def journal_entries_generator(after_timestamp, intention_filter=None):
    while True:
        new_entries = get_journals(after=after_timestamp)
        if new_entries:
            for entry in new_entries:
                if intention_filter == None or entry['utterance']['intention'] == intention_filter:
                    yield entry
            # Update the after_timestamp to the latest entry's createdOn timestamp so we always get new entries
            after_timestamp = new_entries[-1]['createdOn']
        else:
            # If no new entries, wait for a while before checking again
            time.sleep(2)


if __name__ == "__main__":
    # Example usage of the journal_entries_generator
    # Assuming the initial after_timestamp is the current time in ISO format
    # TODO: switch from using datetime.utcnow since its deprecated
    initial_timestamp = datetime.utcnow().isoformat() + 'Z'
    generator = journal_entries_generator(initial_timestamp, "CONVERSATION")

    # Print the journal entries as they come in real-time
    for entry in generator:
        print(entry)

