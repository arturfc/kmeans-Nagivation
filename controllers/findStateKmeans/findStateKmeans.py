"""pioneer_180 controller"""

from controller import Robot, Motor, Lidar
import time
import pandas as pd
import scipy
import random
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import numpy as np
import statistics
import collections

#variáveis globais (cada mapa possui valores específicos destas variáveis)
angle = 81  #angle settings -> mapa1:82    mapa1:82  mapa1:80  mapa1:81
speed = 4   #speed settings -> mapa1:2.5   mapa2:2   mapa3:5   mapa4:4

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
    left_wheel.setVelocity(speed)

    right_wheel = robot.getDevice("right wheel")
    right_wheel.setPosition(float('inf'))
    right_wheel.setVelocity(speed)

    robot.step(TIME_STEP)

def readState(newState, s1, s2, s3, s4, s5, s6, s7):
    if newState == s1: #saida à direita
        return 0;
    if newState == s2: #saida à esquerda 
        return 1;
    if newState == s3: #saída à direita e esquerda
        return 2;
    if newState == s4: #Encruzilhada à esquerda
        return 3;
    if newState == s5: #Encruzilhada à direita
        return 4;
    if newState == s6: #Encruzilhada
        return 5;
    if newState == s7: #corredor
        return 6;
    else:
        return 6;

def executarAcao(estado):
    
    #saida à direita
    if estado == 0:
        print("saida direita")
        b = 0
        while (b <= angle):
            b = b + 1
            turnRight()

        while (b <= 130):
            b = b + 1
            goStraight()

        
    #Saida à esquerda
    if estado == 1:
        print("saida_esquerda")
        b = 0
        while (b <= angle):
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
        if acao == 1: #virar à direita
            while (b <= angle):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b + 1
                goStraight()

        if acao == 2:   #virar à esquerda
            while (b <= angle):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

        

    #Encruzilhada à esquerda
    if estado == 3:
        print("encruzilhada_esquerda")
        acao = random.randint(1, 2)
        b = 0
        if acao == 1: #virar à esquerda
            while (b <= angle):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

        if acao == 2: #seguir reto
            c = 0
            while (c < 150):
                c = c + 1
                goStraight()

    #Encruzilhada à direita    
    if estado == 4:
        print("encruzilhada_direita")
        b = 0
        acao = random.randint(1, 2) 
        if acao == 1: #virar à direita
            while (b <= angle):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b+1
                goStraight()

            if acao == 2:#seguir reto
                c = 0
                while (c < 150):
                    c = c + 1
                    goStraight()

    if estado == 5:
        print("encruzilhada")
        c = 0
        b = 0
        acao = random.randint(1, 3)
        if acao == 1: #seguir reto
            
            while (c < 150):
                c = c + 1
                goStraight()

        if acao == 2: #virar à direita
            b = 0
            while (b <= angle):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b + 1
                goStraight()

                
        if acao == 3 : #virar à esquerda
            b = 0
            while (b <= angle):
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

#definindo o mapa a ser utilizado
dataset = pd.read_csv('mapa1.csv')
dataset = dataset.iloc[:, 0:180].values #coletando apenas os dados

rangeImageCompleteDf = []
rangeImageAux = []
rangeImage = lidar.getRangeImage()
cont = 0
estado = 6 #inicialização como estado 'corredor'

#normalização dos dados
dataset = normalize(dataset)

#execução do kmeans
kmeans = KMeans(n_clusters = 7, init='k-means++', n_init = 10, max_iter = 10000, random_state = 5, algorithm = "auto")
kmeans.fit_predict(dataset)

#captura manual da representação dos estados
s1 = statistics.mode(kmeans.labels_[0:999])        
s2 = statistics.mode(kmeans.labels_[1000:1999])
s3 = statistics.mode(kmeans.labels_[2000:2999])
s4 = statistics.mode(kmeans.labels_[3000:3999])
s5 = statistics.mode(kmeans.labels_[4000:4999])
s6 = statistics.mode(kmeans.labels_[5000:5999])
s7 = statistics.mode(kmeans.labels_[6000:6999])

#coleta constante dos dados em tempo real
while robot.step(TIME_STEP) != -1:
    for cont in range(25):
        goStraight()
        rangeImage = lidar.getRangeImage()  #Pega os dados de cada ponto
        if not rangeImage:
            cont = cont - 1
        else:
            rangeImageAux.append(rangeImage)
    
    estadoAux = estado
    rangeImageCompleteDf = np.array(rangeImageAux)
    rangeImageCompleteDf = normalize(rangeImageCompleteDf)
    estado = readState(statistics.mode(kmeans.predict(rangeImageCompleteDf)), s1, s2, s3, s4, s5, s6, s7)
    
    if (estado == estadoAux):
        executarAcao(estado);
    else:
        rangeImageAux = []
        for cont in range(25):
            goStraight()
            rangeImage = lidar.getRangeImage()  # Pega os dados de cada ponto
            if not rangeImage:
                cont = cont - 1
            else:
                if cont >= 6:
                    rangeImageAux.append(rangeImage)
        
        rangeImageCompleteDf = np.array(rangeImageAux)
        rangeImageCompleteDf = normalize(rangeImageCompleteDf)
        estado = readState(statistics.mode(kmeans.predict(rangeImageCompleteDf)), s1, s2, s3, s4, s5, s6, s7)
        executarAcao(estado)
    rangeImageAux = []


