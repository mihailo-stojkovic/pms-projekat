class InstructionParser:
    """
        Klasa koja je odgovorna za parsiranje instrukcija iz stringa koji se dobija sa serijskog porta. 
        Instrukcije su u formatu "COMCODE ARG1 ARG2 ...", gde je COMCODE kod komande, a ARG1, ARG2, ... su 
        argumenti te komande. Ova klasa omogućava izdvajanje koda komande i njenih argumenata iz datog stringa,
        validaciju formata kao i adekvatno pakovanje primljenih podataka u odgovarajuće strukture. Valdine vrednosti
        za COMCODE su definisane u klasi :class:`ComCode.RecComCode`.
        
        
        DODATAK - ComCode je sada Deprecated feature - nije bilo potrebe za tim u trenutku kad smo izolovali u kompletu
        arduino deo od python dela :'(
    """

    @staticmethod
    def parse_instruction(instruction: str) -> dict:
        # 3 or 4 args, the first three are ints, the fourth is optional and is int 0 or 1
        # there is no more command code at the beggining
        parts = instruction.strip().split()
        if len(parts) < 4 or len(parts) > 5:
            raise ValueError(f"Invalid instruction format: {instruction}")
        return_dict = {
            'ax' : int(parts[0]),
            'ay' : int(parts[1]),
            'az' : int(parts[2]),
            'touched' : int(parts[3])
        }
        return return_dict
        