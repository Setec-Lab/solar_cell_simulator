import pyvisa
import numpy

#functions for power supply
class Fuente:  # Esta clase describe cada neurona
    def __init__(self, instrument, name=None):
        self.fuente = instrument
        self.name = name  # Nombre para identificar en depuracion

 #turn on channel
    def encender_canal(self, channel: int):
        self.fuente.write(":OUTPUT CH{:n},ON".format(channel))
        return self.fuente.query(":OUTP? CH{}".format(channel))

#turn off channel    
    def apagar_canal(self, channel: int):
        self.fuente.write(":OUTPUT CH{:n},OFF".format(channel))
        return self.fuente.query(":OUTP? CH{}".format(channel))

#apply voltage & current    
    def aplicar_voltaje_corriente(self, channel: int, voltaje: float, corriente: float):
        self.fuente.write(":APPLY CH{},{},{}".format(channel, voltaje, corriente))
        return self.fuente.query("APPLY? CH{}".format(channel))

#measure everything (in order returns: voltage, current and power)    
    def medir_todo(self, channel: int):
        medicion = self.fuente.query(":MEASURE:ALL?").split(",")
        medicion[-1] = medicion[-1][:-1]
        voltaje = medicion[0]
        corriente = medicion[1]
        potencia = medicion[2]
        return float(voltaje), float(corriente), float(potencia)

#functions for the electronic load    
class Carga:  # Esta clase describe cada neurona
    def __init__(self, instrument, name=None):
        self.carga = instrument
        self.name = name  # Nombre para identificar en depuracion

#set function : RES, CURR, VOLT, POW        
    def fijar_funcion(self, funcion: str):
        self.carga.write(":SOUR:FUNC {}".format(funcion))
        return self.carga.query(":SOUR:FUNC?")

#turn on load    
    def encender_carga(self):
        self.carga.write(":SOUR:INP:STAT 1")
        return self.carga.query(":SOUR:INP:STAT?")

#turn off load    
    def apagar_carga(self):
        self.carga.write(":SOUR:INP:STAT 0")
        return self.carga.query(":SOUR:INP:STAT?")

#set current only if you are on CC    
    def fijar_corriente(self, corriente: float):
        self.carga.write(":SOUR:CURR:LEV:IMM {}".format(corriente))
        return self.carga.query(":SOUR:CURR:LEV:IMM?")

#set voltage only if you are on CV    
    def fijar_voltaje(self, voltaje: float):
        self.carga.write(":SOUR:VOLT:LEV:IMM {}".format(voltaje))
        return self.carga.query(":SOUR:VOLT:LEV:IMM?")

#set resistance only if you are on CR    
    def fijar_resistencia(self, resistencia: float):
        self.carga.write(":SOUR:RES:LEV:IMM {}".format(resistencia))
        return self.carga.query(":SOUR:RES:LEV:IMM?")
    
#set resistance only if you are on CP (need to verify function)
    def fijar_potencia(self, resistencia: float):
        self.carga.write(":SOUR:POW:LEV:IMM {}".format(resistencia))
        return self.carga.query(":SOUR:POW:LEV:IMM?")    

