import inspect,copy
from typing import Union
import MovesCore.CustomMoves.RainingStars as RainingStars
import MovesCore.Moves as M


class MovesRegistry:
    def __init__(self):
        self.MovesList: dict[str, M.Moves] = {} #WHY IS THIS CALLED A LIST

    def RegisterCustomMove(self, Move: M.Moves):
        if Move.MoveId in self.MovesList:
            print(f"Move with ID {Move.MoveId} is already registered.")
        else:
            self.MovesList[Move.MoveId] = Move

    def GetMove(self, MoveId: str) -> M.Moves: #Actually returns a copy of the move so that the original in registry isn't affected.
        return copy.deepcopy(self.MovesList.get(MoveId, "physical:placeholder"))  # Return placeholder if not found.


#Essentially two methods of registry: Via Object Class, Via Dict
def RegisterMoves(MovesRegistryObj: MovesRegistry, MoveOrParams: Union[M.Moves, dict] = None):
    """
    Register either using a Moves instance or a dict of kwargs for CreateGenericMove """
    if isinstance(MoveOrParams, M.Moves):
        MovesRegistryObj.RegisterCustomMove(MoveOrParams)
    elif isinstance(MoveOrParams, dict):
        Move = M.Moves.CreateGenericMove(**MoveOrParams)
        MovesRegistryObj.RegisterCustomMove(Move)
    else:
        raise ValueError("Invalid syntax for move registration. Check your parameters's order and types.")

def ValidateMoveRegistryKeys(RegistryKeys: list[str], Strict: bool = False) -> bool:
    """
    Compare provided RegistryKeys list to the parameter order of Moves.CreateGenericMove.
    If mismatch, print a helpful warning (or raise if Strict=True). Returns True if match.
    """
    Sig = inspect.signature(M.Moves.CreateGenericMove)
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

# Validate move registry key ordering against CreateGenericMove signature (prints warning or raises ValueError if mismatch)
ValidateMoveRegistryKeys(MoveRegistryKeys, Strict=True)

RegisterMoves(MovesRegistryObj, { #Placeholder
    "MoveId": "physical:placeholder",
    "MoveName": "Placeholder",
    "Description": "Congrats on somehow accessing this move",
    "MoveBaseDamage": 0,
    "MoveBaseStaminaCost": 0,
    "MoveCooldown": 0,
    "MoveType": "Physical"
})
RegisterMoves(MovesRegistryObj, { #Punch
    "MoveId": "physical:punch",
    "MoveName": "Punch",
    "Description": "Punch the enemy for some solid damage!",
    "MoveBaseDamage": 10,
    "MoveBaseStaminaCost": 1,
    "MoveCooldown": 0,
    "MoveType": "Physical"
})
RegisterMoves(MovesRegistryObj, { #Zap
    "MoveId": "void:zap",
    "MoveName": "Zap",
    "Description": "A quick jolt of electricity.",
    "MoveBaseDamage": 7,
    "MoveBaseStaminaCost": 2,
    "MoveCooldown": 0,
    "MoveType": "Void"
})
RegisterMoves(MovesRegistryObj, { #Slap
    "MoveId": "physical:slap",
    "MoveName": "Slap",
    "Description": "A quick slap with a large trout.",
    "MoveBaseDamage": 5,
    "MoveBaseStaminaCost": 1,
    "MoveCooldown": 0,
    "MoveType": "Physical"
})
RegisterMoves(MovesRegistryObj, { #Brilliant Lance
    "MoveId": "light:brilliant_lance",
    "MoveName": "Brilliant Lance",
    "Description": "A brilliant lance of light pierces the enemy.",
    "MoveBaseDamage": 12,
    "MoveBaseStaminaCost": 3,
    "MoveCooldown": 2,
    "MoveType": "Light"
})

RegisterMoves(MovesRegistryObj, RainingStars.RainingStars())
#endregion 
