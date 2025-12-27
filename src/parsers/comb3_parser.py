import re
from typing import Dict, Any

class Comb3Parser:
    @staticmethod
    def match_type(filename: str) -> bool:
        # Aceita .comb, .comb3 e arquivos library específicos do COMB
        return any(filename.lower().endswith(ext) for ext in ['.comb', '.comb3']) or 'lib.comb' in filename.lower()

    @staticmethod
    def parse(content: str) -> Dict[str, Any]:
        result = {"valid": False, "atoms": [], "type": "COMB3", "error": None}
        
        # Estratégia Robusta: COMB3 geralmente lista elementos no topo ou em linhas de entrada
        # Vamos procurar por tokens que parecem elementos químicos
        possible_elements = set()
        lines = content.splitlines()
        
        # Lista negra de palavras comuns que parecem elementos mas não são
        blacklist = {"at", "in", "as", "is", "or", "by", "no", "he", "it", "to", "on", "if", "go", "do"}

        for line in lines[:50]: # Olha as primeiras 50 linhas (o cabeçalho)
            # Remove comentários (#)
            clean_line = line.split('#')[0].strip()
            if not clean_line:
                continue
            
            parts = clean_line.split()
            for part in parts:
                # Se for 1 ou 2 letras, primeira maiúscula (Ex: Si, Cu, O)
                if part.isalpha() and len(part) <= 2 and part[0].isupper():
                    if part.lower() not in blacklist:
                        possible_elements.add(part)

        if possible_elements:
            result["atoms"] = sorted(list(possible_elements))
            result["valid"] = True
        elif len(content) > 100:
            # Fallback: Se o arquivo é grande e tem a extensão certa, aceita como genérico
            result["valid"] = True
            result["atoms"] = ["Generic"]
            result["error"] = "Elementos não detectados explicitamente"
        else:
            result["error"] = "Arquivo vazio ou muito pequeno"

        return result