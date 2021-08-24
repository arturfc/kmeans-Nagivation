import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, difflib
import seaborn as sn
import collections, numpy
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
import statistics

number_of_clusters = 7
np.set_printoptions(threshold=sys.maxsize)  #print data visualisation without truncation
#np.random.seed(5)

#reading entire data
#definir o dataset a ser utilizado para validação
df = pd.read_csv('mapa1/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda_encDireita_encruzilhada_corredor.csv')
x = df.iloc[:, 0:180].values	#mapa2 e mapa2: x = df.iloc[:, 0:180].values


#standardizing the features
from sklearn.preprocessing import StandardScaler
#x = StandardScaler().fit_transform(x)
x = normalize(x)

#transforming features into components using PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=3)
principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(data = principalComponents
            , columns = ['PCA1', 'PCA2', 'PCA3'])

#print(pca.explained_variance_)

#applying kmeans
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = number_of_clusters, init='k-means++', n_init = 10, max_iter = 10000, random_state = 5, algorithm = "auto") #remove n_jobs if it's too slow
y_kmeans = kmeans.fit_predict(x)	#label classification

y_kmeans_dataframe = pd.DataFrame(y_kmeans)	#transformation into dataframe

from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df.label)	#change df.<column> accordingly or positioning by df.iloc[:, [<column_postiion>]].values.ravel()	ie.df.: iloc[:, [2]].values.ravel()
groundTruthLabel = le.transform(df.label) #change df.<column> accordingly or positioning by df.iloc[:, [<column_postiion>]].values.ravel()
groundTruthLabel_dataframe = pd.DataFrame(groundTruthLabel)	#transforming into dataframe

#merging component columns with label column
finalDf = pd.concat([principalDf, y_kmeans_dataframe], axis = 1)	#insert groundTruthLabel_dataframe instead of y_kmeans_dataframe for ground truth classification

#testing if dimension is correct
#print("shape label classification",y_kmeans_dataframe.shape)
#print("shape GT label", groundTruthLabel_dataframe.shape)

#using rand index for clustering validation
from sklearn.metrics.cluster import adjusted_rand_score
print('Grouping validation value by rand index is', "%.3f" % adjusted_rand_score(groundTruthLabel, y_kmeans)) #validation value between 0 and 1


#----------------------------------------------------------------------------------------------------------

# Keep the 'label' column appart + make it numeric for coloring	y_kmeans_dataframe
#y_kmeans_dataframe[0]=pd.Categorical(y_kmeans_dataframe[0])
#my_color=y_kmeans_dataframe[0].cat.codes
#y_kmeans_dataframe = y_kmeans_dataframe.drop([0], 1)

# Keep the 'label' column appart + make it numeric for coloring	GT
print(df.shape)
print(finalDf.shape)

df['label']=pd.Categorical(df['label'])
my_color=df['label'].cat.codes
df = df.drop('label', 1)

#plotting clustering representation by kmeans algorithm
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(principalDf['PCA1'], principalDf['PCA2'], principalDf['PCA3'], c=my_color, cmap="Set2_r", s=15)

# make simple, bare axis lines through space:
xAxisLine = ((min(principalDf['PCA1']), max(principalDf['PCA1'])), (0, 0), (0,0))
ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
yAxisLine = ((0, 0), (min(principalDf['PCA2']), max(principalDf['PCA2'])), (0,0))
ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
zAxisLine = ((0, 0), (0,0), (min(principalDf['PCA3']), max(principalDf['PCA3'])))
ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')
 
# label the axes
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.set_title("Representação 3-D PCA \n Dados não-normalizados", fontsize=30)
plt.show()

