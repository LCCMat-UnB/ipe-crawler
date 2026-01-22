import requests
import os
import time
from src.file_manager import FileManager

class GitHubConnector:
    def __init__(self, token: str = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        else:
            print("⚠️ GitHubConnector initialized without token. Rate limits will be strict.")

        self.file_manager = FileManager()

    def search_files(self, query: str) -> int:
        """
        Paginated search with smart backoff handling for 403 errors.
        """
        base_search_url = f"{self.base_url}/search/code"
        downloaded_count = 0
        
        # Max limits
        max_pages = 9 
        items_per_page = 30 
        
        page = 1
        while page <= max_pages:
            print(f"      ... Paginating: Page {page} for '{query}'")
            
            params = {
                "q": query,
                "per_page": items_per_page,
                "page": page
            }

            try:
                response = requests.get(base_search_url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    
                    if not items:
                        print("      -> No more items found. Stopping pagination.")
                        break

                    for item in items:
                        raw_url = item.get("download_url")
                        file_path = item.get("path")
                        repo = item.get("repository", {}).get("full_name", "unknown")
                        
                        if raw_url:
                            safe_repo = repo.replace("/", "__").replace(":", "")
                            filename = os.path.basename(file_path)
                            save_path = f"data/raw/{safe_repo}/{filename}"
                            
                            if self.file_manager.download_file(raw_url, save_path):
                                downloaded_count += 1
                                print(f"      [OK] {filename}")
                        
                        time.sleep(0.1)

                    page += 1
                    time.sleep(2) 

                elif response.status_code == 403:
                    print("\n      ⏳ Rate Limit Hit (403). Waiting 60 seconds to cool down...")
                    time.sleep(60)
                    print("      🔄 Retrying page...")
                    continue

                else:
                    print(f"\n      ❌ Error {response.status_code}: {response.text}")
                    break

            except Exception as e:
                print(f"\n      ❌ Network Error: {e}")
                break
                
        return downloaded_count