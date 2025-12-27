import re

def extract_metadata(content: str) -> dict:
    metadata = {
        "citation": "Unknown",
        "description": "",
        "year": None
    }
    
    header_lines = content.splitlines()[:50]
    
    citation_patterns = [
        r"(?i)(?:citation|ref|reference|published|article)\s*[:\-]?\s*(.*)",
        r"(?i)(?:doi)\s*[:\-]?\s*(10\..*)",
    ]
    
    description_lines = []

    for line in header_lines:
        line = line.strip()
        clean_line = re.sub(r"^[\!#%]\s*", "", line).strip()
        
        if not clean_line:
            continue

        found_citation = False
        for pattern in citation_patterns:
            match = re.search(pattern, clean_line)
            if match:
                if metadata["citation"] != "Unknown":
                    metadata["citation"] += " | " + match.group(1)
                else:
                    metadata["citation"] = match.group(1)
                found_citation = True
                break
        
        if not metadata["year"]:
            year_match = re.search(r"\b(19|20)\d{2}\b", clean_line)
            if year_match:
                metadata["year"] = int(year_match.group(1))

        if not found_citation and len(clean_line.split()) > 4 and clean_line[0].isalpha():
             description_lines.append(clean_line)

    if description_lines:
        metadata["description"] = ". ".join(description_lines[:2])
        
    return metadata