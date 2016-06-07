#!/usr/bin/python

"""Takes repsonses from GUI and appends them individually to a column.
    Arranges widgets with Item above respective entry boxes."""

import Tkinter as tk
from Tkinter import *
import csv
import time


# Pull items from a text file which contains items from questionnaire
items = open('./questionnaires/Sample/Sample_items.txt').readlines()



class Questionnaire(tk.Frame):
    def __init__(self, root):

        # creates a canvas on top of a frame so that the window can scroll
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        # prints the instructions for the questionnaire
        with open('./questionnaires/Sample/Sample_instructions.txt', 'r') as instructions:
            instr = instructions.read()
        tk.Label(self.frame, text=instr, anchor=W, justify=CENTER).pack()

        # this is a list of response entry boxes
        self.response_entries = []

        # Put these two buttons at the bottom of the window and anchor them there
        tk.Button(self,text="Save response",command=self.save_test).pack(anchor=tk.S,side=tk.BOTTOM)
        

        # new ingredients will be added between the label and the buttons 
        self.add_response_entry()
        

    # function to add new responses
    # brings up widgets of items and entry boxes
    def add_response_entry(self):
        self.response_entries = []
        for i in items:
            tk.Label(self.frame,text='\n'+i).pack(pady=1, anchor=W)
            var = IntVar()
            for n in range(1,5):
                tk.Radiobutton(self.frame, text=n, variable = var, value=n).pack(anchor=W)
            self.response_entries.append(var)

   
    # get contents of all entry boxes
    def save_test(self):
        self.top = Toplevel()
        end = "Are you sure you want to exit?"
        tk.Label(self.top, text=end, justify=CENTER).pack()
        button1 = Button(self.top, text="Yes", command=self.end_questionnaire)
        button2 = Button(self.top, text="No", command=self.dont_end)
        button2.pack(padx=15, side=LEFT)
        button1.pack(padx=15, side=LEFT)


    def end_questionnaire(self):
        answers = []
        with open('subj_info.txt') as f:
            answers = f.readlines()
        answers.append(time.strftime("%m/%d/%Y"))
        for response in self.response_entries:
            answers.append(response.get())
        print answers
        with open('./questionnaires/Sample/Sample.csv', 'a') as f:
            w=csv.writer(f, delimiter=',')
            w.writerow(answers)
        print "[response saved]"
        root.destroy()
        
    def dont_end(self):
        self.top.destroy()

    # reset the scroll region to encompas the inner frame
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.title("Sample")
    Questionnaire(root).pack(side="top", fill="both", expand=True)
    root.mainloop()