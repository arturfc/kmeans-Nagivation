import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, difflib
import seaborn as sn

import csv


#'180/corredor.txt'
#'180/direita.txt'
#'180/corredor_.txt'
#'180/corredor_.txt'
#'180/corredor_.txt'
#'180/corredor_.txt'
#'180/corredor_.txt'

filenames = ['mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda_encDireita_encruzilhada.csv', 'mapa123/statesMerged/trash/corredor.csv'] 

# Open file3 in write mode 
with open('mapa123/statesMerged/csvCombined/direita_esquerda_direitaEsquerda_encEsquerda_encDireita_encruzilhada_corredor.csv', 'w') as outfile: 
  
    # Iterate through list 
    for names in filenames: 
  
        # Open each file in read mode 
        with open(names) as infile: 
  
            # read the data from file1 and 
            # file2 and write it in file3 
            outfile.write(infile.read()) 
  
        # Add '\n' to enter data of file2 
        # from next line 
        
#mapa2/statesMerged/trash/
#mapa2/statesMerged/csvCombined/