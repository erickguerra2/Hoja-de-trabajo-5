###############################################################
#   Programador: Erick Guerra; gue23208@uvg.edu.gt
#   Nombre del programa: simulaciones.py
#   Lenguaje: python 3.9.13
#   Fecha de finalización: 27/02/2024
#   
#  Recursos: Ejemplos en la plataforma y vistos en clase.
#            Internet e inteligencia artificial
#
###############################################################

import simpy
import random

class simulacion:
    def __init__(self, dato, numero, memoria, instru, RAM):
        self.dato = dato
        self.numero = numero
        self.memoria = memoria
        self.instru = instru
        self.RAM = RAM
        self.action = dato.process(self.procesos(self.dato, self.memoria, self.instru))

    def procesos(self, dato, memoria, instru):
        global completados
        with RAM.get(memoria) as req:
            yield req
            print(f"el proceso {self.numero} entro a ready a las {dato.now:7.4f} y se le asigno {memoria} en la RAM")

        while instru > 0:
            i = 0
            bandera1 = True
            while i < instru and i < 3:
                print(f"el proceso {self.numero} tiene {instru} instruccion y van: {dato.now:7.4f}")
                instru -= 1
                i += 1
                yield dato.timeout(1)
                if instru == 0:
                    completados += 1
                    print(f'{dato.now}: Proceso {self.numero} a terminado: {dato.now:7.4f}')
                    RAM.put(memoria)  
                    bandera1 = False
                    break
            if bandera1:
                bandera2 = random.randint(1, 2)
                if bandera2 == 1: 
                    print(f'El proceso {self.numero} entro en')
                    yield dato.timeout(1)  
                    print(f'El proceso {self.numero} finalizo el proceso')
                elif bandera2 == 2:
                    print(f'El proceso {self.numero} ingreso a ready: {dato.now:7.4f}')

def nuevo(dato, inter, procesos):
    global completados
    global numeroproc
    numeroproc = 0
    for i in range(int(procesos)):
        yield dato.timeout(inter)
        numeroproc += 1  
        memoria = random.randint(1, 10)
        instru = random.randint(1, 10)
        if RAM.level >= memoria: 
            print(f"el proceso {numeroproc} inicio: {dato.now:7.4f}")
            simulacion(dato, f'Proceso-{numeroproc}', memoria, instru, RAM)
            yield dato.timeout(1)
        else:
            print(f'{dato.now}: No hay memoria RAM disponible para realizar el proceso {numeroproc}.')

inter = random.expovariate(1/10)
random.seed(100)  
dato = simpy.Environment() 
CPU = simpy.Resource(dato, capacity=3) 
RAM = simpy.Container(dato, init=100, capacity=200) 
completados = 0  # numeroero de procesos completados
numeroproc = 0


procesos = input()
if procesos.isdigit():
    resultado = dato.process(nuevo(dato, inter, procesos))
    dato.run(until=resultado)
