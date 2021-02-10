# -*- coding: utf-8 -*-
"""
PROYECTO DE TEORÍA DE COMUNICACIONES Y SEÑALES
Operaciones Básicas con Señales de secuencias x(n) y Señales de Audio

GRUPO:3CV5

AUTOR:
Velázquez Gen Josué Emmanuel

"""

import tkinter as tk
import sounddevice as sd
from scipy.io.wavfile import write
import wave
import simpleaudio as sa
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter.font as font
#Clase de operaciones
from Operaciones import *

"""------------------
    Globales
-----------------"""

ops = Operaciones()
operaciones=['Suma','Resta','Amplificación/Atenuación','Reflejo','Desplazamiento','Diezmación','Interpolación escalón',
             'Interpolación lineal','Convolución','FFT']
archivo='grabacion.wav'
archivoSalida='grabacionSalida.wav'

"""------------------
    Funciones
-----------------"""

def ocultarHn():
    lblHn.grid_forget()
    txtHn.grid_forget()
    lblHnOrigen.grid_forget()
    txtHnOrigen.grid_forget()
    
def mostrarHn():
    lblHn.grid(sticky="W",column=0,row=4,padx=(20,1))
    txtHn.grid(column=1,row=4,padx=(20,1))
    lblHnOrigen.grid(sticky="W",column=2,row=4,padx=(1,1))
    txtHnOrigen.grid(sticky="W",column=3,row=4,padx=(1,1))

def mostrarReproducirSalida():
    btnReproducirSalida.grid(column=2,row=9,padx=(1,1),columnspan=2,pady=(5,10))


def grabarAudio():
    try:
        fs = 20000
        seconds = 3
        grabacion = sd.rec(int(seconds * fs), samplerate=fs, channels=1,dtype=np.int16)
        sd.wait()
        write('grabacion.wav', fs, grabacion)
        tk.messagebox.showinfo(message="Éxito", title="Grabado con éxito")
    except Exception as e:
        print(e)
        tk.messagebox.showerror(message="Fallido", title="No se grabó, vuelve a intentarlo")
        
def reproducirAudio(archivo_audio):
    wave_obj = sa.WaveObject.from_wave_file(archivo_audio)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    
def calcular():

    global archivo
    #leyendo el archivo como arreglo
    if entradaSeleccionada.get()=="1":
        spf = wave.open(archivo, "r")
        senialOriginal = spf.readframes(-1)
        senialOriginal = np.frombuffer(senialOriginal, "int16")
        tiempo=np.arange(0,len(senialOriginal),1)
        valorLabel="Tiempo"
    else:
        senialOriginal=np.array([float(i) for i in txtSecuencia.get().split(",")])
        tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialOriginal)-(int(txtOrigen.get()))+1,1)])
        valorLabel="n"
    
    #gráfica de señal original
    fig = Figure(figsize=(4, 3), dpi=100)
    fig.add_subplot(111,title="Señal original",xlabel=valorLabel).plot(tiempo,senialOriginal)
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().grid(sticky="W",row=8,column=0,columnspan=2,padx=(20,1),pady=(20,20))
    op=-1;
    for o in range(len(operaciones)):
        if(operacion.get()==operaciones[o]):
            op=o
    calcularOperacion(senialOriginal,op)
        

def calcularOperacion(senialOriginal,op):
    senialDevuelta=np.array(1)
    if op==0:#Suma
        if entradaSeleccionada.get()=="1":
            senialDevuelta=ops.sumar(senialOriginal,senialOriginal)  
            tiempo=np.arange(0,len(senialDevuelta),1)
        else:
            senialHn=np.array([float(i) for i in txtHn.get().split(",")])
            if(int(txtHnOrigen.get())>int(txtOrigen.get())):
                senialOriginal=np.concatenate([np.zeros(abs(int(txtOrigen.get())-int(txtHnOrigen.get()))),senialOriginal])
            elif(int(txtHnOrigen.get())<int(txtOrigen.get())):
                senialHn=np.concatenate([np.zeros(abs(int(txtOrigen.get())-int(txtHnOrigen.get()))),senialHn])
                
            senialDevuelta=ops.sumar(senialOriginal,senialHn)
            tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get()))+1,1)])
    elif op==1:#Resta
        if entradaSeleccionada.get()=="1":
            senialDevuelta=ops.restar(senialOriginal,senialOriginal)   
            tiempo=np.arange(0,len(senialDevuelta),1)
        else:
            senialHn=np.array([float(i) for i in txtHn.get().split(",")])
            if(int(txtHnOrigen.get())>int(txtOrigen.get())):
                senialOriginal=np.concatenate([np.zeros(abs(int(txtOrigen.get())-int(txtHnOrigen.get()))),senialOriginal])
            elif(int(txtHnOrigen.get())<int(txtOrigen.get())):
                senialHn=np.concatenate([np.zeros(abs(int(txtOrigen.get())-int(txtHnOrigen.get()))),senialHn])   
            senialDevuelta=ops.restar(senialOriginal,senialHn)
            tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get()))+1,1)])
        
    elif op==2:#Amplificar
        senialDevuelta=ops.amplificar_atenuar(senialOriginal,float(txtFactor.get()))
        tiempo=np.arange(0,len(senialDevuelta),1)
        if(entradaSeleccionada.get()!="1"):
            tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get()))+1,1)])
    elif op==3:#Reflejar
        senialDevuelta=ops.reflejar(senialOriginal)
        tiempo=np.arange(0,len(senialDevuelta),1)
        if(entradaSeleccionada.get()!="1"):
            tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get()))+1,1)])
            tiempo=np.negative(tiempo)
            tiempo=np.flip(tiempo)
    elif op==4:#Desplazar
        senialDevuelta=ops.desplazar(senialOriginal,int(txtFactor.get()))
        tiempo=np.arange(0,len(senialDevuelta),1)
        if(entradaSeleccionada.get()=="1"):
            if(int(txtFactor.get())<0):
                #tiempo=np.arange(int(txtFactor.get()),len(senialDevuelta),1)
                senialDevuelta=np.concatenate([senialDevuelta[abs(int(txtFactor.get())):],np.zeros(abs(int(txtFactor.get())))])
        
        elif(entradaSeleccionada.get()!="1"):
            tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get()))+1,1)])
            if(int(txtFactor.get())<0):
                tiempo=np.concatenate([np.arange(((int(txtOrigen.get())-int(txtFactor.get()))-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get())-int(txtFactor.get()))+1,1)])     
    elif op==5:#Diezmación
        if(entradaSeleccionada.get()=="1"):
            senialDevuelta=ops.diezmar(senialOriginal,int(txtFactor.get()),0)
            tiempo=np.arange(0,len(senialDevuelta),1)
        else:
            fact=int(txtFactor.get())
            ori=int(txtOrigen.get())
            senialDevuelta=ops.diezmar(senialOriginal,int(txtFactor.get()),(int(txtOrigen.get())-1))
            largo=len(senialDevuelta)
            tiempo=np.concatenate([np.arange(math.floor(ori/fact)*(-1),0,1),np.arange(0,largo-math.floor(ori/fact),1)])
    elif op==6:#Interpolación escalón
        senialDevuelta=ops.interpolarEscalon(senialOriginal,int(txtFactor.get()))
        if(entradaSeleccionada.get()=="1"):
            tiempo=np.arange(0,len(senialDevuelta),1)
        else:
            fact=int(txtFactor.get())
            ori=int(txtOrigen.get())
            largo=len(senialDevuelta)
            tiempo=np.concatenate([np.arange((ori-1)*fact*(-1),0,1),np.arange(0,largo-((ori-1)*fact),1)])
        
    elif op==7:#Interpolación lineal
        senialDevuelta=ops.interpolarLineal(senialOriginal,int(txtFactor.get()))
        tiempo=np.arange(0,len(senialDevuelta),1)
        if(entradaSeleccionada.get()!="1"):
            fact=int(txtFactor.get())
            ori=int(txtOrigen.get())
            largo=len(senialDevuelta)
            tiempo=np.concatenate([np.arange((ori-1)*fact*(-1),0,1),np.arange(0,largo-((ori-1)*fact),1)])
    elif op==8:#Convolución
        if(entradaSeleccionada.get()=="1"):
            senialDevuelta=ops.convolucionar(senialOriginal,senialOriginal)
            tiempo=np.arange(0,len(senialDevuelta),1)
        else:
            senialHn=np.array([float(i) for i in txtHn.get().split(",")])
            senialDevuelta=ops.convolucionar(senialOriginal,senialHn)
            tiempo=np.concatenate([np.arange(((int(txtOrigen.get())+int(txtHnOrigen.get()))-2)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get())+int(txtHnOrigen.get()))+2,1)])
    elif op==9:#FFT
            if(entradaSeleccionada.get()=="1"):
                senialDevuelta=ops.fft1(senialOriginal)
                tiempo=np.arange(0,len(senialDevuelta),1)
            else:
                senialDevuelta=ops.fft(senialOriginal)
                tiempo=np.concatenate([np.arange((int(txtOrigen.get())-1)*(-1),0,1),np.arange(0,len(senialDevuelta)-(int(txtOrigen.get()))+1,1)])
        
    else:
        tk.messagebox.showerror(title="Opción",message="No ha seleccionado una operación")
    
    if(op!=9):
        mostrarNuevaGrafica(senialDevuelta,tiempo)
    else:
        mostrarNuevaGraficaCompleja(senialDevuelta,tiempo)

def mostrarNuevaGrafica(nuevaSenial,tiempo):
     #gráfica de señal nueva
    global archivoSalida
    fs = 44100
    if entradaSeleccionada.get()=="1":
        valorLabel="Tiempo"
        ns=nuevaSenial.astype(dtype=np.int16)
        write(archivoSalida, fs ,ns)
        mostrarReproducirSalida()
        lblSalida.grid_forget()
    else:
        valorLabel="n"
        senalSalida.set(','.join(map(str, nuevaSenial)))
        lblSalida.grid(column=2,row=9,padx=(1,1),columnspan=2,pady=(5,5))
        btnReproducirSalida.grid_forget()
    fig2 = Figure(figsize=(4, 3), dpi=100)
    fig2.add_subplot(111,title="Señal de Salida",xlabel=valorLabel).plot(tiempo,nuevaSenial)
    canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
    canvas2.draw()
    canvas2.get_tk_widget().grid(sticky="W",row=8,column=2,columnspan=2,padx=(1,1),pady=(20,20))

def mostrarNuevaGraficaCompleja(nuevaSenial,tiempo):
     #gráfica de señal compleja nueva (solo FFT)
    global archivoSalida
    fs = 44100
    if entradaSeleccionada.get()=="1":
        valorLabel=""
        ns=nuevaSenial.astype(dtype=np.int16)
        write(archivoSalida, fs ,ns)
        mostrarReproducirSalida()
        lblSalida.grid_forget()
    else:
        senalSalida.set(np.array2string(nuevaSenial,separator=' , '))
        lblSalida.grid(column=2,row=10,padx=(1,1),columnspan=2,pady=(5,5))
        btnReproducirSalida.grid_forget()
        valorLabel="n"
    fig2 = Figure(figsize=(4, 3), dpi=100)
    fig2.add_subplot(111,title="Señal de Salida",xlabel=valorLabel).plot(tiempo,nuevaSenial.real,tiempo,nuevaSenial.imag)
    canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
    canvas2.draw()
    canvas2.get_tk_widget().grid(sticky="W",row=8,column=2,columnspan=2,padx=(1,1),pady=(20,20))
    
"""------------------
    GUI
-----------------"""
#propiedad de la ventana
ventana = tk.Tk()
ventana.geometry('900x700')
ventana.configure(bg="#BDC19E")
ventana.title("Ventana principal")
operacion = tk.StringVar(ventana)
senalSalida = tk.StringVar(ventana)
entradaSeleccionada=tk.StringVar(ventana)

#componentes de ventana

#Definir entrada
lblSenialEntrada=tk.Label(ventana,text="Señal de entrada", font=("Arial Bold", 14))
lblSenialEntrada.grid(row=0,column=0,pady=(20,10),padx=(10,1),sticky="W")

#Audio
rdAudio=tk.Radiobutton(ventana,variable=entradaSeleccionada, text="Audio", value=1,font=("Arial", 10),width="25",command=ocultarHn)
rdAudio.grid(sticky="W",column=0,row=2,padx=(20,1))
btnGrabar=tk.Button(ventana, text="Grabar audio",bg="#F96646",command=grabarAudio)
btnGrabar.grid(sticky="W",column=1,row=2,padx=(20,1))
btnReproducir=tk.Button(ventana, text="Reproducir audio",bg="#6180FF",command=lambda :reproducirAudio(archivo))
btnReproducir.grid(sticky="E",column=1,row=2,padx=(20,1))

#Secuencia
rdSecuencia=tk.Radiobutton(ventana,variable=entradaSeleccionada,text="Secuencia x(n)", value=2,font=("Arial", 10),width="25",command=mostrarHn)
rdSecuencia.grid(sticky="W",column=0,row=3,padx=(20,1))
txtSecuencia = tk.Entry(ventana,width=30)
txtSecuencia.grid(sticky="W",column=1,row=3,padx=(20,1))

lblOrigen=tk.Label(ventana,text="Orígen (índice)", font=("Arial", 10),width=15)
lblOrigen.grid(sticky="W",column=2,row=3,padx=(1,1))
txtOrigen=tk.Entry(ventana,width=5)
txtOrigen.grid(sticky="W",column=3,row=3,padx=(1,1),columnspan=3)

lblHn=tk.Label(ventana,text="h(n)", font=("Arial", 10),width="27")
txtHn=tk.Entry(ventana,width=30)
lblHnOrigen=tk.Label(ventana,text="Origen (posición)", font=("Arial", 10),width=15)
txtHnOrigen=tk.Entry(ventana,width=5)


#Seleccionar operacion
lblOperacion=tk.Label(ventana,text="Operación", font=("Arial Bold", 14))
lblOperacion.grid(row=5,column=0,pady=(20,10),padx=(10,1),sticky="W")
omOperacion=tk.OptionMenu(ventana, operacion, *operaciones)
operacion.set('Seleccionar')
omOperacion.grid(row=6,column=0,padx=(20,1),sticky="W")

#Factor
lblFactor=tk.Label(ventana,text="Factor", font=("Arial", 10),width=10)
lblFactor.grid(row=6,column=1,padx=(20,1),sticky="W")
txtFactor=tk.Entry(ventana,width=10)
txtFactor.grid(row=6,column=1,padx=(20,1),sticky="E")


#Botón de calcular
btnCalcular=tk.Button(ventana, text="CALCULAR",bg="#84DE74",command=calcular)
btnCalcular.grid(column=0,row=7,padx=(20,1),columnspan=5,pady=(20,10))
btnCalcular['font']=font.Font(weight="bold",size=9)

#salida en label
lblSalida=tk.Label(ventana,textvariable=senalSalida, font=("Arial", 10),width=50)

#Botón de reproducir salida
btnReproducirSalida=tk.Button(ventana, text="Reproducir",bg="#f5e251",command=lambda:reproducirAudio(archivoSalida))

ventana.mainloop()
