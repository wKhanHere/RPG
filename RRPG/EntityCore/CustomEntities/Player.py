import EntityCore.LivingEntities as L
import MovesCore.Moves as M
import MovesCore.MovesRegistry as MR
import pandas as P
import copy

class MoveSet:
    def __init__(self, slots: dict | None = None): #!Needs to Deal with Empty Slots
        """Initializes a MoveSet with 4 move slots (M1 to M4). If no slots provided, defaults to placeholders."""
        self.MoveSetObj: dict = slots.copy() if slots else {
            "M1": MR.MovesRegistryObj.GetMove("physical:placeholder"),
            "M2": MR.MovesRegistryObj.GetMove("physical:placeholder"),
            "M3": MR.MovesRegistryObj.GetMove("physical:placeholder"),
            "M4": MR.MovesRegistryObj.GetMove("physical:placeholder")
        }

    def GetMove(self, slot: str = "M1") -> M.Moves:
        """Gets a move from the specified slot, or M1 by default"""
        if slot in ["M1", "M2", "M3", "M4"]:
            return self.MoveSetObj.get(slot)
        print("Invalid slot specified, defaulting to M1.")
        return self.MoveSetObj.get("M1")  # Default to M1 if no slot/incorrect slot specified.

    def SetMove(self, slot: str, move: M.Moves):
        """Sets a move in the specified slot"""
        if slot not in self.MoveSetObj:
            raise KeyError(f"Invalid slot: {slot}")
        self.MoveSetObj[slot] = move

    def Swap(self, slot_a: str, slot_b: str):
        """Swaps two moves in the moveset"""
        self.MoveSetObj[slot_a], self.MoveSetObj[slot_b] = self.MoveSetObj[slot_b], self.MoveSetObj[slot_a]

    def AsList(self) -> list: #converts moveset to a list of move objects, damn
        return [self.MoveSetObj[k] for k in sorted(self.MoveSetObj.keys())]

    def AsSeries(self):  # optional pandas view for display only
        return P.Series(self.MoveSetObj)


class Player(L.LivingEntity):
    def __init__(self,name:str="Player"):
        #region Stats
        super().__init__()
        self.MaxHp = 100
        self.Hp = copy.copy(self.MaxHp)
        self.MaxStamina = 5
        self.Stamina = copy.copy(self.MaxStamina) #I think double defination is stupid, try to find a way around.
        self.MeleeAtk = 5
        self.RangedAtk = 1
        
        #PlayerSpecific Stats:
        self.ExperienceGain:float = 1.0 #Base 1 Experience Gain
        self.GoldGain:float = 1.0 #Base 1 Gold Gain,
        self.MagicFind:float = 1.0 #Base 1 Magic Find
        #endregion Stats

        #region MoveSet
        Move1:M.Moves = MR.MovesRegistryObj.GetMove("physical:punch") #Default Move
        Move2:M.Moves = MR.MovesRegistryObj.GetMove("physical:slap")
        Move3:M.Moves = MR.MovesRegistryObj.GetMove("void:zap")
        Move4:M.Moves = MR.MovesRegistryObj.GetMove("physical:placeholder")
        self.MoveSet:MoveSet = MoveSet({"M1": Move1, "M2": Move2, "M3": Move3, "M4": Move4})
        #endregion MoveSet

        #region Booleans & IDs
        self.InBattle:bool = False
        self.EntityId:str = "entity:player"
        self.EntityName:str = name
        self.PermUpgrades:dict = {} #Permanent Upgrades. Like Max Hp Upgrades,atk,etc.
        #endregion Booleans & IDs

        #region Inventory
        BackpackLabels:list = [
            "ItemId", "Name", "Type", "Quantity", "Rarity", "Location", "Weight", "Description"
        ]
        self.BackpackFoodAndHeals:dict = dict(zip(BackpackLabels,[0]*len(BackpackLabels))) #Healing items and all
        self.BackpackGear:dict = dict() #Gear and all
        self.BackpackMaterials:dict = dict() #Mob drops and all materials
        self.Backpack:P.DataFrame = P.DataFrame({"Materials":self.BackpackMaterials,"Consumables":self.BackpackFoodAndHeals,"Gear":self.BackpackGear}) #Composite backpack which will be accessed. Will contain Each backpack type (Like Toolbelt and pouches)
        
        #endregion inventory
    
    def AddItems(self, items):
        """Add one or more items (dict or list of dicts) to the inventory."""
        if isinstance(items, dict):
            items = [items]
        self.Backpack = P.concat([self.Backpack, P.DataFrame(items)], ignore_index=True)

    def RemoveItem(self, item_id, quantity=1):
        """Remove a quantity of an item by ItemId."""
        idx = self.Backpack[self.Backpack["ItemId"] == item_id].index
        if not idx.empty:
            current_qty = self.Backpack.loc[idx[0], "Quantity"]
            if current_qty > quantity:
                self.Backpack.loc[idx[0], "Quantity"] -= quantity
            else:
                self.Backpack = self.Backpack.drop(idx)
            self.Backpack = self.Backpack.reset_index(drop=True)

    def ShowInventory(self, location=None): #Polish this.
        """Print inventory, optionally filtered by location."""
        if location:
            df = self.Backpack[self.Backpack["Location"] == location]
        else:
            df = self.Backpack
        print(df if not df.empty else "Inventory is empty.")
 
    #region Move Manager
    def MoveSetManager(self): #!!I dont think this is complete:: I think this is managed by Moveset class, I just need execution here.
        #Add a try and catch to this to catch invalid options
        #Make this use MoveSet class functions
        ViewBool:bool = bool(input("[1] View All Moves\n[2] View Learned Moves") - 1) #True -> 2, False -> 1        
        self.ViewMoves(ViewBool)
        #Next up, it will ask if to perform extra actions like change. Think pokemon.
    
    def ViewMoves(self,ViewBool:bool): #!!I dont think this is complete
        print("\n")
        if ViewBool == True:
            for i in list(self.MoveSet.MoveSetObj.keys()): #Fetches keys from moveset objects' dict, then prints chosen move out.
                Move:M.Moves = self.MoveSet.GetMove(i)
                print(f"[{i}] {Move.MoveName}")
            Move:M.Moves = self.MoveSet.GetMove(input("Choose which move to view.\n(Enter in exact format as displayed.)\n"))
            Move.ViewMove()
        else: #A few points for this part: Make it so that Ids are only shown in "debug mode" (make a debug mode now, yay... pain)
            #Make line 7 (respective to here, the one ahead try:) cleaner 
            a = 1
            for i in MR.MovesRegistryObj.MovesList: #Moves list is actually a dictonary btw.
                Move:M.Moves = MR.MovesRegistryObj.MovesList[i]
                print(f"[{a}] {Move.MoveName} (MoveId: \"{i}\")")
                a += 1
            try:
                Move:M.Moves = list(MR.MovesRegistryObj.MovesList.values())[int(input("Choose which move to view.\n[Enter index in exact format as displayed.]\n"))-1]
                Move.ViewMove()
            except (KeyError, ValueError):
                print("Invalid index. Please try again.") #Try making this actually try again.
                
    #endregion
    
    #May need more functions like UseItem, EquipGear.
#Might wanna move a variant of moveset manager to Parent LivingEntity class, as the mobs will choose moves depending on the Player's kit.    
