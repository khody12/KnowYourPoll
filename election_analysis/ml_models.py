import torch
import random
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import sys

from main.models import Poll_Aggregate

#to preface, i am by no means a data scientist or a political analyst, i merely enjoy politics and coding. 
# I would really not take this model too seriously and my data can easily be considered questionable

#polling data sourced from wikipedia, I averaged polling percentage from september to election data.
#  
# dem candidate  support, rep candidate support, dem incumbency, rep incumbency, economic indicator from -1 to 1. -1 = bad, 1 = good

torch.manual_seed(42)
# for midterm elections, incumbency DISadvantage will be applied. i will basically just give however is out of power the 1. 
# ive made the very debatable assumption that the economic indicator is basically irrelevant if there is no incumbent. 
X_data = torch.tensor([
    [0.514, 0.442, 1, 0, 0.7], # FDR vs Landon 1936
    [0.505, 0.425, 1, 0, 0.85], #FDR vs Willkie 1940
    [0.487, 0.45, 1, 0, 0.92], # Fdr vs Dewey 1944
    [0.3933, 0.4783, 1, 0, -0.42], # truman v dewey 1948   # historic polling miss here. 
    [0.51, 0.49, 0, 1, 0.52], # 1950 midterm elections
    [0.4114, 0.5157, 0, 0, 0], # stevenson  v eisenhower 1952
    [0.515, 0.485, 1, 0, -0.53], # 1954 midterm elections
    [0.406, 0.532, 0, 1, 0.72], # Stevenson v eisenhowever 1956
    [0.57, 0.43, 1, 0, 0.08], # 1958 midterm elections
    [0.477, 0.4723, 0, 0, 0], # JFK v Nixon 1960
    [0.555, 0.455, 0, 1, 0.52], # 1962 midterm elections
    [0.6375, 0.315, 0, 0, 0], # LBJ vs goldwater 1964
    [0.525, 0.475, 0, 1, 0.06], # 1966 midterm elections
    [0.39, 0.435, 0, 0, 0], # nixon v humphrey 1968
    [0.53, 0.47, 1, 0, -0.34], # 1970 midterm elections
    [0.3525, 0.605, 0, 1, 0.97], # nixon v mcgovern 1972
    [0.60, 0.40, 0, 1, -0.63], # 1974 midterm elections
    [0.4825, 0.4375, 0, 0, 0], # carter v Ford 1976
    [0.55, 0.45, 0, 1, -0.14], # 1978 midterm elections
    [0.400, 0.4133, 1, 0, -1], # carter v reagan 1980 
    [0.55, 0.45, 1, 0, -0.56], # 1982 midterm elections.
    [0.3885, 0.5628, 0, 1, 0.96], #  mondale vs reagan 1984
    [0.4175, 0.505, 0, 0, 0], # dukakis v HW Bush 1988
    [0.54, 0.46, 0, 1, -0.13], # 1990 midterm elections
    [0.465, 0.354, 0, 1, -0.22], # Clinton v HW bush 1992 
    [0.465, 0.535, 0, 1, 0.30], # midterm elections 1994 
    [0.5219, 0.36125, 1, 0, 0.78], # clinton vs dole 96'
    [0.49, 0.51, 0, 1, 0.54], # midterm elections 1998
    [0.4382, 0.4694, 0, 0, 0], # gore vs Bush 00'
    [0.45, 0.496, 1, 0, 0.06], # midterms 02' house generic ballot - RCP avg incumbency advantages favors democrats as bush in office
    [0.4657, 0.5043, 0, 1, 0.85], # kerry vs bush 04'
    [0.406, 0.521, 1, 0, -0.16], # midterms 06' generic ballot RCP - avg. incumbency advantage favors democrats as bush in office
    [0.4988, 0.4338, 0, 0, 0], # obama vs mccain 08'
    [0.413, 0.507, 0, 1, -0.03], # midterms 10' generic ballot RCP - avg # incumbency advantage favors republicans as obama in office
    [0.48, 0.4656, 1, 0, 0.12], # obama vs romney 2012
    [0.432, 0.456, 0, 1, 0.65], # 2014 midterms generic ballot RCP - avg # incumbency advantges favors reps as obama in office
    [0.4733, 0.4332, 0, 0, 0], # 16 ' clinton v trump
    [0.497, 0.424, 1, 0, 0.62], # 2018 midterms generic ballot rcp - avg # incumbency favors dems as trump in office
    [0.5137, 0.435, 0, 1, 0], # biden v trump. while economy had a recession.. it was a quick one due to mass stimulus. so only ~ -0.2
    [0.455, 0.48, 0, 1, -0.78] # midterms 2022 
    ], dtype=torch.float32)

#if dem candidates win, y =1, if rep wins y = 0
y_data = torch.tensor([
    [1], # 1936 eleection
    [1], # 1940 election
    [1], # 1944 election 
    [1], # 1948 election 
    [0], # 1950 midterm
    [0], # election 1952
    [1], # 1954 mid
    [0],# election 56'
    [1], # 58' mid
    [1], # election 60'
    [0], # mid 62'
    [1], # election 64
    [0], # mid 66'
    [0], # election 68'
    [1], # mid 70'
    [0], # el 72'
    [1], # mid 74'
    [1], # el 76'
    [0], # mid 78'
    [0], # el 1980
    [1], # mid 1982
    [0],# election 1984
    [0],# election 1988
    [1], # midterm 90'
    [1], # election 92
    [0], # midterm 94'
    [1], # election 96'
    [1], # midterm 98'
    [0], # election2000
    [0], # midterm 2002
    [0], # election 2004
    [1], # midterm 2006
    [1], # election 2008
    [0], # mid 2010
    [1], # el 2012
    [0], # mid 2014
    [0], # el 16'
    [1], # mid 18'
    [1], # el 20'
    [0], # mid 22'
]).squeeze()


training_split = int(len(X_data) * 0.8)

X_training_split, X_testing_split = X_data[:training_split], X_data[training_split:]
y_training_split, y_testing_split = y_data[:training_split], y_data[training_split:]

y_training_split = y_training_split.squeeze().float()
y_testing_split = y_testing_split.squeeze().float()


print(y_data.shape)
#sys.exit()


#device = "cuda" if torch.cuda.is_available else "cpu" if you have nvidia gpu, simply include this line and delete the below line
device = "cpu"

class ElectionModelV0(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = nn.Linear(in_features=5, out_features=8)
        self.layer_2 = nn.Linear(in_features=8, out_features=8)
        self.layer_3 = nn.Linear(in_features=8, out_features=1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        

    def forward(self, x):
        x = self.relu(self.layer_1(x))
        x = self.relu(self.layer_2(x))
        x = self.layer_3(x)
        x = self.sigmoid(x)
        
        return x


model_0 = ElectionModelV0().to(device)

loss_fn = nn.BCELoss()
optimizer = optim.Adam(model_0.parameters(), lr = 0.0001)

epochs = 10000

def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()
    acc = (correct/len(y_pred)) * 100
    return acc
train_model = False

if train_model:
    for epoch in range(epochs):
    #1. Forward pass
        y_probs = model_0(X_training_split).squeeze() # our y probability values, probability of Candidate A winning.
        candidate_pred = torch.round(y_probs).squeeze()

    #2. Determine the loss 
    # loss is determined by seeing if the candidate with the higher probability of winning matches the result.
        loss = loss_fn(y_probs, y_training_split)
    # accuracy function is seeing the training data versus the predicted values and seeing how often it gets it right
        acc = accuracy_fn(y_true=y_training_split,
                      y_pred=candidate_pred)
    
    #3. zero grad
        optimizer.zero_grad()

    #4. Loss backward
        loss.backward()

    #5. 
        optimizer.step()

        model_0.eval()
        with torch.inference_mode():
            test_y_probs = model_0(X_testing_split).squeeze()
            test_candidate_pred = torch.round(test_y_probs).squeeze()

            test_loss = loss_fn(test_y_probs, y_testing_split)

            test_acc = accuracy_fn(y_true=y_testing_split, y_pred=test_candidate_pred)

        if epoch % 1000 == 0:
            print(f"Epoch: {epoch} | Loss: {loss}, Acc: {acc:.2f} | Test loss: {test_loss} Test accuracy: {test_acc}")
            print(model_0.state_dict())

if train_model:
    torch.save(model_0.state_dict(), "election_analysis/election_modelV2.pth")
    
loaded_model_0 = ElectionModelV0()
loaded_model_0.load_state_dict(torch.load("election_analysis/election_model.pth"))

loaded_model_0.eval()

Econ_2024 = 0.16

harris_support = Poll_Aggregate.objects.all().latest('date').harris_support
trump_support = Poll_Aggregate.objects.all().latest('date').trump_support



with torch.inference_mode():
    harris_v_trump = torch.tensor([
    [harris_support, trump_support, 0, 0, Econ_2024]
    ])
    new_data_prediction_probs = loaded_model_0(harris_v_trump).squeeze()
    new_data_prediction = torch.round(new_data_prediction_probs)

    print(f"Prediction probability: {new_data_prediction_probs}")
    print(f"Prediction: {new_data_prediction}")

    










# [0.514, 0.442, 1, 0.7], # FDR vs Landon 1936
#     [0.505, 0.425, 1, 0.85], #FDR vs Willkie 1940
#     [0.487, 0.45, 1, 0.92], # Fdr vs Dewey 1944
#     [0.3933, 0.4783, 1, -0.42], # truman v dewey 1948   # historic polling miss here. 
#     [0.51, 0.49, 1, 0.52], # 1950 midterm elections
#     [0.4114, 0.5157, 0, 0], # stevenson  v eisenhower 1952
#     [0.515, 0.485, 1, -0.53], # 1954 midterm elections
#     [0.406, 0.532, -1, 0.72], # Stevenson v eisenhowever 1956
#     [0.57, 0.43, 1, 0.08], # 1958 midterm elections
#     [0.477, 0.4723, 0, 0], # JFK v Nixon 1960
#     [0.555, 0.455, -1, 0.52], # 1962 midterm elections
#     [0.6375, 0.315, 0, 0], # LBJ vs goldwater 1964
#     [0.525, 0.475, -1, 0.06], # 1966 midterm elections
#     [0.39, 0.435, 0, 0], # nixon v humphrey 1968
#     [0.53, 0.47, 1, -0.34], # 1970 midterm elections
#     [0.3525, 0.605, -1, 0.97], # nixon v mcgovern 1972
#     [0.60, 0.40, 1, -0.63], # 1974 midterm elections
#     [0.4825, 0.4375, 0, 0], # carter v Ford 1976
#     [0.55, 0.45, -1, -0.14], # 1978 midterm elections
#     [0.400, 0.4133, 1, -1], # carter v reagan 1980 
#     [0.55, 0.45, 1, -0.56], # 1982 midterm elections.
#     [0.3885, 0.5628, -1, 0.96], #  mondale vs reagan 1984
#     [0.4175, 0.505, 0, 0], # dukakis v HW Bush 1988
#     [0.54, 0.46, 1, -0.13], # 1990 midterm elections
#     [0.465, 0.354, -1, -0.22], # Clinton v HW bush 1992 
#     [0.465, 0.535, -1, 0.30], # midterm elections 1994 
#     [0.5219, 0.36125, 1, 0.78], # clinton vs dole 96'
#     [0.49, 0.51, -1, 0.54], # midterm elections 1998
#     [0.4382, 0.4694, 0, 0], # gore vs Bush 00'
#     [0.45, 0.496, 1, 0.06], # midterms 02' house generic ballot - RCP avg incumbency advantages favors democrats as bush in office
#     [0.4657, 0.5043, -1, 0.85], # kerry vs bush 04'
#     [0.406, 0.521, 1, -0.16], # midterms 06' generic ballot RCP - avg. incumbency advantage favors democrats as bush in office
#     [0.4988, 0.4338, 0, 0], # obama vs mccain 08'
#     [0.413, 0.507, -1, -0.03], # midterms 10' generic ballot RCP - avg # incumbency advantage favors republicans as obama in office
#     [0.48, 0.4656, 1, 0.12], # obama vs romney 2012
#     [0.432, 0.456, -1, 0.65], # 2014 midterms generic ballot RCP - avg # incumbency advantges favors reps as obama in office
#     [0.4733, 0.4332, 0, 0], # 16 ' clinton v trump
#     [0.497, 0.424, 1, 0.62], # 2018 midterms generic ballot rcp - avg # incumbency favors dems as trump in office
#     [0.5137, 0.435, -1, 0], # biden v trump. while economy had a recession.. it was a quick one due to mass stimulus. so only ~ -0.2
#     [0.455, 0.48, -1, -0.78] # midterms 2022 






# import torch
# import random
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import DataLoader, TensorDataset
# import sys

# #to preface, i am by no means a data scientist or a political analyst, i merely enjoy politics and coding. 
# # I would really not take this model too seriously and my data can easily be considered questionable

# #polling data sourced from wikipedia, I averaged polling percentage from september to election data.
# #  
# # dem candidate  support, rep candidate support, dem incumbency, rep incumbency, economic indicator from -1 to 1. -1 = bad, 1 = good

# torch.manual_seed(42)
# # for midterm elections, incumbency DISadvantage will be applied. i will basically just give however is out of power the 1. 
# # ive made the very debatable assumption that the economic indicator is basically irrelevant if there is no incumbent. 
# X_data = torch.tensor([
#     [0.514, 0.442, 1, 0, 0.7], # FDR vs Landon 1936
#     [0.505, 0.425, 1, 0, 0.85], #FDR vs Willkie 1940
#     [0.487, 0.45, 1, 0, 0.92], # Fdr vs Dewey 1944
#     [0.393, 0.4783, 1, 0, -0.42], # truman v dewey 1948   # historic polling miss here. 
#     [0.4114, 0.5157, 0, 0, 0], # stevenson  v eisenhower 1952
#     [0.406, 0.532, 0, 1, 0.72], # Stevenson v eisenhowever 1956
#     [0.477, 0.4723, 0, 0, 0], # JFK v Nixon 1960
#     [0.6375, 0.315, 0, 0, 0], # LBJ vs goldwater 1964
#     [0.39, 0.435, 0, 0, 0], # nixon v humphrey 1968
#     [0.3525, 0.605, 0, 1, 0.97], # nixon v mcgovern 1972
#     [0.4825, 0.4375, 0, 0, 0], # carter v Ford 1976
#     [0.400, 0.4133, 1, 0, -1], # carter v reagan 1980 
#     [0.3885, 0.5628, 0, 1, 0.96], #  mondale vs reagan 1984
#     [0.4175, 0.505, 0, 0, 0], # dukakis v HW Bush 1988
#     [0.465, 0.354, 0, 1, -0.22], # Clinton v HW bush 1992 
#     [0.5219, 0.36125, 1, 0, 0.78], # clinton vs dole 96'
#     [0.4382, 0.4694, 0, 0, 0], # gore vs Bush 00'
#     [0.4657, 0.5043, 0, 1, 0.85], # kerry vs bush 04'
#     [0.4988, 0.4338, 0, 0, 0], # obama vs mccain 08'
#     [0.48, 0.4656, 1, 0, -0.12], # obama vs romney 2012
#     [0.4733, 0.4332, 0, 0, 0], # clinton v trump
#     [0.5137, 0.435, 0, 1, -0.2] # biden v trump. while economy had a recession.. it was a quick one due to mass stimulus. so only ~ -0.2
#     ], dtype=torch.float32)

# #if dem candidates win, y =1, if rep wins y = 0
# y_data = torch.tensor([
#     [1],
#     [1],
#     [1],
#     [1],
#     [0],
#     [0],
#     [1],
#     [1],
#     [0],
#     [0],
#     [1],
#     [0],
#     [0],
#     [0],
#     [1],
#     [1],
#     [0],
#     [0],
#     [1],
#     [1],
#     [0],
#     [1]
# ]).squeeze()
 

# training_split = int(len(X_data) * 0.8)

# X_training_split, X_testing_split = X_data[:training_split], X_data[training_split:]
# y_training_split, y_testing_split = y_data[:training_split], y_data[training_split:]

# y_training_split = y_training_split.squeeze().float()
# y_testing_split = y_testing_split.squeeze().float()

# #sys.exit()


# #device = "cuda" if torch.cuda.is_available else "cpu" if you have nvidia gpu, simply include this line and delete the below line
# device = "cpu"

# class ElectionModelV0(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.layer_1 = nn.Linear(in_features=5, out_features=8)
#         self.layer_2 = nn.Linear(in_features=8, out_features=8)
#         self.layer_3 = nn.Linear(in_features=8, out_features=1)
#         self.relu = nn.ReLU()
#         self.sigmoid = nn.Sigmoid()
        

#     def forward(self, x):
#         x = self.relu(self.layer_1(x))
#         x = self.relu(self.layer_2(x))
#         x = self.layer_3(x)
#         x = self.sigmoid(x)
#         return x


# model_0 = ElectionModelV0().to(device)


# loss_fn = nn.BCELoss()
# optimizer = optim.Adam(model_0.parameters(), lr = 0.0001)

# epochs = 10000

# def accuracy_fn(y_true, y_pred):
#     correct = torch.eq(y_true, y_pred).sum().item()
#     acc = (correct/len(y_pred)) * 100
#     return acc

# train_model = True

# if train_model:
#     for epoch in range(epochs):
#     #1. Forward pass
#         y_probs = model_0(X_training_split).squeeze() # our y probability values, probability of Candidate A winning.
#         candidate_pred = torch.round(y_probs).squeeze()

#     #2. Determine the loss 
#     # loss is determined by seeing if the candidate with the higher probability of winning matches the result.
#         loss = loss_fn(y_probs, y_training_split)
#     # accuracy function is seeing the training data versus the predicted values and seeing how often it gets it right
#         acc = accuracy_fn(y_true=y_training_split,
#                       y_pred=candidate_pred)
    
#     #3. zero grad
#         optimizer.zero_grad()

#     #4. Loss backward
#         loss.backward()

#     #5. 
#         optimizer.step()

#         model_0.eval()
#         with torch.inference_mode():
#             test_y_probs = model_0(X_testing_split).squeeze()
#             test_candidate_pred = torch.round(test_y_probs).squeeze()

#             test_loss = loss_fn(test_y_probs, y_testing_split)

#             test_acc = accuracy_fn(y_true=y_testing_split, y_pred=test_candidate_pred)

#         if epoch % 1000 == 0:
#             print(f"Epoch: {epoch} | Loss: {loss}, Acc: {acc:.2f} | Test loss: {test_loss} Test accuracy: {test_acc}")
#             print(model_0.state_dict())

# if train_model:
#     torch.save(model_0.state_dict(), "election_analysis/election_modelV2.pth")
    
# loaded_model_0 = ElectionModelV0()
# loaded_model_0.load_state_dict(torch.load("election_analysis/election_modelV2.pth"))




# loaded_model_0.eval()



# with torch.inference_mode():
#     harris_v_trump = torch.tensor([
#     [39.2, 52.3, 0, 1, 0.34]
#     ])
#     new_data_prediction_probs = loaded_model_0(harris_v_trump).squeeze()
#     new_data_prediction = torch.round(new_data_prediction_probs)

#     print(f"Prediction probability: {new_data_prediction_probs}")
#     print(f"Prediction: {new_data_prediction}")
