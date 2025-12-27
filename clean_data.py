import os
import json
import hashlib
from src.parsers.factory import ParserFactory
from src.utils import extract_metadata  # Certifique-se de ter criado o src/utils.py

# --- CONFIGURATION ---
RAW_DATA_DIR = "data/raw"
OUTPUT_FILE = "data/master_index.json"

def get_file_hash(content: str) -> str:
    """Generates a unique MD5 hash for the file content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def extract_repo_info(filepath: str) -> str:
    """
    Extracts repository name from folder structure.
    Expected: data/raw/owner__repo/filename
    """
    try:
        parts = filepath.replace("\\", "/").split("/")
        if len(parts) >= 3:
            folder_name = parts[-2]
            return folder_name.replace("__", "/")
    except:
        pass
    return "Unknown/Local"

def clean_database():
    print(f"Starting cleaning process in {RAW_DATA_DIR}...")
    
    if not os.path.exists(RAW_DATA_DIR):
        print(f"❌ Directory {RAW_DATA_DIR} not found.")
        return

    master_index = []
    seen_hashes = set()
    
    stats = {
        "total_scanned": 0,
        "valid": 0,
        "duplicates": 0,
        "errors": 0,
        "skipped_unknown": 0
    }

    # Walk through all directories
    for root, dirs, files in os.walk(RAW_DATA_DIR):
        for filename in files:
            file_path = os.path.join(root, filename)
            stats["total_scanned"] += 1

            # 1. IDENTIFY PARSER (Using Factory)
            parser_class = ParserFactory.get_parser(filename)
            
            if not parser_class:
                # If no parser matches the extension, skip it
                stats["skipped_unknown"] += 1
                continue

            # 2. READ CONTENT
            try:
                # Try UTF-8 first, fallback to Latin-1 (common in older scientific files)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                
                # 3. DEDUPLICATION (MD5 Hash)
                file_hash = get_file_hash(content)
                if file_hash in seen_hashes:
                    stats["duplicates"] += 1
                    continue
                
                # 4. PARSE PHYSICS (Elements, Validity)
                result = parser_class.parse(content)

                if result["valid"]:
                    seen_hashes.add(file_hash)
                    stats["valid"] += 1
                    
                    # 5. EXTRACT METADATA (Citations, Year, Description)
                    meta_info = extract_metadata(content)

                    # Determine type (Use parser return or class name fallback)
                    pot_type = result.get("type", parser_class.__name__.replace("Parser", ""))

                    entry = {
                        "id": file_hash,
                        "filename": filename,
                        "type": pot_type,  # e.g., ReaxFF, EAM, Tersoff
                        "elements": result["atoms"],
                        "system": "-".join(result["atoms"]),
                        "local_path": file_path,
                        "source_repo": extract_repo_info(file_path),
                        
                        # New Metadata Fields
                        "citation": meta_info["citation"],
                        "description": meta_info["description"],
                        "year": meta_info["year"]
                    }
                    master_index.append(entry)
                else:
                    stats["errors"] += 1
                    print(f"Invalid {pot_type} file: {filename} - {result.get('error')}")

            except Exception as e:
                print(f"Critical error processing {filename}: {e}")
                stats["errors"] += 1

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(master_index, f, indent=2)

    print("\n--- Summary ---")
    print(f"Total Files Scanned: {stats['total_scanned']}")
    print(f"Valid Potentials:    {stats['valid']}")
    print(f"Duplicates Ignored:  {stats['duplicates']}")
    print(f"Unknown Extensions:  {stats['skipped_unknown']}")
    print(f"Parsing Errors:      {stats['errors']}")
    print(f"Database saved to:   {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_database()