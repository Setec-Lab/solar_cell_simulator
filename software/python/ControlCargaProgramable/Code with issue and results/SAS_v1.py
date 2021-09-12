import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import math
import controller
import time

sizeArray = 1024

serial = 2
parallel = 3

InputIsc = 0.5196*parallel
InputImp = 0.5029*parallel
InputVmp = 2.409*serial
InputVoc = 2.690*serial
InputVoc_Tcomp = 0
InputVmp_Tcomp = 0
InputPcos = 1
InputT = 0


def scalevars(voc_tcomp, vmp_tcomp, pcos, voc, vmp, imp, isc, t):
    sVoc = voc - (t * voc_tcomp)
    sVmp = vmp - (t * vmp_tcomp)
    sImp = pcos * imp
    sIsc = pcos * isc
    return sVoc, sVmp, sImp, sIsc


sVoc, sVmp, sImp, sIsc = scalevars(InputVoc_Tcomp, InputVmp_Tcomp, InputPcos, InputVoc, InputVmp, InputImp, InputIsc,
                                   InputT)


def generate_table(Voc, Vmp, Imp, Isc):
    Rs = (Voc - Vmp) / Imp
    a = (Vmp * (1 + (Rs * Isc) / Voc) + Rs * (Imp - Isc)) / Voc
    N = math.log10(2 - 2 ** a) / math.log10(Imp / Isc)
    i = np.zeros(sizeArray)
    v = np.zeros(sizeArray)
    r = np.zeros(sizeArray)
    for x in range(0, sizeArray):
        I = (x * Isc) / (sizeArray - 1)
        V = Voc * math.log10(2 - ((I / Isc) ** N))
        V = V / math.log10(2)
        V = V - Rs * (I - Isc)
        V = V / (1 + ((Rs * Isc) / Voc))
        P = V * I
        v[x] = V
        i[x] = I
        if I == 0:
            r[x] = 10000
        else:
            r[x] = V / I

    return v, i, r

def VoltageInterpolation(tableVoltage, tableCurrent, inputVoltage):
    for i in range(0, sizeArray-1):
        if inputVoltage > tableVoltage[i]:
            iOut = tableCurrent[i] + (tableCurrent[i+1]-tableCurrent[i])*(inputVoltage-tableVoltage[i])/(tableVoltage[i+1]-tableVoltage[i])
            break
    return iOut

def CurrentInverseInterpolation(tableVoltage, tableCurrent, inputCurrent):
    for i in range(0, sizeArray-1):
        if inputCurrent < tableVoltage[i]:
            vOut = tableVoltage[i]+(tableVoltage[i+1]-tableVoltage[i])*((inputCurrent - tableCurrent[i])/(tableCurrent[i+1]-tableCurrent[i]))
            break
    return vOut

def ResistanceInterpolation(tableResistance, tableCurrent, inputResistance):
    for i in range(0, sizeArray-1):
        if inputResistance>tableResistance[i] or i==1022 :
            iOut = tableCurrent[i] + (tableCurrent[i+1]-tableCurrent[i])*(inputResistance-tableResistance[i])/(tableResistance[i+1]-tableResistance[i])
            break
    return iOut

def CalculateResistance(Vsens, Isens):
    if Isens != 0 :    
        return Vsens/Isens
    else :
        print("error, I = 0")
        return 0

def writeInNotepad(time, counter, vc, ic, rc, vm, im, rm):
    file.write("\n")
    file.write(str(time))
    file.write(",")
    file.write(str(counter))
    file.write(",")
    file.write(str(vc))
    file.write(",")
    file.write(str(ic))
    file.write(",")
    file.write(str(vc/ic))
    file.write(",")
    file.write(str(vm))
    file.write(",")
    file.write(str(im))
    file.write(",")
    file.write(str(vm/im))
    print("File updated")


#define arrays 
v, i, r = generate_table(sVoc, sVmp, sImp, sIsc)

#connect to programmable load
print("connecting to programmable generator and load")
rm = pyvisa.ResourceManager()
fuente = rm.open_resource(rm.list_resources()[0])
#carga = rm.open_resource(rm.list_resources()[0])
Fuente = controller.Fuente(fuente, "Fuentesita")
#Carga = controller.Carga(carga, "carguita")
print(fuente.query("*IDN?"))
#print(carga.query("*IDN?"))
print("Connected")
time.sleep(2)


#round sIsc and sVoc
sIsc = round(sIsc, 2)
sVoc = round(sVoc, 2)

# Turn on power output and setting it to CV 
print("Max values: {}V {}A".format(sVoc, sIsc))
print(Fuente.aplicar_voltaje_corriente(1, sVoc, sIsc))
print(Fuente.encender_canal(1))
time.sleep(2)

#Turn on power load and set to 2ohms


voltage = 0
current = 0
resistance = 0
power = 0
outputV = 0
outputI = 0
loadResistance = 2
loadVoltage = 0
loadCurrent = 0

boost = 0
counter = 0

#open a file
file = open("SAS_Resistance_IV_Curve.txt", "w")
file.write("This notepad takes measurements from the generator and then the load")
file.write("\nTime,Counter,Vc,Ic,Rc,Vm,Im,Rm")

#Setting up timer and counter
inicio = time.time()
tiempo = time.time()

while counter <= 20:
    
    initialLoopTime = time.time()
    
    
    #Measuring V and I outputed by the generator
    voltage, current, power = Fuente.medir_todo(1)
    resistance = round(CalculateResistance(voltage, current), 2)
    print("Measured values: {}V {}A {}W {}R".format(voltage, current, power, resistance))

    if (power != 0):
        #using interpolation functions to find correct I and V according to IV curve
        outputI = round(ResistanceInterpolation(r, i, resistance), 2)
        outputV = round(CurrentInverseInterpolation(v, i, outputI),2)

        #updating V and I output values
        print("Values to output: {}V. {}A".format(outputV, outputI))
        Fuente.aplicar_voltaje_corriente(1, outputV, outputI)

        #set boost to 0 because we do not need to bosst signal to sVoc and sIsc
        boost = 0
        
    elif (power == 0 and boost != 2):
        #if power is 0 we re-output Isc and Voc 2 times before we assume that the load was removed
        boost += 1
        print("Power = 0! Rebooting {}".format(boost))
        print(Fuente.aplicar_voltaje_corriente(1, sVoc, sIsc))
        time.sleep(2)
    else :
        print("Load was removed from generator")
        break

    #uptdate notepad 
    writeInNotepad(time.time()-inicio, counter, outputV, outputI, 0, voltage, current, 0)
    print("time elapsed in loop: {}s".format(time.time() - initialLoopTime))
    print()
    print()

    

    

    #update counter and wait to not overload generator
    time.sleep(2)
    counter += 1
    

elapsado = time.time() - inicio
print("Time elapsed: {}".format(elapsado))
print(Fuente.apagar_canal(1))
file.close()
