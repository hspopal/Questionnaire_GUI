#!/usr/bin/python

import Tkinter as tk
import time
from Tkinter import *
import os
 

"""GUI with frame one as subject info, frame two as questionnaire selection. 
    Frame three opens selected questionnaires as new windows."""


TITLE_FONT = ("Helvetica", 18, "bold")

# list created here so it can be referenced throughout the classes
selection = []

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")
        
        self.response_entries = []


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.response_entries = []
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # create a label for directions
        label = tk.Label(self, text="Enter LBC ID", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        
        # create an entry box for entering subject ID and save entry to list
        entry = tk.Entry(self)
        entry.pack()
        self.response_entries.append(entry)
        
        # automatically display the current date
        date = time.strftime("%m/%d/%Y")
        tk.Label(self, text = "Date: "+date).pack()

        # buttons to save subj info and to go to next frame
        button1 = tk.Button(self, text="Save & Continue",
                            command=self.subject_info)
        button1.pack()
        
        

    # save the subject's ID and today's date to a temporary csv
    def subject_info(self):
        answers = []
        for response in self.response_entries:
            answers.append(response.get())
        #answers.append(time.strftime("%m/%d/%Y"))
        print answers
        with open('subj_info.txt', 'w') as f:
            for subj in answers:
                f.write(subj)
        print "[response saved]"
        self.controller.show_frame("PageOne")



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Choose Questionnaires", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        
        # list contents of dir as check boxes
        path = './questionnaires/'
        self.all_questionnaires = os.listdir(path)
        self.all_questionnaires = self.all_questionnaires[1:]
        self.states = []
        for q in self.all_questionnaires:
            var = tk.IntVar()
            chk = Checkbutton(self, text=str(q), variable=var)
            chk.pack(anchor=W)
            self.states.append(var)  # save checkbox states as list
        self.controller = controller

        # buttons to go back to first frame or continue to launch frame
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack(side=LEFT)
        
        # button to trigger questionnaire selection save
        Button(self, text='Save & Continue', 
                command=self.save_states).pack(side=RIGHT)


    # save states of questionnaire check boxes
    def save_states(self):
        self.controller.show_frame("PageTwo")
        new = self.state()
        for i, j in enumerate(new):
            if j==1:
                selection.append(self.all_questionnaires[i])
        return selection


        
    def state(self):
        return map((lambda var: var.get()), self.states)
        
    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # button to launch questionnaires
        button1 = tk.Button(self, text="Open", command=self.onOpen)
        button1.pack()
        
        # states have to be defined for some stupid reason
        self.states = []
        self.state()


    # open whatever questionnaires have been selected    
    def onOpen(self):
        for s in selection:
            os.system('.\\questionnaires\\' + s + '\\' + s + '_program.py')

    
    # save states of questionnaire check boxes (has to be defined again)
    def save_states(self):
        new = self.state()
        for i, j in enumerate(new):
            if j==1:
                selection.append(self.all_questionnaires[i])
        return selection
        

    def state(self):
        return map((lambda var: var.get()), self.states)



if __name__ == "__main__":
    app = SampleApp()
    app.title("ASD Questionnaires")
    def close():
        app.quit()
        print("Written by Haroon of House Popal, first of his name, \nKing of the IRTAs and the summer students, \nLord of the Dorm, and Protector of the Data.")
    button1 = tk.Button(app, text="Quit", command=close)
    button1.pack()
    app.mainloop()
