import inspect
from typing import Union
import copy
import ItemsCore.Items as I

class ItemsRegistry:
    def __init__(self):
        self.ItemsList: dict[str, I.Item] = {}

    def RegisterItem(self, Item: I.Item):
        if Item.ItemId in self.ItemsList:
            print(f"Item with ID {Item.ItemId} is already registered.")
        else:
            self.ItemsList[Item.ItemId] = Item

    def GetItem(self, ItemId: str) -> I.Item | None:
        return self.ItemsList.get(ItemId, "item:placeholder")

def RegisterItems(RegistryObj: ItemsRegistry, ItemOrParams: Union[I.Item, dict]):
    """
    Register either using an Item instance or a dict of kwargs for CreateGenericItem.
    Supported parent keys: "Name", "Type", "StacksTo", "Rarity", "SellCost"
    Subclass-specific keys (example for Weapon): "Durability", "WeaponDamage", "DamageType", "WeaponType"
    """
    if isinstance(ItemOrParams, I.Item):
        RegistryObj.RegisterItem(ItemOrParams)
    elif isinstance(ItemOrParams, dict):
        item = I.Item.CreateGenericItem(**ItemOrParams)
        RegistryObj.RegisterItem(item)
    else:
        raise ValueError("Invalid syntax for item registration. Provide Item or dict.")

def ValidateItemRegistryKeys(RegistryKeys: list[str], Strict: bool = False) -> bool:
    """
    Compare provided RegistryKeys list to the parameter order of Item.CreateGenericItem.
    If mismatched, print a helpful warning (or raise if Strict=True). Returns True if match.
    """
    sig = inspect.signature(I.Item.CreateGenericItem)
    expected = [p.name for p in sig.parameters.values() if p.name != "cls"]
    if expected != RegistryKeys:
        msg = (
            "Warning: ItemRegistryKeys does not match Item.CreateGenericItem parameter order.\n"
            f"Expected (from CreateGenericItem): {expected}\n\n"
            f"Current (ItemRegistryKeys): {RegistryKeys}\n"
        )
        if Strict:
            raise ValueError(msg)
        else:
            print(msg)
            return False
    return True

def BuildItemRegistryKeysFromInit() -> list[str]:
    """
    Build keys from a default Item instance (__init__ order), but keep only
    those that are valid kwargs for CreateGenericItem (so **dict calls won’t fail).
    """
    probe = I.Item()
    init_order_keys = list(probe.__dict__.keys())
    sig = inspect.signature(I.Item.CreateGenericItem)
    allowed = {p.name for p in sig.parameters.values() if p.name != "cls"}
    return [k for k in init_order_keys if k in allowed]

#region Registry
ItemsRegistryObj = ItemsRegistry()
# Item registry keys mirror the CreateGenericItem parameter order
ItemRegistryKeys: list = BuildItemRegistryKeysFromInit()
# Validate registry key ordering against CreateGenericItem Signature (raises ValueError when mismatch)
ValidateItemRegistryKeys(ItemRegistryKeys, Strict=True)

# Example registrations
# Register a Weapon subclass instance
RegisterItems(ItemsRegistryObj, Weapon.Weapon())

# Register a generic placeholder item via dict
RegisterItems(ItemsRegistryObj, {
    "ItemId": "item:placeholder",
    "Name": "Placeholder Item",
    "Type": "Misc",
    "StacksTo": 64,
    "Rarity": "Common",
    "SellCost": 1
})

# Register a weapon via dict (includes parent keys + subclass keys)
RegisterItems(ItemsRegistryObj, {
    "ItemId": "item:iron_sword",
    "Name": "Iron Sword",
    "Type": "Weapon",
    "StacksTo": 1,
    "Rarity": "Uncommon",
    "SellCost": 25,
    # Weapon-specific
    "Durability": 250,
    "WeaponDamage": 7.0,
    "DamageType": "Physical",
    "WeaponType": "Sword",
})