# Brute Force vs Knuth-Morris-Pratt Pattern Matching

## The KMP Algorithm
Uses a pointer for the index of the sequence and a pointer for the index of the pattern. When the characters at both pointer positions match, both pointers move forward. Otherwise, reset the pattern pointer to the last value in the table.

### Preprocessing
- Verify that there is enough table entries to find the pattern

### Brute Force Implementation
- Compare the given sequence to a given pattern at all possible starting positions
- Returns the total number of matches and the time taken for the search

### KMP Implementation
- At each step, check if there is a partial match between the `sequence[sIndex+pIndex]` and `pattern[pIndex]`
- If there is, increment pattern index counter
- If there isn't, there is either a full match or a mismatch, and the text pointer is moved
    - If there is a full match, increment matches tracker
    - If there is a mismatch, reset pattern index
- Returns the number of matches in the forward strand, the number of matches in the complement strand, and the time taken for the search

## Discussion
1. **The GC-content is an important statistic that is often calculated on genomes. It is
simply the percentage of guanines (G) and cytosines (C) in the genome. In other
words, it is equal to `(G + C)/(A + C + G + T ) ∗ 100`. Knowing that the genome
of Sorangium cellulosum is 13,033,779 bps long, you can easily calculate the GC-
content using the program that you have just built. It is actually possible to get
the GC-content in only one run of the program.**
    
    a) **What is the single query that you have to make to get both the total number
        of Cs and Gs at the same time? Why does it work?**
        
        Since the program finds matches with both the original sequence and the reverse complement, the pattern used in the query would be either `G` or `C`. For example, the query could be: `python A1.py Sorangium_cellulosum.fasta G` . This works because the program first counts all matches of G in the sequence. This gives us **4649278** matches of G. Then it counts the matches of G in the reverse complement sequence, 
        which would occur where C is in the original sequence (since G’s nucleotide pair is C). This gives us **4649278** matches of G which are actually instances of C in the original sequence. Adding the results together gives the total number of Gs and Cs, which is **9298556**.
    
    b) **What is the GC-content of this genome?**
        
        Using the query from the previous question results in **9298556**. So the GC-content of this genome is `(9298556) / 13033779) * 100  = 71.34197994%`

2. **Using your program, search for the following pattern in the Sorangium cellulosum
genome: AACGTT.**

    a) **Are you seeing anything special with the number of matches that you are
        getting? If you notice something interesting, explain what it is.**

        Yes, this pattern returns an even 400 matches, which is unique from the results of other patterns I’ve tried matching (none of the ones I tried ended in 0).

    b) **If your answer to the previous questions was yes, can you explain why this is
        happening (or is it just a coincidence)?**

        This could indicate that this pattern codes for a pair of amino acids  that appear commonly in the DNA sequence, since amino acids are made up of 3 nucleotides. 

3. **When you test the two different algorithms with different patterns on the Sorangium
    cellulosum genome, you can see that the duration of the search varies. Of course
    there is a natural variation in the actual runtimes when you run the same search mul-
    tiple times in a row (maybe approximately ±0.5 seconds). However there are some
    patterns that can be searched significantly faster than others with KMP (compared
    to the brute-force approach).**

    a) **Find a pattern that runs significantly (i.e. more than just 1-2 seconds) faster
    using the KMP algorithm. Hint: you can try patterns that contain only the
    same type of nucleotide.**

        `CCCC` is a pattern that runs significantly faster with KMP (~20.45s) than with Brute Force (~30.11s).

    b) **Based on your understanding of how KMP works, and based on what you now
    know of the Sorangium cellulosum genome, explain why that pattern that you
    mentioned above can be searched more quickly with KMP.**

        The Sorangium Cellulosum genome has a 71% GC content, which could mean that the  pattern CCCC is repeated often. 
        The worst case of the brute force algorithm occurs when there’s a mismatch at the last spot in the pattern, causing
        the algorithm to search through the entire sequence and entire pattern. 
        KMP never rechecks previously matched characters and uses information discovered about those matched characters 
        when doing comparisons. When there is a mismatch, KMP tries to find the longest suffix of the pattern that is 
        also a prefix of the pattern and moves the pattern index based on it. KMP doesn't move the text index by 1 like in 
        brute force, instead it moves j based on the pattern index and table values. 