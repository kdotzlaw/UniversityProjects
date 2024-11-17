# Neighbour Joining

## Process
- Preprocessing: Read a distal matrix file and returns the list of taxa names and a distance matrix of key-value pairs: `{(taxa1,taxa2):distance}`
- Unions the distance for each taxon in given list based on the distance matrix
- Create a delta matrix which is used to determine which taxa need to be pulled away at each step
- Perform neighbour joining recursively:
    - Determine which taxa to pull away using delta matrix
    - Calculate branch lengths for the pull-away taxa