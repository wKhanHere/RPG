class Moves:
    def __init__(self):
        self.MoveId: str = ""
        self.MoveName: str = ""
        self.Description: str = ""
        self.MoveOnCooldown: bool = False  # Used to manage spamming.
        self.MoveCooldown: float = 0  # Cooldown in turns
        self.MoveCurrentCooldown: float = 0  # Used for tracking how many turns left.

    def __init_subclass__(Atk):
        Atk.MoveBaseDamage: float = 1  # Might wanna make this scale with levels and all.
        Atk.MoveBaseStaminaCost: float = 1
        Atk.MoveType: str = "Physical"  # Could turn types into their classes too and use type as a class for its own datatype
    
    # def __init_subclass__(Effect):
    #     Effect.Type: Effect = Stun()  # Create an effects class and all for this.

    def ViewMove(self):
        dashwidth = int((len(self.Description)+14)*0.5)
        print(f"{'-'*dashwidth}MOVE{'-'*dashwidth}")
        print(
            f"Name: {self.MoveName}\n"
            f"Type: {self.MoveType}\n"
            f"Base Damage: {self.MoveBaseDamage}\n"
            f"Stamina Cost: {self.MoveBaseStaminaCost}\n"
            f"Cooldown: {self.MoveCooldown}\n"
            f"Description: {self.Description}") 
        print(f"{'-'*((dashwidth*2)+4)}")

    @classmethod
    def CreateGenericMove(cls, MoveId, MoveName, Description, MoveBaseDamage, MoveBaseStaminaCost, MoveCooldown, MoveType):
        Move = cls()
        Move.MoveId = MoveId
        Move.MoveName = MoveName
        Move.Description = Description
        Move.MoveBaseDamage = MoveBaseDamage
        Move.MoveBaseStaminaCost = MoveBaseStaminaCost
        Move.MoveCooldown = MoveCooldown
        Move.MoveType = MoveType
        return Move
