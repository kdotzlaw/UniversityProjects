# Recognizing Temporal Patterns using an Echo State Network
A custom **Python** implmentation of a recurrent neural network that analyzes timeseries data using **matplotlib** amd **numpy**.
Created for Machine Learning at the University of Manitoba.

### Echo State Network
An Echo State Network is a type of recurrent neural network used to recognize temporal patterns like K-Step Ahead Forcasting. Specifically, ESNs use backpropagation to feed optimized hyperparameters back into its recurrent internal state. 

### K-Step Ahead Forcasting
K-Step Ahead Forcasting predicts the value of the timeseries data k timesteps ahead of the current time t. In this implementation,
I use Mean-Square Error to determine prediction accuracy.
K-Step Ahead Forcasting is used in both the validation stage and testing stage of model evaluation.

## Process
For a detailed description of the process of model training and evaluation,  [view the notebook](ESN.ipynb).


Essentially, **batch training** is done using a subset of the original dataset using input weights, recurrent weights, a sigmoid activation function, and the total number of hidden layer neurons to find the states and then **ridge regression** is used to calculate the optimized weights.
**Cross-Validation** is done on a subset of the original data, where hyperparameters are optimized and the error of the model is calculated via **mean-square error**.
K-Step Ahead Forcasting is done in both the validation and testing stages, where 1 step is used to evaluate hyperparameters and k>1 steps is used to calculate model predictions.


## Results 

### Evaulation of 2Sine Timeseries Data
The model is trained with 50 hidden neurons and a regularization parameter of 0.5.
- The optimized number of hidden layer neurons was found to be 10
- The optimized regularization parameter was found to be 5.0
- The optimized data split (ie the split with lowest MSE) was found to be 40/30/30 (training/validation/testing)
- 1-Step Ahead Prediction had a MSE of 0.142, indicating that the model generalizes well
- 2-Step Ahead Prediction had a MSE of 1.24, demonstrating that error compounds overtime
- Predictions with k>2 had higher MSEs and were less accurate the more steps ahead 
  
### Evaluation of Lorenz Timeseries Data
The model is trained using 20 hidden neurons and a regularization parameter of 0.1.
- The optimized number of hidden layer neurons was found to be 10
- The optimized regularization parameter was found to be 0.01
- The optimized data split (ie the split with the lowest MSE) was found to be 80/10/10 (training/validation/testing)
- 1-Step Ahead Prediction had a MSE of 7.626, likely because the dataset varies more than the 2Sine dataset though the predictions and targets look visually similar
- 2-Step Ahead Prediction had a MSE of 111.611, indicating that error compounds overtime
- Predictions with k>2 had higher MSEs and were less accurate the more steps ahead
  
## Conclusions
- The Lorenz model demonstrates that increased model complexity leads to overfitting and a failure to generalize, as its data points had higher varience and its function was more complex compared to the 2Sine dataset. Additionally, the complexity of the Lorenz function causes a smaller regularization parameter, causing outliers to significantly affect weight optimizations.
- K-Step Ahead prediction produces less accurate results the more steps ahead you attempt to predict because error compounds overtime and predictions are fed back into the model.
  
