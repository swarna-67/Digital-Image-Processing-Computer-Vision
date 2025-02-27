# -*- coding: utf-8 -*-
"""Lab7-latestweight.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UDKpabCaW62BCjXLjpbOAoHesO_IJvIi
"""



##importing the necessary packages from matplot lib and pyplot to get the final plots
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import seed
from numpy.random import normal

##to ensure that random data generated is constant 
seed(2)

#create the first gaussian normal distribution with mean at 1,1 standard deviation 0.4 and data size 200
datax = np.random.normal(loc=1, scale = 0.4, size=200)
datay = np.random.normal(loc =1,scale = 0.4, size =200)

#get the data plotted 

plt.scatter(datax, datay, c = 'r')

#create the 2nd gaussian normal distribution centred at (3,2) and standard deviation 0.4 data size 200

datax1 = np.random.normal(loc = 3, scale = 0.4, size =200)
datax2 = np.random.normal(loc = 2, scale = 0.4, size = 200)
plt.scatter(datax1, datax2, c = 'b')



plt.title('Two Gaussians with minimal overlap ')

plt.show()

#################################################################
##implementing the gaussian distribution with substantial overlap

#create the first gaussian normal distribution with mean at 1,1 standard deviation 0.6 and data size 200
dataz = np.random.normal(loc=1, scale = 0.7, size=200)   ##previous 1.0 , then 0.7
dataw = np.random.normal(loc =1,scale = 0.7, size =200)

#get the data plotted 

plt.scatter(dataz, dataw, c = 'r')

#create the 2nd gaussian normal distribution with mean at 3,2 and deviation 0.6 little higher for substantial overlap

dataz1 = np.random.normal(loc = 3, scale = 0.7, size =200)
dataw2 = np.random.normal(loc = 2, scale = 0.7, size = 200)
plt.scatter(dataz1, dataw2, c = 'b')

plt.title('Two Gaussians with substantial overlap ')

plt.show()

##steps to generate the training data x, using  random generator for the same 
#in this step the data generated in the first step is converted to represent input features and bias which is used for training the perceptron 
import matplotlib.pyplot as plt
import numpy as np
import random
sample_size = 200
#convert the orientation or reshape the array so that each 
#datax and datay is a 200*1 column matrix 
datax = datax.reshape(-1,1)
datay = datay.reshape(-1,1)
#combine the 2 column array into single with 2 columns to represent 2 feautres for data ceterd at 1,1
X_combined1 = np.hstack((datax, datay))
#stores the output data with label zero 
numy1 = np.zeros(200)
numy1 = numy1.reshape(-1,1)
#stpres the data output with label one
numy2 = np.ones(200)
numy2 = numy2.reshape(-1,1)

#combine the 2 column array into single with 2 columns to represent 2 feautres for the data centered at 3,2
datax1 = datax1.reshape(-1,1)
datax2 = datax2.reshape(-1,1)

X_combined2 = np.hstack((datax1, datax2))

##concatenate to represent the final X data with 400 rows and 3 columns

X = np.concatenate((X_combined1 , X_combined2))
#thrid column added as 1 to represent the bias
zero_arr = np.ones((400,1))
X = np.hstack((X, zero_arr))
Y = np.concatenate((numy1,numy2))
print(X.shape)
print(Y.shape)
#plt.hist(nums2)
plt.show()

##before training split the available data to training set and testing set  using test train split from sklearn package
from sklearn.model_selection import train_test_split
X_train, X_test,  Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state = 42)
#always a good way to split the training to test data is in the ration 8:1
##get the dimensions of the training x and y data
print(Y_train.shape)
print(X_train.shape)
print(X_test.shape)
print(Y_test.shape)

#implement a perceptron and a gradient decent optimizer to train wieghts w1 w2 and w3 for narrow data--minimal overlap

##defines the class Perceptron that has multiple definitions for each task - training , predicting and checking the accuracy or correctness 
class Percept():
###intialization of the class by passing the self and learning rate
    def __init__(self, learning_rate ):
        self.learn = learning_rate
        self.bias = None
        self.weights = None
 #bias and weight is kept as none initially        
   
#here the weughts and bias are trained based om the epoch passed
    def train(self, X_trn, Y_trn, epoch):
   

      #initialize the weights to 3*1 array
        self.bias = 0   
        self.weights = np.zeros(3)
        
        #training and learning of the weights 
        #weight array to store the weigjts upon each iteration of the training process
        weight_arr = np.zeros((epoch, 3))

        for i in range(epoch):   ##different iterations
          #for every iteration we loop over evry row of the training data in this case with 319 rows
            for j in range(319):
            #for every row the fout is calculated as x0w0 + x1w1 + x2w3 = fout
                f_out = np.dot(X_trn[j, :], self.weights) + self.bias

                #if fout is greater than zero keep final output as 1 else 0
                if f_out > 0:
                
                  y_out = 1
                else:
                  y_out = 0
                 

                #updating the weight and bias based on diff in the actual data and prediction based on weights
                diff = Y_trn[j] - y_out
                #find the delta to calculate the updated weights and bias
                delta = self.learn*diff*X_trn[j]
                self.weights = self.weights + delta
                #print(self.weights[0])
                self.bias = self.bias + self.learn*diff
                #after updating for each row at the end of every iteration the final weigjts and bias is updated to the array 
            w1 = self.weights[0]   
            w2 = self.weights[1]
            w3 = self.weights[2]
            weight_arr[i, 0] =w1
            weight_arr[i, 1] =w2
            weight_arr[i, 2] =w3
            # print(weight_arr)
    
        #return the weight and bias for every iteration after training        
        return weight_arr, self.bias
       

#defines the prediction function where the for a given training data we find the prediction 
    def prediction(self, X_trn):
        #prediction is done based on caluclating the xowo + x1w1 + b = fout
        final_out =np.dot(X_trn, self.weights) + self.bias
        #based on fout get a final output prediction of 0 or1
        y_predn = np.where(final_out > 0. , 1, 0)

        #if final_out > 0:
         #         y_pred = 1
        #else:
         #         y_pred = 0
        #print(final_out)
        y_pred = y_predn.reshape((80,1))
        return y_pred
        
    def accuracy(self,y_actual, y_ours):
     
        
        #calulcates the length of the ypredicted to get the denominator for accuracy 
        val = len(y_ours)
        # for i in range(val):
        #   err = (y_actual[i] - y_ours[i])**2
        # mean_square = err/val
        #print(mean_square)
        #wherever the prediction and the actual output label data matches that is considered as accurate
        bool_val = y_actual == y_ours
        #print(bool_val)
        ##accruacry percentage is total correct values / total values
        num = np.sum(bool_val)
        
       
        
        acc = num / val
        #returns the accuracy 
        return acc

##Train the model  , to show variation of the model with alpha loweer learning rate 0.000006 ----->minimal overlap-> narrow data

obj = Percept(0.000006)
epoch = 2000
#defiens the epoch 
#initialize the final weigt array in numpy 
final_weight =  np.zeros((epoch, 3))
#for i in range(len(epoch)):
#for i in range(epoch):
  #final_weight[i, :], bi= obj.train(X_train, Y_train, epoch)
#calls the train function by passing training data and epoch 
final_weight, bi= obj.train(X_train, Y_train, epoch)
yp = obj.prediction(X_test)
#gets the a=prediction and accuracy on test data
result = obj.accuracy(Y_test, yp)
result = result*100
  
#print sthe bias and the accuracy on the console
#print(final_weight) ## 7 *3
print(bi)
#print(yp)
print('Accuracy on testing data is for lower learning rate %.2f%%', result)

#Graph to plot the decision boundary that classifies the two different classes

obj =Percept(0.2)
w, b = final_weight, bi

##extract the weights and bias from the perceptron function 
weight2 = w[1999,0]
weight1= w[1999,1]
bias = b
#defiens a maximum boundary for the x axis for plotting the graph 
x0_min = -4
x0_max = 4
#to plot the decision boundary 
prod_max = weight2 * x0_max
#calculates the slope and intercept using the weights and bias to get the final decisoon boundary 
x1_max = ( (-(prod_max) - bias) 
          / weight1 )

prod_min = weight2 * x0_min

x1_min = ( (-(prod_min) - bias) 
          / weight1 )

##use subplot from matplotlib.pyplot library 

fig, pt = plt.subplots(1, figsize=(7, 3))
#plot the grpah based on the calculated slope and intercept based on the weights w1 w2 and bias w3
pt.plot([x0_min, x0_max], [x1_min, x1_max])
#title of the plot 
plt.title("Plot for data and final decision boundary ")
#defines hte x ais and y axis
plt.xlabel("Data feature 1 ")
plt.ylabel("Data feature 2")
#scattes the test data 
plt.scatter(X_test[:, 0], X_test[:, 1], marker="+", c=Y_test)


plt.show()



### to show variation  of weights with lower learning rate----->minimal overalap -  narrow data
#impor the necessary pacakage 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#initalize the y axis data that represents the number of iterations 
epoch = epoch+1
final_weight = final_weight
y_val = np.arange(1, 2001)      #reshape(-1, 1)
# print(y_val)
# print(final_weight.shape)



##print(data)

# Create a DataFrame for the data to plot using weights y axis  and training iteration in x axis 
td = pd.DataFrame({'Training iterations': y_val,
                    'Weight 1': final_weight[:, 0],
                    'Weight 2': final_weight[:, 1],
                    'Weight 3': final_weight[:, 2]})
#df = pd.DataFrame(data, columns=['Weight1', 'Weight2', 'Weight3'])
# Create a line plot of the weights over training iterations
td.plot(kind='line', x='Training iterations', y=['Weight 1', 'Weight 2', 'Weight 3'])
#td.title('Behaviour of weigjts with training iterations')
plt.title("Plot for training weights vs iterations ")
#displays the plot 
plt.show()

#Train the model  , to show variation of the model with alpha higer learning rate 0.6 ----->minimal overlap-> narrow data

obj =Percept(0.2)
epoch = 2000
#defiens the epoch 
#initialize the final weigt array in numpy 
final_weight =  np.zeros((epoch, 3))
#for i in range(len(epoch)):
#for i in range(epoch):
#calls the train function by passing training data and epoch

final_weight, bi= obj.train(X_train, Y_train, epoch)
yp = obj.prediction(X_test)
#gets the a=prediction and accuracy on test data
result = obj.accuracy(Y_test, yp)
result = result*100



#print sthe bias and the accuracy on the console
print(bi)
print('Accuracy on training %.2f%%', result)

### to show variation  of weights with higher learning rate----->minimal overalap -  narrow data
#impor the necessary pacakage 

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#initalize the y axis data that represents the number of iterations
epoch = epoch+1
final_weight = final_weight
y_val = np.arange(1, 2001)      #reshape(-1, 1)
# print(y_val)
# print(final_weight.shape)


# Create a DataFrame for the data to plot using weights y axis  and training iteration in x axis 
td = pd.DataFrame({'Training iterations': y_val,
                   'Weight 1': final_weight[:, 0],
                   'Weight 2': final_weight[:, 1],
                   'Weight 3': final_weight[:, 2]})

# Create a line plot of the weights over training iterations
td.plot(kind='line', x='Training iterations', y=['Weight 1', 'Weight 2', 'Weight 3'])
plt.title("Plot for training weights vs iterations ")
##displays the final plot as shown below 
plt.show()

"""TRAINING OF THE PERCEPTRON AND WEIGHTS FOR THE MORE OVERLAPPING DATA ----WIDE DATA"""

##steps to generate the training data x, using  random generator for the same 
#in this step the data generated in the first step is converted to represent input features and bias which is used for training the perceptron 
sample_size = 200
#convert the orientation or reshape the array so that each 
#datax and datay is a 200*1 column matrix 
dataz = dataz.reshape(-1,1)
dataw = dataw.reshape(-1,1)
#combine the 2 column array into single with 2 columns to represent 2 feautres for data ceterd at 1,1
X_combined1 = np.hstack((dataz, dataw))
#stores the output data with label zero 
numy1 = np.zeros(200)
numy1 = numy1.reshape(-1,1)
#stores the output data with label one 
numy2 = np.ones(200)
numy2 = numy2.reshape(-1,1)
dataz1 = dataz1.reshape(-1,1)
dataw2 = dataw2.reshape(-1,1)
#combine the 2 column array into single with 2 columns to represent 2 feautres for the data centered at 3,2

X_combined2 = np.hstack((dataz1, dataw2))

##concatenate to represent the final X data with 400 rows and 3 columns

X = np.concatenate((X_combined1 , X_combined2))
#thrid column added as 1 to represent the bias
zero_arr = np.ones((400,1))
X = np.hstack((X, zero_arr))
Y = np.concatenate((numy1,numy2))
print(X.shape)
print(Y.shape)

plt.show()

##before training split the available data to training set and testing set  using test train split from sklearn package
from sklearn.model_selection import train_test_split
X_train, X_test,  Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state = 100)
#always a good way to split the training to test data is in the ration 8:1
##get the dimensions of the training x and y data
print(Y_train.shape)
print(X_train.shape)
print(X_test.shape)
print(Y_test.shape)

#implement a perceptron and a gradient decent optimizer to train wieghts w1 w2 and w3 for wide data--large overlap

##defines the class Perceptron that has multiple definitions for each task - training , predicting and checking the accuracy or correctness 
class Percept():
###intialization of the class by passing the self and learning rate
    def __init__(self, learning_rate ):
        self.learn = learning_rate
        self.bias = None
        self.weights = None
 #bias and weight is kept as none initially        
   
#here the weughts and bias are trained based om the epoch passed
    def train(self, X_trn, Y_trn, epoch):
   

      #initialize the weights to 3*1 array
        self.bias = 0  
        self.weights = np.zeros(3)
       
        #training and learning of the weights 
        #weight array to store the weigjts upon each iteration of the training process
        weight_arr = np.zeros((epoch, 3))

        for i in range(epoch):   ##different iterations
          #for every iteration we loop over evry row of the training data in this case with 319 rows
            for j in range(319):
            #for every row the fout is calculated as x0w0 + x1w1 + x2w3 = fout
                f_out = np.dot(X_trn[j, :], self.weights) + self.bias
                
                #if fout is greater than zero keep final output as 1 else 0
                if f_out > 0:
                
                  y_out = 1
                else:
                  y_out = 0
                 

                #updating the weight and bias based on diff in the actual data and prediction based on weights
                diff = Y_trn[j] - y_out
                #find the delta to calculate the updated weights and bias
                delta = self.learn*diff*X_trn[j]
                self.weights = self.weights + delta
                #print(self.weights[0])
                self.bias = self.bias + self.learn*diff
                #after updating for each row at the end of every iteration the final weigjts and bias is updated to the array 
            w1 = self.weights[0]   
            w2 = self.weights[1]
            w3 = self.weights[2]
            weight_arr[i, 0] =w1
            weight_arr[i, 1] =w2
            weight_arr[i, 2] =w3
            # print(weight_arr)
    
        #return the weight and bias for every iteration after training        
        return weight_arr, self.bias
       

#defines the prediction function where the for a given training data we find the prediction 
    def prediction(self, X_trn):
        #prediction is done based on caluclating the xowo + x1w1 + b = fout
        final_out =np.dot(X_trn, self.weights) + self.bias
        #based on fout get a final output prediction of 0 or1
        y_predn = np.where(final_out > 0. , 1, 0)

        #if final_out > 0:
         #         y_pred = 1
        #else:
         #         y_pred = 0
        #print(final_out)
        y_pred = y_predn.reshape((80,1))
        return y_pred
        
    def accuracy(self,y_actual, y_ours):
     
        
        #calulcates the length of the ypredicted to get the denominator for accuracy 
        val = len(y_ours)
        # for i in range(val):
        #   err = (y_actual[i] - y_ours[i])**2
        # mean_square = err/val
        #print(mean_square)
        #wherever the prediction and the actual output label data matches that is considered as accurate
        bool_val = y_actual == y_ours
        #print(bool_val)
        ##accruacry percentage is total correct values / total values
        num = np.sum(bool_val)
        
       
        
        acc = num / val
        #returns the accuracy 
        return acc

##Train the model  , to show variation of the model with alpha 0.1 higj learning rate  ----->wider data high overlap

obj =Percept(0.2)
epoch = 2000
#defiens the epoch 
#initialize the final weigt array in numpy 
final_weight =  np.zeros((epoch, 3))
#for i in range(len(epoch)):
#for i in range(epoch):
#calls the train function by passing training data and epoch

final_weight, bi= obj.train(X_train, Y_train, epoch)
yp = obj.prediction(X_test)
#gets the a=prediction and accuracy on test data
result = obj.accuracy(Y_test, yp)
result = result*100



#print sthe bias and the accuracy on the console
print(bi)
print('Accuracy on training %.2f%%', result)

##to plot the final decision boundary for substantial overlap - wide data with higjer learining rate


w, b = final_weight, bi

##extract the weights and bias from the perceptron function 
weight2 = w[1999,0]
weight1= w[1999,1]
bias = b
#defiens a maximum boundary for the x axis for plotting the graph 
x0_min = -3
x0_max = 3
#to plot the decision boundary 
prod_max = weight2 * x0_max
#calculates the slope and intercept using the weights and bias to get the final decisoon boundary 
x1_max = ( (-(prod_max) - b) 
          / weight1 )

prod_min = weight2 * x0_min

x1_min = ( (-(prod_min) - b) 
          / weight1 )

##use subplot from matplotlib.pyplot library 

fig, pt = plt.subplots(1, figsize=(7, 3))
#plot the grpah based on the calculated slope and intercept based on the weights w1 w2 and bias w3
pt.plot([x0_min, x0_max], [x1_min, x1_max])
#title of the plot 
plt.title("Plot for data and final decision boundary ")
#defines hte x ais and y axis
plt.xlabel("Data feature 1 ")
plt.ylabel("Data feature 2")
#scattes the test data 
plt.scatter(X_test[:, 0], X_test[:, 1], marker="+", c=Y_test)


plt.show()

### to show variation  of weights with alpha 0.1----->high overalap -  wider data

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#initalize the y axis data that represents the number of iterations
epoch = epoch+1
final_weight = final_weight
y_val = np.arange(1, 2001)      #reshape(-1, 1)
# print(y_val)
# print(final_weight.shape)


# Create a DataFrame for the data to plot using weights y axis  and training iteration in x axis 
td = pd.DataFrame({'Training iterations': y_val,
                   'Weight 1': final_weight[:, 0],
                   'Weight 2': final_weight[:, 1],
                   'Weight 3': final_weight[:, 2]})

# Create a line plot of the weights over training iterations
td.plot(kind='line', x='Training iterations', y=['Weight 1', 'Weight 2', 'Weight 3'])

##displays the final plot as shown below 
plt.title("Plot for training weights vs iterations ")
plt.show()

##Train the model  , to show variation of the model with lower learning rate -> alpha 0.0000004 ----->wider data--high overlap


#obj = Percept(0.000000000004)
obj = Percept(0.000006)
epoch = 2000
#defiens the epoch 
#initialize the final weigt array in numpy 
final_weight =  np.zeros((epoch, 3))
#for i in range(len(epoch)):
#for i in range(epoch):
  #final_weight[i, :], bi= obj.train(X_train, Y_train, epoch)
#calls the train function by passing training data and epoch 
final_weight, bi= obj.train(X_train, Y_train, epoch)
yp = obj.prediction(X_test)
#gets the a=prediction and accuracy on test data
result = obj.accuracy(Y_test, yp)
result = result*100
  
#print sthe bias and the accuracy on the console
#print(final_weight) ## 7 *3
print(bi)
#print(yp)
print('Accuracy on testing data is for lower learning rate %.2f%%', result)

## to show variation  of weights with alpha 0.1 ----->substantial overalap -  wider data

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#initalize the y axis data that represents the number of iterations
epoch = epoch+1
final_weight = final_weight
y_val = np.arange(1, 2001)      #reshape(-1, 1)
# print(y_val)
# print(final_weight.shape)

# Create a DataFrame for the data to plot using weights y axis  and training iteration in x axis 

td = pd.DataFrame({'Training iterations': y_val,
                   'Weight 1': final_weight[:, 0],
                   'Weight 2': final_weight[:, 1],
                   'Weight 3': final_weight[:, 2]})

# Create a line plot of the weights over training iterations
td.plot(kind='line', x='Training iterations', y=['Weight 1', 'Weight 2', 'Weight 3'])
plt.title("Plot for training weights vs iterations ")

# Show the plot
plt.show()

