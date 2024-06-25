import uuid
import json
import requests
import os
import logging
from datetime import datetime, timezone
from collections import deque
from typing import Dict, Any, Type, Union, Optional
from pydantic import BaseModel, Field, field_validator
from utils import config, rabbit_hole

# Ensure logging is configured to display messages
logging.basicConfig(level=logging.INFO)


class Entry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias='_id')
    userId: str
    createdOn: datetime
    modifiedOn: datetime
    archived: bool
    type: str
    title: str
    data: Dict[str, Any]
    utterance: Dict[str, str]

    @field_validator('createdOn', 'modifiedOn', mode='before')
    def convert_to_datetime(cls, value: str) -> datetime:
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid date format: {value}")

    class Config:
        extra = 'ignore'
        populate_by_name = True


class ImageEntry(Entry):
    data: Dict[str, Any]

    def get_resource_urls(self):
        for key in ['aiGeneratedImageData', 'visionData']:
            if key in self.data:
                return [file.get('url') for file in self.data[key].get('files', []) if file.get('url')]
        return []

    def get_signed_resource_urls(self) -> list:
        try:
            response = rabbit_hole.fetch_user_entry_resource(json.dumps(self.get_resource_urls()))
            return response.get('resources', [])
        except Exception as e:
            logging.error(f"Failed to fetch signed resource URLs: {e}")
            return []

    def save_resources(self, directory: str) -> list:
        urls = self.get_resource_urls()
        signed_urls = self.get_signed_resource_urls()

        saved_files = []
        for idx, resource_url in enumerate(signed_urls):
            try:
                response = requests.get(resource_url)
                response.raise_for_status()

                save_name = self.id + "_" + urls[idx].split('/')[-1]
                save_path = os.path.join(directory, save_name)
                with open(save_path, 'wb+') as file:
                    file.write(response.content)
                saved_files.append(save_path)

                save_path = save_path.replace("/", "\\")
                logging.info(f"Saved image to {save_path}")

            except requests.RequestException as e:
                logging.error(f"Failed to download image from {resource_url}: {e}")

            except Exception as e:
                logging.error(f"Failed to save resource: {e}")

        return saved_files


class AiGeneratedImageEntry(ImageEntry):
    pass


class VisionEntry(ImageEntry):
    pass


class NoteEntry(Entry):
    pass


class ConversationEntry(Entry):
    pass


class SearchEntry(Entry):
    pass


class SearchMemoryEntry(Entry):
    pass


# Map entry types to their corresponding classes
entry_type_mapping = {
    'image': ImageEntry,
    'ai-generated-image': AiGeneratedImageEntry,
    'vision': VisionEntry,
    'note': NoteEntry,
    'conversation': ConversationEntry,
    'search': SearchEntry,
    'search-memory': SearchMemoryEntry
}

def create_entry_model(entry_data: Dict[str, Any]) -> Entry:
    entry_type = entry_data.get('type')
    EntryModel = entry_type_mapping.get(entry_type, Entry)
    return EntryModel(**entry_data)


class Journal:
    def __init__(self, max_entries: int):
        self.entries = deque(maxlen=max_entries)
        self.interactions = deque(maxlen=max_entries)

    def add_entry(self, entry_data: Union[Dict[str, Any], str], llm_response: str = None) -> Optional[Entry]:
        '''
        Adds an entry to the journal.
        '''
        if isinstance(entry_data, str):
            entry_data = self._create_basic_entry(entry_data)

        try:
            entry = self._create_entry(entry_data)
            if entry:  # Only add if entry is not None
                self._log_debug(f"Entry created successfully: {entry}")
                self.entries.append(entry)
                if llm_response:
                    self._add_interaction(entry, llm_response)
            return entry

        except (TypeError, ValueError) as e:
            logging.error(f"Failed to instantiate entry: {e}")
            return None

    def _create_basic_entry(self, user_input: str) -> Dict[str, Any]:
        return {
            "_id": str(uuid.uuid1()),
            "userId": "local_user",
            "createdOn": datetime.now(timezone.utc).isoformat(),
            "modifiedOn": datetime.now(timezone.utc).isoformat(),
            "archived": False,
            "type": "conversation",
            "title": "CLI Input",
            "data": {"conversationData": {"textContent": ""}},
            "utterance": {"prompt": user_input, "intention": "CONVERSATION"}
        }

    def _create_entry(self, entry_data: Dict[str, Any]) -> Optional[Entry]:
        entry_type = entry_data.get('type')
        entry_class: Type[Entry] = entry_type_mapping.get(entry_type)

        if entry_class is not None:
            self._log_debug(f"Creating entry of type: {entry_type}")
            try:
                entry = entry_class(**entry_data)
                return entry
            except Exception as e:
                logging.error(f"Error creating entry of type {entry_type}: {e}")
                return None
        else:
            self._log_debug(f"Unknown entry type: {entry_type}, skipping entry creation.")
            return None

    def _add_interaction(self, entry: Entry, llm_response: str):
        interaction = {
            "_id": entry.id,
            "user prompt": entry.utterance['prompt'],
            "LLM response": llm_response
        }
        self.interactions.append(interaction)

    def _log_debug(self, message: str):
        if config.config.get("debug", False):
            logging.info(message)

    def last_entry(self) -> Optional[Entry]:
        return self.entries[-1] if self.entries else None

    def get_entries(self) -> list:
        return list(self.entries)

    def get_entry_by_id(self, entry_id: str) -> Optional[Entry]:
        for entry in self.entries:
            if entry.id == entry_id:
                return entry
        return None

    def get_entry_by_index(self, index: int) -> Optional[Entry]:
        if 0 <= index < len(self.entries):
            return self.entries[index]
        return None

    def last_interaction(self) -> Optional[Dict[str, str]]:
        return self.interactions[-1] if self.interactions else None

    def get_interactions(self) -> list:
        return list(self.interactions)

    def get_interaction_by_id(self, entry_id: str) -> Optional[Dict[str, str]]:
        for interaction in self.interactions:
            if interaction['_id'] == entry_id:
                return interaction
        return None

    def get_interaction_by_index(self, index: int) -> Optional[Dict[str, str]]:
        if 0 <= index < len(self.interactions):
            return self.interactions[index]
        return None
