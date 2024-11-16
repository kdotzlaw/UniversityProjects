import sys
import pandas as pd

def setup(dfEmissions, dfTransitions, sOutput):
    print("----Emissions----")
    print(dfEmissions)
    print("----Transitions----")
    print(dfTransitions)
    # Build table - lenRows = # states (ie len of col in transitions dataframe), lenCols = len(sOutput)
    numstates = len(dfTransitions.axes[1])
    dfTable = pd.DataFrame(index=range(numstates - 1), columns=range(len(sOutput) + 1))
    # print(dfTable)
    # set up row names
    dfTable.index = dfTransitions.axes[1][1::]
    # print(dfEmissions.index)
    dfTable.columns = dfEmissions.axes[1]
    # initialize table
    dfTable.iloc[0][0] = 1
    for i in range(1, dfTable.shape[1]):
        dfTable.iloc[0][i] = 0
    for i in range(1, dfTable.shape[0]):
        dfTable.iloc[i][0] = 0
    # print(dfTable)
    return dfTable


def forward(dfEmissions, dfTransitions, sOutput, dfTable, state, time):
    # if we are at the last state, return total prob
    '''if state == 'B' and time == 0:
        return 1'''
    # print(dfTable)
    # DO COLUMN BY COLUMN, not row by row
    '''# look at all states from previous time point
    for i in range(1, len(sOutput)): #loop through each timepoint (or 1 col at a time)
        # for each column, look at each state that could emit character at timepoint i
        for s in range(1,dfEmissions.shape[1]):
            #print(dfEmissions.columns[s])
            sum = 0
            # for each state k at previous timepoint (t-1) that could transition to state s
            for k in range(1,dfTransitions.shape[1]):
                #print(dfTransitions.index[k])
                sum+=forward(dfEmissions,dfTransitions,sOutput, dfTable, dfTransitions.index[k], i-1)*dfTransitions[k][i-1]
                print("--------------")
                #sum += dfTable.iloc[k][i-1] * dfTransitions.iloc[k][i-1]
                print(str(sum))
                print(dfTable.iloc[k][i-1])
                exit(1)
            #dfTable.iloc[state][i] = sum*dfEmissions[state][sOutput[i]] where state is current state'''
    # print("Emission states = "+str(dfEmissions.index)+ " Transitions states = "+str(dfTransitions.columns))
    try:
        if state == 'E':
            print("This ends the recursion")
            return dfTable.iloc[-1][-1], dfTable
        else:
            for i in range(1, len(sOutput)):
                for s in dfEmissions.loc[i - 1]:  # for each state in row of emissions - Q1...
                    print("State in emissions: ", s)
                    if dfEmissions[s][i] != 0 and dfEmissions[i] == sOutput[i]:  # if s emits sOutput[i]
                        sum = 0
                        for k in dfTransitions.columns:  # for each state k in transitions
                            if k == dfTransitions.iloc[s]:  # if k can transition to s, sum it recursively
                                sum += (forward(dfEmissions, dfTransitions, sOutput, dfTable, k, i - 1) *
                                        dfTransitions.iloc[k][s])
                    dfTable[s][i] = sum * dfEmissions.iloc[s, sOutput[i]]
    except:
        print("Issues with accessing correct rows/columns in pandas dataframe")
    return dfTable.iloc[-1][-1], dfTable


if __name__ == '__main__':
    '''
    -----PARSING----
    1. emissions: 
        --> tab seperated columns with row headers
        --> col headers = output alphabet of HMM (alphatbet can change)
        --> row headers = names of ALL silent states in HMM (ie states that can emit characters)
            ---> could have different numbers of non-silent state
    2. transition prob matrix
        --> tab seperated cols with row headers
        --> cols with row headers = all states in HMM (including silent states B and E)
        --> matrix is NOT symmetrical: row header = source of transition, col header = destination state
        --> NON SILENT STATES WILL HAVE SAME NAME IN TRANSITION & EMISSION FILES
    3. output alphabet
        --> Guarenteed to be the same alphabet as in the emission file
    '''
    if len(sys.argv) < 4:
        print(
            "To run the Forward Algorithm, enter: python HMM.py <emissions_name>.txt <transition_name>.txt <alphabet_sequence>")
        sys.exit(0)
    fEmission = sys.argv[1]
    fTransition = sys.argv[2]
    sOutput = sys.argv[3]
    # read in emissions as a dataframe
    dfEmissions = pd.read_table(fEmission, delimiter='\t')
    # print(dfEmissions)
    # read in transitions
    dfTransitions = pd.read_table(fTransition, delimiter='\t')
    # run Forward Algorithm
    dfOrig = setup(dfEmissions, dfTransitions, sOutput)
    ##print(dfOrig.axes[0], dfOrig.axes[1])
    result = forward(dfEmissions, dfTransitions, sOutput, dfOrig, 'B', 0)
    # result = forward(dfEmissions,dfTransitions,sOutput,dfOrig)
    print("Total Probability = ", result[0])
    print("####### TABLE #########")
    print(result[1])
