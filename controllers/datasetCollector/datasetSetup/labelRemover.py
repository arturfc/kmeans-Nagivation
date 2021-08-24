import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, difflib
import seaborn as sn

import csv



with open('360/encruzilhada_direita.txt',"r") as fin:
    with open('360/encDireita.txt',"w") as fout:
        writer=csv.writer(fout)
        for row in csv.reader(fin):
            writer.writerow(row[:-3])

with open('360/encDireita.txt', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.writelines(line for line in lines if line.strip())
        f.truncate()
