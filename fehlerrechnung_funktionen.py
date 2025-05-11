"""
module containing the functions used in the main program errclc.py
mainly the functions are used to calculated tangent slopes numerically on n-dimensional
surfaces


example for the use of the function list_error_calc:

the first input value will be of type dict and will have the structure
data[variable_name][[x1, x1, and so on...], [xerr1, xerr2, and so on...]]
so a list consisting of two lists which will contain a value and its error at similar indices.
for constants, brackets may be omitted as the function will map shorter lists with less entries to
longer lists with more entries by
iterating  on the entries in those list more slowly.

the second input valie will be of type string and should contain the formula to be applied to the
data in a shape recognizable by python.
trigonometric and other common mathematical functions need not be specifically named of imported
since they're already imported by default
withing this module.

the function returns a list of two lists which are the calculated values and their errors and
similar indeces.
so an example of using the function in practice may look like this:
data={"var1":[[x1, x2, and so on... ], [xerr1, xerr2, and so on... ]],
"var2":((y1, y2, and so on... ), (yerr1, yerr2, and so on...))}
formula="var1/var2"
data["newvar"]=list_error_calc(data, formula)
"""
import matplotlib.pyplot as plt
import math as m
from math import sin, cos, tan, asin, acos, atan, exp, e, pi, log
import numpy as np
from scipy.optimize import curve_fit
from sympy import *
import json
"""
font={'family' : 'normal', 'weight' : 'normal','size':12}

font = {'weight':'normal', 'size':12}
"""
"""
def NIST_replace(t):
    read = open("allascii.txt", "r")
    consts_raw = read.read()
    read.close()
    c = consts_raw.split("\n")
    NIST = {}
    for N in c[12:365]:
        NIST[str(N[0:60].strip())] = [float(N[60:85].strip().replace(" ", "").replace("...", "")),
        float(N[60:85].strip().replace(" ", "").replace("(exact)", "0").replace("...", "")),
        str(N[110:].strip().replace(" ", ""))]
    important_keys = []
    i = int(t.count("#")/2)
    l = str(" "+t).split("#")
    j = 0
    while j < i :
        s1 = str("#"+l[2*j+1]+"#")
        t = t.replace(s1, str(NIST[l[2*j+1]][0]))
        j += 1
    return t
"""

def load_json(filepath):
    with open(filepath) as f:
        const_json = f.read()
        f.close()
    constants = json.loads(const_json)
    return constants

def NIST_replace(t):
    constants = load_json("./constants.json")
    #print(constants["!c"])
    for key in constants.keys():
        t = t.replace("!%s"%key, constants[key])
    return t

def add_consts_to_data(data,function):
    constants = load_json("./constants.json")
    #print(constants["!c"])
    for key in constants.keys():
        #print(key)
        if "!%s"%key in function:
            C = constants[key]
            print("NIST-constant %s detected! substituting value..."%key)
            if C[1] == "0":
                function = function.replace("!%s"%key, C[0])
            else:
                data["!%s"%key] = [float(C[0]), float(C[1])]
    return data, function

def eat_string(mainstring, substrings):
    constants = load_json("./constants.json")

    for s in substrings:
        mainstring = mainstring.replace(s, "")
    for operator in ("*", "+", "-", "/"):
        mainstring = mainstring.replace(operator, "")
    for const in constants.keys():
        mainstring = mainstring.replace("!%s"%const, "")
    print(mainstring)
    if mainstring == "":
        return True
    else:
        return False





def f(x, m, b):
    return m*x+b

def fitAndPlot(x_data, Y, ax=None, f=f, function="m*x+b", label=None, color=None):
    """
    function fits data to a given functionen using scipy.optimize.curve_fit and plots that data to
    a given axis.
    """
    x, xerr, y, yerr = *x_data, *Y
    popt, pcov = curve_fit(f, x, y)
    coef = np.transpose(np.array((popt, np.sqrt(np.diag(pcov)))))
    vString = ", "
    i = 1
    for co in coef:
        vString += "a_%s=%.4g \u00b1 %.4g\n" % (i, *roundwitherror(*co))
        i += 1
    x_data = np.linspace(np.min(x), np.max(x))
    plt.errorbar(x=x, xerr=xerr, y=y, yerr=yerr, capsize=2, elinewidth=1, lw=0)
    plt.plot(x_data, f(x_data, *popt), color=color, lw=0.6, label=function + vString)
    plt.legend()
    plt.show()
    #return popt, perr

def linearize(x, y, ax, label=None, color=None):
    popt, pcov = curve_fit(f, x, y)
    perr = np.sqrt(np.diag(pcov))
    ((m, b), (merr, berr)) = popt, perr
    x_data = np.linspace(np.min(x), np.max(x))
    ax.plot(x_data, f(x_data, m, b), color=color, lw=0.5, label="""f=mx+b, m=%.4g \u00b1 %.4g,
        \nb=%.4g\u00b1 %.4g""" %  (*roundwitherror(m, merr), *roundwitherror(b, berr)))
    #return popt, perr

def killchars(s, chars):
    """
    removes the characters in chars from a string s and returns that string again.
    """
    for char in chars:
        ss = s.split(char)
        S = ""
        for i in ss:
            S += i
        s = S
    return s

def listifyString(s, delimiter, ignorePercent=True):
    """
    takes a string which is assumed to have multiple semi-numerical elements within it
    and separates them according to the given delimiter
    """
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
    """
    rounds a number up to a given degree of decimals
    """
    multiplier = 10 ** decimals
    return m.ceil(n * multiplier) / multiplier
    #das ist alles nur geklaut-von den prinzen(aus dem internetz)

def getdecimals(x):
    """
    returns the number of decimal places within a number, orders of magnitude over
    1 i.e. 10, 100, 1000
    will be returned as a negative number of decimal accuracy
    """
    i = 0
    while not (x >= 1 and x < 10):
        if x >= 10:
            i -= 1
            x /= 10
        if x < 1:
            i += 1
            x *= 10
    return i

def roundwitherror(x, err):
    """
    rounds a number with a given error to the precision of that error, after it has rounded
    the error up
    """
    if isinstance(x, list) and len(x) == 1:
        x = x[0]
    if isinstance(err, list) and len(err) == 1:
        err = err[0]
    if not isinstance(err, (int, float, np.int64, np.float64)):
        return x, err
    elif err == 0:
        return x, 0
    elif err == np.inf:
        return x, err
    else:
        k = err*(10**(getdecimals(err)))
        if k < 3:
            rerr = round_up(err, (getdecimals(err)+1))
            rx = round(x, getdecimals(rerr)+1)
        else:
            rerr = round_up(err, (getdecimals(err)))
            rx = round(x, getdecimals(rerr))
        return rx, rerr

def pop_arg(args, xarg): #this might be useless at this point
    """
    deprecated legacy module from old version
    """
    for arg in args.split(","):
        if xarg in arg:
            args.remove(arg)
    return args #maybe just remove this shit

def get_slope(function, allargs, xarg, tolerance=0.000001):
    """
    die partielle ableitung von function mit den argumenten args nach xarg an der stelle xarg
    args=pop_arg(allargs, xarg)#stellt sich heraus dass das total unnötig war
    returns the slope of the function with respect to the given argument at the given point allargs
    """
    args = allargs
    dx = 1
    slope_last = (
        (calc_custom_func(function, "%s,%s+%s)"%(args, xarg, dx)))-
        (calc_custom_func(function, "%s,%s-%s)"%(args, xarg, dx)))
        )/(2*dx)
    dx *= 0.5
    slope_new = (
        (calc_custom_func(function, "%s,%s+%s)"%(args, xarg, dx)))-
        (calc_custom_func(function, "%s,%s-%s)"%(args, xarg, dx)))
        )/(2*dx)
    #print(slope_new-slope_last)
    while abs(slope_new-slope_last) > tolerance:
        #print(slope_new-slope_last)
        slope_last = slope_new
        dx *= 0.5
        slope_new = (
            (calc_custom_func(function, "%s,%s+%s)"%(args, xarg, dx)))-
            (calc_custom_func(function, "%s,%s-%s)"%(args, xarg, dx)))
            )/(2*dx)
    return slope_new

def find_minimum(function, allargs, xarg, tolerance=0.001, right_bound=10, left_bound=-10):
    """
    finds the minimum slope of the function
    """
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
    return x_min

def calc_custom_func(function, args):
    """
    executes a function which is given as a string, which has args as variables
    """
    #print("args: %s"%args)
    #print("function: %s"%function)
    #print(args.split(","))
    #print(args)
    xarg = args.split(",")[-1].split("=")
    
    function = function.replace(xarg[0], xarg[1])
    #print(xarg.split())
    #function = function.replace(xarg)
    for arg in args.split(","):
        #print(arg)
        #print(arg.split("="))
        ags = arg.split("=")
        function = function.replace(ags[0], ags[1])
        #print("test")
        #print("function %s"%function)
    return eval(function)

def error_calc(function, values):
    """
    values is of type dict, with a real value and an error attached
    values should be handled through a list of dicts, each entry representing one set of
    corresponding values.
    """
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
    allargs = allargs[:-1]
    for val in vals:
        xarg = str(val)+"="+str(values[val])
        xerrkey = "delta_"+str(val)
        error += get_slope(function, allargs, xarg)*values[xerrkey]
    trueval = calc_custom_func(function, allargs)
    return trueval, error

def new_error_calc(function, values):
    """
    function is of type string. something like "m*v**2".
    while values is a dictionary of lists {"m":[34,6], "v":[3,1]}
    """
    error = 0
    keys = values.keys()
    args = ""
    for key in keys:
        args += str(key)+"="+str(values[key][0])+","
    args=args[:-1]
    trueval = calc_custom_func(function, args)
    for key in keys:
        error += abs(get_slope(function, args, str(key)+"=("+str(values[key][0]))*values[key][1])
    return trueval, error

def new_new_error_calc(function, values, latex=False):
    """
    i have no earthly idea what the fuck i was trying to do here. i think it was about changing the way the expression is evaluated
    to use sympy instead of the botched, garbled string eval shit i'm doing right now but i never bothered to actually get it working
    i think. anyways i fixed the string bullshit so this is the way we're going here. all i wanna do is not have to do partial
    derivatives anymore. i just want to be happy.
    """
    function = parse_expr(function)
    args = function.args
    dargs = []
    for arg in args:
        exec("%s=symbols('%s')" % (str(arg), str(arg)))
        exec("Delta_%s=symbols('Delta_%s')" % (str(arg), str(arg)))
        dargs.append("Delta_%s" % arg)
    D = 0
    for arg in args:
        D += diff(function, arg)*dargs[args.index(arg)]
    for arg in args:
        D = D.subs(arg, values[str(arg)][0]).subs(dargs[args.index(arg)], values[str(arg)][1])
    error = function
    for arg in args:
        function = function.subs(arg, values[str(arg)][0])
    value = function
    return value, error








"""#legacy version of this function without input listification and generally worse overall.
def list_error_calc(data, function):
    result=[[], []]
    keys=data.keys()
    lens=[]
    for key in keys:
    	if type(data[key][0]) == list or tuple:
        	lens.append(len(data[key][0]))
    	if type(data[key][0]) == list or tuple:
        	lens.append(len(data[key][1]))
    
    i=0
    while i < min(lens): #die bedingung muss erst noch geschaffen werden.
        d={}
        for key in keys:
            d[key]=[data[key][0][i], data[key][1][i]]
        x, xerr=new_error_calc(function, d)
        result[0].append(x)
        result[1].append(xerr)
        i += 1
    return result
"""

def list_error_calc(data, function, roundput=False):
    """
    i know most of my annotations are troll-bullshit that helps nobody but this
    ain't NASA so i can do whatever the fuck i want motherfucker
    ^^ i'll never get anywhere with that mindset LOL
    """
    #print(data)
    data, function = add_consts_to_data(data, function)
    data = listifyData(data)
    
    result = [[], []]
    keys = data.keys()
    lens = []
    indexdict = {}
    for key in keys:
        indexdict[key] = [0, 0]
        t = type(data[key][0])
        if t == list or t == tuple:
            #this still need cleaning up
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
    for key in keys:
        """this makes it so that lists of different lenghts are stretched to accomodate eachother.
        constants are now possible by just typing them and leaving them as is
        """
        indexdict[key][0] = [indexdict[key][0]/j, 0]
        #fick dich python du schlange dafür dass du tuple mit len(t)=1 zu int umfickst
        indexdict[key][1] = [indexdict[key][1]/j, 0]
        #oh gott dieser käse mit den indizes fliegt mir noch um die ohren...
    i = 0
    while i < max(lens): #die bedingung muss erst noch geschaffen werden.
        d = {}
        for key in keys:
            d[key] = [
                data[key][0][int(indexdict[key][0][1])],
                data[key][1][int(indexdict[key][1][1])]
            ] #tut er schon
            #print(d)
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

def roundList(x_data):
    """
    rounds an entire list of value-error-pairs using roundwitherror()
    """
    Y = [[], []]
    i = 0
    while i < len(x_data[0]):
        a, b = roundwitherror(x_data[0][i], x_data[1][i])
        Y[0].append(a)
        Y[1].append(b)
    return Y

def listifyData(data):
    """
    this is the price you pay for soft-typed languages.
    sanitize your input and wash yo ass
    """
    for d in data:
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

def plot_linear(dat, x_name, y_name, x_label, y_label, color="b", label=None, title=None, fit=True):
    x, xerr, y, yerr = dat[x_name][0], dat[x_name][1], dat[y_name][0], dat[y_name][1]
    dat = listifyData(dat)
    popt, pcov = curve_fit(linf, x, y)
    perr = np.sqrt(np.diag(pcov))
    plt.errorbar(
        x=x, xerr=xerr, y=y, yerr=yerr, capsize=2, elinewidth=1, lw=0, color=color, label=label
        )
    x_data = np.arange(min(x), max(x), (max(x) - min(x))/100)
    m, merr, b, berr = popt[0], perr[0], popt[1], perr[1]
    if fit:
        plt.plot(
            x_data, linf(x_data, m, b), color=color, lw=0.7,
            label="f=mx+b, m=%.4g \u00b1 %.4g, b=%.4g \u00b1 %.4g" %
            (*roundwitherror(m, merr), *roundwitherror(b, berr))
            )
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()

def expf(x, k, a):
    """
    a goddamn function, what else do you need to know?
    """
    return a*(1-k**(-x))

def plot_exponential(dat, x_name, y_name, x_label, y_label, color="b", label=None, title=None, fit=True):
    """
    creates a nice figure
    """
    x, xerr, y, yerr = dat[x_name][0], dat[x_name][1], dat[y_name][0], dat[y_name][1]
    dat = listifyData(dat)
    popt, pcov = curve_fit(expf, x, y)
    perr = np.sqrt(np.diag(pcov))
    plt.errorbar(x=x, xerr=xerr, y=y, yerr=yerr, capsize=2, elinewidth=1,
        lw=0, color=color, label=label)
    x_data = np.arange(min(x), max(x), (max(x) - min(x))/100)
    k, kerr, a, aerr = popt[0], perr[0], popt[1], perr[1]
    if fit:
        plt.plot(
            x_data, expf(x_data, k, a), color=color, lw=0.7,
            label="f=a*(1-k**(-x)), k=%.4g \u00b1 %.4g, a=%.4g \u00b1 %.4g" %
            (*roundwitherror(k, kerr), *roundwitherror(a, aerr))
            )
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()

def pre(x, xerr):
    """
    pretty error rounding
    returns properly formatted string to be used as a label in pyplot figure
    """
    h = getdecimals(xerr)
    g = getdecimals(x)
    x, xerr = roundwitherror(x, xerr)
    s = killchars(str(xerr).split("e")[0], (".", "0"))
    if str(x).split(".")[1] == "0":
        x = int(x)
    if g < h:
        x = str(x)+("0"*(h-g))
    return "%s(%s)" % (x, s)
