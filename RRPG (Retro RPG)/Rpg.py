import random
import copy
import LevelCreation.GridStructure as GS
import EntityCore.LivingEntitiesRegistry as LER
import EntityCore.LivingEntities as L
#import ItemsCore.ItemsRegistry as IR
#import ItemsCore.Items as I
import MovesCore.MovesRegistry as MR
import MovesCore.Moves as M
class Battle:
    def __init__(self,MobPool:list,LootPool:list): #Add a default mobpool and lootpool.
        self.MobPool = MobPool if MobPool else []
        self.LootPool = LootPool if LootPool else []
        self.BattleGrid:GS.Grid = GS.Grid(5, 5) #Default 5x5 grid for battles.
        self.TurnOrder:list = [] #List of LivingEntity objects in turn order.
if __name__ == "__main__":
    print("RPG Module Loaded")
    Player1:L.LivingEntity = copy.deepcopy(LER.EntitiesRegistryObj.GetEntity("entity:player"))
    Slime:L.LivingEntity = copy.deepcopy(LER.EntitiesRegistryObj.GetEntity("entity:slime"))
    Player1.ViewMoves(False)
    print(Player1.EntityUUID)