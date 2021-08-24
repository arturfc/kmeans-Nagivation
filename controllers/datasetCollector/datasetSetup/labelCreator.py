import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, difflib
import seaborn as sn

colors = ["curva_direita"]
label = "label"
with open('newTest/curvaDireitaFullLabeled.csv') as input_file, open('newTest/curvaDireitaFullLabeled2.csv', 'w') as output_file:
    for i, line in enumerate(input_file):
    	
    	
        color = colors[i % len(colors)]
        if i==0:
        	new_line = '{},{}\n'.format(line.rstrip(), label)
        else:
        	new_line = '{},{}\n'.format(line.rstrip(), color)

        output_file.write(new_line)

#f = open("180/direita.txt", "r")
#print(f.read())
