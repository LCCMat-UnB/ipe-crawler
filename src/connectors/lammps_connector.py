import requests
import os
import time
from src.file_manager import FileManager

class LammpsOfficialConnector:
    """
    Directly scrapes the 'potentials' directory from the official LAMMPS GitHub repository.
    Source: https://github.com/lammps/lammps
    """
    def __init__(self, token: str = None):
        self.api_url = "https://api.github.com/repos/lammps/lammps/contents/potentials"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        
        self.file_manager = FileManager()
        # Extensions we care about
        self.target_extensions = {
            '.reax', 'ffield', '.eam', '.alloy', '.fs', '.meam', 
            '.sw', '.tersoff', '.airebo', '.rebo', '.comb3'
        }

    def run(self) -> int:
        print("\n--- 🏛️  Starting LAMMPS Official Repository Crawl ---")
        downloaded_count = 0
        
        try:
            # 1. Get list of files in the 'potentials' directory
            response = requests.get(self.api_url, headers=self.headers)
            
            if response.status_code == 200:
                files = response.json()
                print(f"   Found {len(files)} files in LAMMPS/potentials. Filtering...")

                for item in files:
                    filename = item.get('name', '')
                    download_url = item.get('download_url')
                    
                    # Check if it is a potential file based on extension
                    is_potential = any(filename.lower().endswith(ext) for ext in self.target_extensions)
                    # Special check for 'ffield.reax' variations
                    if 'ffield' in filename.lower(): 
                        is_potential = True

                    if is_potential and download_url:
                        # Save structure: data/raw/lammps__official/filename
                        save_path = f"data/raw/lammps__official/{filename}"
                        
                        if self.file_manager.download_file(download_url, save_path):
                            #print(f"      [OK] {filename}")
                            downloaded_count += 1
                        
                        time.sleep(0.1) # Be polite
            
            elif response.status_code == 403:
                 print("   ❌ Rate Limit Exceeded on LAMMPS Connector.")
            else:
                 print(f"   ❌ Error accessing LAMMPS repo: {response.status_code}")

        except Exception as e:
            print(f"   ❌ Connection Error: {e}")

        print(f"   ✅ LAMMPS Official finished. New files: {downloaded_count}")
        return downloaded_count