import os
import uuid
import json
import requests
import datetime
import logging
from urllib.parse import quote
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Any, Union
from utils import config, rabbit_hole


@dataclass
class Entry:
    _id: str
    userId: str
    createdOn: datetime.datetime
    modifiedOn: datetime.datetime
    archived: bool
    type: str
    title: str
    data: Dict[str, Any]
    utterance: Dict[str, str]


    def __post_init__(self):
        # Convert ISO 8601 string to datetime
        self.createdOn = self._convert_to_datetime(self.createdOn)
        self.modifiedOn = self._convert_to_datetime(self.modifiedOn)
    

    @staticmethod
    def _convert_to_datetime(date_str: str) -> datetime.datetime:
        try:
            return datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")


    def get_data(self) -> Dict[str, Any]:
        return self.data


    def set_data(self, new_data: Dict[str, Any]):
        self.data = new_data


@dataclass
class SearchEntry(Entry):
    pass


@dataclass
class ConversationEntry(Entry):
    pass


@dataclass
class NoteEntry(Entry):
    pass


@dataclass
class ImageEntry(Entry):
    data: dict


    def get_resource_urls(self):
        '''
        Returns a list of file URLs, if any, for the given entry.
        '''
        for key in ['aiGeneratedImageData', 'visionData']:
            if key in self.data:
                return [file.get('url') for file in self.data[key].get('files', []) if file.get('url')]
        return []
    

    def get_signed_resource_urls(self) -> List[str]:
        '''
        Returns a list of signed URLs, if any, for the given entry.
        '''
        response = rabbit_hole.fetch_user_entry_resource(json.dumps(self.get_resource_urls()))
        return response.get('resources', [])


    def save_resources(self, directory: str):
        '''
        Saves the files for the given entry, if any, to the specified directory.
        '''
        urls = self.get_resource_urls()
        signed_urls = rabbit_hole.fetch_user_entry_resource(json.dumps(urls))

        saved_files = []
        for idx, resource_url in enumerate(signed_urls['resources']):
            try:
                # fetch resource
                response = requests.get(resource_url)
                response.raise_for_status()

                # write file to disk
                save_name = self._id + "_" + urls[idx].split('/')[-1]
                save_path = os.path.join(directory, save_name)
                with open(save_path, 'wb+') as file:
                    file.write(response.content)
                saved_files.append(save_path)

                # log success
                save_path = save_path.replace("/", "\\")
                logging.info(f"Saved image to {save_path}")

            except requests.RequestException as e:
                logging.error(f"Failed to download image from {resource_url}: {e}")

            except Exception as e:
                logging.error(f"Failed to save resource: {e}")
        
        return saved_files


@dataclass
class AiGeneratedImageEntry(ImageEntry):
    pass


@dataclass
class VisionEntry(ImageEntry):
    pass


class Journal:
    def __init__(self, max_entries: int):
        self.entries = deque(maxlen=max_entries)
        self.interactions = deque(maxlen=max_entries)


    def add_entry(self, entry_data: Union[Dict[str, Any], str], llm_response: str = None) -> Union[Entry, None]:
        '''
        Adds an entry to the journal.
        '''
        if isinstance(entry_data, str):
            entry_data = self._create_basic_entry(entry_data)
        
        try:
            entry = self._create_entry(entry_data)
            self.entries.append(entry)
            if llm_response:
                self._add_interaction(entry, llm_response)
            return entry
        
        except (TypeError, ValueError) as e:
            print(f"Failed to instantiate entry: {e}")

    

    def _create_basic_entry(self, user_input: str) -> Dict[str, Any]:
        return {
            "_id": str(uuid.uuid1()),
            "userId": "local_user",
            "createdOn": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "modifiedOn": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "archived": False,
            "type": "conversation",
            "title": "CLI Input",
            "data": {"conversationData": {"textContent": ""}},
            "utterance": {"prompt": user_input, "intention": "CONVERSATION"}
        }

    def _create_entry(self, entry_data: Dict[str, Any]) -> Entry:
        entry_type = entry_data['type']
        if entry_type == 'search':
            return SearchEntry(**entry_data)
        elif entry_type == 'conversation':
            return ConversationEntry(**entry_data)
        elif entry_type == 'ai-generated-image':
            return AiGeneratedImageEntry(**entry_data)
        elif entry_type == 'vision':
            return VisionEntry(**entry_data)
        elif entry_type == 'note':
            return NoteEntry(**entry_data)
        else:
            raise ValueError(f"Unknown entry type: {entry_type}")


    def _add_interaction(self, entry: Entry, llm_response: str):
        interaction = {
            "_id": entry._id,
            "user prompt": entry.utterance['prompt'],
            "LLM response": llm_response
        }
        self.interactions.append(interaction)


    def last_entry(self) -> Union[Entry, None]:
        if self.entries:
            return self.entries[-1]
        return None


    def get_entries(self) -> List[Entry]:
        return list(self.entries)


    def get_entry_by_id(self, entry_id: str) -> Union[Entry, None]:
        for entry in self.entries:
            if entry._id == entry_id:
                return entry
        return None
    

    def get_entry_by_index(self, index: int) -> Union[Entry, None]:
        if 0 <= index < len(self.entries):
            return self.entries[index]
        return None
    

    def last_interaction(self) -> Union[Dict[str, str], None]:
        if self.interactions:
            return self.interactions[-1]
        return None
    

    def get_interactions(self) -> List[Dict[str, str]]:
        return list(self.interactions)
    

    def get_interaction_by_id(self, entry_id: str) -> Union[Dict[str, str], None]:
        for interaction in self.interactions:
            if interaction['_id'] == entry_id:
                return interaction
        return None


    def get_interaction_by_index(self, index: int) -> Union[Dict[str, str], None]:
        if 0 <= index < len(self.interactions):
            return self.interactions[index]
        return None
