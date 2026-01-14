import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin
from src.file_manager import FileManager

class NistConnector:
    """
    Scrapes the NIST Interatomic Potentials Repository (IPR).
    Focus: EAM, MEAM, and metal potentials.
    URL: https://www.ctcms.nist.gov/potentials/
    """
    def __init__(self):
        self.base_url = "https://www.ctcms.nist.gov/potentials/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Scientific ResearchBot/1.0; LCCMat)"
        }
        self.file_manager = FileManager()

    def run(self) -> int:
        print("\n--- 🧪 Starting NIST IPR Scraper ---")
        downloaded_count = 0
        
        try:
            # 1. Fetch Main Page
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2. Find all system pages
            # NIST structure usually lists systems in the main page or under specific categories
            links = soup.find_all('a', href=True)
            
            # Filter links that look like system entries (usually contain 'entry' or 'system')
            # and ensure we form a proper absolute URL
            system_pages = []
            for l in links:
                href = l['href']
                # NIST links are often relative. Urljoin handles this, 
                # BUT we must ensure we don't pick up mailto: or external sites
                if 'potentials/entry' in href or ('system' in href and not href.startswith('http')):
                     full_sys_url = urljoin(self.base_url, href)
                     system_pages.append(full_sys_url)
            
            # Deduplicate
            system_pages = list(set(system_pages))
            print(f"   Found {len(system_pages)} system pages to inspect.")
            
            # 3. Visit each system page
            # We limit to first 200 to prevent infinite loops if something goes wrong
            for sys_url in system_pages: 
                try:
                    # CRITICAL FIX: Ensure sys_url ends with slash to handle relative links correctly
                    if not sys_url.endswith('/'):
                        sys_url += '/'

                    sys_resp = requests.get(sys_url, headers=self.headers, timeout=10)
                    sys_soup = BeautifulSoup(sys_resp.text, 'html.parser')
                    
                    # Find file links within the system page
                    file_links = sys_soup.find_all('a', href=True)
                    
                    targets = ('.eam', '.alloy', '.meam', '.adp', '.reax', '.sw', '.tersoff')

                    for fl in file_links:
                        href = fl['href']
                        
                        # Check if it matches our target extensions
                        if any(href.lower().endswith(ext) for ext in targets):
                            
                            # Construct download URL
                            # If href is absolute (http...), use it. 
                            # If relative, join with sys_url (which now has the trailing slash fix)
                            full_download_url = urljoin(sys_url, href)
                            
                            filename = os.path.basename(href)
                            # Remove weird query parameters if any
                            if '?' in filename:
                                filename = filename.split('?')[0]

                            # Save to nist folder
                            save_path = f"data/raw/nist__ipr/{filename}"
                            
                            # Download
                            if self.file_manager.download_file(full_download_url, save_path):
                                #print(f"      [OK] NIST: {filename}")
                                downloaded_count += 1
                                
                    time.sleep(0.1) # Be polite
                except Exception as e:
                    # If one page fails, just skip to next
                    # print(f"      [Warn] Failed processing page {sys_url}: {e}")
                    continue

        except Exception as e:
            print(f"   ❌ Error scraping NIST: {e}")

        print(f"   ✅ NIST finished. New files: {downloaded_count}")
        return downloaded_count