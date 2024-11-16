# University Projects

## [Query Optimization](QueryOptimization.pdf)
Wrote and optimized queries for Databases 2 at the University of Manitoba.
- Compared non-optimized SQLite queries to queries optimized with non-clustering B+ tree indexes, covering indexes, and partial indexes.
- Analyzed storage space and pages used per database entry.
- Optimizating with indexes reduced the amount of unused bytes on pages, and queries with covering indexes had consistently faster runtimes.
- Data skewing typically caused indexes on single columns to have a significantly worse runtime, although queries that selected a smaller subset of data performed well with single column indexes.

## [Echo State Network (ESN)](ESN-MachineLearning/ESN.ipynb)
Implemented an Echo State Network, evaluated the impact of hyperparameters on the results, and examined the effects of K-Step Ahead Forcasting on model performance. Created for Machine Learning at the University of Manitoba.
- Trained model using batch training, sigmoid activation function, and a training dataset (a subset of the original dataset).
- Optimized weights using ridge regression and hyperparameter tuning.
- Used cross validation on the validation dataset (a subset of the original dataset), optimized the number of hidden layer neurons, the amount of training data used to train the model, and the regularization parameter. Evaluated error using Mean-Square Error (MSE) and K-Step Ahead Prediction.
- Resulting model has predicted values very close to actual values for both datasets using 1-Step Ahead Prediction. The further you forcast (ie the larger the K-Step), the less accurate the results because of needing to use prediction data instead of training data and error compounds.

## [Blockchain](Blockchain/a3.py)
