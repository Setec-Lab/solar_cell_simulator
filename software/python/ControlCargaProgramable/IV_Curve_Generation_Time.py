import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import math
import controller
import time


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

nbPoints = 35840
nbIteration = 10000
timeTable = np.array([0.0]*nbIteration)



def scalevars(voc_tcomp, vmp_tcomp, pcos, voc, vmp, imp, isc, t):
    sVoc = voc - (t * voc_tcomp)
    sVmp = vmp - (t * vmp_tcomp)
    sImp = pcos * imp
    sIsc = pcos * isc
    return sVoc, sVmp, sImp, sIsc





def generate_table_methode1(Voc, Vmp, Imp, Isc, sizeArray):

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


initialTime = 0
finalTime = 0
for a in range(0,nbIteration) :
    #start clock
    initialTime = time.time()
    #start computing
    sVoc, sVmp, sImp, sIsc = scalevars(InputVoc_Tcomp, InputVmp_Tcomp, InputPcos, InputVoc, InputVmp, InputImp, InputIsc,
                                   InputT)
    v, i, r = generate_table_methode1(sVoc, sVmp, sImp, sIsc, nbPoints)
    #computing is finished
    finalTime = time.time() - initialTime
    #Record overall time
    timeTable[a] = finalTime

#calculate average time 
s = 0;
for a in range(0, len(timeTable)):
    s = s + timeTable[a]
s = s/nbIteration

print("number of iterations : " + str(nbIteration) + "number of points : " + str(nbPoints))
print("Average time is " + str(s))

#For method 1 - using formulas from repository
#for 1024 avg is 0.0012090672731399537s  (10000 iterations)
#for 2048 avg is 0.002367471432685852s  (10000 iterations)
#for 4096 avg is 0.00477643187046051s  (10000 iterations)
#for 15360 avg is 0.017930469632148744s  (10000 iterations)
#for 20480 avg is 0.024136067795753478s  (10000 iterations)
#for 20480 avg is 0.024136067795753478s  (10000 iterations)
#for 40960 avg is 0.04873370180130005s  (10000 iterations)
