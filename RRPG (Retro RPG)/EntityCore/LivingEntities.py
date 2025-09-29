import copy, uuid
import pandas as P

class LivingEntity():
    def __init__(self):
        #Gear (Inventory)
        self.EquippedGear:dict = { 
            "Helmet": None,"Chestplate": None,"Leggings": None,"Boots": None,"Gloves": None,
            "MainHandWeapon": None,"OffHandWeapon": None,
            "Artifacts":[None],
            } #All slots none for now, will be refined later.
              #This should be coded in such a way that, if an entity class is defined with an EquippedGear dict containing more than just this, it also counts towards its stats.
        #IDs and Names.
        self.EntityId:str = "entity:placeholder" #Used for registry and all
        self.EntityName:str = "Placeholder Entity" #Used for displaying name and all
        self.EntityUUID:uuid.UUID = uuid.uuid4() #Unique for each entity, used for saving and all.
        #Stats
        self.MaxHp:float = 20 #MaxHP: Determine by Player Perm Upgrades, Player Gear, Player Potions, and Base 20
        self.Hp:float = copy.copy(self.MaxHp) #Tracked by health function.
        self.MaxStamina:float = 3 #AP System like in Reverse1999
        self.Stamina:float = copy.copy(self.MaxStamina)
        self.MeleeAtk:float = 1 #Base 1, Also Affected by Stamina cost: Charged Attacks Take Extra Stamina.
        self.RangedAtk:float = 1 #Base 1, Affected also by Throwing Power -> Essentialy use multiple turns to deal more damage #Think Imbibitor Lunae (Danheng)
        #Both Atk, Affected by Gear and buffs and tree upgrades.
        #Condition for attacking is keeping having "Stamina" (Regens like in Reverse1999's AP, used like Honkai Starrail's Action Points)
        self.CriticalChance:float = 0.05 #Base 5% crit chance
        self.CriticalDamage:float = 1.5 #Base 150% Crit Damage
        self.Evasion:float = 0.05 #Base 5% Dodge Chance
        self.Speed:float = 1.0 #Base 1 Speed #Affects turn order in battles. #alike speed and action values in Honkai Starrail
        self.Effects:P.DataFrame = P.DataFrame(columns=["EffectName","Duration","EffectStrength"]) #Dataframe to store effects, their durations and strengths.
        #Might need to add functions to add effects, remove effects, tick effects (reduce duration by 1 each turn), clear effects (remove all effects)
        
        #Atk Power values for each type. Used to derive damage multipliers.
        self.PhysicalPower:float = 1 #Base 1, Typeless(i.e. Physical) attack damage power multiplier
        self.EarthPower:float = 0
        self.WaterPower:float = 0
        self.FirePower:float = 0
        self.WindPower:float = 0
        self.LightningPower:float = 0
        self.VoidPower:float = 0
        self.LightPower:float = 0
        self.StellarPower:float = 0
        #Defense Will use direct values unlike power value scaling of atks.
        self.PhysicalRes:float = 1 #Base 1, Reduces Physical Damage taken.
        self.EarthRes:float = 0
        self.WaterRes:float = 0
        self.FireRes:float = 0
        self.WindRes:float = 0
        self.LightningRes:float = 0
        self.VoidRes:float = 0
        self.LightRes:float = 0
        self.StellarRes:float = 0
        
    @classmethod #this along with the init function needs a entity gear read and thus applying those stats to the entity.
    def CreateGenericEntity(
        cls,
        EquippedGear:dict = { 
            "Helmet": None,"Chestplate": None,"Leggings": None,"Boots": None,"Gloves": None,
            "MainHandWeapon": None,"OffHandWeapon": None,
            "Artifacts":[None],
            },
        EntityId:str = "entity:placeholder", EntityName:str = "Placeholder Entity",
        MaxHp:float = 20.0, MaxStamina:float = 3.0,
        MeleeAtk:float = 1.0, RangedAtk:float = 1.0,
        CriticalChance:float = 0.05, CriticalDamage:float = 1.5,
        Evasion:float = 0.05, Speed:float = 1.0,
        PhysicalPower:float = 1.0, EarthPower:float = 0.0, WaterPower:float = 0.0, FirePower:float = 0.0,
        WindPower:float = 0.0, LightningPower:float = 0.0, VoidPower:float = 0.0, LightPower:float = 0.0, StellarPower:float = 0.0,
        PhysicalRes:float = 1.0, EarthRes:float = 0.0, WaterRes:float = 0.0, FireRes:float = 0.0,
        WindRes:float = 0.0, LightningRes:float = 0.0, VoidRes:float = 0.0, LightRes:float = 0.0, StellarRes:float = 0.0,
    ):
        Entity: LivingEntity = cls()
        # Identity
        Entity.EquippedGear = EquippedGear
        Entity.EntityId = EntityId
        Entity.EntityName = EntityName
        # Core stats
        Entity.MaxHp = MaxHp
        Entity.Hp = copy.copy(Entity.MaxHp)
        Entity.MaxStamina = MaxStamina
        Entity.Stamina = copy.copy(Entity.MaxStamina)
        Entity.MeleeAtk = MeleeAtk
        Entity.RangedAtk = RangedAtk
        Entity.CriticalChance = CriticalChance
        Entity.CriticalDamage = CriticalDamage
        Entity.Evasion = Evasion
        Entity.Speed = Speed
        # Powers
        Entity.PhysicalPower = PhysicalPower
        Entity.EarthPower = EarthPower
        Entity.WaterPower = WaterPower
        Entity.FirePower = FirePower
        Entity.WindPower = WindPower
        Entity.LightningPower = LightningPower
        Entity.VoidPower = VoidPower
        Entity.LightPower = LightPower
        Entity.StellarPower = StellarPower
        # Defenses
        Entity.PhysicalRes = PhysicalRes
        Entity.EarthRes = EarthRes
        Entity.WaterRes = WaterRes
        Entity.FireRes = FireRes
        Entity.WindRes = WindRes
        Entity.LightningRes = LightningRes
        Entity.VoidRes = VoidRes
        Entity.LightRes = LightRes
        Entity.StellarRes = StellarRes
        return Entity
    
        #For loottables, there will be no parameters here, it will be managed indivitually by each entity class, maybe even a loottable builder class.
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
        self.MeleeAtk = 1
        self.RangedAtk = 1
        self.PhysicalPower = 1
        self.EarthPower = 0
        self.WaterPower = 0
        self.FirePower = 0
        self.WindPower = 0
        self.VoidPower = 0
        self.LightPower = 0
        


