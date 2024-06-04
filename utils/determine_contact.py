import json
from fuzzywuzzy import fuzz

def find_closest_match(recipient, json_file):
  """Finds the closest contact match in a JSON file.

  Args:
    search_string: The string to search for.
    json_file: Path to the JSON file containing contacts.

  Returns:
    A dictionary containing the closest matching contact, or None if no match is found.
  """

  with open(json_file, 'r') as f:
    contacts = json.load(f)

  best_match = None
  best_score = 0

  for contact in contacts:
    name_score = fuzz.ratio(recipient.lower(), contact['name'].lower())
    if name_score > best_score:
      best_match = contact
      best_score = name_score

  return best_match
