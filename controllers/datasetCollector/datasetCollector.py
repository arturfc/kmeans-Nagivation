"""pioneer_180 controller"""

from controller import Robot, Motor, Lidar
import time
import pandas as pd
import leEstadoAtual
import scipy
import random
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import numpy as np
import statistics
import collections

def turnRight():
    left_wheel = robot.getDevice("left wheel")
    left_wheel.setPosition(float('inf'))
    left_wheel.setVelocity(3.0)

    right_wheel = robot.getDevice("right wheel")
    right_wheel.setPosition(float('inf'))
    right_wheel.setVelocity(1.0)
    robot.step(TIME_STEP)

def turnLeft():
    left_wheel = robot.getDevice("left wheel")
    left_wheel.setPosition(float('inf'))
    left_wheel.setVelocity(1.0)

    right_wheel = robot.getDevice("right wheel")
    right_wheel.setPosition(float('inf'))
    right_wheel.setVelocity(3.0)
    robot.step(TIME_STEP)

def goStraight():
    left_wheel = robot.getDevice("left wheel")
    left_wheel.setPosition(float('inf'))
    left_wheel.setVelocity(2.0)

    right_wheel = robot.getDevice("right wheel")
    right_wheel.setPosition(float('inf'))
    right_wheel.setVelocity(2.0)

    robot.step(TIME_STEP)

def readState(newState, s1, s2, s3, s4, s5, s6, s7):
    #print(newState)
    if newState == s1:
        return 0;
    if newState == s2:
        return 1;
    if newState == s3:
        return 2;
    if newState == s4:
        return 3;
    if newState == s5:
        return 4;
    if newState == s6:
        return 5;
    if newState == s7:
        return 6;
    else:
        return 6;

def executarAcao(estado):
    #Saida a direita
    if estado == 0:
        print("saida direita")
        b = 0
        while (b <= 80):
            b = b + 1
            turnRight()

        while (b <= 130):
            b = b + 1
            goStraight()

        
    #Saida a esquerda
    if estado == 1:
        print("saida_esquerda")
        b = 0
        while (b <= 80):
            b = b + 1
            turnLeft()

        while (b <= 130):
            b = b + 1
            goStraight()

        

    #Saida direita e esquerda
    if estado == 2:
        print("saida_direita_esquerda")
        acao = random.randint(1, 2)
        b = 0
        if acao == 1: #Direita
            while (b <= 80):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b + 1
                goStraight()

        if acao == 2:   #esquerda
            while (b <= 80):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

        

    #Encruzilhada a esquerda
    if estado == 3:
        print("encruzilhada_esquerda")
        acao = random.randint(1, 2)
        b = 0
        if acao == 1: #Esquerda
            while (b <= 80):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

        if acao == 2: #Reto
            c = 0
            while (c < 150):
                c = c + 1
                goStraight()

        
    if estado == 4:
        print("encruzilhada_direita")
        b = 0
        acao = random.randint(1, 2)
        if acao == 1: #direita
            while (b <= 80):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b+1
                goStraight()

            if acao == 2:#reto
                c = 0
                while (c < 150):
                    c = c + 1
                    goStraight()

    if estado == 5:
        print("encruzilhada")
        c = 0
        b = 0
        acao = random.randint(1, 3)
        if acao == 1: #Reto
            
            while (c < 150):
                c = c + 1
                goStraight()

        if acao == 2: #direita
            b = 0
            while (b <= 80):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b + 1
                goStraight()

                
        if acao == 3 : #esquerda
            b = 0
            while (b <= 80):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

    if estado == 6:
        print("corredor")
        goStraight()
        

    if estado == 7:
        print("Erro ao encontrar o estado !")
        goStraight()
        


TIME_STEP = 32

# Criando o robo
robot = Robot()  # Pioneer 3

# inicializando os dispositivos
lidar = robot.getDevice("Sick LMS 291")  # Alcance de 80 metros e pega os dados em 180 graus
lidar.enable(TIME_STEP)  # O Lidar mede informações em metros da renderização do sensor
lidar.enablePointCloud()
#goStraight()

# DEFINICOES
dataset = leEstadoAtual.create_df()
rangeImageCompleteDf = []
rangeImageAux = []
rangeImage = lidar.getRangeImage()
cont = 0
estado = 6
aux = 0

v = 0.67 #velocidade do robô
for cont in range(500): #quantidade de dados a serem coletados
    left_wheel = robot.getDevice("left wheel")
    left_wheel.setPosition(float('inf'))
    left_wheel.setVelocity(v)

    right_wheel = robot.getDevice("right wheel")
    right_wheel.setPosition(float('inf'))
    right_wheel.setVelocity(v)

    robot.step(TIME_STEP)
    rangeImage = lidar.getRangeImage()  # Pega os dados de cada ponto
    if not rangeImage:
        cont = cont - 1
        print("caiu aqui")
    else:
        rangeImageAux.append(rangeImage)

print("finalizado")

arr = np.array(rangeImageAux)
np.savetxt("mapa1/dadobruto/encDireita3.csv", arr, delimiter=",")


import csv
with open('mapa1/dadobruto/encDireita3.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('mapa1/dadobruto/encDireita3.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179])
    w.writerows(data)

colors = ["encDireita"]
label = "label"
with open('mapa1/dadobruto/encDireita3.csv') as input_file, open('mapa1/encDireita3L.csv', 'w') as output_file:
    for i, line in enumerate(input_file):
    	
    	
        color = colors[i % len(colors)]
        if i==0:
        	new_line = '{},{}\n'.format(line.rstrip(), label)
        else:
        	new_line = '{},{}\n'.format(line.rstrip(), color)

        output_file.write(new_line)

print("pronto")
print(np.amax(arr))
print(np.amin(arr))
print(arr.shape)
#print(arr)
#print(len(rangeImage))
#print(np.any(np.isnan(rangeImage)))
#print(np.any(np.isfinite(rangeImage)))