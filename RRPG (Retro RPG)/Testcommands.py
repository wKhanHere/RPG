#updates and work required.
#1: [notice] A new release of pip is available: 24.3.1 -> 25.2
#[notice] To update, run: C:\Users\khan6\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe -m pip install --upgrade pip
#essentially update pip

#2: WARNING: The scripts f2py.exe and numpy-config.exe are installed in 'C:\Users\khan6\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts' which is not on PATH.
#Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

#Insights from here.
'''def function(i:int) -> int:
    if i == 1:
        return type(f"{i}")
    return i**2
print(function(2))
print(function(1))'''
#Insight 1: Even if function is typed for an output, it works regards of output typing.

"""x,y = (1,2)
print(x,"Koi",y)"""
#Insight 2: Unpacking works as expected

"""x:int = ["Koi"]
print(x)"""
#Type Casting is not strict apparently; Insight 3

"""def func(condition) -> None:
    if condition == False:
        return None
    return True
if func(True) == 1:
    print("What the heck")"""
#What on earth happens here? It works but why and how (?)Insight 4

'''list = [1,2,3,4,5,6,7,8,9,10]
del list[1:]
print(list)'''
#Insight 5: Deletes all elements except first

#Insight 6: Writing a Multiline comment just below a class or function to give it that on hover explanation text.
#Note: It must be a multiline comment

#Insight 7: To import a python file, the file extension must be ".py" with matching case, else it doesn't work. Don't ask me now.
'''class looptest():
    def loop(self,x):
        for i in range(0,x):
            print(x**i)
        print("Next")
        while 1 > 0:
            print(f"The number is {x}")
            x += 1
            if x > 10:
                break
loop:looptest = looptest()
loop.loop(5)'''

#Insight 8: Nested loops work as intended within functions and function calls.

"""import math
print(math.asin(1/2))"""

#Insight 9: Just some inverse trig functions

'''if 1 in {1:"Yes",2:"No"}:
    print("Yes")'''
#Insight 10: Using membership operators on dictionaries checks keys only.

#Insight 11: kwargs with dictionaries
'''#If MoveOrParams is:
{
    "MoveId": "magic:zap",
    "MoveName": "Zap",
    "Description": "A quick jolt of electricity.",
    "MoveBaseDamage": 7,
    "MoveBaseStaminaCost": 2,
    "MoveCooldown": 1,
    "MoveType": "Magic"
}
#It’s the same as calling:
Moves.CreateGenericMove(
    MoveId="magic:zap",
    MoveName="Zap",
    Description="A quick jolt of electricity.",
    MoveBaseDamage=7,
    MoveBaseStaminaCost=2,
    MoveCooldown=1,
    MoveType="Magic"
)
#Summary:
#**dict unpacks the dictionary so each key-value pair is passed as a named argument to the function. 
# The function’s parameter names must match the dictionary’s keys.'''


#Insight 12: Excerpt from Moves.py
''' else:
            a = 1
            for i in M.MovesRegistryObj.MovesList: #Uni move set does not have anything as of now
                Move:M.Moves = M.MovesRegistryObj.MovesList[i]
                print(f"[{a}] {Move.MoveName} (MoveId: \"{i}\")")
                a += 1
            try:
                Move:M.Moves = M.MovesRegistryObj.MovesList[input("Choose which move to view.\n[Enter index in exact format as displayed.]")]
                Move.ViewMove()  #Add a view move function to parent Moves Class
            except KeyError:
                print("Invalid index. Please try again.")'''
    #Example of try and except block to catch errors.