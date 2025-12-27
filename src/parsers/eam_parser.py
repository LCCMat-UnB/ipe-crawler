import re
from typing import Dict, Any

class EAMParser:
    @staticmethod
    def match_type(filename: str) -> bool:
        valid_exts = {'.eam', '.alloy', '.fs', '.meam'}
        return any(filename.lower().endswith(ext) for ext in valid_exts)

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        result = {"valid": False, "atoms": [], "type": "EAM/Alloy", "error": None}
        
        if not content or len(content) < 50:
            result["error"] = "File too small or empty"
            return result

        possible_elements = set()
        common_words_blacklist = {"at", "in", "as", "is", "or", "by", "no", "he", "it", "to", "on"}
        
        lines = content.splitlines()[:20]
        for line in lines:
            clean_line = re.sub(r'[#!].*', '', line).strip()
            words = clean_line.split()
            for word in words:
                if word.isalpha() and len(word) <= 2 and word[0].isupper():
                    if word.lower() not in common_words_blacklist:
                        possible_elements.add(word)

        if possible_elements:
            result["atoms"] = sorted(list(possible_elements))
            result["valid"] = True
        else:
            result["atoms"] = ["Metals?"]
            result["valid"] = True
            result["error"] = "Elements not explicitly detected in header"

        return result