"""
super duper error calculation
"""

import pprint
import time as t


import tkinter as tk
import matplotlib.pyplot as plt
import math as m
import numpy as np
from scipy.optimize import curve_fit
#import xerox
from plotting import tkinter_plot, savefig

from fehlerrechnung_funktionen import (roundwitherror, list_error_calc, listifyString, killchars, fitAndPlot, NIST_replace)

#https://www.youtube.com/watch?v=yMR45cZbvDw # youtube sentdex






class SampleApp(tk.Tk):
    """
    window program
    """
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
                PlotPage,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
        #scheißverfickter forloop
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PageOne")
    def show_frame(self, page_name):
        """
        docstring
        """
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class PlotPage(tk.Frame):
    """
    docstring
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.x_name = tk.StringVar()
        self.y_name = tk.StringVar()
        self.x_data = tk.StringVar()
        self.y_data = tk.StringVar()


        tk.Button(
            self, text="Back",
            command=lambda: controller.show_frame("PageOne")
            ).grid(column=0, row=0, sticky="W")
        self.plotbutton = tk.Button(
            self, text="Plot",
            command=lambda: fitAndPlot(
                PageOne.data[self.x_data.get()],
                PageOne.data[self.y_data.get()]
                )
            )
        PageOne.data = {"a":((1,2,3,4), (1,1,1,1)), "b":((2,4,5,6), (1,1,1,1))}
        tk.Button(
            self, text="more plot", command=lambda: self.makePlot() 
            ).grid(column=0, row=1, sticky="W")
        self.plotbutton.grid(column=0, row=2, sticky="W")
        tk.Entry(self, textvariable=self.x_name).grid(column=1, row=3)
        tk.Entry(self, textvariable=self.y_name).grid(column=1, row=4)
        tk.Entry(self, textvariable=self.x_data).grid(column=1, row=5)
        tk.Entry(self, textvariable=self.y_data).grid(column=1, row=6)
        tk.Label(self, text="x Name").grid(column=0, row=3, sticky="W")
        tk.Label(self, text="y Name").grid(column=0, row=4, sticky="W")
        tk.Label(self, text="x Data").grid(column=0, row=5, sticky="W")
        tk.Label(self, text="x Data").grid(column=0, row=6, sticky="W")
        tk.Button(self, text="save", command=lambda: savefig(self.fig)).grid(column=0, row=7)
        self.option_menu_y = tk.OptionMenu(self, self.x_data, *PageOne.data.keys())
        self.option_menu_y.grid(column=0, row=8)

        self.variable = tk.StringVar()
        PlotPage.menu_y = self.option_menu_y["menu"]
        PlotPage.menu_y.add("command", label="test", command=lambda value="test": self.x_data.set("test"))
        """
        while True:
            self.option_menu_y.grid_forget()
            self.option_menu_y = tk.OptionMenu(self, self.x_data, PageOne.data.keys())
            self.option_menu_y.grid(column=0, row=8)
            t.sleep(5)
        """
        """
        self.opt = tk.OptionMenu(self, self.variable, *PageOne.data.keys())
        self.opt.config(width=90, font=('Helvetica', 12))
        self.opt.place(x=20, y=170, width=125, height=20)
        """

    def update_option_menu(self, menu, labels):
        menu.delete(0, "end")
        #print("test")
        for label in labels:
            menu.add("command", label=label, command=lambda value=label: self.x_data.set(label))

    def makePlot(self):
        """
        dcostring
        """
        self.fig = tkinter_plot(
                self, *PageOne.data[self.x_data.get()], *PageOne.data[self.y_data.get()],
                self.x_name.get(), self.y_name.get()
                )

class StartPage(tk.Frame):
    """
    docstring
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="MOIN", font=("helvetica", 30))
        label.pack(side="top", fill="x", pady=100, padx=100)
        button1 = tk.Button(
            self, text="Fehlerrechner",
            command=lambda: controller.show_frame("PageOne")
            )
        quitbutton = tk.Button(self, text="Ende", command=self.quit)
        button1.pack()
        quitbutton.pack()

class PageOne(tk.Frame):
    """
    docstring
    """
    data = {}
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.row_number = 2
        self.v = tk.IntVar()
        c = tk.Checkbutton(self, text="Excel", variable=self.v, command=lambda: self.FR())
        c.grid(row=0, column=5)
        self.roundput = tk.IntVar()
        d = tk.Checkbutton(
            self,
            text="Round Output",
            variable=self.roundput,
            command=lambda: self.FR()
            )
        d.grid(row=1, column=5)

        self.result_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.formula_var = tk.StringVar()
        tk.Label(self, text="Formel").grid(row=0, column=2)
        tk.Label(self, text="Folgewert").grid(row=0, column=3)
        tk.Label(self, text="Folgefehler").grid(row=0, column=4)
        self.backbutton = tk.Button(
            self, text="zurück", command=lambda: controller.show_frame("StartPage")
            )
        self.backbutton.grid(row=1, column=1)
        self.formulaEntry = tk.Entry(self, textvariable=self.formula_var)
        self.formulaEntry.grid(row=1, column=2)
        self.result_entry = tk.Entry(self, textvariable=self.result_var)
        self.result_entry.grid(row=1, column=3)
        self.result_error_entry = tk.Entry(self, textvariable=self.error_var)
        self.result_error_entry.grid(row=1, column=4)
        self.plot_button = tk.Button(
            self, text="Plotten (WIP)", command=lambda: controller.show_frame("PlotPage")
            )
        self.plot_button.grid(row=2, column=1)
        self.calc_button = tk.Button(self, text="Folgefehler berechnen", command=lambda: self.FR())
        self.calc_button.grid(row=3, column=1)
        tk.Label(self, text="Präsentiert von Camel Zigaretten").grid(row=0, column=1)
        self.addbutton = tk.Button(self, text="neue Zeile", command=lambda: self.Widgets("add"))
        self.removebutton = tk.Button(
            self, text="Zeile entfernen", command=lambda: self.Widgets("remove")
            )
        self.testbutton = tk.Button(self, text="Werte übernehmen", command=lambda: self.getList())
        self.label3 = tk.Label(self, text="Wert")
        self.label4 = tk.Label(self, text="Fehler")
        self.label7 = tk.Label(self, text="Bezeichnung")
        self.addbutton.grid(row=3, column=5)
        self.testbutton.grid(row=4, column=1)
        self.label3.grid(row=2, column=2)
        self.label4.grid(row=2, column=3)
        self.label7.grid(row=2, column=4)
        self.Widgets("add")
        self.delimiter = tk.StringVar()
        self.delimiter.set(",")
        self.custom_delimiter = tk.Entry(self, textvariable=self.delimiter)
        self.custom_delimiter.grid(row=0, column=6)

    def FR(self):
        """
        docstring
        """
        F = self.formula_var.get()
        F = NIST_replace(F)
        if len(F):
            a = []
            for key in self.data.keys():
                a.append(key in F and key != "")
            if all(a):
                X = list_error_calc(self.data, F, roundput=self.roundput.get())
                if self.v.get() == 1:
                    result = killchars(str(X[0]).strip("[]").replace(
                        ",", "\n").replace(",", self.delimiter.get()), " "
                                      )
                    error = killchars(str(X[1]).strip("[]").replace(
                        ",", "\n").replace(",", self.delimiter.get()), " "
                                     )
                else:
                    result = str(X[0]).strip("[]")
                    error = str(X[1]).strip("[]")
                self.result_var.set(result)
                self.error_var.set(error)
                i = 0
                paste = ""
                x, err = X
                while i < len(x):
                    if i == len(x) - 1:
                        paste += str(x[i])+"\t"+str(err[i])
                    else:
                        paste += str(x[i])+"\t"+str(err[i])+"\n"
                    i += 1
                #xerox.copy(paste)
                #print("pasted to clipboard")
            else:
                print("Referenced nonexistent variables in function. Check variable names!")
        PlotPage.update_option_menu(PlotPage, PlotPage.menu_y, self.data.keys())

    def Widgets(self, state):
        """
        docstring
        """

        if state == "add":
            self.row_number = self.row_number + 1
            if self.row_number > 3:
                self.addbutton.grid_remove()
            if self.row_number > 4:
                self.removebutton.grid_remove()
            self.entry_pos_x = tk.Entry(self)
            self.entry_pos_y = tk.Entry(self)
            self.entry_name = tk.Entry(self)
            self.entry_pos_x.grid(row=self.row_number, column=2)
            self.entry_pos_y.grid(row=self.row_number, column=3)
            self.entry_name.grid(row=self.row_number, column=4)
            self.addbutton.grid(row=self.row_number, column=5)
            if self.row_number > 3:
                self.removebutton.grid(row=self.row_number, column=6)
        if state == "remove":
            self.addbutton.grid_remove()
            self.removebutton.grid_remove()
            for self.entry in PageOne.grid_slaves(self):
                if int(
                        self.entry.grid_info()["row"]
                    ) == int(self.row_number) and int(self.entry.grid_info()["column"] > 1):
                    self.entry.grid_forget()
            self.addbutton.grid(row=self.row_number - 1, column=5)
            if self.row_number > 4:
                self.removebutton.grid(row=self.row_number - 1, column=6)
            self.row_number = self.row_number - 1

    def getList(self, delimiter=","):
        """
        docstring
        """
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
                            """
                            replace designated physical constants with NIST values
                            """
                            t = slave.get()
                            t = NIST_replace(t)
                            l.append(listifyString(t.strip(delimiter), delimiter))
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

#################################################################################################
if __name__ == "__main__":
    try:
        app = SampleApp()
        app.title("OTFR")
        app.mainloop()
        app.destroy()
    except tk.TclError as tkerr:
        print("exited from TclError: {}".format(tkerr))
