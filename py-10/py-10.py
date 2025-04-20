

#U-Mon

class U_Mon:
    def __init__(self, name, EType, health, move_name, move_strength):
        self._MonName: str = name
        self._ElementType: str = EType
        self._Health: int = health
        self._Move_Name: str = move_name
        self._MoveStrength: int = move_strength
        pass
    
    @property
    def Name(self) -> str:
        return self._MonName
    @property
    def ElementType(self) -> str:
        return self._ElementType
    @property
    def Health(self) -> int:
        return self._Health
    @property
    def MoveName(self) -> str:
        return self._Move_Name
    @property
    def MoveStrength(self) -> int: 
        self._MoveStrength
        
    @Name.setter
    def Name(self, Name: str) -> None:
        if not isinstance(Name, str) or not Name.strip():
            raise ValueError("Name must be a non-empty string")
        self._MonName = Name
    
    def useMove(self, opponent):
        pass
    
    def __str__(self):
        pass
    
    
Gek = U_Mon("Gecko", "Fire", 100, "Ember", 20)
Snor = U_Mon("Snorlax", "Normal", 200, "Yawn", 10)


