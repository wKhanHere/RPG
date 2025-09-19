import inspect
from typing import Union
import copy
import pandas as P

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
        print("---------------MOVE---------------")
        print(f"Name: {self.MoveName}\nType: {self.MoveType}\nBase Damage: {self.MoveBaseDamage}\nStamina Cost: {self.MoveBaseStaminaCost}\nCooldown: {self.MoveCooldown}\nDescription: {self.Description}") 
        print("----------------------------------")

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

class MovesRegistry:
    def __init__(self):
        self.MovesList: dict[str, Moves] = {}

    def RegisterCustomMove(self, Move: Moves):
        if Move.MoveId in self.MovesList:
            print(f"Move with ID {Move.MoveId} is already registered.")
        else:
            self.MovesList[Move.MoveId] = Move

    def GetMove(self, MoveId: str) -> Moves: #Actually returns a copy of the move so that the original in registry isn't affected.
        return copy.deepcopy(self.MovesList.get(MoveId, "physical:placeholder"))  # Return placeholder if not found.

class MoveSet:
    def __init__(self, slots: dict | None = None): #!Needs to Deal with Empty Slots
        '''Initializes a MoveSet with 4 move slots (M1 to M4). If no slots provided, defaults to placeholders.'''
        self.MoveSetObj: dict = slots.copy() if slots else {"M1": MovesRegistryObj.GetMove("physical:placeholder"), "M2": MovesRegistryObj.GetMove("physical:placeholder"), "M3": MovesRegistryObj.GetMove("physical:placeholder"), "M4": MovesRegistryObj.GetMove("physical:placeholder")}

    def GetMove(self, slot: str | None = None) -> Moves:
        '''Gets a move from the specified slot, or M1 by default'''
        if slot:
            return self.MoveSetObj.get(slot)
        return self.MoveSetObj.get("M1")  # Default to M1 if no slot specified.

    def SetMove(self, slot: str, move: Moves):
        '''Sets a move in the specified slot'''
        if slot not in self.MoveSetObj:
            raise KeyError(f"Invalid slot: {slot}")
        self.MoveSetObj[slot] = move

    def Swap(self, slot_a: str, slot_b: str):
        '''Swaps two moves in the moveset'''
        self.MoveSetObj[slot_a], self.MoveSetObj[slot_b] = self.MoveSetObj[slot_b], self.MoveSetObj[slot_a]

    def AsList(self) -> list: #converts moveset to a list of move objects, damn
        return [self.MoveSetObj[k] for k in sorted(self.MoveSetObj.keys())]

    def AsSeries(self):  # optional pandas view for display only
        return P.Series(self.MoveSetObj)

class Punch(Moves):
    def __init__(self):
        super().__init__()
        super().__init_subclass__()
        self.MoveId = "physical:punch"
        self.MoveName = "Punch"
        self.Description = "Punch the enemy for some solid damage!"
        self.MoveBaseDamage = 10
        self.MoveBaseStaminaCost = 1
        self.MoveCooldown = 0  # Spammable in same round.
        self.MoveType = "Physical"

class Placeholder(Moves):  # Might wanna rebrand this to something like Struggle in Pkmn.
    def __init__(self):
        super().__init__()
        super().__init_subclass__()
        self.MoveId = "physical:placeholder"
        self.MoveName = "Placeholder"
        self.Description = "Congrats on somehow accessing this move"
        self.MoveBaseDamage = 0
        self.MoveBaseStaminaCost = 0
        self.MoveCooldown = 0
        self.MoveType = "Physical"
        # No effects or anything, just a placeholder move.

def RegisterMoves(MovesRegistryObj: MovesRegistry, MoveOrParams: Union[Moves, dict] = None):
    """
    Register either using a Moves instance or a dict of kwargs for CreateGenericMove """
    if isinstance(MoveOrParams, Moves):
        MovesRegistryObj.RegisterCustomMove(MoveOrParams)
    elif isinstance(MoveOrParams, dict):
        Move = Moves.CreateGenericMove(**MoveOrParams)
        MovesRegistryObj.RegisterCustomMove(Move)
    else:
        raise ValueError("Invalid syntax for move registration. Check your parameters's order and types.")

def ValidateMoveRegistryKeys(RegistryKeys: list[str], Strict: bool = False) -> bool:
    """
    Compare provided RegistryKeys list to the parameter order of Moves.CreateGenericMove.
    If mismatch, print a helpful warning (or raise if Strict=True). Returns True if match.
    """
    Sig = inspect.signature(Moves.CreateGenericMove)
    # exclude 'cls' if present
    expected = [p.name for p in Sig.parameters.values() if p.name != "cls"]
    if expected != RegistryKeys:
        msg = (
            "Warning: MoveRegistryKeys does not match Moves.CreateGenericMove parameter order.\n"
            f"Expected (from CreateGenericMove): {expected}\n"
            f"Current (MoveRegistryKeys): {RegistryKeys}\n"
        )
        if Strict:
            raise ValueError(msg)
        else:
            print(msg)
            return False
    return True

#region Registry
MovesRegistryObj: MovesRegistry = MovesRegistry()
# Move registry keys mirror the CreateGenericMove parameter order
MoveRegistryKeys: list = [
    "MoveId",
    "MoveName",
    "Description",
    "MoveBaseDamage",
    "MoveBaseStaminaCost",
    "MoveCooldown",
    "MoveType",
]

# Validate move registry key ordering against CreateGenericMove signature (prints warning or raises)
ValidateMoveRegistryKeys(MoveRegistryKeys, Strict=True)

RegisterMoves(MovesRegistryObj, Punch())
RegisterMoves(MovesRegistryObj, Placeholder())
RegisterMoves(MovesRegistryObj, {
    "MoveId": "void:zap",
    "MoveName": "Zap",
    "Description": "A quick jolt of electricity.",
    "MoveBaseDamage": 7,
    "MoveBaseStaminaCost": 2,
    "MoveCooldown": 1,
    "MoveType": "Void"
})
RegisterMoves(MovesRegistryObj, dict(zip(MoveRegistryKeys, ["physical:slap","Slap","A quick slap with a large trout.",5,1,0,"Physical"]))) #Just for testing
#Essentially three methods of registry: Via Object Class, Via Dict, Via List
#endregion
