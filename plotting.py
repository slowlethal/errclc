import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

def tkinter_plot(master, x, xerr, y, yerr, x_name, y_name):
    fig = Figure(figsize=(5, 4), dpi=100)
    #fig, ax = plt.subplots(1, 1)
    #fig.add_subplot(111).errorbar(x=x, y=y, xerr=xerr, yerr=yerr, capsize=2, elinewidth=1, lw=0)
    ax = fig.add_subplot(111)
    ax.errorbar(x=x, y=y, xerr=xerr, yerr=yerr, capsize=2, elinewidth=1, lw=0)
    ax.set_xlabel(r"%s"%x_name)
    ax.set_ylabel(r"%s"%y_name)
    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    canvas.get_tk_widget().grid(column=3, row=0, columnspan=40, rowspan=40, padx=20, pady=20)
    return fig

def savefig(fig):
    fig.savefig("fig_1")



"""



root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()


"""


# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.