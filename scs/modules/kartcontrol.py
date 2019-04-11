#You can import any required modules here

#This can be anything you want
moduleName = "kartcontrol"

#All of the words must be heard in order for this module to be executed
commandWords = ["turn"]

def execute(command, args):
    kartmodule = args[0]
    app = kartmodule.app
    commands = command.split(' ')
    print(commands)
    
    if("on" in commands):
        print("Turn kart on!")
    if("off" in commands):
        print("Turn kart off!")
    
    return
