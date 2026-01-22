import os
import time
from dotenv import load_dotenv

# Import all connectors
from src.connectors.github_connector import GitHubConnector
from src.connectors.gitlab_connector import GitLabConnector  # <--- NEW
from src.connectors.lammps_connector import LammpsOfficialConnector
from src.connectors.nist_connector import NistConnector

# --- CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()

def main():
    print("--- LCCMat Potential Crawler Initiated ---")
    start_time = time.time()
    total_downloaded = 0

    # 1. Setup Tokens
    github_token = os.getenv("GITHUB_TOKEN")
    gitlab_token = os.getenv("GITLAB_TOKEN") # <--- NEW

    if not github_token:
        print("⚠️  WARNING: GITHUB_TOKEN not found in .env. Rate limits will be very low.")
    if not gitlab_token:
        print("⚠️  WARNING: GITLAB_TOKEN not found in .env. GitLab search might fail or be limited.")

    # ==============================================================================
    # STAGE 1: GLOBAL GITHUB SEARCH (Community & Experimental)
    # ==============================================================================
    print("\n📡 STAGE 1: Global GitHub Search (Broad Sweep)")
    
    try:
        gh_connector = GitHubConnector(token=github_token)
        
        # Specific file syntax queries work well on GitHub
        github_queries = [
            "filename:ffield.reax", "extension:reax", "extension:comb3",
            "extension:eam", "extension:alloy",
            "extension:sw", "extension:tersoff",
            "extension:airebo", "extension:rebo"
        ]

        print(f"   Targeting {len(github_queries)} file categories...")

        for query in github_queries:
            print(f"\n   👉 Processing query: '{query}'")
            try:
                count = gh_connector.search_files(query)
                total_downloaded += count
                time.sleep(1) 
            except Exception as e:
                print(f"   ❌ Error processing query '{query}': {e}")
    except Exception as e:
        print(f"   ❌ Critical Error in GitHub Connector init: {e}")

    # ==============================================================================
    # STAGE 2: LAMMPS OFFICIAL REPOSITORY (Gold Standard)
    # ==============================================================================
    print("\n" + "-"*40)
    print("📡 STAGE 2: LAMMPS Official Repository (Standard Potentials)")
    
    try:
        lammps_connector = LammpsOfficialConnector(token=github_token)
        count_lammps = lammps_connector.run()
        total_downloaded += count_lammps
    except Exception as e:
        print(f"   ❌ Error in LAMMPS Connector: {e}")

    # ==============================================================================
    # STAGE 3: NIST INTERATOMIC POTENTIALS REPOSITORY (Metals Focus)
    # ==============================================================================
    print("\n" + "-"*40)
    print("📡 STAGE 3: NIST IPR (High-Quality Metal Potentials)")
    
    try:
        nist_connector = NistConnector()
        count_nist = nist_connector.run()
        total_downloaded += count_nist
    except Exception as e:
        print(f"   ❌ Error in NIST Connector: {e}")

    # ==============================================================================
    # STAGE 4: GLOBAL GITLAB SEARCH (Project-Based Search)
    # ==============================================================================
    print("\n" + "-"*40)
    print("📡 STAGE 4: Global GitLab Search (Project-Based Strategy)")
    
    try:
        gl_connector = GitLabConnector(token=gitlab_token)
        
        gitlab_queries = [
            "Stillinger-Weber", 
            "ReaxFF", 
            "Tersoff Potential", 
            "EAM Potential", 
            "AIREBO",
            "Interatomic Potentials"
        ]
        
        print(f"   Targeting {len(gitlab_queries)} project topics...")

        for query in gitlab_queries:
            print(f"\n   👉 Processing GitLab query: '{query}'")
            try:
                count = gl_connector.search_files(query)
                total_downloaded += count
                time.sleep(2) # Little extra sleep for GitLab
            except Exception as e:
                print(f"   ❌ Error processing query '{query}': {e}")
                
    except Exception as e:
        print(f"   ❌ Error in GitLab Connector: {e}")

    # ==============================================================================
    # FINAL SUMMARY
    # ==============================================================================
    elapsed_time = time.time() - start_time
    print("\n" + "="*40)
    print(f"Crawler Finished in {elapsed_time:.2f} seconds.")
    print(f"Total New Files Downloaded: {total_downloaded}")
    print("="*40)
    print("Next Step: Run 'python clean_data.py' to index and validate these files.")

if __name__ == "__main__":
    main()