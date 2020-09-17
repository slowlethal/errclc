import sympy as sp
from IPython.display import display, Math, Latex

#Hier die Variablen deklarieren/ "d" ist reserviert und darf nicht verwendet werden
h,r,T = sp.symbols('h r T') #hier Eure Variablennamen einsetzen
variablen = [h,r,T]         #hier Eure Variablennamen einsetzen
#Zahlenwerte und Fehlerwerte
variablen_werte = [2.8,4.2,2.4]  #Werte h=2.8, r=4.2, T=2.4 /hier Eure Werte einsetzen
fehler_werte = [0.3,0.2,0.1]     # dito fuer die Fehler /hier Eure Werte einsetzen

""""
Hier die Funktion deklarieren
Potenzen a hoch b: a**b
bei Funktionen wie sin, sqrt, etc. den Namensraum "sp" vorransetzen z.B. sp.sin()"""

funktion = (h*r**2*sp.sqrt(T))

fehler = 0
fehlersymbole=[]
ableitungen_quadr = []

for var in variablen:
    d = sp.symbols('d' + var.name)        #Symbole fuer die Fehler generieren
    fehlersymbole.append(d)               #Fehlersymbole in Liste eintragen
    partial = sp.diff(funktion, var) * d  #Partielle Differentation und mit mit Fehlersymbol 'd' multiplizieren
    ableitungen_quadr.append(partial**2)  
    fehler = fehler + partial**2

fehler_abs=sp.simplify(sp.sqrt(fehler))              #Latex Format fuer den absoluten Fehler
fehler_rel=sp.simplify(sp.sqrt(fehler/funktion**2))  #Latex Format fuer den relativen Fehler

#Berechnung der Zahlenwerte
funktions_wert=sp.Subs(funktion,variablen,variablen_werte).doit() #Variablenwerte (Zahlen) in Formel einsetzen und
                                                                  #Funktionswert berechnen
err1=sp.Subs(fehler,variablen,variablen_werte).doit()             #Variablenwerte (Zahlen) in FehlerFormel einsetzen 

err2=sp.Subs(err1,fehlersymbole,fehler_werte).doit()              #Variablenwerte (Zahlen) in FehlerFormel einsetzen und
                                                                  #Funktionswert berechnen

                                                                  #Latex Darstellungen
print('Funktion:')
display(Math("f="+sp.latex(funktion)))

print('Messwerte:')
for i in range(len(variablen)):
    display(Math(str(variablen[i])+'='+ str(variablen_werte[i])+'\pm '+ str(fehler_werte[i])))  #Messwerte mit Fehler

print('Absoluter Fehler:')
display(Math(r'\Delta f='+sp.latex(fehler_abs).replace('d',r'\Delta ')))   #Formel absoluter Fehler
print('Relativer Fehler:')
display(Math(r"\Delta f/f="+sp.latex(fehler_rel).replace('d',r'\Delta '))) #Formel relativer Fehler
display(Math("f= %6.2f \pm %6.2f" %(funktions_wert,sp.sqrt(err2))))        #Messwert und Wert des absoluten Fehler
display(Math("f= %6.2f \pm %6.1f %s" %(funktions_wert,sp.sqrt(err2)/funktions_wert*100," \%"))) #dito als relativer Fehler




