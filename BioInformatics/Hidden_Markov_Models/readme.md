# Hidden Markov Models (HMMs)

Uses an emission probability matrix, a transition probablity sequence, an output sequence that uses the same alphabet as the emission probability matrix, and an implementation of the Forward Algorithm to determine the total probabilty that the output sequence is produced by the HMM.

## HMMs
HMMs are a stochastic model that have the Markov property of memorylessness (ie that the probability of going to the next state only depends on the current state) and have hidden states.

An HMM consists of:
- A set of abstract states
- An alphabet of output tokens
- A transition probabilty matrix, where each cell is the probabilty of going from state i to state j
- An emission probability matrix, where each cell is the probabilty of a state i emitting an output token


## The Forward Algorithm
The Forward Algorithm calculates the total probability that a given output sequence is produced by the HMM.
Given:
- `x1...xn`: an output sequence 
- `s`: a state in the HMM states
- `F[s,t]`: he probability of emitting x1...xt (t < n) by a path that ends in state s
Now, the forward algorithm is recursively called to determine `F[E,n]` where `E` is the end state using `F[s,t]`.
`F[s,t]` is recursively calculated as follows:
- If s is the start state AND t = 0, `F[s,t]` is 1
- If either (but not both) s is the start state OR t = 0, then `F[s,t]` is 0
- Otherwise (the recursive case): `F[s,t]=` `Es,xt` * the sum of all k that can transition to s `(Tk,s * Forward[k,t-1])`, where `F[k,t-1]` is the probability that we were at state k in the previous step

The total probability that the output sequence is produced by the HMM is located in the last cell of the dynamic programming table.


### Implementation
- Read in transition and emission matrices as dataframes
- Initialize the original dynamic programming table
- Call the forward algorithm:
    - For index of the output sequence (index = 1 to length-1):
        - For each state s that emits output at position index:
            - Set the sum to 0
            - For each state k with k transitioning to s
                - Recursively calculate the sum with: `sum+=F[k,index-1] * TransitionMatrix[k,s]`
            -  Update dynamic programming table: `F[s,index] = sum * EmissionMatrix[s, output at position index]`
            - If the state is 'E' , the end state has been reached and the total probability of the HMM producing the sequence and the calculated dynamic programming table are returned.

