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
        return self._MoveStrength
        
    @Name.setter
    def Name(self, Name: str) -> None:
        if not isinstance(Name, str) or not Name.strip():
            raise ValueError("Name must be a non-empty string")
        self._MonName = Name
        
    @Health.setter
    def Health(self, Health: int) -> None:
        if not isinstance(Health, int) or Health < 0:
            print(f"{self.Name} is fainted!")
        self._Health = Health
    
    def useMove(self, opponent) -> bool:
        if not isinstance(opponent, U_Mon):
            raise ValueError("Opponent must be an instance of U_Mon")
        opponent._Health -= self._MoveStrength
        print(f"{self._MonName} used {self._Move_Name} on {opponent._MonName}!")
        if opponent._Health <= 0:
            print(f"{opponent._MonName} fainted!")
            opponent._Health = 0
            return False
        return True
        
    def __str__(self):
        return f"{self._MonName} (Type: {self._ElementType}, Health: {self._Health})"
    
Gek = U_Mon("Gecko", "Fire", 100, "Ember", 20)
Snor = U_Mon("Snorlax", "Normal", 200, "Yawn", 10)

print(Gek)  # Initial state
print(Snor)
w = True
while w:
    if Gek.useMove(Snor) != w: # this could be better determined by a speed stat or something
        w = False
    elif Snor.useMove(Gek) != w:
        w = False
    print(Gek)  # After moves
    print(Snor)  # After moves