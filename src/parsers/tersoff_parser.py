from typing import Dict, Any, Set

class TersoffParser:
    @staticmethod
    def match_type(filename: str) -> bool:
        return filename.lower().endswith('.tersoff')

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        result = {"valid": False, "atoms": [], "type": "Tersoff", "error": None}
        atoms_found: Set[str] = set()
        
        lines = content.splitlines()
        for line in lines:
            parts = line.strip().split()
            if not parts or parts[0].startswith('#'):
                continue
            
            candidates = parts[:3]
            for cand in candidates:
                if cand.isalpha() and len(cand) <= 2 and cand[0].isupper():
                    atoms_found.add(cand)

        if atoms_found:
            result["valid"] = True
            result["atoms"] = sorted(list(atoms_found))
        elif len(content) > 50:
            result["valid"] = True
            result["atoms"] = ["C/Si/Ge?"]
        else:
            result["error"] = "Empty Tersoff file"

        return result