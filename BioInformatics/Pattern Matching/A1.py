# Comp 3820 A1

# brute force - return: num matches in forward strand, num matches in complement strand, time taken for search
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import time


def bruteforce(sequence, pattern):
    # need to time searches
    matches = 0
    flag = True
    # start brute force
    start = time.time()
    # search seq - compare txt to pattern at all possible starting positions
    for i in range(len(sequence) - len(pattern)):
        flag = True  # reset flag
        for j in range(len(pattern)):
            if sequence[i + j] != pattern[j]:
                flag = False
                break
        if flag:
            matches += 1

    end = time.time()
    return end - start, matches


def preprocessing(pattern):
    i = 0
    table = [None] * (len(pattern) + 1)  # because 0 1 2 3 table entries, if pattern len = 3
    # assert (len(pattern) == 3)
    j = -1
    table[0] = -1
    while i < len(pattern):  # could be len+1
        while j > -1 and pattern[i] != pattern[j]:
            j = table[j]
        i += 1
        j += 1
        if i < len(pattern) and pattern[i] == pattern[j]:  # could be len+1
            table[i] = table[j]
        else:
            # print(i)
            table[i] = j
    return table


# KMP - return: num matches in forward strand, num matches in complement strand, time taken for search
def kmp(sequence, pattern):
    M = len(sequence)
    N = len(pattern)
    matches = 0
    table = preprocessing(pattern)
    start = time.time()
    # at each step, compare sequence[j+i] with pattern[i]
    # if match (current spot match NOT FULL OCCURENCE), i++ and continue
    # if mismatch OR finding a full occurence: j=j+i-table[i] AND i = table[i] OR 0 if table[i] < 0
    j = 0
    i = 0
    while j < M:
        #partial match
        if i < N and i + j < M and pattern[i] == sequence[j + i]:
            i += 1
        #mismatch or full match
        else:
            j = j + i - table[i] #move text pointer
            if i == N:
                matches+=1
            if table[i] < 0:
                i = 0
            else:
                i = table[i]
    end = time.time()
    return end - start, matches


# read in from file and detect cmd input
def main():
    print("To run the brute force algorithm, enter: python A1.py <fasta file> <pattern> -b")
    print("To run the KMP algorithm, enter: python A1.py <fasta file> <pattern>")
    print('Or run the Test Suite (runs both algorithms using select patterns including ATG, AACGTT), '
          'by entering: t')
    # get user input
    userinput = input()
    sInput = userinput.split()  # turn input into array so we can get filenames and patterns
    if sInput[0] != 't':
        filename = sInput[2]
        pattern = sInput[3]
        if len(sInput) == 5:
            tag = 'brute force'
        else:
            tag = 'kmp'
        # read fasta file
        sequence = Bio.SeqIO.read(filename, 'fasta').seq
        if tag == 'brute force':
            result_reg = bruteforce(sequence, pattern)  # correct num matches
            print("Total number of matches in forward strand = " + str(result_reg[1]))
            result_rc = bruteforce(sequence.reverse_complement(), pattern)  # correct  num matches
            print("Total number of matches in reverse complement strand = " + str(result_rc[1]))
            print("Completed the search in " + str(result_reg[0] + result_rc[0]) + 'seconds')
            # print(str(result_reg[0]))
        else:
            result_reg = kmp(sequence, pattern)  # correct num matches
            print("Total number of matches in forward strand = " + str(result_reg[1]))
            result_rc = kmp(sequence.reverse_complement(), pattern)
            print("Total number of matches in reverse complement strand = " + str(result_rc[1]))
            print("Completed the search in " + str(result_reg[0] + result_rc[0]) + 'seconds')
    else:
        print("running test suite")
        sequence = Bio.SeqIO.read('Sorangium_cellulosum.fasta', 'fasta').seq
        array = ['ATG','AAA', 'TT', 'CCCC','GCC','GGC','AACGTT']
        for i in range(len(array)):
            print("Running brute force for " + array[i])
            result_reg = bruteforce(sequence, array[i])  # correct num matches
            print("Total number of matches in forward strand = " + str(result_reg[1]))
            result_rc = bruteforce(sequence.reverse_complement(), array[i])  # correct  num matches
            print("Total number of matches in reverse complement strand = " + str(result_rc[1]))
            print("Completed the search in " + str(result_reg[0] + result_rc[0]) + 'seconds')
            print("Running KMP on " + array[i])
            result_reg = kmp(sequence, array[i])  # correct num matches
            print("Total number of matches in forward strand = " + str(result_reg[1]))
            # print("Reg " + str(len(sequence)) + "RC " + str(len(sequence.reverse_complement()))) --> lengths are the same
            # print(sequence[len(sequence)-1])
            # print(sequence.reverse_complement()[len(sequence)-1])
            result_rc = kmp(sequence.reverse_complement(), array[i])
            print("Total number of matches in reverse complement strand = " + str(result_rc[1]))
            print("Completed the search in " + str(result_reg[0] + result_rc[0]) + 'seconds')


# end of main
if __name__ == '__main__':
    main()
