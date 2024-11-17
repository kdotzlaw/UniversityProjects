# Neighbour Joining

## Process
- Preprocessing: Read a distal matrix file and returns the list of taxa names and a distance matrix of key-value pairs: `{(taxa1,taxa2):distance}`
- Union the distance for each taxon in given list based on the distance matrix, which creates the UTable
- Create a delta matrix which is used to determine which taxa need to be pulled away at each step
-  Delta matrix values are calculated using the formula: `delta_ij = (N-2) * dist_ij - Ui - Uj`, where:
    - `dist_ij` is distance matrix at key where key is (taxa1, taxa2)
    - `N` is the number of taxa
    - `Ui` is UTable at key 0
    - `Uj` is UTable at key 1
- Perform neighbour joining recursively: 
    1. Find the key (taxa1=i,taxa2=j) that gives the minimum value of delta
    2. Pull away key(i,j) & form a cherry with parent (ij)
    3. calulate distance from i,j to parent ij using:
        - `D(i,p) = 0.5 * D(i,j) + D(j,k) + [(Ui - Uj)/(N-2)]`
        - `D(j,p) = D(i,j) - D(i-p)`
    4. calculate all distances from nodes k to parent ij (where k is not i or j) using `D(k,p) = 0.5 * [D(i,k) + D(j,k) - D(i,j)] for all k (k not i or j)`
    5. Go back to step 2 with key (p)
    6. Base Case: empty or 3 branches left (use Fitch-Margoliash)
    
