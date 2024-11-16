
import sys


def readDistMatrixFile(filename):
    """This method parses a distance matrix file.
    
    Parameters
    ----------
    filename : str
        The path to a file.

    Returns
    -------
    list of str
        The list of taxa names.

    dict with key = (taxa1, taxa2) and value = distance
        The dictionary contains distances as values and the keys are pairs of taxa (str).
    """
    f = open(filename)
    # create taxa list
    taxa = f.readline()
    taxa = taxa[1:]
    taxa = taxa.split("\t")
    taxa[len(taxa) - 1] = taxa[len(taxa) - 1].split("\n")[0]
    # create distMatrix dictionary
    distMatrix = {}
    line = f.readline()
    while line is not None:
        # split line
        spl = line.split("\t")
        index = 1
        if len(spl) == index:
            break
        for t in taxa:
            key = (spl[0], t)
            # make sure to get rid of newlines
            value = spl[index].split('\n')[0]
            index += 1
            distMatrix[key] = value
        line = f.readline()
    return taxa, distMatrix


def produceUTable(listOfTaxa, distMatrix):
    """This produces the U table: union of distances for each taxon in the supplied list of taxa.You are correct! The key should be just 1 taxon here in the U table dictionary. This was just a copy-paste error in the comments of the NJ.py file.
    
    Parameters
    ----------
    listOfTaxa : list of str
        The list of all taxa.

    distMatrix : dict
        The distance matrix.

    Returns
    -------
    dict with key = (taxa1, taxa2) and value = U distance
        The dictionary contains U distances as values and the keys are pairs of taxa (str).

    """
    UTable = {}
    sum = 0
    count = 0
    for t in listOfTaxa:
        for key in distMatrix:
            if t in key and count < len(listOfTaxa):
                value = distMatrix[key]
                sum += float(value)
        # update utable
        UTable[t] = sum
        sum = 0
        count += 1
    return UTable


# To produce a delta matrix from a distance matrix given as a parameter (also takes a list of taxa and the uTable as parameters).
# Returns the delta matrix (as a dictionary, where the key is a pair of taxa and the value is the delta value)
def produceDeltaMatrix(listOfTaxa, distMatrix, uTable):
    """This produces the delta matrix.
    
    Parameters
    ----------
    listOfTaxa : list of str
        The list of all taxa.

    distMatrix : dict
        The distance matrix.

    uTable : dict
        The U distance matrix, as returned by the produceUTable method.

    Returns
    -------
    dict with key = (taxa1, taxa2) and value = delta value
        The dictionary contains delta values as values and the keys are pairs of taxa (str).

    """
    # FORUMULA: delta_ij = (N-2) * dist_ij - Ui - Uj (where N = number of taxa)
    N = len(listOfTaxa)
    #print(N)
    delta = {}
    for key in distMatrix:
        val = (N - 2) * (float(distMatrix[key])) - float(uTable[key[0]]) - float(uTable[key[1]])
        delta[key] = val
    return delta


def neighborJoiningRec(listOfTaxa, distMatrix): #//TODO: DOESNT WORK FOR 2nd PROVIDED TXTS BUT DOES WORK FOR EXAMPLE.TXT, AND DISTMATRIX.TXT
    # //TODO: ONLY DO DIST CALCULATIONS USING ONE OF (X1,X2) (X2,X1)
    """This is a recursive method. It does all the steps of NJ, updates the distance matrix and calls itself
    on the updated distance matrix and updated list of taxa. This method is also in charge of outputting all the results to the console.
    
    Parameters
    ----------
    listOfTaxa : list of str
        The list of all taxa.

    distMatrix : dict
        The distance matrix.

    """
    # call required methods
    '''
    PROCESS
    -------------
    1. Find the key (i,j) that gives min value of delta
    2. Pull away (i,j) & form cherry with parent (ij)
    3. Calculate distance from i, j to parent ij
        ---> General: D(i,p) = 0.5*D(i,j) +  [ (Ui - Uj) / (N-2) ] 
        ---> And: D(j,p) = D(i,j)-D(i,p)
    4. Calculate all distances from nodes k to parent ij (where k is not i or j) 
        ---> D(k,p) = 0.5 * [D(i,k) + D(j,k) - D(i,j)] for all k  (k not i or j)
    5. Go to 2 with key (p)
    6. Base Case: empty or 3 branches left (use Fitch-Margoliash)
    '''
    # recursive case
    if len(listOfTaxa) >= 3:
        N = len(listOfTaxa)
        dist = {}
        for key in distMatrix:
            if key[0] != key[1] and (key[0] < key[1] or len(key[1]) > 2):
                dist[key] = distMatrix.get(key)
        distMatrix = dist
       # print("DISTMATRIX")
        #printDelta(distMatrix)
        uTable = produceUTable(listOfTaxa, distMatrix)
        #print("UTABLE"+str(uTable))
        delta = produceDeltaMatrix(listOfTaxa, distMatrix, uTable)
        #print(matrix)
        # cant pull away same taxa, so remove. Also remove all duplicates ie (X2,X1)
        '''delta = {}
        for key in matrix:
            if key[0] != key[1] and (key[0] < key[1] or len(key[1])>2):
                delta[key] = matrix.get(key)
        print("POST PREPROCESS-delta")
        printDelta(delta)'''
        keyMin = min(delta, key=delta.get)
        print("-Pulling away " + keyMin[0] + " and " + keyMin[1])
        parent = keyMin[0] + keyMin[1]
        val = (uTable[keyMin[0]]-uTable[keyMin[1]])/(N-2)
        #distIParent = round(0.5 * (float(distMatrix[keyMin])+val),2)
        distIParent = 0.5 * (float(distMatrix[keyMin]) + val)
        print("Distance between " + keyMin[0] + " and parent " + parent + " = " + str(distIParent))
        #distJParent = round((float(distMatrix[keyMin]) - distIParent),2)
        distJParent = (float(distMatrix[keyMin]) - distIParent)
        print("Distance between " + keyMin[1] + " and parent " + parent + " = " + str(distJParent))
        # calculate distances to parent for all other children
        for t in listOfTaxa:
            if t not in keyMin:
                # recalculate distances
                #newkey1 = (parent,t)
                newkey2 = (t,parent)
                #print(newkey)
                #val = 0.5*(float(distMatrix[(keyMin[0],t)])+float(distMatrix[(keyMin[1],t)]) - float(distMatrix[keyMin]))
                tuple1 = ()
                tuple2 = ()
                if (keyMin[0],t) in distMatrix.keys():
                    tuple1 = (keyMin[0],t)
                else:
                    tuple1 = (t, keyMin[0])
                if (keyMin[1],t) in distMatrix.keys():
                    tuple2 = (keyMin[1],t)
                else:
                    tuple2 = (t, keyMin[1])
                val = (float(distMatrix[tuple1]) + float(distMatrix[tuple2])) - float(
                    distMatrix[keyMin])
                #distMatrix[newkey1] = val*0.5
                distMatrix[newkey2] = val*0.5
        # update distMatrix with parentIJ, childrenIJ and remove i,j and keys containing ij since all distances update
        # create list of keys to remove
        remKeys = []
        for key in distMatrix:
            if key[0] in keyMin or key[1] in keyMin:
                remKeys.append(key)
        # loop through removalKeys and delete them from distMatrix
        for key in remKeys:
            if key!=parent:
                del(distMatrix[key])
        # update taxa list: i,j are removed, add new parentIJ
        listOfTaxa.remove(keyMin[0])
        listOfTaxa.remove(keyMin[1])
        listOfTaxa.append(parent)
        #print(listOfTaxa)
        #printDelta(distMatrix)
        neighborJoiningRec(listOfTaxa, distMatrix)
    else:
        #print("BASE CASE")
        #printDelta(distMatrix)
        # only 2 taxa left: both parents --> parent join parent
        print("Finally, distance between "+listOfTaxa[0]+" and "+listOfTaxa[1]+" is "+str(distMatrix[(listOfTaxa[0],listOfTaxa[1])]))
        return
        #exit(0)

'''
printDelta is used for debugging purposes to print dictionaries in a more readable way
'''
def printDelta(delta):
    for key in delta:
        print(key, delta.get(key))


############
####MAIN####
############

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("USAGE:  python  NJ.py  distMatrix")
        sys.exit(0)

    taxaList, distDict = readDistMatrixFile(sys.argv[1])
    '''utable = produceUTable(taxaList,distDict)
    print(utable)
    delta = produceDeltaMatrix(taxaList,distDict,utable)
    print(delta)'''
    neighborJoiningRec(taxaList, distDict)
