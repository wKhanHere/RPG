import random
import copy
from typing import Any

import pandas


class CellObject: #Cells are fundamental units of a maze grid: Wall is permanent, Edge is a way to differentiate cells, will finalize to walls.
    def __init__(self,Type:str="PLACEHOLDER",Weight:float=0):
        self.TypeList:list = ["Empty","Wall","Edge","PLACEHOLDER"]
        self.TypeSet(Type)
        self.Weight:float = Weight #For events
        self.Finalized:bool = False #Used to check if tile is iterated
        self.Type = "PLACEHOLDER"
    def TypeSet(self,Type) -> None:
        if Type in self.TypeList:
            self.Type = Type
        else:
            print("Invalid Type Given: Replacing with placeholder.")
    def Info(self) -> None:
        print("Type:",self.Type,"\nFinalized:",self.Finalized,"\nWeight:",self.Weight)

class Grid:
    """An object used to Manage Grid Data."""
    def __init__(self,x:int,y:int) -> None: #please use odd numbered grids
        self.x_dim:int = 2*x+1
        self.y_dim:int = 2*y+1
        self.EmptyTiles:list = [] #This refers to Empty cells initially
        self.GridHolder:dict = {} #Base, isn't really used
        self.GridHolderFinal:dict = {}
        self.AllDir:tuple = (0, 1, 2, 3) #("up","left","down","right") #This is now not stupid. Nice
        self.ProcessingGrid:dict = {}  #Essentially Midway work Grid, Grid base is base grid and grid final is result
        self.TypeList:list = ["Empty","Wall","Edge","PLACEHOLDER"]
        self.UnFUniversal:list = [] #Basically Base Mapped to Unfinalized keys (processing keys)
        self.UnFEmpty:list = [] #It is a list of keys local to this function, which sets cords to finalized if the Finalizing Wilson Sequence occurs: NOTE This uses USEFUL TILES  Cords (They all are empty at this stage)
        self.MoveDir:str = "" #Needed to be predefined for ChooseDir() to work
        self.EndGenerationStep1:bool = False #So that I don't run the gen loop 10000 times

    def SetGridBase(self) -> None:
        """Creates a basic grid used for running maze creation algorithms."""
        for j in range(0,self.y_dim): #Adds cells to Maze grid, Empty Base Walls
          for i in range(0,self.x_dim):
            self.GridHolder[(i,j)] = CellObject()
            if (i % 2 == 0 and j % 2 == 0) or (i in [0,self.x_dim-1]) or (j in [0,self.y_dim-1]):  self.GridHolder[(i,j)].TypeSet("Wall")
            elif (i%2 == 0 and j%2 ==1) or (i%2 == 1 and j%2 ==0): self.GridHolder[(i,j)].TypeSet("Edge")
            else: 
                self.GridHolder[(i,j)].TypeSet("Empty")
                self.EmptyTiles.append(((i-1)/2,(j-1)/2))         
        self.ProcessingGrid = copy.deepcopy(self.GridHolder)
        xytuple:tuple = self.GetRandEmpty() #Adds Initial Point for generation: Is converted into Tile Keys next
        x:int = (xytuple[0]-1)/2 #x,y represent current x,y
        y:int = (xytuple[1]-1)/2 #Crude conversion to Empty tiles coordinates
        self.ProcessingGrid[(2*x+1,2*y+1)].Finalized = True
    def ViewBase(self,clean:bool = False) -> None:
        for j in range(0,self.y_dim): #The i,j ordering is correct, if you think otherwise think again
            for i in range(0,self.x_dim):
                Cell:CellObject = self.GridHolder[(i, j)]
                if Cell.Type == "Wall":
                    print("🟨 ",end = "")
                elif Cell.Type == "Empty" and Cell.Finalized == False and (i,j) not in self.UnFUniversal:
                    print("🟦 ",end = "") #Unprocessed
                elif Cell.Finalized:
                    print("🔷 ", end= "") #Final
                elif (i,j) in self.UnFUniversal:
                    print("🟧 ", end= "") #Processing
                elif Cell.Type == "Edge":
                    print("🟩 ",end ="")
                if not clean:
                    print((i,j),end="")
            print()
        print("\n\n\n")
    def ViewProcessed(self,clean:bool = False) -> None:
        try:
            for j in range(0,self.y_dim): #The i,j ordering is correct, if you think otherwise think again
                for i in range(0,self.x_dim):
                    Cell:CellObject = self.ProcessingGrid[(i, j)]
                    if Cell.Type == "Wall":
                        print("🟨 ",end = "")
                    elif Cell.Type == "Empty" and Cell.Finalized == False and (i,j) not in self.UnFUniversal:
                        print("🟦 ",end = "") #Unprocessed
                    elif Cell.Finalized:
                        print("🔷 ", end= "") #Final
                    elif (i,j) in self.UnFUniversal:
                        print("🟧 ", end= "") #Processing
                    elif Cell.Type == "Edge":
                        print("🟩 ",end ="")
                    if not clean:
                        print((i,j),end="")
                print()
            print("\n")
        except AttributeError:
          print("Processing Grid Object Not Found (Generation is Complete)")  
    def ViewFinal(self,clean:bool = False) -> None:
        for j in range(0,self.y_dim):
            for i in range(0,self.x_dim):
                Cell:CellObject = self.GridHolderFinal[(i, j)]
                if Cell.Type == "Wall":
                    print("🔶 ",end = "")
                elif Cell.Finalized:
                    print("🔷 ", end= "") #Final
                if not clean:
                    print((i,j),end="")
            print()
        print("\n\n\n")
    def GetAllType(self, Type) -> list:
        """Fetches all the keys for cells w/ a specified type
        \n Only derives from Processing Grid.
        """
        ChoiceList:list = []
        for i in self.ProcessingGrid.keys():
            Cell:CellObject = self.ProcessingGrid[(i[0], i[1])]
            if Cell.Type == Type and Cell.Finalized == False:
                ChoiceList.append(i)
        return ChoiceList
    def GetRandEmpty(self) -> Any | None:
        """Returns a cords of a random "Empty" cell (key) (For Processing Grid only)"""
        ListEmpty:list = self.GetAllType("Empty")
        if not ListEmpty:
            return None
        return random.choice(ListEmpty)
    def ChooseDir(self,x:int,y:int) -> int:
        """Returns an int for moving to adjacent cell. The code is as follows:
        \n 0 -> Up
        \n 1 -> Left
        \n 2 -> Down
        \n 3 -> Right"""
        ChosenDir:list = []
        ValidKeys = copy.deepcopy(self.EmptyTiles)
        if (x,y+1) in ValidKeys and self.MoveDir != 2:
            ChosenDir.append(self.AllDir[0])
        if (x-1,y) in ValidKeys and self.MoveDir != 3:
            ChosenDir.append(self.AllDir[1])
        if (x,y-1) in ValidKeys and self.MoveDir != 0:
            ChosenDir.append(self.AllDir[2])
        if (x+1,y) in ValidKeys and self.MoveDir != 1:
            ChosenDir.append(self.AllDir[3])
        return random.choice(ChosenDir)
    @staticmethod
    def DirToKey(Dir:int, Coord:list) -> tuple:
        """Returns Next Coordinate according input direction code.
        \n Essentially converts ChooseDir's int code to a tangible direction."""
        if Dir == 0:
            Coord[1] += 1
        if Dir == 1:
            Coord[0] -= 1
        if Dir == 2:
            Coord[1] -= 1
        if Dir == 3:
            Coord[0] += 1
        return tuple(Coord)
    def GenMazeLoop(self) -> None:
        while 1 > 0:
            #Please Put this into the class: To measure how much is done and make % not a troll and use that % value to switch b/w generation algorithms
            Maze.GenMaze_Step1()   
            if Maze.EndGenerationStep1:
                Maze.GenMaze_Step2()
                print("Processing 100% Done!")
                break
    def GenMaze_Step1(self) -> None:
        """Wilson Algorithm for Mazes, creates the base maze without tile population."""
        xytuple:tuple = self.GetRandEmpty() #Adds Initial Point for generation: Is converted into Tile Keys next
        if xytuple is None: #Essentially if all tiles are finalized, it returns None and thus Gen function ends.
            self.EndGenerationStep1 = True
            return
        x:int = (xytuple[0]-1)/2 #x,y represent current x,y
        y:int = (xytuple[1]-1)/2 #Crude conversion to Empty tiles coordinates
        self.UnFEmpty.append((x,y))
        self.UnFUniversal.append((2*x+1,2*y+1))
        while 1>0:
            self.MoveDir = self.ChooseDir(x,y) #Essentially Chooses a dir, and then moves accordingly in proceeding lines    
            x2,y2 = self.DirToKey(self.MoveDir,[x,y]) #It is first stored in x2 y2 just to get the Edge cell inbetween and add it to list.
            CorrespondingCell:CellObject = self.ProcessingGrid[(2 * x2 + 1, 2 * y2 + 1)]
            self.UnFEmpty.append((x2,y2))
            self.UnFUniversal.append((2*x2+1,2*y2+1))
            self.UnFUniversal.append((x+x2+1,y+y2+1)) #This refers to Edge cell in between
            x = copy.deepcopy(x2)
            y = copy.deepcopy(y2)
            if CorrespondingCell.Finalized:
                for i in self.UnFUniversal:
                    Cell:CellObject = self.ProcessingGrid[i]
                    Cell.Finalized = True
                    if Cell.Type == "Edge": Cell.Type = "Empty"
                del self.UnFEmpty[0:]
                del self.UnFUniversal[0:]
                break
            elif self.UnFEmpty.count((x2,y2)) > 1:
                del self.UnFEmpty[1:]
                del self.UnFUniversal[1:]
                x = self.UnFEmpty[0][0]
                y = self.UnFEmpty[0][1] 
    def GenMaze_Step2(self) -> None: #Make Walls Final, Make Edges Final and Walls. Calls Final Step after done
        for i in self.GetAllType("Wall"):
            Cell:CellObject = self.ProcessingGrid[i]
            Cell.Finalized = True
        for i in self.GetAllType("Edge"):
            Cell:CellObject = self.ProcessingGrid[i]
            Cell.Finalized = True
            Cell.Type = "Wall"
        self.GenMaze_StepFinal()
    def GenMaze_StepFinal(self) -> None: #Just load Processing grid onto GridHolderFinal and Dump Processing grid
        self.GridHolderFinal = copy.deepcopy(self.ProcessingGrid)
        del self.ProcessingGrid
if __name__ == "__main__":
    xdim = int(input("Enter X: "))
    ydim = int(input("Enter Y: "))
    Maze = Grid(xdim,ydim)
    Maze.SetGridBase()
    Maze.GenMazeLoop()
    Maze.ViewFinal(True) #True -> Clean Result (No Coordinates)

    import matplotlib.pyplot as pplot
    MazeDataFrame:pandas.DataFrame = pandas.DataFrame(index = range(Maze.y_dim),columns = range(Maze.x_dim))
    NEmpty:int = 40
    NWall:int = 0
    NEdge:int = 12
    NPlaceholder:int = 35
    for i in range(Maze.x_dim-1):
        for j in range(Maze.y_dim-1):
            print((i,j))
            cellGot = Maze.GridHolderFinal[(i,j)]
            MazeDataFrame.iat[i,j] = cellGot
            if cellGot.Type == "Empty":
                NEmpty += 1
            elif cellGot.Type == "Wall":
                NWall += 1
            elif cellGot.Type == "Edge":
                NEdge += 1
            else:
                NPlaceholder += 1
    pplot.pie([NEmpty, NWall, NEdge, NPlaceholder],labels=["No. of Empty","No. of Wall","No. of Edge","No. of Placeholder"],explode = [1,0,0,0],autopct="%5.2f%%")
    pplot.show()

#We could replace the ChooseDir and Dir to key with one function if we instead converted the selected coordinate tuple pair into an array, did vector operations (up down left right you know maths) and then shipped it back as a tuple