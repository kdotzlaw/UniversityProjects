import Bio
import Bio.SeqIO
import numpy
import sys

### Global variables ###
sequencesDict = {}  # a dictionary mapping a sequence/alignment name to its sequence(s).
# Sequence(s) are stored as a list --> will be useful for representing alignments (multiple sequences aligned)
# These 3 costs are getting populated in the main, this is just their initialization:
matchCost = 0
mismatchCost = 0
gapCost = 0


def processAlignmentOrder(alignOrder):
    """This method manages the alignment process based on the alignment order received as a parameter.

    Parameters
    ----------
    alignOrder : str
    
        A string representing the order of the alignments to be processed (i.e. the first line in the input file).
        In this string, the alignments are separated by commas (e.g. A-B,C-D,E-F,...).
        An alignment is represented by the name of the two sequences/alignments to be aligned separated by a dash.
        (e.g. A-B is the alignment between sequences A and B, and AB-CD is the alignment between alignments AB and CD, etc.).
    """
    # parse
    alignList = alignOrder.split(',')
    for i in range(len(alignList)):
        trackKey = alignList[i]
        split = alignList[i].split('-')
        clustalW(split[0], split[1])


def clustalW(seqName1, seqName2):
    """This method processes each alignment and prints the progress and intermediate/final results. It calls the buildTable, fillTable, traceback and printAlignment methods.
    The resulting alignment (represented as a list of strings) will be stored in the sequencesDict using the concatenated seqNames as the key 
    (e.g. aligning A-B will result in the alignment named AB).

    Parameters
    ----------
    seqName1 : str
        The name of the first sequence/alignment to be aligned (note: this corresponds to a key in sequencesDict).

    seqName2 : str
        The name of the second sequence/alignment to be aligned (note: this corresponds to a key in sequencesDict).

    """
    print("Working on aligning: " + seqName1 + " with " + seqName2)
    # remember that sequencedict is GLOBAL
    print("Aligning " + seqName1)
    for i in range(len(sequencesDict[seqName1])):
        print(sequencesDict[seqName1][i])
    print("Aligning " + seqName2)
    for i in range(len(sequencesDict[seqName2])):
        print(sequencesDict[seqName2][i])
    # call methods
    table = buildTable(len(sequencesDict[seqName1][0]) + 1, len(sequencesDict[seqName2][0]) + 1)
    # print(table)
    filled_table = fillTable(table, sequencesDict[seqName1], sequencesDict[seqName2])
    print(filled_table)
    #print(sequencesDict[seqName1], sequencesDict[seqName2])
    alignment = traceback(filled_table, sequencesDict[seqName1], sequencesDict[seqName2])
    # update dictonary
    sequencesDict[seqName1 + seqName2] = alignment
    # print(sequencesDict)
    print("-------Resulting alignment: " + seqName1 + seqName2)
    printAlignment(alignment)


def buildTable(lenSeqs1, lenSeqs2):
    """This method builds the dynamic programming table (a numpy array) and initializes the first row and first column.

    Parameters
    ----------
    lenSeqs1 : int
        The length of the sequence/alignment of the first group to be aligned (note: a group can be either one sequence or the result of a previous alignment).

    lenSeqs2 : int
        The length of the sequence/alignment of the second group to be aligned (note: a group can be either one sequence or the result of a previous alignment).
    

    Returns
    -------
    numpy array
        The initialized table.
    """
    # initialize first row and first col with gap penalties
    if lenSeqs1 >= lenSeqs2:
        table = numpy.zeros([lenSeqs2, lenSeqs1])
        table[0][0] = 0.0
        for i in range(1, lenSeqs2):
            table[i][0] = table[i - 1][0] + gapCost
        for j in range(1, lenSeqs1):
            table[0][j] = table[0][j - 1] + gapCost
    else:
        table = numpy.zeros([lenSeqs1, lenSeqs2])
        table[0][0] = 0.0
        for i in range(1, lenSeqs2):
            table[i][0] = table[i - 1][0] + gapCost
        for j in range(1, lenSeqs1):
            table[0][j] = table[0][j - 1] + gapCost
    return table


def fillTable(table, seqsList1, seqsList2):
    # print("Begin fill table")
    """This method fills up the initialized numpy table by calculating the maximum score for each cell.

    Parameters
    ----------
    table : numpy array
        The previously initialized dynamic programming table.

    seqsList1 : list of strings
        The list of sequences of the first group to be aligned (note: a group can be either one sequence or the result of a previous alignment).

    seqsList2 : list of strings
        The list of sequences of the second group to be aligned (note: a group can be either one sequence or the result of a previous alignment).
    """
    # if sequence size is 1, only passing in single characters, else passing in pairs of char0s, pairs of char1s...
    # calc SOP for each cell: SOP result always added to diagonal. Take MAX{SOP_diagonal, gap_top, gap_left}
   # PREPROCESSING
    charList1 = [''] * len(seqsList1[0])
    charList2 = [''] * len(seqsList2[0])
    
    # build character lists
    for count in range(len(seqsList1[0])):
        for s1 in seqsList1:
            charList1[count] = charList1[count] + s1[count]
        for s2 in seqsList2:
            if count < len(seqsList2[0]):
                charList2[count] = charList2[count] + s2[count]
            else:
                break
                
    # Sum of Pairs
    for i in range(1, len(charList2) + 1):
        for j in range(1, len(charList1) + 1):
            sop = calculateSumOfPairs([charList1[j - 1]], [charList2[i - 1]])
            
            # Debug output near the cell we're interested in
            if i == 4 and j == 5:
                print(f"\nCalculating cell (4,5):")
                print(f"Characters being compared: {charList1[j-1]} with {charList2[i-1]}")
                print(f"SOP value: {sop}")
                print(f"Diagonal score would be: {table[i-1][j-1]} + {sop} = {table[i-1][j-1] + sop}")
                print(f"Top score would be: {table[i][j-1]} + {gapCost} = {table[i][j-1] + gapCost}")
                print(f"Left score would be: {table[i-1][j]} + {gapCost} = {table[i-1][j] + gapCost}")
            
            if sop == 1:
                table[i][j] = table[i - 1][j - 1] + sop
            else:
                diagonal = table[i - 1][j - 1] + sop
                top = table[i][j - 1] + gapCost
                left = table[i - 1][j] + gapCost
                table[i][j] = max(diagonal, top, left)
                
            if i == 4 and j == 5:
                print(f"Final score chosen: {table[i][j]}")

    return table


def calculateSumOfPairs(charList1, charList2):
    """This method calculates a sum of pairs score normalized by the number of pairs.

        Parameters
        ----------
        charList1 : list of chars
            A list containing all the characters (nucleotides or gaps) at a certain position in the first group (if the group is just one sequence, only one character will be contained in the list).

        charList2: list of chars
            A list containing all the characters (nucleotides or gaps) at a certain position in the second group (if the group is just one sequence, only one character will be contained in the list).

        Returns
        -------
        float
            The normalized sums of pairs score.
        """
    result = 0.0
    normalize = 0
    for char1 in charList1:
        for char2 in charList2:
            for i in range(len(char1)):
                for j in range(len(char2)):
                    if char1[i]==char2[j]:
                        result+=matchCost
                    else:
                        if char1[i] == '-' or char2[j]=='-':
                            result+=gapCost
                        else:
                            result+=mismatchCost
                    normalize+=1

    return result / normalize





def printAlignment(seqsList):
    """This method just prints the alignment corresponding to a list of strings (sequences).

    Parameters
    ----------
    seqsList : list of strings
        The alignment that we want to print out to the console.
    """
    for i in range(len(seqsList)):
        print(seqsList[i])
    print("########################")

def traceback(table, seqsList1, seqsList2):
    """This method does a traceback in the completed dynamic programming table to produce an alignment.
    Only one optimal alignment is to be returned. In the case where an optimal score comes from more than one previous cell (diagonal, left, top), always prioritize,
    in this order: (1) matches/mismatches, (2) gaps from the left, (3) gaps from the top.
    """
    row = table.shape[0] - 1  # vertical/top-bottom dimension
    col = table.shape[1] - 1  # horizontal/left-right dimension
    
    # Create array to store aligned sequences
    totalLen = len(seqsList1) + len(seqsList2)
    optimal = ["" for _ in range(totalLen)]
    score = table[row][col]
    
    # Build character lists like in fillTable
    charList1 = [''] * len(seqsList1[0])
    charList2 = [''] * len(seqsList2[0])
    
    for count in range(len(seqsList1[0])):
        for s1 in seqsList1:
            charList1[count] = charList1[count] + s1[count]
        for s2 in seqsList2:
            if count < len(seqsList2[0]):
                charList2[count] = charList2[count] + s2[count]
            else:
                break
    
    while row >= 0 and col >= 0:
        # Priority 1: Check if current score came from diagonal using sop
        if row > 0 and col > 0:
            diag_score = table[row - 1][col - 1]
            # Calculate sop for current position
            sop = calculateSumOfPairs([charList1[col-1]], [charList2[row-1]])
            
            # Check if we got here through diagonal using the actual sop value
            if score == diag_score + sop:
                # Add characters from both groups
                for i in range(len(seqsList1)):
                    optimal[i] = seqsList1[i][col-1] + optimal[i]
                for i in range(len(seqsList2)):
                    optimal[i + len(seqsList1)] = seqsList2[i][row-1] + optimal[i + len(seqsList1)]
                row -= 1
                col -= 1
                score = diag_score
                continue
        
        # Priority 2: Check if current score came from left
        if col > 0:
            left_score = table[row][col-1]
            if score == left_score + gapCost:
                # Add characters from group 1, gaps for group 2
                for i in range(len(seqsList1)):
                    optimal[i] = seqsList1[i][col-1] + optimal[i]
                for i in range(len(seqsList2)):
                    optimal[i + len(seqsList1)] = "-" + optimal[i + len(seqsList1)]
                col -= 1
                score = left_score
                continue
        
        # Priority 3: Check if current score came from top
        if row > 0:
            top_score = table[row-1][col]
            if score == top_score + gapCost:
                # Add gaps for group 1, characters from group 2
                for i in range(len(seqsList1)):
                    optimal[i] = "-" + optimal[i]
                for i in range(len(seqsList2)):
                    optimal[i + len(seqsList1)] = seqsList2[i][row-1] + optimal[i + len(seqsList1)]
                row -= 1
                score = top_score
                continue
        
        # If we get here, we must be at (0,0) or something is wrong
        if row == 0 and col == 0:
            break
        '''else:
            print(f"\nDiagnostic at position row={row}, col={col}:")
            print(f"Current score: {score}")
            if row > 0 and col > 0:
                print(f"Diagonal score: {diag_score}")
                print(f"SOP value: {sop}")
                print(f"Diagonal check: {score} == {diag_score} + {sop}")
            if col > 0:
                print(f"Left score: {table[row][col-1]}")
                print(f"Left check: {score} == {table[row][col-1]} + {gapCost}")
            if row > 0:
                print(f"Top score: {table[row-1][col]}")
                print(f"Top check: {score} == {table[row-1][col]} + {gapCost}")
            break'''
    
    return optimal
############
####MAIN####
############

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print("USAGE:  python  ClustalW.py  inputFile  matchCost  mismatchCost  gapCost")
        sys.exit(0)

    filename = sys.argv[1]
    matchCost = int(sys.argv[2])
    mismatchCost = int(sys.argv[3])
    gapCost = int(sys.argv[4])

    # Read the file and call processAlignmentOrder below:
    # open file in read mode
    f = open(filename)
    # read alignments - string of comma-seperated alignments
    alignments = f.readline()
    # exclude newline
    alignments = alignments[:len(alignments) - 1]
    # print(alignments)
    key = ''
    value = ''
    for x in f:
        # set key
        if x[0] == '>':
            # key = (x.split('>'))[1].split('\n')[0]
            key = x[1:len(x) - 1]
        else:  # create dict entry
            # remove newline characters
            if x[len(x) - 1] == '\n':
                value = x[:len(x) - 1]
            else:
                value = x[:len(x)]
        sequencesDict[key] = [value]
    # set precision of numpy array
    numpy.set_printoptions(precision=3)
    # print(alignments)
    processAlignmentOrder(alignments)
