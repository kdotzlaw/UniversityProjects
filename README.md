# University Projects
A collection of various projects done during my bachelor's of Computer Science at the University of Manitoba.

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


## [Blockchain](Blockchain)
A distributed computing application that builds and validates a blockchain by requesting blocks from peers. This application was built in Python and uses Socketsto send requests and receive responses from peers. It purely
builds and validates the blockchain. There is no block mining implemented because other peers on the network mined blocks faster than the local application could.
- On joining the network, a keep_alive ping is sent to 3 random peers and is repeated every 30 seconds
- Blocks are requested round-robin from all peers with the longest chain
- Announced blocks are stored globally and added to chain after its built
- Each block is individually validated when its received
- The chain is validated end-to-end before sending it to a peer
- The consensus process is done every 2 minutes to ensure the application blockchain remains synched with the network longest chain
Created for a Distributed Computing course at the University of Manitoba.

## [2D Multiagent Systems Communication Evaluation](Multiagent-Systems)
A research project on efficent methods of communication of 2D multiagent systems. Each method was evaluated based on its ability to determine the necessity of communication, information space allotment, value calculations, and dealing with common communication problems.

Created for an introductory AI course at the University of Manitoba.

## [BioInformatics](BioInformatics)
A collection of various python code that explores bioinformatic algorithms and concepts.
Created during a BioInformatics course at the University of Manitoba.

### [Pattern Matching with Brute Force & Knuth-Morris-Pratt](BioInformatics/Pattern_Matching)
Compares a brute force method of pattern matching to the Knuth-Morris-Pratt bioinformatic algorithm by examining runtime of identifying patterns to the Sorangium cellulosum genome.

### [Multiple Sequence Alignment with ClustalW](BioInformatics/Multiple_Sequence_Alignment)
Uses the bioinformatic algorithm ClustalW to build a dynamic programming table based on 2 given sequences, fill each cell based on the calculated sum of pairs score, and return optimal alignments determined via traceback.

### [Neighbour Joining](BioInformatics/Neighbour_Joining/)
A recursive bioinformatic algorithm that uses a matrix of taxa pairs and the associated distance to determine which taxa need to be pulled away and form a cherry.

### [Hidden Markov Models](BioInformatics/Hidden_Markov_Models)
An implementation of a stochastic model with the Markov property that uses a transition matrix, an emission matrix, the forward algorithm, and an output sequence
to determine the total probability that the given output sequence is produced by the model.


## [Computer Security](ComputerSecurity/)

A collection of various assignments done in a Computer Security course at the University of Manitoba using Python, SQL, C, and Linux.

### [Encryption and Decryption](ComputerSecurity/rsa)

A comparison between CBC encryption and ECB encryption on a given image, and a demonstration of  RSA encryption and decryption on given text.

### [Buffer Overflow Exploit & Address Randomization](ComputerSecurity/buffer-overflow)
An experiment to determine the impact of address randomization on buffer overflow exploits, and a demonstration of a buffer overflow exploit.

### [Environment Variables](ComputerSecurity/env-vars)
A demonstration of environment variable manipulation in Linux, including passing environment variables between processes. Additionally explores the PATH environment variable and how it affects SUID programs.

### [SQL Injection](ComputerSecurity/SQL-injection)
Demonstrates  SQL injection attacks on a website using both CMD and website user input to perform injections. SQL injections include injection via `SELECT`, appending a new SQL statement to user input, and injection via `UPDATE`.

### [SYN Flooding & SYN Cookie Countermeasure](ComputerSecurity/SYN-flooding)
Demonstrates a SYN flooding attack and SYN cookie countermeasure using docker containers to simulate a victim and an attacker.
