import inspect
from typing import Union
import copy
import EntityCore.LivingEntities as L
import EntityCore.CustomEntities.Player as Player

class EntitiesRegistry():
    def __init__(self):
        self.EntitiesList: dict[str, L.LivingEntity] = {}

    def RegisterEntity(self, Entity: L.LivingEntity):
        if Entity.EntityId in self.EntitiesList:
            print(f"Entity with ID {Entity.EntityId} is already registered.")
        else:
            self.EntitiesList[Entity.EntityId] = Entity

    def GetEntity(self, EntityId: str) -> L.LivingEntity | None:
        return self.EntitiesList.get(EntityId, "entity:placeholder")  # Return placeholder if not found.

def RegisterEntities(RegistryObj: EntitiesRegistry, EntityOrParams: Union[L.LivingEntity, dict]): 
    """
    Register either using a LivingEntity instance or a dict of kwargs for CreateGenericEntity.\n
    The dict can contain any of the following keys:\n
        "EquippedGear":dict 
        #default: { "Helmet": None, "Chestplate": None, "Leggings": None, "Boots": None, "Gloves": None, "MainHandWeapon": None, "OffHandWeapon": None, "Artifacts":[None]}\n
        "EntityId": str,            # default "entity:placeholder"\n
        "EntityName": str,          # default "Placeholder Entity"\n
        "MaxHp": float,             # default 20.0\n
        "MaxStamina": float,        # default 3.0\n
        "MeleeAtk": float,          # default 1.0\n
        "RangedAtk": float,         # default 1.0\n
        "CriticalChance": float,    # default 0.05\n
        "CriticalDamage": float,    # default 1.5\n
        "Evasion": float,           # default 0.05\n
        "Speed": float,             # default 1.0\n
        "PhysicalPower": float,     # default 1.0\n
        "EarthPower": float,        # default 0.0\n
        "WaterPower": float,        # default 0.0\n
        "FirePower": float,         # default 0.0\n
        "WindPower": float,         # default 0.0\n
        "LightningPower": float,    # default 0.0\n
        "VoidPower": float,         # default 0.0\n
        "LightPower": float,        # default 0.0\n
        "StellarPower": float,      # default 0.0\n
        "PhysicalRes": float,       # default 1.0\n
        "EarthRes": float,          # default 0.0\n
        "WaterRes": float,          # default 0.0\n
        "FireRes": float,           # default 0.0\n
        "WindRes": float,           # default 0.0\n
        "LightningRes": float,      # default 0.0\n
        "VoidRes": float,           # default 0.0\n
        "LightRes": float,          # default 0.0\n
        "StellarRes": float         # default 0.0\n
    \n
    Any omitted values will use the defaults from CreateGenericEntity.\n
    """
    if isinstance(EntityOrParams, L.LivingEntity):
        RegistryObj.RegisterEntity(EntityOrParams)
    elif isinstance(EntityOrParams, dict):
        Entity = L.LivingEntity.CreateGenericEntity(**EntityOrParams)
        RegistryObj.RegisterEntity(Entity)
    else:
        raise ValueError("Invalid syntax for entity registration. Provide LivingEntity or dict.")

def ValidateEntityRegistryKeys(RegistryKeys: list[str], Strict: bool = False) -> bool:
    """
    Compare provided RegistryKeys list to the parameter order of LivingEntity.CreateGenericEntity.
    If mismatch, print a helpful warning (or raise if Strict=True). Returns True if match.
    """
    Sig = inspect.signature(L.LivingEntity.CreateGenericEntity)
    # exclude 'cls' if present
    expected = [p.name for p in Sig.parameters.values() if p.name != "cls"]
    if expected != RegistryKeys:
        msg = (
            "Warning: EntityRegistryKeys does not match LivingEntity.CreateGenericEntity parameter order.\n"
            f"Expected (from CreateGenericEntity): {expected}\n\n"
            f"Current (EntityRegistryKeys): {RegistryKeys}\n"
        )
        if Strict:
            raise ValueError(msg)
        else:
            print(msg)
            return False
    return True

def BuildEntityRegistryKeysFromInit() -> list[str]:
    """
    Build keys from a default LivingEntity instance (__init__ order), but keep only\n
    those that are valid kwargs for CreateGenericEntity (so **dict calls won’t fail).\n
    This auto-updates keys if you reorder attributes in init or change CreateGenericEntity’s accepted parameters.\n
    If you later add more params to CreateGenericEntity, they’ll be picked up automatically as long as they’re set in init too.
    """
    probe = L.LivingEntity()
    init_order_keys = list(probe.__dict__.keys())
    sig = inspect.signature(L.LivingEntity.CreateGenericEntity)
    allowed = {p.name for p in sig.parameters.values() if p.name != "cls"}
    return [k for k in init_order_keys if k in allowed]
 
#region Registry    
EntitiesRegistryObj = EntitiesRegistry()
# Entity registry keys mirror the CreateGenericEntity parameter order
EntityRegistryKeys: list = BuildEntityRegistryKeysFromInit()
# Validate registry key ordering against CreateGenericEntity Signature (raises ValueError when mismatch)
ValidateEntityRegistryKeys(EntityRegistryKeys, Strict=True)

RegisterEntities(EntitiesRegistryObj, Player.Player())
RegisterEntities(EntitiesRegistryObj, { #Placeholder
    "EntityId": "entity:placeholder",
    "EntityName": "Placeholder Entity",
    "MaxHp": 20.0,
    "MaxStamina": 3.0,
    "MeleeAtk": 1.0,
    "RangedAtk": 1.0,
    "PhysicalPower": 1.0,
    "EarthPower": 0.0,
    "WaterPower": 0.0,
    "FirePower": 0.0,
    "WindPower": 0.0,
    "VoidPower": 0.0,
    "LightPower": 0.0,
})
RegisterEntities(EntitiesRegistryObj, { #Slime
    "EntityId": "entity:slime",
    "EntityName": "White Slime", #White -> Wind
    "MaxHp": 30.0,
    "MaxStamina": 4.0,
    "MeleeAtk": 1.0,
    "WindPower": 1.0,
    "RangedAtk": 2
})
#Essentially three methods of registry: Via Object Class, Via Dict, Via List
#endregion

