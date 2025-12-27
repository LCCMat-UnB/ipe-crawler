import os
import time
from dotenv import load_dotenv

# Import all connectors
from src.connectors.github_connector import GitHubConnector
from src.connectors.lammps_connector import LammpsOfficialConnector
from src.connectors.nist_connector import NistConnector

# --- CONFIGURATION ---
# Load environment variables (GITHUB_TOKEN) from .env file
load_dotenv()

def main():
    print("--- LCCMat Potential Crawler Initiated ---")
    start_time = time.time()
    total_downloaded = 0

    # 1. Setup Token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("⚠️  WARNING: GITHUB_TOKEN not found in .env. Rate limits will be very low.")

    # ==============================================================================
    # STAGE 1: GLOBAL GITHUB SEARCH (Community & Experimental)
    # ==============================================================================
    print("\n📡 STAGE 1: Global GitHub Search (Broad Sweep)")
    
    gh_connector = GitHubConnector(token=token)
    
    # Extensive list of queries to catch all types
    search_queries = [
        # Reactive
        "filename:ffield.reax",
        "extension:reax",
        "extension:comb3",
        
        # Metals (EAM/Alloy)
        "extension:eam",
        "extension:alloy",
        
        # Semiconductors (Si/C)
        "extension:sw",
        "extension:tersoff",
        
        # Carbon
        "extension:airebo",
        "extension:rebo"
    ]

    print(f"   Targeting {len(search_queries)} file categories...")

    for query in search_queries:
        print(f"\n   👉 Processing query: '{query}'")
        try:
            count = gh_connector.search_files(query)
            total_downloaded += count
            time.sleep(1) 
        except Exception as e:
            print(f"   ❌ Error processing query '{query}': {e}")

    # ==============================================================================
    # STAGE 2: LAMMPS OFFICIAL REPOSITORY (Gold Standard)
    # ==============================================================================
    print("\n" + "-"*40)
    print("📡 STAGE 2: LAMMPS Official Repository (Standard Potentials)")
    
    try:
        lammps_connector = LammpsOfficialConnector(token=token)
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
    # FINAL SUMMARY
    # ==============================================================================
    elapsed_time = time.time() - start_time
    print("\n" + "="*40)
    print(f"Crawler Finished in {elapsed_time:.2f} seconds.")
    print(f"Total New Files Downloaded: {total_downloaded}")
    print("="*40)
    print("Next Step: Run 'python clean_data.py' to index these new files.")

if __name__ == "__main__":
    main()