import os
import requests

class FileManager:
    def __init__(self):
        self.timeout = 10 

    def download_file(self, url: str, save_path: str) -> bool:
        """
        Downloads a file from a URL to a local path.
        Returns True if successful, False otherwise.
        """
        if os.path.exists(save_path):
            return False

        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True

        except Exception as e:
            print(f"\n❌ Error saving {save_path}: {e}")
            return False