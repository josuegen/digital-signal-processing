# -*- coding: utf-8 -*-
"""
PROYECTO DE TEORÍA DE COMUNICACIONES Y SEÑALES
Clase auxiliar de operaciones del proyecto

GRUPO:3CV5

AUTOR:
Velázquez Gen Josué Emmanuel
"""

import numpy as np
from itertools import zip_longest
import tkinter as tk


class Operaciones:
    
    def Operaciones(self):
        pass
    
    def sumar(self,senial1,senial2):
        return np.array([sum(n) for n in zip_longest(senial1, senial2, fillvalue=0)])
        
    def restar(self,senial1,senial2):
        senial2=np.negative(senial2)
        return np.array([sum(n) for n in zip_longest(senial1, senial2, fillvalue=0)])
        
    def amplificar_atenuar(self,senal,factor):
        return np.array(factor*(np.array(senal)))
    
    def reflejar(self,senal):
        return np.flip(senal)
    
    def desplazar(self,senal,factor):
        if(factor>0):
            return np.concatenate([np.zeros(factor),senal])
        elif(factor<0):
            return np.concatenate([senal,np.zeros(abs(factor))])
            
    def diezmar(self,senal,factor,origen):
        #indices=np.concatenate([np.arange(origen,-1,-(factor)),np.arange(origen,len(senal),factor)])
        s1=np.array(senal[:origen+1])
        s2=np.array(senal[origen:])
        s1=np.flip(s1)
        s1p=s1[::factor].copy()
        s2p=s2[::factor].copy()
        s1p=np.flip(s1p)
        return np.concatenate([s1p[:-1],s2p])
    
    def interpolarEscalon(self,senal,factor):
        return np.repeat(senal,factor)
    
    def interpolarLineal(self,senal,factor):
        senial=senal.copy()
        while(factor>1):
            sign=[]
            for i in range(len(senial)-1):
                sign.extend((senial[i],(senial[i]+senial[i+1])/2))
            senial=sign
            factor=factor-1
        return np.array(sign)
        
    def convolucionar(self,senal,senal2):
        return np.convolve(senal,senal2)
    
        
    def dft(self,senal):
        N = senal.shape[0]
        n = np.arange(N)
        k = n.reshape((N, 1))
        M = np.exp(-2j * np.pi * k * n / N)
        return np.dot(M, senal)
    
    def fft(self,senal):
        N = senal.shape[0]
        if(N%2)>0:
            tk.messagebox.showerror(title="Longitud",message="La entrada debe tener longitud 2^n")
        elif(N<=2):
            return self.dft(senal)
        else:
            pares = self.fft(senal[::2])
            impares = self.fft(senal[1::2])
            terms = np.exp(-2j * np.pi * np.arange(N) / N)
            return np.concatenate([pares + terms[:int(N/2)] * impares,pares + terms[int(N/2):] * impares])
        
    def fft1(self,senal):
        return np.fft.fft(senal)
        
        
