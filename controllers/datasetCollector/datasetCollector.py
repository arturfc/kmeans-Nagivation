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
import csv

v = 0.67 #velocidade do robô
dataToBeCollected = 500 #quantidade de dados a serem coletados
stateIdentified = ["encDireita"]
fileNoLabel = "encDireita3.csv"
fileWithLabel = "encDireita3L.csv"

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


TIME_STEP = 32

# Criando o robo
robot = Robot()  # Pioneer 3

# inicializando os dispositivos
lidar = robot.getDevice("Sick LMS 291")  # Alcance de 80 metros e pega os dados em 180 graus
lidar.enable(TIME_STEP)  # O Lidar mede informações em metros da renderização do sensor
lidar.enablePointCloud()

# DEFINICOES
rangeImageCompleteDf = []
rangeImageAux = []
rangeImage = lidar.getRangeImage()
cont = 0

print("Inicializando a coleta de dados")
for cont in range(dataToBeCollected): #quantidade de dados a serem coletados
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
        print("nao eh pra cair aqui")
    else:
        rangeImageAux.append(rangeImage)

print("Salvando dados...")

arr = np.array(rangeImageAux)
np.savetxt(fileNoLabel, arr, delimiter=",")


with open(fileNoLabel, newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open(fileNoLabel,'w',newline='') as f:
    w = csv.writer(f)
    w.writerow([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179])
    w.writerows(data)

label = "label"
with open(fileNoLabel) as input_file, open(fileWithLabel, 'w') as output_file:
    for i, line in enumerate(input_file):
    	
    	
        color = stateIdentified[i % len(stateIdentified)]
        if i==0:
        	new_line = '{},{}\n'.format(line.rstrip(), label)
        else:
        	new_line = '{},{}\n'.format(line.rstrip(), color)

        output_file.write(new_line)

print("Coleta finalizada")