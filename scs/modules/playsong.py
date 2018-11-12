#You can import any required modules here

#This can be anything you want
moduleName = "playsong"

#All of the words must be heard in order for this module to be executed
commandWords = ["play"]

def execute(command, *args):
    #Write anything you want to be executed when the commandWords are heard
    #The 'command' parameter is the command you speak
    comm = command.split('play', 1)
    gui = args[0]
    print(comm)
    print(command)
    gui.play_song(comm[1])
    return
