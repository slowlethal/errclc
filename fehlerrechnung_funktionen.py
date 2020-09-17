import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math as m
from math import sin, cos, tan, asin, acos, atan, exp, e, pi, log
import numpy as np
import decimal
import pyperclip as ppc

"""
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}
"""
font = {'weight' : 'normal',
        'size'   : 12}
import matplotlib
matplotlib.rc('font', **font)
import matplotlib.pyplot as plt


def f(x, m, b):
    return m*x+b

def linearize(x, y, ax, label = None, color = None):
    popt, pcov = curve_fit(f, x, y)
    perr = np.sqrt(np.diag(pcov))
    ((m, b), (merr, berr)) = popt, perr
    print(roundwitherror(m, merr), roundwitherror(b, berr))
    X = np.linspace(np.min(x), np.max(x))
    ax.plot(X, f(X, m, b),color = color, lw = 0.5, 
                           label = "f = mx+b, m = %.4g \u00b1 %.4g,\nb = %.4g \u00b1 %.4g" % 
                           (*roundwitherror(m, merr), *roundwitherror(b, berr)))
    

    #return popt, perr



def killchars(s, chars):
    for char in chars:
        ss = s.split(char)
        S = ""
        for i in ss:
            S += i
        s = S
    return s

def listifyString(s, delimiter, ignorePercent = True):
    if len(s) == 0:
        return [0]
    else:
        s = killchars(s, ("[", "]", "(", ")"))
        L = []
        for i in s.split(delimiter):
            if "%" in i:
                L.append(str(i))
            else:
                L.append(float(i))
        return L

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return m.ceil(n * multiplier) / multiplier #das ist alles nur geklaut-von den prinzen(aus dem internetz)

def getdecimals(x):
    X = str(x).strip("[]")
    if "e" in X:
        a, b = X.split("e")
        return -int(b)
    elif "." in X:
        a, b = X.split(".")
        if float(a) != 0:
            return 1-len(a)
        if float(a) == 0:
            i = 0
            while float(b[i]) == 0:
                i+=1
            return i+1
    elif X.isnumeric():
        return -len(X)

def roundwitherror(x,err):
    if type(x) == list and len(x) == 1:
        x = x[0]
    if type(err) == list and len(err) == 1:
        err = err[0]

    if err == 0:
        return x, 0
    else:
        k = err*(10**(getdecimals(err)))
        
        
        if k < 3:
            rerr = round_up(err,(getdecimals(err)+1))
            rx = round(x,getdecimals(rerr)+1)
        else:
            rerr = round_up(err, (getdecimals(err)))
            rx = round(x, getdecimals(rerr))
        return rx, rerr

def pop_arg(args, xarg): #this might be useless at this point
    for arg in args.split(","):
        if xarg in arg:
            args.remove(arg)
    return args #maybe just remove this shit

def get_slope(function, allargs, xarg, tolerance = 0.000001): # die partielle ableitung von function mit den argumenten args nach xarg an der stelle xarg
    #args = pop_arg(allargs, xarg)#stellt sich heraus dass das total unnötig war
    args = allargs
    dx =  1
    slope_last = ((calc_custom_func(function,str(args)+","+str(xarg)+"+"+str(dx)))-(calc_custom_func(function,str(args)+","+str(xarg)+"-"+str(dx))))/(2*dx)
    dx *= 0.1
    slope_new = ((calc_custom_func(function,str(args)+","+str(xarg)+"+"+str(dx)))-(calc_custom_func(function,str(args)+","+str(xarg)+"-"+str(dx))))/(2*dx)
    while abs(slope_new-slope_last)> tolerance:
    	slope_last = slope_new
    	dx *= 0.5
    	slope_new = ((calc_custom_func(function,str(args)+","+str(xarg)+"+"+str(dx)))-(calc_custom_func(function,str(args)+","+str(xarg)+"-"+str(dx))))/(2*dx)
    return slope_new

def find_minimum(function, allargs, xarg, tolerance = 0.001, right_bound = 10, left_bound = -10):
    if right_bound and left_bound != 0:
        interval = (right_bound - left_bound)/2
        x_min = right_bound
    while interval > tolerance:
        new_slope = get_slope(function, allargs, str(xarg)+"="+str(x_min), 0.001)
        if new_slope < 0:
            x_min += interval
            interval /= 2
        if new_slope > 0:
            x_min -= interval
            interval /= 2
        #print(x_min)
    return x_min

def calc_custom_func(function, args):
    for arg in args.split(","):
        exec(arg)
    return eval(function)

def error_calc(function, values):#values is of type dict, with a real value and an error attached###values should be handled through a list of dicts, each entry representing one set of corresponding values.
    error = 0#alt und scheisse
    keys = values.keys()
    vals = []
    errs = []
    for key in keys:
        if "delta_" not in key:
            vals.append(key)
        if "delta_" in key:
            errs.append(key)
    allargs = ""
    for val in vals:
        arg = str(val)+"="+str(values[val])+","
        allargs += arg

    for val in vals:
        xarg = str(val)+"="+str(values[val])
        xerrkey = "delta_"+str(val)
        error += get_slope(function, allargs, xarg)*values[xerrkey]
    trueval = calc_custom_func(function, allargs)
    return trueval, error

def new_error_calc(function, values): #function is of type string. something like "m*v**2". while values is a dictionary of lists {"m":[34,6], "v":[3,1]}
    error = 0
    keys = values.keys()
    args = ""
    for key in keys:
        args += str(key)+"="+str(values[key][0])+","
    trueval = calc_custom_func(function, args)
    for key in keys:
    	error += abs(get_slope(function, args, str(key)+"="+str(values[key][0]))*values[key][1])
    return trueval, error

"""#legacy version of this function without input listification and generally worse overall.
def listErrorCalc(data, function):
    result = [[], []]
    keys = data.keys()
    lens = []
    for key in keys:
    	if type(data[key][0]) == list or tuple:
        	lens.append(len(data[key][0]))
    	if type(data[key][0]) == list or tuple:
        	lens.append(len(data[key][1]))
    
    i = 0
    while i < min(lens): #die bedingung muss erst noch geschaffen werden.
        d = {}
        for key in keys:
            d[key] = [data[key][0][i], data[key][1][i]]
        x, xerr = new_error_calc(function, d)
        result[0].append(x)
        result[1].append(xerr)
        i += 1
    return result
"""

def listErrorCalc(data, function, roundput = False): #i know most of my annotations are troll-bullshit that helps nobody but this ain't NASA so i can do whatever the fuck i want motherfucker
    data = listifyData(data)
    result = [[], []]
    keys = data.keys()
    lens = []
    indexdict = {}
    for key in keys:
        indexdict[key] = [0, 0]
        t = type(data[key][0]) 
        if t == list or t == tuple:#this still need cleaning up
            lens.append(len(data[key][0]))
            indexdict[key][0] = len(data[key][0])
        elif t == int or t == float:
            lens.append(1)
            indexdict[key][0] = 1
        else:
            print("Type error in list conversion")
        t = type(data[key][1])
        if t == int or t == float:
            lens.append(1)
            indexdict[key][1] = 1
        elif t == list or t == tuple:
            lens.append(len(data[key][1]))
            indexdict[key][1] = len(data[key][1])
        else:
            print("Type error in list conversion")
    j = max(lens)
    for key in keys:    #this makes it so that lists of different lenghts are stretched to accomodate eachother. constants are now possible by just typing them and leaving them as is
        indexdict[key][0] = [indexdict[key][0]/j, 0]#fick dich python du schlange dafür dass du tuple mit len(t) = 1 zu int umfickst
        indexdict[key][1] = [indexdict[key][1]/j, 0]#oh gott dieser käse mit den indizes fliegt mir noch um die ohren...
    i = 0
    while i < max(lens): #die bedingung muss erst noch geschaffen werden.
        d = {}
        for key in keys:
            d[key] = [
            data[key][0][ int(indexdict[key][0][1]) ], 
            data[key][1][ int(indexdict[key][1][1]) ] 
            ] #tut er schon
        if roundput == 0:
            x, xerr = new_error_calc(function, d)
        if roundput == 1:
            x, xerr = roundwitherror(*new_error_calc(function, d))
        result[0].append(x)
        result[1].append(xerr)
        i += 1
        for key in keys:#jeden listenindex um das korrespondierende inkrement erhöhen
            indexdict[key][0][1] += indexdict[key][0][0]
            indexdict[key][1][1] += indexdict[key][1][0]
    return result
        
def roundList(X):
    Y = [[], []]
    i = 0
    while i < len(X[0]):
        a, b = roundwitherror(X[0][i], X[1][i])
        Y[0].append(a)
        Y[1].append(b)
    return Y
#lmao ima l33t haxxor xd
def listifyData(data): #this is the price you pay for soft-typed languages. 
    for d in data:  #sanitize your input and wash yo ass
        t = type(data[d])
        if t == list:
            pass
        elif t == tuple:
            data[d] = list(data[d])
        elif t == int or float:
            data[d] = [data[d], 0]
        for i in (0, 1):
            t = type(data[d][i])
            if t == list:
                pass 
            elif t == tuple:
                data[d][i] = list(data[d][i])
            elif t == int or float:
                data[d][i] = [data[d][i]]
    return data     #i am a literal god

def linf(x, m, b):
    return m*x+b

def linPlot(dat, xName, yName, xLabel, yLabel, color = "b", label = None, title = None, fit = True):
    x, xerr, y, yerr = dat[xName][0], dat[xName][1], dat[yName][0], dat[yName][1]
    print(dat)
    dat = listifyData(dat)
    print(dat)
    popt, pcov = curve_fit(linf, x, y)
    perr = np.sqrt(np.diag(pcov))
    plt.errorbar(x = x, xerr = xerr, y = y, yerr = yerr, capsize = 2, elinewidth = 1, lw = 0, color = color, label = label)
    X = np.arange(min(x), max(x), (max(x) - min(x))/100)
    m ,merr, b, berr = popt[0], perr[0], popt[1], perr[1]
    if fit == True:
        plt.plot(X, linf(X, m, b), color = color, lw = 0.7, label = "f = mx+b, m = %.4g \u00b1 %.4g, b = %.4g \u00b1 %.4g" % (*roundwitherror(m, merr), *roundwitherror(b, berr)))
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()

def expf(x, k, a):
    return a*(1-k**(-x))

def expPlot(dat, xName, yName, xLabel, yLabel, color = "b", label = None, title = None, fit = True):
    x, xerr, y, yerr = dat[xName][0], dat[xName][1], dat[yName][0], dat[yName][1]
    print(dat)
    dat = listifyData(dat)
    print(dat)
    popt, pcov = curve_fit(expf, x, y)
    perr = np.sqrt(np.diag(pcov))
    plt.errorbar(x = x, xerr = xerr, y = y, yerr = yerr, capsize = 2, elinewidth = 1, lw = 0, color = color, label = label)
    X = np.arange(min(x), max(x), (max(x) - min(x))/100)
    k ,kerr, a, aerr = popt[0], perr[0], popt[1], perr[1]
    if fit == True:
        plt.plot(X, expf(X, k ,a), color = color, lw = 0.7, label = "f = a*(1-k**(-x)), k = %.4g \u00b1 %.4g, a = %.4g \u00b1 %.4g" % (*roundwitherror(k, kerr), *roundwitherror(a, aerr)))
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()




def pre(x, xerr): #pretty error rounding
    print(x)
    print(xerr)
    h = getdecimals(xerr)
    g = getdecimals(x)
    x, xerr = roundwitherror(x, xerr)
    s = killchars(str(xerr).split("e")[0], (".", "0"))
    if str(x).split(".")[1] == "0":
        x = int(x)
    if g < h:
        x = str(x)+("0"*(h-g))
    return "%s(%s)" % (x, s)




def paste2clip(x, err):
    i = 0
    paste = ""
    while i < len(x):
        if i == len(x) - 1:
            paste += str(x[i])+"\t"+str(err[i])
        else:
            paste += str(x[i])+"\t"+str(err[i])+"\n"
        i += 1
    ppc.copy(paste)
    return "pasted"
        
    


"""
example for the use of the function listErrorCalc:

the first input value will be of type dict and will have the structure
data[variable_name][[x1, x1, and so on...], [xerr1, xerr2, and so on...]]
so a list consisting of two lists which will contain a value and its error at similar indices.
for constants, brackets may be omitted as the function will map shorter lists with less entries to longer lists with more entries by 
iterating  on the entries in those list more slowly. 

the second input valie will be of type string and should contain the formula to be applied to the data in a shape recognizable by python.
trigonometric and other common mathematical functions need not be specifically named of imported since they're already imported by default
withing this module. 

the function returns a list of two lists which are the calculated values and their errors and similar indeces. 
so an example of using the function in practice may look like this:
data = {"var1":[[x1, x2, and so on... ], [xerr1, xerr2, and so on... ]], "var2":((y1, y2, and so on... ), (yerr1, yerr2, and so on...))}
formula = "var1/var2"
data["newvar"] = listErrorCalc(data, formula)
"""



