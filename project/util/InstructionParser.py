from ComCode import RecComCode, SendComCode

class InstructionParser:
    """
        Klasa koja je odgovorna za parsiranje instrukcija iz stringa koji se dobija sa serijskog porta. 
        Instrukcije su u formatu "COMCODE ARG1 ARG2 ...", gde je COMCODE kod komande, a ARG1, ARG2, ... su 
        argumenti te komande. Ova klasa omogućava izdvajanje koda komande i njenih argumenata iz datog stringa,
        validaciju formata kao i adekvatno pakovanje primljenih podataka u odgovarajuće strukture. Valdine vrednosti
        za COMCODE su definisane u klasi :class:`ComCode.RecComCode`.
    """

    @staticmethod
    def parse_instruction(instruction: str) -> dict:
        parts = instruction.strip().split()
        if len(parts) == 0:
            raise ValueError("Empty instruction")
        
        command_code = parts[0]
        args = parts[1:]
        
        return {
            "command_code": command_code,
            "args": args
        }
        