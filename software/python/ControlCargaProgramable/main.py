import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import math
import controller
import time

# MODOS DE CARGA:
# RES, CURR, VOLT, POW

# rm = pyvisa.ResourceManager()
# print(rm.list_resources())
#
# carga = rm.open_resource(rm.list_resources()[0])
# fuente = rm.open_resource(rm.list_resources()[1])
#
# print(fuente.query("*IDN?"))
#
# Fuente = controller.Fuente(fuente, "Fuentesita")
# Carga = controller.Carga(carga, "carguita")

InputIsc = 0.5196
InputImp = 0.5029
InputVmp = 2.409
InputVoc = 2.690
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
    i = np.zeros(1024)
    v = np.zeros(1024)
    r = np.zeros(1024)
    for x in range(0, 1024):
        I = (x * Isc) / 1023.0
        V = Voc * math.log10(2 - ((I / Isc) ** N))
        V = V / math.log10(2)
        V = V - Rs * (I - Isc)
        V = V / (1 + ((Rs * Isc) / Voc))
        P = V * I
        v[x] = V
        i[x] = I
        r[x] = V / I
    return v, i, r


v, i, r = generate_table(sVoc, sVmp, sImp, sIsc)


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

vout =

plt.plot(v, i)
plt.show()

# print(Fuente.aplicar_voltaje_corriente(1, 5, 1))
# print(Carga.fijar_funcion("RES"))
# print(Carga.fijar_resistencia(6))
# print(Carga.encender_carga())
# print(Fuente.encender_canal(1))
# time.sleep(7)
# print(Fuente.apagar_canal(1))
# print(Carga.apagar_carga())
