from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
from utils.get_env import ICLOUD_USER, ICLOUD_PASS
import os

class ICloudManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api = None

    def connect(self):
        try:
            self.api = PyiCloudService(self.username, self.password)

            if self.api.requires_2fa:
                print("Two-factor authentication required.")
                code = input("Enter the code you received on your devices: ")
                result = self.api.validate_2fa_code(code)
                print("Code validation result: ", result)

                if not result:
                    print("Failed to verify security code")
                    return False

                if not self.api.is_trusted_session:
                    print("Session is not trusted. Requesting trust...")
                    result = self.api.trust_session()
                    print("Session trust result: ", result)

                    if not result:
                        print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
                        return False

            print("Successfully connected to iCloud.")
            return True

        except PyiCloudFailedLoginException:
            print("Failed to log in to iCloud. Please check your credentials.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

class ICloudGatherer:
    def __init__(self, api):
        self.api = api

    def get_photos(self):
        try:
            photos = self.api.photos.all
            return photos
        except Exception as e:
            print(f"An error occurred while fetching photos: {e}")
            return []

    def get_contacts(self):
        try:
            contacts = self.api.contacts.all()
            return contacts
        except Exception as e:
            print(f"An error occurred while fetching contacts: {e}")
            return []

    def get_notes(self):
        try:
            notes = self.api.notes.all()
            return notes
        except Exception as e:
            print(f"An error occurred while fetching notes: {e}")
            return []

class ICloudSender:
    def __init__(self, api):
        self.api = api

    def upload_photo(self, photo_path):
        try:
            with open(photo_path, 'rb') as photo_file:
                self.api.photos.upload(photo_file)
            print(f"Photo '{photo_path}' uploaded successfully to iCloud.")
            return True
        except Exception as e:
            print(f"An error occurred while uploading the photo: {e}")
            return False

def main():
    # Replace with your iCloud credentials
    ICLOUD_USERNAME = ICLOUD_USER
    ICLOUD_PASSWORD = ICLOUD_PASS

    # Path to the photo you want to upload
    PHOTO_PATH = 'assets/LAH_splash.png'

    icloud_manager = ICloudManager(ICLOUD_USERNAME, ICLOUD_PASSWORD)

    if icloud_manager.connect():
        gatherer = ICloudGatherer(icloud_manager.api)
        sender = ICloudSender(icloud_manager.api)

        photos = gatherer.get_photos()
        print(f"Retrieved {len(photos)} photos from iCloud.")

        contacts = gatherer.get_contacts()
        print(f"Retrieved {len(contacts)} contacts from iCloud.")

        notes = gatherer.get_notes()
        print(f"Retrieved {len(notes)} notes from iCloud.")

        if os.path.exists(PHOTO_PATH):
            sender.upload_photo(PHOTO_PATH)
        else:
            print(f"Photo path '{PHOTO_PATH}' does not exist.")

if __name__ == "__main__":
    main()