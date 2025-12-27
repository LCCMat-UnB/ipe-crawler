from typing import Dict, Any, Set
import re

class SWParser:
    @staticmethod
    def match_type(filename: str) -> bool:
        return filename.lower().endswith('.sw')

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        result = {"valid": False, "atoms": [], "type": "Stillinger-Weber", "error": None}
        atoms_found: Set[str] = set()
        
        filename_hint = re.findall(r'([A-Z][a-z]?)', content[:0])
        
        lines = content.splitlines()
        for line in lines:
            if line.strip().startswith(('!', '#')):
                continue
                
            parts = line.strip().split()
            for part in parts:
                if part.isalpha() and len(part) <= 2 and part[0].isupper():
                    if part not in ["To", "No", "Is"]:
                        atoms_found.add(part)

        if atoms_found:
            result["valid"] = True
            result["atoms"] = sorted(list(atoms_found))
        elif len(content) > 100:
             result["valid"] = True
             result["atoms"] = ["Si?"]
        else:
            result["error"] = "Empty or invalid SW file"

        return result