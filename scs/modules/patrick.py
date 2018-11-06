#You can import any required modules here

#This can be anything you want
moduleName = "patrick"

#All of the words must be heard in order for this module to be executed
commandWords = ["guess", "here"]

def execute(command, *args):
    #Write anything you want to be executed when the commandWords are heard
    #The 'command' parameter is the command you speak
    gui = args[0]
    gui.guess_who_here()
    return
