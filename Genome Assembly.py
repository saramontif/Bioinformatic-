#using a user specified file
print 'please write the name of the file you want to check'
fileName = raw_input() + '.txt'

#reading the data and writing it into a dictionary
def readDataFromFile(fileName):
    name = fileName 
    dna_seq_file = open(name)
    d = {}
    for line in dna_seq_file:
        num = line[:1]
        d[num]= line[2:-1]
    return d

#finding the avarage length of the sequences.
#Including use of the previous function
def meanLength(fileName):
    d = readDataFromFile(fileName)
    mean, s = 0, 0
    for i,j in d.items():
        mean = mean + len(j)
        s= s+1
    mean = mean/float(s)
    return mean

#finding the overlap of two sequences
def getOverlap(left, right):
    for i in range(len(left)):
        if left[i:] == right[:len(left)-i]:
            return left[i:]
    return ''

#the function returns a dictionary of dictionaries containing the number of
#overlaping bases for a pair of reads in a specific orientation.
def getAllOverlaps(reads):
    d = dict()
    for name1, seq1 in reads.items():
        for name2, seq2 in reads.items():
            if name1 == name2:
                continue
            if name1 not in d:
                d[name1] = dict()
            d[name1][name2] = len(getOverlap(seq1, seq2))

    return d

#printing the dictionary in a nicely - formed matrix
def prettyPrint(d):
    print '   ',
    for j in sorted(d, key=int):
        print "% 3s" % j,
    print
    for i in sorted(d, key=int):
        print "% 3s" % i,
        for j in sorted(d, key=int):
            if i == j:
                s = '  -'
            else:
                s = "% 3s" % d[str(i)][str(j)]
            print s,
        print

#finding the first read
def findFirstRead(overlaps):
    for i in overlaps:
        signif = False
        for j in d[i]:
            if d[j][i] > 3:
                signif = True
        if not signif:
            return i

#an help function, which returns the key associated
#with the largest value at the dictionary given
def findKeyForLargestValue(d):
    m = max(d.values())
    for i in d:
        if d[i] == m:
            return i

#The function returns a list of read names
#in the order in which they are represented the genomic sequence.
def findOrder(first, d):
    if max(d[first].values()) < 3:
        return [first]
    else:
        nex = findKeyForLargestValue(d[first])
        return [first] + findOrder(nex, d)

#the last but not least function!
#It  reconstruct the genomic sequence.
#using the previos functions ofcourse
def assembleGenome(readOrder, reads, overlaps):
    g = ''
    for read in readOrder[:-1]:
        right = max(x for x in overlaps[read].values() if x >= 3)
        g += reads[read][:-right]
    g += reads[readOrder[-1]]
    return g

#printing the results as requested
print '\nThe raw fragments:\n'
reads = readDataFromFile(fileName)
print reads
d = getAllOverlaps(reads)
print '\nThe overlaps matrix:\n'
prettyPrint(d)
order = findOrder(findFirstRead(reads), getAllOverlaps(reads))
print '\nThe order of the fragments:\n'
print order
print '\nThe final joined sequence:\n'
print assembleGenome(order, reads, d)
