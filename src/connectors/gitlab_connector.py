import requests
import os
import time
import urllib.parse
from src.file_manager import FileManager

class GitLabConnector:
    def __init__(self, token: str = None, gitlab_url: str = "https://gitlab.com", base_folder: str = "data/raw"):
        self.base_url = f"{gitlab_url}/api/v4"
        self.web_url = gitlab_url
        self.base_folder = base_folder
        self.headers = {}
        
        if token:
            self.headers["PRIVATE-TOKEN"] = token.strip() # Ensure no whitespace
        
        self.file_manager = FileManager()

    def search_files(self, query: str) -> int:
        """
        Hybrid Strategy to avoid 403 block:
        1. Search PROJECTS related to the term.
        2. Within those projects, list files recursively.
        3. Filter and download relevant files.
        """
        print(f"🔄 Starting 'Project-First' strategy for: '{query}'")
        downloaded_count = 0
        
        # 1. Search PROJECTS (scope=projects is allowed globally)
        projects = self._search_projects(query)
        print(f"📦 Found {len(projects)} relevant projects. Scanning files...")

        # 2. Iterate over found projects
        for proj in projects:
            project_id = proj['id']
            project_path = proj['path_with_namespace']
            default_branch = proj.get('default_branch', 'master')
            
            print(f"   📂 Scanning project: {project_path}...")
            
            # Get project file tree
            files = self._get_project_tree(project_id)
            
            for file_node in files:
                # FILTER HERE
                # Download if filename contains query OR ends with .sw (project context)
                filename = file_node['path']
                
                # Match Logic: Contains term or is .sw extension
                # (You can add .reax here if needed)
                match_condition = (query.lower() in filename.lower()) or filename.endswith('.sw')
                
                if file_node['type'] == 'blob' and match_condition:
                    # Build Raw URL
                    safe_filename = urllib.parse.quote(filename, safe='/')
                    raw_url = f"{self.web_url}/{project_path}/-/raw/{default_branch}/{safe_filename}"
                    
                    # Define local path
                    safe_repo = project_path.replace("/", "__").replace(":", "")
                    local_filename = os.path.basename(filename)
                    save_path = f"{self.base_folder}/{safe_repo}/{local_filename}"
                    
                    if self.file_manager.download_file(raw_url, save_path):
                        downloaded_count += 1
                        print(f"      [OK] {local_filename}")
                    
                    time.sleep(0.1) # API Respect (Rate Limiting)
            
            time.sleep(1) # Pause between projects

        return downloaded_count

    def _search_projects(self, query: str):
        """
        MAXIMIZED: Search up to 500 projects (5 pages of 100) per query.
        """
        all_projects = []
        url = f"{self.base_url}/search"
        
        # Maximize items per page
        for page in range(1, 6):
            params = {
                "scope": "projects",
                "search": query,
                "per_page": 100, # API Maximum
                "page": page
            }
            try:
                print(f"      🔎 [GitLab] Searching Projects '{query}' - Page {page}...")
                resp = requests.get(url, headers=self.headers, params=params)
                
                if resp.status_code == 200:
                    data = resp.json()
                    if not data:
                        break # No more results
                    all_projects.extend(data)
                    time.sleep(1)
                else:
                    break
            except Exception as e:
                print(f"      ⚠️ Error searching projects: {e}")
                break
                
        return all_projects

    def _get_project_tree(self, project_id: int):
        """
        MAXIMIZED: Paginates the file tree to retrieve ALL files.
        """
        url = f"{self.base_url}/projects/{project_id}/repository/tree"
        all_files = []
        page = 1
        
        while True:
            params = {
                "recursive": True,
                "per_page": 100, # API Maximum
                "page": page
            }
            try:
                resp = requests.get(url, headers=self.headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if not data:
                        break
                    all_files.extend(data)
                    
                    # Check headers for next page availability
                    total_pages = int(resp.headers.get('X-Total-Pages', 1))
                    if page >= total_pages:
                        break
                    
                    page += 1
                    time.sleep(0.2) # Short pause to avoid 429 Rate Limit
                else:
                    break
            except:
                break
                
        return all_files