from tkinter import *
from tkinter import ttk

class Application(ttk.Frame):
    
    @classmethod
    def main(cls):
        NoDefaultRoot()
        root = Tk()
        app = cls(root)
        app.grid(column=1, row=1)
        root.resizable(True, True)
        root.geometry("800x480")
        #root.attributes("-fullscreen", True)
        root.bind("<F11>", app.toggleFullScreen)
        root.mainloop()
        
    def __init__(self, root, **args):
        super().__init__(root, **args)
        print("Initialized application")
        self.root = root
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        
    def create_variables(self):
        self.fullscreen = True
        
    def toggleFullScreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        
    def create_widgets(self):
        self.but1 = Button(self, text="Press Me!", command=self.but1)
        self.but2 = Button(self, text="Press Me!", command=self.but2)
        self.but3 = Button(self, text="Middle!", command=lambda c: print("Middle!"))
        
    def grid_widgets(self):
        self.but1.grid(column=0, row=0)
        self.but2.grid(column=1, row=1)
        self.but3.grid(column=2, row= 2)
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
            
    def pp(self, butt):
        if(butt == self.but1):
            print("Button 1 pressed")
        elif(butt == self.but2):
            print("Button 2 pressed")
        print("Hello, world!")
        
    def but1(self):
        self.pp(self.but1)
        
    def but2(self):
        self.pp(self.but2)
        
if __name__ == '__main__':
    Application.main()
