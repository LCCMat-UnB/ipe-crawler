import re
from typing import Dict, Any, List

class EAMParser:
    VALID_ELEMENTS = {
        'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
        'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
        'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
        'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
        'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
        'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
        'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
        'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
        'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
    }

    IGNORE_TERMS = {'eam', 'alloy', 'meam', 'fs', 'set', 'param', 'func', 'library', 
                    'potential', 'zhou', 'mishin', 'foiles', 'adp', 'data'}

    @staticmethod
    def match_type(filename: str) -> bool:
        valid_exts = {'.eam', '.alloy', '.fs', '.meam'}
        return any(filename.lower().endswith(ext) for ext in valid_exts)

    @classmethod
    def _extract_from_filename(cls, filename: str) -> List[str]:
        found = set()
        clean_name = re.sub(r'[-_\d\.]', ' ', filename).strip()
        tokens = clean_name.split()

        for token in tokens:
            if token.lower() in cls.IGNORE_TERMS:
                continue
            
            matches = re.findall(r'[A-Z][a-z]?', token)
        
            if matches:
                reconstructed = "".join(matches)
                if reconstructed == token or reconstructed in token: 
                    valid_matches = [m for m in matches if m in cls.VALID_ELEMENTS]
                    found.update(valid_matches)
        
        return list(found)

    @classmethod
    def parse(cls, content: str, filename: str = "") -> Dict[str, Any]:
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
                    if word.lower() not in common_words_blacklist and word in cls.VALID_ELEMENTS:
                        possible_elements.add(word)

        if not possible_elements and filename:
            from_name = cls._extract_from_filename(filename)
            possible_elements.update(from_name)

        if possible_elements:
            result["atoms"] = sorted(list(possible_elements))
            result["valid"] = True
        else:
            result["atoms"] = ["Not detected"]
            result["valid"] = True
            result["error"] = "Elements not detected in header or filename"

        return result