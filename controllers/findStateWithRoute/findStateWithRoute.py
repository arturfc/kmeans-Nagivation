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

#rota pré-definida OBS: considerando a posição inicial do mapa 'map4Routed'
'''
metodologia de route (em 'map4Routed'):
Segue abaixo a rota teoricamente gerada por um algoritmo gerador de rotas:
[esquerda, direita, esquerda, esquerda, direita, esquerda, reto, direita, direita, direita]

onde, se identificado:
    esquerda: 0 é reto; 1 fazer curva
    direita: 0 é reto; 1 fazer curva
    reto: 0 seguir reto
'''
route = [1, 0, 0, 0, 0, 1, 0, 0, 0, 1] #esta rpta funcionará apenas em map4Routed

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

def executarAcao(estado, route):
    if estado == 0:
        print("Estado identificado: saida direita")
        b = 0
        while (b <= angle):
            b = b + 1
            turnRight()

        while (b <= 130):
            b = b + 1
            goStraight()
   
    #Saida a esquerda
    if estado == 1:
        print("Estado identificado: saida_esquerda")
        b = 0
        while (b <= angle):
            b = b + 1
            turnLeft()

        while (b <= 130):
            b = b + 1
            goStraight()

    #Saida direita e esquerda
    if estado == 2:
        print("Estado identificado: saida_direita_esquerda")
        b = 0
        if route == 0: #Direita
            while (b <= angle):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b + 1
                goStraight()

        if route == 1:   #esquerda
            while (b <= angle):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

        
    #Encruzilhada a esquerda
    if estado == 3:
        print("Estado identificado: encruzilhada_esquerda")
        b = 0
        if route == 1: #Esquerda
            while (b <= angle):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

        if route == 0: #Reto
            c = 0
            while (c < 150):
                c = c + 1
                goStraight()

        
    if estado == 4:
        print("Estado identificado: encruzilhada_direita")
        b = 0
        if route == 1: #direita
            while (b <= angle):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b+1
                goStraight()

            if route == 0:#reto
                c = 0
                while (c < 150):
                    c = c + 1
                    goStraight()

    if estado == 5:
        print("Estado identificado: encruzilhada")
        c = 0
        b = 0
        if route == 0: #Reto
            
            while (c < 150):
                c = c + 1
                goStraight()

        if route == 1: #direita
            b = 0
            while (b <= angle):
                b = b + 1
                turnRight()

            while (b <= 130):
                b = b + 1
                goStraight()

                
        if route == 2 : #esquerda
            b = 0
            while (b <= angle):
                b = b + 1
                turnLeft()

            while (b <= 130):
                b = b + 1
                goStraight()

    if estado == 6:
        print("Estado identificado: corredor")
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
aux = 0


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
        rangeImage = lidar.getRangeImage()  # Pega os dados de cada ponto
        if not rangeImage:
            cont = cont - 1
        else:
            rangeImageAux.append(rangeImage)
    
    estadoAux = estado    
    rangeImageCompleteDf = np.array(rangeImageAux)
    rangeImageCompleteDf = normalize(rangeImageCompleteDf)
    estado = readState(statistics.mode(kmeans.predict(rangeImageCompleteDf)), s1, s2, s3, s4, s5, s6, s7)
  
    if (estado == estadoAux):
        if (aux >= len(route)):
            left_wheel = robot.getDevice("left wheel")
            left_wheel.setPosition(float('inf'))
            left_wheel.setVelocity(0)
        
            right_wheel = robot.getDevice("right wheel")
            right_wheel.setPosition(float('inf'))
            right_wheel.setVelocity(0)
            break
        
        if (aux < len(route)):
            executarAcao(estado, route[aux]);
            if (estado != 6):
                aux+=1
               
    else:
        rangeImageAux = []
        for cont in range(25):
            goStraight()
            rangeImage = lidar.getRangeImage()  # Pega os dados de cada ponto
            
            if not rangeImage:
                cont = cont - 1
            else:
                if cont >= 5:
                    rangeImageAux.append(rangeImage)
        
        
        rangeImageCompleteDf = np.array(rangeImageAux)
        rangeImageCompleteDf = normalize(rangeImageCompleteDf)
        estado = readState(statistics.mode(kmeans.predict(rangeImageCompleteDf)), s1, s2, s3, s4, s5, s6, s7)
        
        if (aux >= len(route)):
            left_wheel = robot.getDevice("left wheel")
            left_wheel.setPosition(float('inf'))
            left_wheel.setVelocity(0)
        
            right_wheel = robot.getDevice("right wheel")
            right_wheel.setPosition(float('inf'))
            right_wheel.setVelocity(0)
            break
            
        if (aux < len(route)):
            executarAcao(estado, route[aux])
            if (estado != 6):
                aux+=1
                
        
    rangeImageAux = []


