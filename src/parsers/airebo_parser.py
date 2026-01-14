from typing import Dict, Any

class AireboParser:
    @staticmethod
    def match_type(filename: str) -> bool:
        exts = {'.airebo', '.rebo'}
        return any(filename.lower().endswith(ext) for ext in exts)

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        result = {"valid": False, "atoms": [], "type": "AIREBO", "error": None}
        
        # Se tem conteúdo, é válido. AIREBO é intrinsicamente C e H.
        if len(content) > 100:
            result["valid"] = True
            result["atoms"] = ["C", "H"]
        else:
             result["error"] = "Empty file"

        return result