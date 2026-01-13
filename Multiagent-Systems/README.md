# Effective Communication Techniques in 2D Multi-Agent Systems

## Abstract

Communication in multi-agent systems is vitally important for agents to continually update their incomplete views allowing them to efficiently execute actions throughout the system environment. 
The chosen communication protocol will affect decision making and therefor the level of expected performance.  
Using a selected set of success criteria which includes the necessity of communication, information space allotment, value calculations and dealing with common communication problems, 
both cognitive communication techniques and reinforcement learning techniques were compared.  After analyzing both cognitive communication techniques and reinforcement learning techniques, 
and evaluating all techniques using the success criteria outlined, it can be conclusively stated that reinforcement learning is the most effective communication technique. 

### 2D Multi-Agent Systems

#### Common Communication Problems
Common communication problems include the following:

##### The Hidden State Problem
As described by McCallum, the hidden state problem occurs when the next action taken by an agent depends on hidden information that is not known to the agent. McCallum 
states that identifying hidden information requires that agents have longer training periods. 

##### The Credit Assignment Problem
According to Metaric, Fu and Anderson, the credit assignment problem occurs when feedback is given at the end of an action sequence and agents are unable to assign credit to the correct action.

#### Reinforcement Learning
Metaric and Anderson et al. describe reinforcement learning as a method of allowing agents to receive feedback based on the outcome of their actions, where rewards and
punishments are determined by the environment.
Hasinoff differentiates between two types of reinforcement learning: agents that learn the policy directly and agents that traverse policy space directly.
Methods used in reinforcement learning include learning using the Value over States Function (VVSF), direct policy traversal, and Gradient Ascent.

#### Cognitive Communication
An agent in a system encounters one or more types of uncertainty which is addressed via communication.
Cognitive communication techniques include the Myopic approach, the Centralized approach and Decentralized approach.

##### Myopic Cognitive Communication
According to Becker et al., a Myopic algorithm deals with uncertainty by finding at least one optimal solution using two myopic assumptions:
sources of information are isolated and should be evaluated in isolation, and sequential decisions should be made in a 1-step horizon.
This approach is effective at evaluating the value of information in single agents.

##### Non-Myopic Cognitive Communication
Non-myopic communication techniques include both the centralized and decentralized approaches.
As described by Xuan and Lesser, centralized policies idenfity the decisions of agents regarding the overall system state.
Contrastly, Xuan and Lesser describe decentralized policies as those that are required to only assume partial system knowledge in each agent, causing each agent to deal with communication directly.
Xuan and Lesser differentiate between the centralized and decentralized approaches by stating that agents using a decentralized policy do not observe the global state automatically, while centralized agents use the global
state as the starting point for their decision making.


## Evaluation
There are 4 criteria that were used to evaluate the effectiveness of the communication techniques.  In order to determine the most effective communication technique, I assign points to each criterion so 
quantitatively, the higher the points, the more effective the communication technique is.
A maximum of 6 points can be awarded in total.

#### Choice to Communicate:

1 point is awarded if the policy allows agents to choose when to communicate. 0 points is given if agents are not allowed to choose when to communicate.

#### Information Space Allotment
If the space required to store information is low, the policy recieves 2 points. If the space required to store information  is medium, the policy recieves 1 point. If the space required to store information is high, the policy recieves 0 points.

#### Value Calculations
If the policy does any type of value calculation, it receives 1 point. No points are given if the policy does not do any type of value calculation.

#### Solutions to Common Communication Problems
If the policy solves more than one common communication problems, it receives 2 points. If the policy solves only one common communication problem, it receives 1 point. If the policy does not solve any common communication problems, it receives 0 points.

### Results

| Communication Technique | Choice to Communicate | Information Space Allotment | Value Calculations | Solutions to Common Communication Problems | Total |
| --- | --- | --- | --- | --- | --- |
| Reinforcement Learning | 1 | 1 | 1 | 2 | 5 |
|Myopic Cognitive Communication | 1 | 1 | 1 | 0 | 3 |
|Non-Myopic Cognitive Communication | 1 | 0 | 1 | 0 | 2 | 
|Centralized Cognitive Communication | 1 | 0 | 1 | 0 | 2 |
|Decentralized Cognitive Communication | 1 | 0 | 1 | 0 | 2 |
| Cognitive Communication (maximum) | 1 | 1 | 1 | 0 | 3 |



## Conclusion
Reinforcement learning is the most effective communication technique.