import inspect
import copy, uuid
from typing import Union
import Moves as M
import pandas as P

#whats left is the big wall of gear, inventory and stuff like that, not only for players but also for mobs.
#also loottables
#pain
#gpt help me

class LivingEntity():
    def __init__(self):
        #Stats
        self.MaxHp:float = 20 #MaxHP: Determine by Player Perm Upgrades, Player Gear, Player Potions, and Base 20
        self.Hp:float = copy.copy(self.MaxHp) #Tracked by health function.
        self.MaxStamina:float = 3 #AP System like in Reverse1999
        self.Stamina:float = copy.copy(self.MaxStamina)
        #Both Atk, Affected by Gear and buffs and tree upgrades.
        #Condition for attacking is keeping having "Stamina" (somewhat like AP in Reverse1999, but this will also have an exact replica of AP for multi attack turn planning (Basically Reverse1999 Gameplay))
        
        #New Stats: Add these to the constructor class method
        self.CritcalChance:float = 0.05 #Base 5% crit chance
        self.CritcalDamage:float = 1.5 #Base 150% Crit Damage
        self.DodgeChance:float = 0.05 #Base 5% Dodge Chance
        self.Armor:float = 0.0 #Base 0 Armor
        self.HealthRegen:float = 0.0 #Base 0 Health Regen per turn
        self.StaminaRegen:float = 1.0 #Base 1 Stamina Regen per turn
        self.Speed:float = 1.0 #Base 1 Speed
        
        #New Stats End
        
        #Fancy Stats: These exist, cool stuff, all default to 1 or 0
        self.ContactAtk:float = 1 #Base 1, Also Affected by Stamina cost: Charged Attacks Take Extra Stamina.
        self.RangedAtk:float = 1 #Base 1, Affected also by Throwing Power -> Essentialy use multiple turns to deal more damage, #Stuff like Quick Shot etc wil be here (Turn cost essentially)
        #Power values for each type: I am gonna make like 16types and create something similiar to Pokemon type matching since what I don't quite like about Wynn is other than Max Dpsing, you really can just ignore other types
        self.PhysicalPower:float = 1 #Base 1, Typeless(Physical) attack damage power multiplier
        self.EarthPower:float = 0
        self.WaterPower:float = 0
        self.FirePower:float = 0
        self.WindPower:float = 0
        self.VoidPower:float = 0
        self.LightPower:float = 0 
        #Similiarly, add ContactDefense, RangedDefense, Type Defenses. 
        
        #You might need an inventory system for Living Entity.
        
        #IDs and Names.
        self.EntityId:str = "entity:placeholder" #Used for registry and all
        self.EntityName:str = "Placeholder Entity" #Used for displaying name and all
        self.EntityUUID:uuid.UUID = uuid.uuid4() #Unique for each entity, used for saving and all.
       
    @classmethod
    def CreateGenericEntity(cls,EntityId: str = "entity:placeholder",EntityName: str = "Placeholder Entity",MaxHp: float = 20.0,MaxStamina: float = 3.0,ContactAtk: float = 1.0,RangedAtk: float = 1.0,PhysicalPower: float = 1.0,EarthPower: float = 0.0,WaterPower: float = 0.0,FirePower: float = 0.0,WindPower: float = 0.0,VoidPower: float = 0.0,LightPower: float = 0.0): 
        Entity:LivingEntity = cls()
        Entity.EntityId = EntityId
        Entity.EntityName = EntityName
        Entity.MaxHp = MaxHp
        Entity.Hp = copy.copy(Entity.MaxHp)
        Entity.MaxStamina = MaxStamina
        Entity.Stamina = copy.copy(Entity.MaxStamina)
        Entity.ContactAtk = ContactAtk
        Entity.RangedAtk = RangedAtk
        Entity.PhysicalPower = PhysicalPower
        Entity.EarthPower = EarthPower
        Entity.WaterPower = WaterPower
        Entity.FirePower = FirePower
        Entity.WindPower = WindPower
        Entity.VoidPower = VoidPower
        Entity.LightPower = LightPower
        return Entity
    
        #May need more detailed entity creation functions like CreateMonsterEntity, CreateNPCEntity and all.
        #That may also include functions for loot tables and all.
        #Also might need to add more parameters here like resistances and all.
        #Also might need to add status effects and all.
        #May need to add functions for LivingEntity like TakeDamage, Heal, UseStamina, RecoverStamina, Die and all.

class PlaceholderEntity(LivingEntity):
    def __init__(self):
        super().__init__()
        self.EntityId = "entity:placeholder"
        self.EntityName = "Placeholder Entity"
        self.MaxHp = 20
        self.Hp = copy.copy(self.MaxHp)
        self.MaxStamina = 3
        self.Stamina = copy.copy(self.MaxStamina)
        self.ContactAtk = 1
        self.RangedAtk = 1
        self.PhysicalPower = 1
        self.EarthPower = 0
        self.WaterPower = 0
        self.FirePower = 0
        self.WindPower = 0
        self.VoidPower = 0
        self.LightPower = 0
        

class Player(LivingEntity):
    def __init__(self,Name:str="Player"):
        #region Stats
        super().__init__()
        self.MaxHp = 100
        self.Hp = copy.copy(self.MaxHp)
        self.MaxStamina = 5
        self.Stamina = copy.copy(self.MaxStamina) #I think double defination is stupid, try to find a way around.
        self.ContactAtk = 5
        self.RangedAtk = 1
        
        #PlayerSpecific Stats:
        self.ExperienceGain:float = 1.0 #Base 1 Experience Gain
        self.GoldGain:float = 1.0 #Base 1 Gold Gain,
        self.MagicFind:float = 1.0 #Base 1 Magic Find
        #endregion Stats

        #region MoveSet
        Move1:M.Moves = M.MovesRegistryObj.GetMove("physical:punch") #Default Move
        Move2:M.Moves = M.MovesRegistryObj.GetMove("physical:slap")
        Move3:M.Moves = M.MovesRegistryObj.GetMove("void:zap")
        Move4:M.Moves = M.MovesRegistryObj.GetMove("physical:placeholder")
        self.MoveSet:M.MoveSet = M.MoveSet({"M1": Move1, "M2": Move2, "M3": Move3, "M4": Move4}) #May wanna make this a list or Array (numpy one)
        #endregion MoveSet

        #region Booleans & IDs
        self.InBattle:bool = False
        self.EntityId:str = "entity:player"
        self.EntityName:str = Name
        self.PermUpgrades:dict = {} #Permanent Upgrades. Like Max Hp Upgrades,atk,etc.
        #endregion Booleans & IDs

        #region Inventory
        self.BackpackFoodAndHeals:dict = {} #Healing items and all
        self.BackpackGear:dict = {} #Gear and all
        self.BackpackMaterials:dict = {} #Mob drops and all materials
        self.Backpack:dict ={} #Composite backpack which will be accessed. Will contain Each backpack type (Like Toolbelt and pouches)
        
        self.Backpack = [
            "ItemId", "Name", "Type", "Quantity", "Rarity", "Location", "Weight", "Description"
        ]
        self.Inventory = P.DataFrame(columns=self.Backpack)

        # Example: Add some starter items
        starter_items = [
            {
                "ItemId": "food:apple",
                "Name": "Apple",
                "Type": "Food",
                "Quantity": 5,
                "Rarity": "Common",
                "Location": "Backpack",
                "Weight": 0.2,
                "Description": "Restores a small amount of HP."
            },
            {
                "ItemId": "gear:sword",
                "Name": "Iron Sword",
                "Type": "Gear",
                "Quantity": 1,
                "Rarity": "Uncommon",
                "Location": "Equipped",
                "Weight": 3.0,
                "Description": "A basic iron sword."
            }
        ]
        self.AddItems(starter_items)
        #endregion inventory
    
    def AddItems(self, items):
        """Add one or more items (dict or list of dicts) to the inventory."""
        if isinstance(items, dict):
            items = [items]
        self.Inventory = P.concat([self.Inventory, P.DataFrame(items)], ignore_index=True)

    def RemoveItem(self, item_id, quantity=1):
        """Remove a quantity of an item by ItemId."""
        idx = self.Inventory[self.Inventory["ItemId"] == item_id].index
        if not idx.empty:
            current_qty = self.Inventory.loc[idx[0], "Quantity"]
            if current_qty > quantity:
                self.Inventory.loc[idx[0], "Quantity"] -= quantity
            else:
                self.Inventory = self.Inventory.drop(idx)
            self.Inventory = self.Inventory.reset_index(drop=True)

    def ShowInventory(self, location=None):
        """Print inventory, optionally filtered by location."""
        if location:
            df = self.Inventory[self.Inventory["Location"] == location]
        else:
            df = self.Inventory
        print(df if not df.empty else "Inventory is empty.")

    def TotalWeight(self):
        """Return total carried weight."""
        return (self.Inventory["Quantity"] * self.Inventory["Weight"]).sum()       
     
    #region Move Manager
    def MoveSetManager(self): #!!I dont think this is complete
        #Add a try and catch to this to catch invalid options
        ViewBool:bool = bool(input("[1] View All Moves\n[2] View Learned Moves") - 1) #True -> 2, False -> 1        
        self.ViewMoves(ViewBool)
        #Next up, it will ask if to perform extra actions like change. Think pokemon.
    
    def ViewMoves(self,ViewBool:bool): #!!I dont think this is complete
        print("\n")
        if ViewBool == True:
            for i in list(self.MoveSet.MoveSetObj.keys()):
                Move:M.Moves = self.MoveSet.GetMove(i)
                print(f"[{i}] {Move.MoveName}")
            Move:M.Moves = self.MoveSet.GetMove(input("Choose which move to view.\n(Enter in exact format as displayed.)\n"))
            Move.ViewMove() #Add a view move function to parent Moves Class
        else:
            MovesRegistryObj:M.MovesRegistry = M.MovesRegistryObj
            a = 1
            for i in MovesRegistryObj.MovesList: #Uni move set does not have anything as of now
                Move:M.Moves = MovesRegistryObj.MovesList[i]
                print(f"[{a}] {Move.MoveName}, (MoveId: \"{i}\")")
                a += 1
            Move:M.Moves = MovesRegistryObj.MovesList[input("Choose which move to view.\n[Enter index in exact format as displayed.]")] #Add a try and catch to this to catch invalid options
            Move.ViewMove()  #Add a view move function to parent Moves Class
    #endregion
    
    #May need more functions like UseItem, EquipGear.
#Might wanna move a variant of moveset manager to Parent LivingEntity class, as the mobs will choose moves depending on the Player's kit.    
    
class EntitiesRegistry():
    def __init__(self):
        self.EntitiesList: dict[str, LivingEntity] = {}

    def RegisterEntity(self, Entity: LivingEntity):
        if Entity.EntityId in self.EntitiesList:
            print(f"Entity with ID {Entity.EntityId} is already registered.")
        else:
            self.EntitiesList[Entity.EntityId] = Entity

    def GetEntity(self, EntityId: str) -> LivingEntity | None:
        return self.EntitiesList.get(EntityId, "entity:placeholder")  # Return placeholder if not found.


def RegisterEntities(RegistryObj: EntitiesRegistry, EntityOrParams: Union[LivingEntity, dict]): 
    """
    Register either using a LivingEntity instance or a dict of kwargs for CreateGenericEntity.\n
    The dict can contain any of the following keys:\n
        "EntityId": str,          # default "entity:placeholder"\n
        "EntityName": str,        # default "Placeholder Entity"\n
        "MaxHp": float,           # default 20.0\n
        "MaxStamina": float,      # default 3.0\n
        "ContactAtk": float,      # default 1.0\n
        "RangedAtk": float,       # default 1.0\n
        "PhysicalPower": float,   # default 1.0\n
        "EarthPower": float,      # default 0.0\n
        "WaterPower": float,      # default 0.0\n
        "FirePower": float,       # default 0.0\n
        "WindPower": float,       # default 0.0\n
        "VoidPower": float,       # default 0.0\n
        "LightPower": float       # default 0.0\n
    \n
    Any omitted values will use the defaults from CreateGenericEntity.\n
    """
    if isinstance(EntityOrParams, LivingEntity):
        RegistryObj.RegisterEntity(EntityOrParams)
    elif isinstance(EntityOrParams, dict):
        Entity = LivingEntity.CreateGenericEntity(**EntityOrParams)
        RegistryObj.RegisterEntity(Entity)
    else:
        raise ValueError("Invalid syntax for entity registration. Provide LivingEntity or dict.")

def ValidateEntityRegistryKeys(RegistryKeys: list[str], Strict: bool = False) -> bool:
    """
    Compare provided RegistryKeys list to the parameter order of LivingEntity.CreateGenericEntity.
    If mismatch, print a helpful warning (or raise if Strict=True). Returns True if match.
    """
    Sig = inspect.signature(LivingEntity.CreateGenericEntity)
    # exclude 'cls' if present
    expected = [p.name for p in Sig.parameters.values() if p.name != "cls"]
    if expected != RegistryKeys:
        msg = (
            "Warning: EntityRegistryKeys does not match LivingEntity.CreateGenericEntity parameter order.\n"
            f"Expected (from CreateGenericEntity): {expected}\n"
            f"Current (EntityRegistryKeys): {RegistryKeys}\n"
        )
        if Strict:
            raise ValueError(msg)
        else:
            print(msg)
            return False
    return True
 
#region Registry    
EntitiesRegistryObj = EntitiesRegistry()
# Entity registry keys mirror the CreateGenericEntity parameter order
EntityRegistryKeys: list = [
    "EntityId",
    "EntityName",
    "MaxHp",
    "MaxStamina",
    "ContactAtk",
    "RangedAtk",
    "PhysicalPower",
    "EarthPower",
    "WaterPower",
    "FirePower",
    "WindPower",
    "VoidPower",
    "LightPower"
]
# Validate registry key ordering against CreateGenericEntity Signature (prints warning when mismatch)
ValidateEntityRegistryKeys(EntityRegistryKeys, Strict=True)

RegisterEntities(EntitiesRegistryObj, Player())
RegisterEntities(EntitiesRegistryObj, PlaceholderEntity())
RegisterEntities(EntitiesRegistryObj, {
    "EntityId": "entity:slime",
    "EntityName": "White Slime", #White -> Wind
    "MaxHp": 30.0,
    "MaxStamina": 4.0,
    "ContactAtk": 1.0,
    "WindPower": 1.0,
    "RangedAtk": 2
})
RegisterEntities(EntitiesRegistryObj, dict(zip(EntityRegistryKeys, ["entity:goblin","Goblin",40.0,4.0,2.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0]))) #Green -> Earth
#Essentially three methods of registry: Via Object Class, Via Dict, Via List
#endregion

Player1 = copy.deepcopy(EntitiesRegistryObj.GetEntity("entity:player"))
Slime = copy.deepcopy(EntitiesRegistryObj.GetEntity("entity:slime"))
Goblin = copy.deepcopy(EntitiesRegistryObj.GetEntity("entity:goblin"))
Player1.ViewMoves(True)

