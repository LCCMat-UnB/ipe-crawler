import hashlib
import re
from typing import List, Dict, Optional, Any

class ReaxFFParser:
    """
    Responsible for validating and extracting chemical metadata from ReaxFF files.
    """
    @staticmethod
    def match_type(filename: str) -> bool:
        valid_extensions = {'.reax', 'ffield', '.comb3'}
        return any(ext in filename.lower() for ext in valid_extensions)

    @staticmethod
    def get_content_hash(content: str) -> str:
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        lines = content.splitlines()
        result = {
            "valid": False,
            "atoms": [],
            "error": None
        }

        if not lines:
            result["error"] = "Empty file"
            return result

        try:
            is_reax = False
            atom_count = 0
            atom_line_index = -1

            for i, line in enumerate(lines[:300]):
                clean_line = line.strip().lower()
                
                if not clean_line or clean_line.startswith("!"):
                    continue

                parts = clean_line.split()
                
                if parts and parts[0].isdigit():
                    rest_of_line = " ".join(parts[1:])
                    if "atom" in rest_of_line:
                        atom_count = int(parts[0])
                        atom_line_index = i
                        is_reax = True
                        break

            if not is_reax:
                result["error"] = "Could not find a line matching pattern: [INT] ... 'atom' ..."
                return result

            atoms = []
            current_line = atom_line_index + 1
            
            while len(atoms) < atom_count and current_line < len(lines):
                line = lines[current_line].strip()
                
                if not line or line.startswith("!"):
                    current_line += 1
                    continue
                
                parts = line.split()
                if parts:
                    element = parts[0]
                    if element.isalpha() and len(element) <= 2:
                        atoms.append(element)
                    elif len(atoms) > 0:
                        pass
                
                current_line += 1

            if len(atoms) > 0: 
                result["valid"] = True
                result["atoms"] = sorted(list(set(atoms)))
            else:
                 result["error"] = f"Found atom count {atom_count} but could not extract element symbols."

        except Exception as e:
            result["valid"] = False
            result["error"] = f"Parsing exception: {str(e)}"

        return result