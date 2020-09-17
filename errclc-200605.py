
import tkinter as tk
import matplotlib.pyplot as plt
import math as m
import numpy as np
from scipy.optimize import curve_fit


import sys
sys.path.append("/home/ole/Desktop/Projekt_1")
from fehlerrechnung_funktionen import roundwitherror, listErrorCalc, listifyString, killchars, paste2clip

import pprint
import time as t

#https://www.youtube.com/watch?v=yMR45cZbvDw # youtube sentdex
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # IMMER BRAV ALLE SEITEN ADDEN!!
        for F in (
            StartPage,
            PageOne,
            PlotPage,
            ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
        #scheißverfickter forloop
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PageOne")
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class PlotPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.xName = ""
        self.yName = ""
        self.xData = ""
        self.yData = ""


        tk.Button(self, text = "Back", command = lambda: controller.show_frame("PageOne")).grid(row = 0, column = 0)

        tk.Entry(self, textvariable = self.xName).grid(row = 1, column = 1)
        tk.Entry(self, textvariable = self.yName).grid(row = 2, column = 1)
        tk.Entry(self, textvariable = self.xData).grid(row = 3, column = 1)
        tk.Entry(self, textvariable = self.yData).grid(row = 4, column = 1)
        tk.Label(self, text = "x Name").grid(row = 1, column = 0)
        tk.Label(self, text = "y Name").grid(row = 2, column = 0)
        tk.Label(self, text = "x Data").grid(row = 3, column = 0)
        tk.Label(self, text = "x Data").grid(row = 4, column = 0)
    def makePlot(self):
        pass

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MOIN", font = ("helvetica",30))
        label.pack(side="top", fill="x", pady=100, padx = 100)
        button1 = tk.Button(self, text="Fehlerrechner", command=lambda: controller.show_frame("PageOne"))
        quitbutton = tk.Button(self, text = "Ende", command = self.quit)
        button1.pack()
        quitbutton.pack()
class PageOne(tk.Frame):
    data = {}
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.names = ("entryMass",
                      "entryPosx",
                      "entryPosy",
                      "entryVelx",
                      "entryVely"
                      )
        self.row_number = 2

        self.v = tk.IntVar()
        c = tk.Checkbutton(self, text = "Excel", variable = self.v, command = lambda:self.FR())
        c.grid(row = 0, column = 5)
        self.roundput = tk.IntVar()
        d = tk.Checkbutton(self, text = "Round Output", variable = self.roundput, command = lambda:self.FR())
        d.grid(row = 1, column = 5)
        """
        clipbutton = tk.Button(self, text = "Copy", command = lambda:self.copy2clip())
        clipbutton.grid(row = 2, column = 5)
        """

        self.resultVar = tk.StringVar()
        self.errorVar = tk.StringVar()
        self.clipVar = tk.StringVar()
        self.formulaVar = tk.StringVar()
        tk.Label(self, text = "Formel").grid(row = 0, column = 2)
        tk.Label(self, text = "Folgewert").grid(row = 0, column = 3)
        tk.Label(self, text = "Folgefehler").grid(row = 0, column = 4)
        
        self.backbutton = tk.Button(self, text="zurück", command=lambda: controller.show_frame("StartPage"))
        self.backbutton.grid(row = 1, column = 1)
        self.formulaEntry = tk.Entry(self, textvariable = self.formulaVar)
        self.formulaEntry.grid(row = 1, column = 2)
        self.resultEntry = tk.Entry(self, textvariable = self.resultVar)
        self.resultEntry.grid(row = 1, column = 3)
        self.resultErrorEntry = tk.Entry(self, textvariable = self.errorVar)
        self.resultErrorEntry.grid(row = 1, column = 4)
        self.clipEntry = tk.Entry(self, textvariable = self.clipVar)
        self.clipEntry.grid(row = 2, column = 5)
        self.Plotbutton = tk.Button(self, text = "Plotten (WIP)", command = lambda:controller.show_frame("PlotPage"))
        self.Plotbutton.grid(row = 2, column = 1)
        self.calcButton = tk.Button(self, text = "Folgefehler berechnen", command = lambda:self.FR())
        self.calcButton.grid(row = 3, column = 1)

        self.label1 = tk.Label(self, text="Präsentiert von Camel Zigaretten")
        
        self.addbutton = tk.Button(self, text = "neue Zeile", command = lambda : self.Widgets("add"))
        self.removebutton = tk.Button(self, text = "Zeile entfernen", command = lambda : self.Widgets("remove"))
        self.testbutton = tk.Button(self, text = "Werte übernehmen", command = lambda : self.getList())
        self.label3 = tk.Label(self, text = "Wert")
        self.label4 = tk.Label(self, text = "Fehler")
        self.label7 = tk.Label(self, text = "Bezeichnung")
        self.label1.grid(row = 0, column = 1)
        
        self.addbutton.grid(row = 3, column = 5)
        self.testbutton.grid(row = 4, column = 1)
        self.label3.grid(row = 2, column = 2)
        self.label4.grid(row = 2, column = 3)
        self.label7.grid(row = 2, column = 4)
        self.Widgets("add")

        self.Delimiter = tk.StringVar()
        self.Delimiter.set(",")
        self.customDelimiter = tk.Entry(self, textvariable = self.Delimiter)
        self.customDelimiter.grid(row = 0, column = 6)



    def FR(self):
    	F = self.formulaVar.get()
    	if len(F) > 0:
            a = []
            for key in self.data.keys():
                a.append(key in F and key != "")
            if all(a) == True:
                X = listErrorCalc(self.data, F, roundput = self.roundput.get())
                if self.v.get() == 1:
                    result = killchars(str(X[0]).strip("[]").replace(",", "\n").replace(",", self.Delimiter.get()), " ")
                    error = killchars(str(X[1]).strip("[]").replace(",", "\n").replace(",", self.Delimiter.get()), " ")
                else:
                    result = str(X[0]).strip("[]")
                    error = str(X[1]).strip("[]")
                self.resultVar.set(result)
                self.errorVar.set(error)
                i = 0
                paste = ""
                x, err = X
                while i < len(x):
                    if i == len(x) - 1:
                        paste += str(x[i])+"\t"+str(err[i])
                    else:
                        paste += str(x[i])+"\t"+str(err[i])+"\n"
                    i += 1
                self.clipVar.set(paste)
                print("pasted")
            else:
                print("Referenced nonexistent variables in function. Check variable names!")

    def Widgets(self, state):
        if state == "add":
            self.row_number = self.row_number + 1
            if self.row_number > 3:
                self.addbutton.grid_remove()
            if self.row_number > 4:
                self.removebutton.grid_remove()
            self.entryPosx = tk.Entry(self)
            self.entryPosy = tk.Entry(self)
            self.entryName = tk.Entry(self)
            self.entryPosx.grid(row = self.row_number, column = 2)
            self.entryPosy.grid(row = self.row_number, column = 3)
            self.entryName.grid(row = self.row_number, column = 4)
            self.addbutton.grid(row = self.row_number, column = 5)
            if self.row_number > 3:
                self.removebutton.grid(row = self.row_number, column = 6)
        if state == "remove":
            self.addbutton.grid_remove()
            self.removebutton.grid_remove()
            for self.entry in PageOne.grid_slaves(self):
                if int(self.entry.grid_info()["row"]) == int(self.row_number) and int(self.entry.grid_info()["column"] > 1):
                    self.entry.grid_forget()
            self.addbutton.grid(row = self.row_number - 1, column = 5)
            if self.row_number > 4:
                self.removebutton.grid(row = self.row_number - 1, column = 6)
            self.row_number = self.row_number - 1
    def getList(self, delimiter = ","):
        i = 3
        if self.v.get() == 1:
            delimiter = "\n"
        slaves = PageOne.grid_slaves(self)
        entries = {}
        while i <= self.row_number:
            l = [] 
            k = 2
            while k <= 4:
                for slave in slaves:
                    if slave.grid_info()["row"] == i and slave.grid_info()["column"] == k:
                        if k <= 3:
                            l.append(listifyString(slave.get().strip(delimiter), delimiter))
                        if k == 4:
                            name = str(slave.get())
                k += 1
            i += 1
            x, err = l
            k = len(err)/len(x)
            j = 0
            ERR = []
            while j < len(x):
                e = str(err[int(j*k)])
                if "%" in e:
                    ERR.append(x[j]*float(e.split("%")[0])/100)
                else:
                    ERR.append(float(e))
                j += 1
            entries[name] = (x, ERR)
        PageOne.data = entries
        #print(PageOne.data)

###################################################################################################################

if __name__ == "__main__":
    app = SampleApp()
    app.title("OTFR")
    app.mainloop()
    app.destroy()

