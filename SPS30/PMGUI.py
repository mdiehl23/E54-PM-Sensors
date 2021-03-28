from tkinter import *
'''
This screen will display once a successful data pull has been completed.
@Author: Matt Diehl
'''
class SuccessScreen(Tk):
    def __init__(self,pm25,pm10):
        Tk.__init__(self)
        self.pm10 = pm10
        self.pm25 = pm25
        self.makeScreen()
        
    def makeScreen(self):
        self.title("PM Data Logger")
        mainframe = Frame(self)
        mainframe.configure(bg = 'blue')
        mainframe.pack(fill = BOTH, expand = True, pady = 5)

        title_text = Label(mainframe, text = "Data Pull Complete.", bg = 'blue', fg = 'white', font = 'Helvetica 36 bold')
        title_text.pack(fill = BOTH, expand = True, pady = 10)

        pm25_label = Label(mainframe, text = "Average PM 2.5 Concentration: " + self.pm25, bg = 'blue', fg = 'white', font = 'Helvetica 24 bold')
        pm25_label.pack(fill = BOTH, expand = True, pady = 10)

        pm10_label = Label(mainframe, text = "Average PM 10 Concentration: " + self.pm10, bg = 'blue', fg = 'white', font = 'Helvetica 24 bold')
        pm10_label.pack(fill = BOTH, expand = True, pady = 10)

        quit_but = Button(mainframe, text = "Close Window", bg = 'White', fg = 'blue', font = 'Helvetica 24 bold')
        quit_but['command'] = self.destroy
        quit_but.pack(expand = True, pady = 5)

'''
This screen will display when something goes wrong.
@Author: Matt Diehl
'''
class FailedScreen(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.makeScreen()

    def makeScreen(self):
        self.title("PM Data Logger")
        mainframe = Frame(self)
        mainframe.configure(bg = 'blue')
        mainframe.pack(fill = BOTH, expand = True, pady = 5)

        title_text = Label(mainframe, text = "Data Pull Failed. Try Again", bg = 'blue', fg = 'white', font = 'Helvetica 36 bold')
        title_text.pack(fill = BOTH, expand = True, pady = 10)

        quit_but = Button(mainframe, text = "Close Window", bg = 'White', fg = 'blue', font = 'Helvetica 24 bold')
        quit_but['command'] = self.destroy
        quit_but.pack(expand = True, pady = 5)
        
