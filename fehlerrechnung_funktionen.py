"""
module containing the functions used in the main app errclc.py
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

def f(x, m, b):
    return m*x+b

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
