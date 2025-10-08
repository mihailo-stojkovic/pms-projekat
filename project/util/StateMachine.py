from util.MachineStates import MachineStates as State
import threading

class StateMachine:
    """ 
    Singleton klasa koja obezbeđuje upravljanje stanjima aplikacije. 
    U trenutnoj verziji, ova klasa omogućava postavljanje i dohvatanje trenutnog stanja mašine stanja.
    **Važna napomena** je da ova klasa ne implementira nikakvu logiku validacije prelaza između stanja.
    **Ne preporučuje se** da se ova klasa koristi direktno iz drugih delova aplikacije **osim iz menadžera stanja**.
    """
    
    __instance = None
    __class_lock = threading.Lock()    
    
    
    def __init__(self):
        self.__state = State.INIT
            
    
    
    @classmethod
    def initialize(cls):
        if not cls.__instance:
            with cls.__class_lock:
                if not cls.__instance:
                    cls.__instance = StateMachine()
        return cls.__instance
    
    
    @classmethod
    def get_state(cls):
        """ Metoda koja dohvata trenutno stanje mašine stanja.
        Raises:
            Exception: Ako mašina stanja nije inicijalizovana.

        Returns:
            :class:`MachineStates`:Trenutno stanje mašine stanja.
        """
        if not cls.__instance:
            raise Exception("StateMachine not initialized. Call 'initialize' first.")
        return cls.__instance.__state
    
    @classmethod
    def set_state(cls, new_state: State):
        """ Metoda koja postavlja novo stanje mašine stanja.
        U trenutnoj implementaciji, ova metoda ne vrši nikakvu dodatnu validaciju prelaza između stanja i dovodi do
        toga da se stanje jednostavno menja na novo prosleđeno stanje. U budućim verzijama, može se dodati
        validacija kako bi se osiguralo da su prelazi između stanja dozvoljeni prema definisanoj logici aplikacije.
        Za sada, pravilo korišćenja ove klase je da se ova metoda poziva samo od strane menadžera stanja, koji je odgovoran
        za upravljanje validnim prelazima između stanja, a da svi ostili delovi aplikacije samo čitaju trenutno stanje
        putem metode :meth:`get_state`.

        Args:
            new_state (:class:`MachineStates`) : Novo stanje koje treba postaviti.

        Raises:
            Exception: Ukoliko mašina stanja nije inicijalizovana.
            ValueError: Ako prosleđeno novo stanje nije validna vrednost iz enumeracije :class:`MachineStates`.
        """
        if not cls.__instance:
            raise Exception("StateMachine not initialized. Call 'initialize' first.")
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of MachineStates Enum.")
        print(f"StateMachine: Changing state from {cls.__instance.__state} to {new_state}")
        cls.__instance.__state = new_state