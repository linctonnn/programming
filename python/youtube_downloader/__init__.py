import os
import logging
from googleapiclient.discovery import build

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_env(filepath=".env"):
    """
    Load environment variables from a .env file.

    Args:
        filepath (str): Path to the .env file. Defaults to ".env".

    Raises:
        FileNotFoundError: If the .env file is not found.
    """
    try:
        with open(filepath, encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    logging.warning(f"Skipping malformed line (no '='): {line}")
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if not key:
                    logging.warning(f"Skipping line with empty key: {line}")
                    continue
                os.environ[key] = value
                logging.debug(f"Loaded env var: {key}")
        logging.info(f"Environment variables loaded from {filepath}")
    except FileNotFoundError:
        logging.error(f"File {filepath} not found")
        raise
    except Exception as e:
        logging.error(f"Unexpected error loading env file: {e}")
        raise

class YouTube:
    """
    Wrapper class for YouTube Data API v3.

    Provides method to search channels by handle or name.
    """

    def __init__(self):
        self.youtube_api_key = os.environ.get("YouTube_API")
        if not self.youtube_api_key:
            logging.error("YouTube API key not found in environment variables!")
            raise ValueError("YouTube API key not found in environment variables!")
        self.youtube = build("youtube", "v3", developerKey=self.youtube_api_key)
        logging.info("YouTube API client initialized")

    def search_response(self, handle, max_results=1):
        """
        Search for a YouTube channel by its handle or name and return API response.

        Args:
            handle (str): The YouTube channel handle or name (without @).
            max_results (int, optional): Number of results to return. Defaults to 1.

        Returns:
            dict: Response from YouTube Data API.
        """
        handle = handle.lstrip("@")
        try:
            request = self.youtube.search().list(
                q=handle,
                part="snippet",
                type="channel",
                maxResults=max_results
            )
            response = request.execute()
            logging.info(f"Search completed for handle: {handle}")
            return response
        except Exception as e:
            logging.error(f"Error during YouTube search: {e}")
            return None

    def get_channel_id(self, channel_id):
        """
        Placeholder for method to get channel details by channel ID.
        """
        pass

if __name__ == "__main__":
    load_env()
    user_input = input("Enter the YouTube channel handle (with or without @): ").lstrip('@')
    youtube = YouTube()
    result = youtube.search_response(user_input)
    if result:
        print(result)
    else:
        logging.error("Failed to get search result")

