# Multiple Sequence Alignment

### ClustalW Algorithm
Builds a dynamic programming table based on 2 given sequences and fills it based on the calculated sum of pairs scores.
Optimal alignments are identified by tracing back through the table.

### ClustalW Implementation
Takes 2 sequences and processes each alignment, tracks progress, reports intermediate and final results. 
The process is as follows:
- Build the dynamic programming table based on sequence lengths and initialize the first row and column
- Fill the table by calculating the maximum score for each cell using normalized sum of pairs
- Track alignments by tracing back through the dynamic programming table and updating a global dictionary of alignments
- Traceback only returns 1 optimal alignment