import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, difflib
import seaborn as sn
import collections, numpy
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
import statistics
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics.cluster import adjusted_rand_score


#df = pd.read_csv('mapa1/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda.csv')
#x = df.iloc[:, 0:180].values	#mapa2 e mapa2: x = df.iloc[:, 0:180].values

#x = normalize(x)

def ARIresult(x, number_of_clusters):

	x = df.iloc[:, 0:180].values
	#x = normalize(x)
	kmeans = KMeans(n_clusters = number_of_clusters, init='k-means++', n_init = 10, max_iter = 10000, random_state = 5, algorithm = "auto") #remove n_jobs if it's too slow
	y_kmeans = kmeans.fit_predict(x)
	y_kmeans_dataframe = pd.DataFrame(y_kmeans)
	le = preprocessing.LabelEncoder()
	le.fit(df.label)
	groundTruthLabel = le.transform(df.label) 
	groundTruthLabel_dataframe = pd.DataFrame(groundTruthLabel)	
	print("%.3f" % adjusted_rand_score(groundTruthLabel, y_kmeans), end=' ', flush=True)

for i in range(2,8):
	if i == 2:
		for j in range(2,8):
			df = pd.read_csv('mapa123/statesMerged/csvCombined/direita_esquerda.csv')
			ARIresult(df, j)

	if i == 3:
		for j in range(2,8):
			df = pd.read_csv('mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda.csv')
			ARIresult(df, j)

	if i == 4:
		for j in range(2,8):
			df = pd.read_csv('mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda.csv')
			ARIresult(df, j)

	if i == 5:
		for j in range(2,8):
			df = pd.read_csv('mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda_encDireita.csv')
			ARIresult(df, j)

	if i == 6:
		for j in range(2,8):
			df = pd.read_csv('mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda_encDireita_encruzilhada.csv')
			ARIresult(df, j)

	if i == 7:
		for j in range(2,8):
			df = pd.read_csv('mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda_encDireita_encruzilhada_corredor.csv')
			ARIresult(df, j)

	print('\n')

print('\n saiu...')