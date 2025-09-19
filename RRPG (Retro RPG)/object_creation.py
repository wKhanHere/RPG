#*<Number> -> Solved ; <Number> -> Unsolved ; $<Number> -> Important ; +<Number> -> Extra Ideas, not mentioned anywhere in code.
#*1 Overwrites parent code, find a way to overload/copy paste parent code here. -> Solved, Call super().<func>() in <func>()
#2 Really isnt a problem, just an idea to reduce work on computer by checking for Consuming logic only for consumables.
#$2.33 Add Object Deletion Function at some point, checking for "ghost item" variables on them (Currently Ghost Item Data is only updated when useItem is called, so there may be a way to keep count 0 items as souveniers but I always believed ppl who wish to do that, deserve it as a trophy.)
#*2.5 Created bool "usable_item" to be checked for before running, if False, useItem code is aborted. (Aborted in child class, so as to give the generic cd/count msg from Parent)
'''*3 Clean Solution, defined function for only one object, 
and used a "void call" (my terminology) by calling the map function over a 
list of "to be added" artifacts via names internally mapped (hardcodded, can be changed 
to map function but i think the same code would be repeated) and the target (player) and 
then those arguments are iterated one by one, giving me a complete inv with items, also 
void call var is deleted in next line'''
#$4 With the above fix also using uuids now from UUID module for each artifact, how tf am i supposed to refer to the objects via these ids? (Maybe another UUID Dictionary?)
#+5 Switch to Snake Case
#+6 Does anything other than artifacts really need UUIDs?
#7 The only reason I might need usable item tag is to list on use effects in Menus, and to sort by useable items in bags.
import random, uuid #Use uuid.uuid4() or uuid.uuid1(). The Latter uses Comp's ip and stuff, so security risk, dont.
class Item():
    '''Defines an Item object class which contains data about amount, effects and use triggers.'''
    def __init__(self):
        self.name:str = "<Name>"
        self.type:str = "Basic Item" #Essentially the placeholder as well as basic tier.
        self.usable_item:bool = False #Is set to true for Artifacts, Food, Potion, etc.
        self.count:int = 0 #Not Used/Implemented      
        self.consumable:bool = False #Only food-like items are consumable, for now. Consumable means reduce quantity on use.
        self.cd:float = 0.0 #0 is essentially Spam.
        self.CurCd:float = 0.0 #Is the current cooldown for item. #Not Used/Implemented
        self.uuid:str = "GENERICUUID" 
        self.ghost_item:bool = False #If is True, (Marked For Delete) delete it via a function later. (#2.33)
    def useItem(self):
        '''Under item class, only implements item existance and cooldown check.'''
        if self.CurCd == 0 and self.count >= 1: #Not Used/Implemented
            self.count = self.count - 1 if self.consumable == True else self.count #2 can be optimized to only check for consumables and reduce them
            if self.count == 0:
                self.ghost_item = True
                self.CurCd = -1
                return #Sets an Invalid CurCd for ghost item and aborts THIS function, still allowing THIS time child to execute. Marked For Delete
            self.CurCd = self.cd
        elif self.count <= 0:
            print("Not enough of", self.name)
            self.usable_item = False 
            '''#2.33 This implies this object shouldn't even be here. Also in upper case, when self.count == 0, it needs to be deleted.
            Using the later bool "ghost item", delete the object later. (some sort of inv cleaner function)'''
            self.ghost_item = True 
        elif not self.CurCd <= 0: #Not Used/Implemented
            print(self.name, "is under cooldown of", self.CurCd ,"seconds!") #2.5Make this abort the child useItem() as well
            self.usable_item = False
class Artifact(Item):
    def __init__(self):
        super().__init__()
        self.type = "Artifact" #Not Used/Implemented
        self.consumable = False
        self.uuid = "aGENERICUUID" # a -> Artifact
        self.usable_item = True #(7)Is the Condition which must/can be used as criteria to be satisfied for useItem() function to occur.
        
    def useItem(self):
        super().__init__()
class DieArtifact(Artifact):
    def __init__(self): #*1 
        super().__init__()
        self.name = "Die of The Devil"
        self.cd = 3 #Not Used/Implemented
        self.count = 1 #Not Used/Implemented
    def useItem(self,player,arti): #*1
        super().useItem()
        if self.usable_item == False:
            return
        self.n:int = random.randint(1,6)
        self.g:int = int(input(("Hahaha, What's your guess, pawny one! ", player.inv_arti[arti].name,self.n)))
        if self.g == self.n:
            print("Luck favors the weak!")
            #Do something
        else:
            print("Hahaha! Insufferable.")
class person(): #I mean export this to rpg
    def __init__(self):
        self.name:str = "Pawny One"
        self.inv_arti = []
    def useArti(self,key):
        Arti:Artifact = self.inv_arti[key]
        Arti.useItem()
def arti_creation(arti:str,target:person) -> None: #arti takes name, and then is mapped to corresponding arti
    if arti == "fate_die":
        target.inv_arti.append(DieArtifact()) #*3 this shit can probably be cleaned with dsa, cuz currently by adding an item, removing that item, and then adding a similiar item and then IT back results in two items with same uuid)
        target.inv_arti[-1].uuid = uuid.uuid4() #4 Utilizes UUID Module to assign unique uuids, Now, how tf will I access them for use? I dont fucking know.
def arti_validator(arti:str):
    return arti in valid_arti_list
def void_map_call(func,*input_list:list) -> None: # *input_list for parameter accepts multiple values and turns it into a tuple and for an argument, accepts a tuple and turns it into a bunch of values
    void_call = list(map(func,*input_list)) #What this basically does is tricks map into thinking it will return values, but it returns None, and while doing that, it iterated over each object the arti creation command, saving me some lines of code
    del(void_call) #Saves Space Ig.
player1 = person()
valid_arti_list = ["fate_die","invalidpieceofshit"]
arti_given_list = ["fate_die","fate_die","invalidpieceofshit","fate_die"] #artifacts to add
arti_given_list = list(filter(arti_validator,arti_given_list)) #Checks whether Artifacts asked for in arti_given_list is valid or not, and returns a valid list of artifacts
plrmap_list = [] #target mapping for arti creation
for i in range(0,len(arti_given_list)):
    plrmap_list.append(player1)  #assigns a target to every artifact, in this case only player 1
'''void_call = list(map(arti_creation,arti_given_list,plrmap_list)) #What this basically does is tricks map into thinking it will return values, but it returns None, and while doing that, it iterated over each object the arti creation command, saving me some lines of code
del(void_call) #Saves Space Ig.'''
void_map_call(arti_creation,arti_given_list,plrmap_list)
print(player1.inv_arti)
for i in range (0,len(player1.inv_arti)):
    print("[",i+1,"]",player1.inv_arti[i].name,player1.inv_arti[i].uuid)
arti:Artifact = player1.inv_arti[int(input(("Choose the artifact"))) - 1] #Place holder code ofc
arti.useItem(player1,arti) 
#player1 is only used here for visual code, not actually as "self" or something
#What is bro yapping.