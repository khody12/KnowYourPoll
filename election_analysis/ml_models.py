import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

#to preface, i am by no means a data scientist or a political analyst, i merely enjoy politics and coding. 
# I would really not take this model too seriously and my data can easily be considered questionable

#polling data sourced from wikipedia, I averaged polling percentage from september to election data.
#  
# dem candidate  support, rep candidate support, dem incumbency, rep incumbency, economic indicator from -1 to 1. -1 = bad, 1 = good


# ive made the very debatable assumption that the economic indicator is basically irrelevant if there is no incumbent. 
X_data = torch.tensor([
    [51.4, 44.2, 1, 0, 0.7], # FDR vs Landon 1936
    [50.5, 42.5, 1, 0, 0.85], #FDR vs Willkie 1940
    [48.7, 45, 1, 0, 0.92], # Fdr vs Dewey 1944
    [39.33, 47.83, 1, 0, -0.42], # truman v dewey 1948   # historic polling miss here. 
    [41.14, 51.57, 0, 0, 0], # stevenson  v eisenhower 1952
    [40.6, 53.2, 0, 1, 0.72], # Stevenson v eisenhowever 1956
    [47.7, 47.23, 0, 0, 0], # JFK v Nixon 1960
    [63.75, 31.5, 0, 0, 0], # LBJ vs goldwater 1964
    [39, 43.5, 0, 0, 0], # nixon v humphrey 1968
    [35.25, 60.5, 0, 1, 0.97], # nixon v mcgovern 1972
    [48.25, 43.75, 0, 0, 0], # carter v Ford 1976
    [40.0, 41.33, 1, 0, -1], # carter v reagan 1980 
    [38.85, 56.28, 0, 1, 0.96], #  mondale vs reagan 1984
    [41.75, 50.5, 0, 0, 0], # dukakis v HW Bush 1988
    [46.5, 35.4, 0, 1, -0.22], # Clinton v HW bush 1992 
    [52.19, 36.125, 1, 0, 0.78], # clinton vs dole 96'
    [43.82, 46.94, 0, 0, 0], # gore vs Bush 00'
    [46.57, 50.43, 0, 1, 0.85], # kerry vs bush 04'
    [49.88, 43.38, 0, 0, 0], # obama vs mccain 08'
    [48, 46.56, 1, 0, -0.12], # obama vs romney 2012
    [47.33, 43.32, 0, 0, 0], # clinton v trump
    [51.37, 43.5, 0, 1, -0.2] # biden v trump. while economy had a recession.. it was a quick one due to mass stimulus. so only ~ -0.2
    ], dtype=torch.float32)

#if dem candidates win, y =1, if rep wins y = 0
y_data = torch.tensor([
    [1],
    [1],
    [1],
    [1],
    [0],
    [0],
    [1],
    [1],
    [0],
    [0],
    [1],
    [0],
    [0],
    [0],
    [1],
    [1],
    [0],
    [0],
    [1],
    [1],
    [0],
    [1]
])

training_split = len(X_data) * 0.8

X_training_split, X_testing_split = X_data[:training_split], X_data[training_split:]
Y_training_split, y_testing_split = y_data[:training_split], y_data[training_split:]



