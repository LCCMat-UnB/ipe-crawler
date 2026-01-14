from src.parsers.reax_parser import ReaxFFParser
from src.parsers.eam_parser import EAMParser
from src.parsers.sw_parser import SWParser
from src.parsers.tersoff_parser import TersoffParser
from src.parsers.airebo_parser import AireboParser
from src.parsers.comb3_parser import Comb3Parser

class ParserFactory:
    @staticmethod
    def get_parser(filename: str):
        filename_lower = filename.lower()

        # COMB3
        if Comb3Parser.match_type(filename_lower):
            return Comb3Parser

        # ReaxFF
        if ReaxFFParser.match_type(filename_lower):
            return ReaxFFParser
            
        # EAM / Alloy
        if EAMParser.match_type(filename_lower):
            return EAMParser
            
        # AIREBO / REBO
        if AireboParser.match_type(filename_lower):
            return AireboParser
            
        # Stillinger-Weber
        if SWParser.match_type(filename_lower):
            return SWParser
            
        # Tersoff
        if TersoffParser.match_type(filename_lower):
            return TersoffParser
            
        return None