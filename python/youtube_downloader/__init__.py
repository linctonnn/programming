import os
import logging
from googleapiclient.discovery import build

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def load_env(filepath=".env"):
    """
    Load environment variables from a .env file.

    Args:
        filepath (str): Path to the .env file. Defaults to ".env".

    Raises:
        FileNotFoundError: If the .env file is not found.
        ValueError: If a line in the .env file is malformed.
    """

    try:
        with open(filepath, encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                # Skip empty lines or comments
                if not line or line.startswith("#"):
                    continue
                try:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if not key:
                        logging.warning(f"Skipping line with empty key: {line}")
                        continue
                    os.environ[key] = value
                    logging.debug(f"Loaded env var: {key}")
                except ValueError:
                    logging.warning(f"Skipping malformed line: {line}")
            logging.info(f"Environment variables loaded from {filepath}")
    except FileNotFoundError:
        logging.error(f"File {filepath} not found")
        raise
    except Exception as e:
        logging.error(f"Unexpected error loading env file: {e}")
        raise

class YouTube:
    """
    Wrapper class for YouTube Data API V3
    Serve function searching channel whit handle
    """

    def __init__(self):
        self.youtube_api_key = os.environ.get("YouTube_API")
        if not self.youtube_api_key:
            raise ValueError("Youtube API key not found in environment variables!")
        self.youtube = build("youtube", "v3", developerKey = self.youtube_api_key)

    def search_response(self, handle, max_results = 1):
        """
        Search for a YouTube channel by it's handle or name and return API response.

        Args:
            handle(str) : The YouTube channel handle or name (without @)
            max_results (int, optional) : Number of result to return. Default to 1.
        """

        handle = handle.lstrip("@")

        requests = self.youtube.search().list( 
                q = handle,
                part = "snippet",
                type = "channel",
                maxResults = max_results
                )
        response = requests.execute()
        return response

    def get_channel_id(self, channel_id):
        pass

if __name__ == "__main__":
    user_input = input("Enter the YouTube channel handle (with or without @): ").lstrip('@')
    youtube = YouTube()
    result = youtube.search_response(user_input) 
    print(result)
