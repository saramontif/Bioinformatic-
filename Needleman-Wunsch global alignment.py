import sys

#using a user specified file and parameters.
print 'please write the name of the file you want to align'
name = raw_input()+'.txt'
dna = open(name)
print 'do you want to choose the penalty yourself? yes/no'
ans = raw_input()
if ans == 'yes':
    print 'please write the match, mismatch and gap score'
    match, mismatch, gap = raw_input(),raw_input(),raw_input()
    penalty = {'MATCH': int(match), 'MISMATCH': int(mismatch), 'GAP': int(gap)}

else:
    penalty = {'MATCH': 1, 'MISMATCH': -1, 'GAP': -2}

#printing the matrixes
def solve(mat, s1, s2):
    s2 = '0' + s2
    s = '         0  | '
    for i in range(len(s1)):
        s = s+ s1[i]+' |  '
    print '\n',s
    for i in range(len(s1)):
        print
        for j in range(len(s2)+1):
            if j == 0:
                print s2[i], ' | ',
            print "%  4s" % str(mat[i][j]),
    print '\n\n'

#an help function, returns the place's score
def match(alpha, beta, penalty):
    if alpha == beta:
        return penalty['MATCH']
    elif alpha == '-' or beta == '-':
        return penalty['GAP']
    else:
        return penalty['MISMATCH']

#an help function, returns the place's pointer
def Pointer(diagonal,horizontal,vertical):
    pointer = max(diagonal,horizontal,vertical) 
    if(diagonal == pointer):
        return 'D'
    elif(horizontal == pointer):
        return 'V'
    else:
         return 'H'  

#build the matrixes, initialize it
def needlemanWunsch(s1, s2,penalty):
    
    #building the matrixes
    n, m = len(s1)+1, len(s2)+1
    scores =  [[x for x in range(n)] for y in range(m)]
    pointers =  [[x for x in range(n)] for y in range(m)]
    
    #Initializing the matrixes
    for i in range(m):
        scores[i][0] = penalty['GAP'] * i
        pointers[i][0] = 'V'
    for j in range(n):
        scores[0][j] = penalty['GAP'] * j
        pointers[0][j] = 'H'
    pointers[0][0] = 0

    #Filling the matrixes
    for i in range(1, m ):
        for j in range(1, n ):
            diagonal = scores[i-1][j-1] + match(s1[j-1], s2[i-1], penalty)
            horizontal = scores[i-1][j] + penalty['GAP']
            vertical = scores[i][j-1] + penalty['GAP']
            scores[i][j] = max(diagonal,horizontal,vertical)
            pointers[i][j] = Pointer(diagonal,horizontal,vertical)

    #printing the matrixes
    solve(scores, s1,s2)
    solve(pointers,s1,s2)
    return scores

#the traceBack function
def traceBack(m,s1,s2, pt):
    i, j= len(s1), len(s2)
    align1, align2, path = '', '', ''
    while i > 0 and j > 0:
        score_current = m[i][j]
        score_diag = m[i-1][j-1]
        score_left = m[i][j-1]
        score_up = m[i-1][j]
        #finding the costless path, by comparing the up, down + diagonal 
        if score_current == score_diag + match(s1[i-1], s2[j-1], pt):
            a1,a2 = s1[i-1],s2[j-1]
            i,j = i-1,j-1
            path = path +'D'
        elif score_current == score_up + pt['GAP']:
            a1,a2 = s1[i-1],'-'
            i -= 1
            path = path +'V'
        elif score_current == score_left + pt['GAP']:
            a1,a2 = '-',s2[j-1]
            j -= 1
            path = path +'H'
        align1 += a1
        align2 += a2          

    #if one of the sequences is done
    while i > 0:
        a1,a2 = s1[i-1],'-'
        align1 += a1
        align2 += a2
        i -= 1
        path = path +'V'
        
    while j > 0:
        a1,a2 = '-',s2[j-1]
        align1 += a1
        align2 += a2
        j -= 1
        path = path +'H'
    
    align1 = align1[::-1]
    align2 = align2[::-1]

    print '\nPath:\n\n', path
    print '\nPairwise Alignment:\n'
    print(align2)  
    print(align1)
    return


#sending the sequences to the function:
seq1, seq2, c = '', '', 0
for line in dna:
    line = line.rstrip()
    if line[0] != '>':
        if c==0:
            seq1=line
            c=1
        else:
            seq2 =line

nw = needlemanWunsch(seq1,seq2, penalty)
traceBack(nw,seq2,seq1, penalty)
    
