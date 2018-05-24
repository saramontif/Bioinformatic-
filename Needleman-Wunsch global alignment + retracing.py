import random

print 'please write the number of random sequences you want to align, and their size'
num, size = int(raw_input()), int(raw_input())
penalty = {'MATCH': 1, 'MISMATCH': 0, 'GAP': 0}

#generate a random dna seq in a given length
def generate(length, type_of):
    protein_list = ['M', 'T', 'Q', 'A', 'P', 'F', 'L', 'S', 'V', 'E', 'G', 'H', 'I', 'W', 'R', 'D', 'K', 'N', 'Y', 'C']
    if type_of == 'dna':
        return ''.join(random.choice('CGTA') for _ in xrange(length))
    elif type_of == 'protein':
        return ''.join(random.choice(protein_list) for _ in xrange(length))
 
#an help function, returns the place's score
def match(alpha, beta, penalty):
    if alpha == beta:
        return penalty['MATCH']
    elif alpha == '-' or beta == '-':
        return penalty['GAP']
    else:
        return penalty['MISMATCH']

#build the matrixes, initialize it
def needlemanWunsch(s1, s2,penalty):
    
    #building the matrixes
    n, m = len(s1)+1, len(s2)+1
    scores =  [[x for x in range(n)] for y in range(m)]
    
    #Initializing the matrixes
    for i in range(m):
        scores[i][0] = penalty['GAP'] * i
    for j in range(n):
        scores[0][j] = penalty['GAP'] * j

    #Filling the matrixes
    for i in range(1, m ):
        for j in range(1, n ):
            diagonal = scores[i-1][j-1] + match(s1[j-1], s2[i-1], penalty)
            horizontal = scores[i-1][j] + penalty['GAP']
            vertical = scores[i][j-1] + penalty['GAP']
            scores[i][j] = max(diagonal,horizontal,vertical)
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
    seqN = len(align1)
    sym = ''
    seq_score = 0
    ident = 0
    for i in range(seqN):
        a1 = align1[i]
        a2 = align2[i]
        if a1 == a2:
            sym = sym + a1
            ident = ident +1
            seq_score += match(a1, a2, pt)
        else: 
            seq_score += match(a1, a2, pt)
            sym += ' '
            
    Ident = seq_score/seqN * 100
    
    #print('Identity = %2.1f percent' % ident)
    #print('Score = %d\n'% seq_score)

    return ident

#working on and generating sequences:
def check(num, size, pt, to):
    seq1, seq2, d, l, n, m, idet = '', '', [], [], 0.0, 0.0 , 0.0
    #with gap
    for i in range(num):
        seq1, seq2 = generate(size,to), generate(size, to)
        nw = needlemanWunsch(seq1,seq2, penalty)
        idet = traceBack(nw,seq2,seq1, penalty)
        d.append(idet)
    for i in d:
        n = n + i
    n = n/num
    #without gap
    for i in range(num):
        seq1, seq2 = generate(size,to), generate(size, to)
        idet = 0.0
        for i in range(size):
            if seq1[i] == seq2[i]:
                idet = idet + 1
        idet = idet/size*100
        l.append(idet)
    for i in l:
        m = m + i
    m =  m/num
    return n, m

#calling the check function:
a,b = check(num, size, penalty, 'dna')
c,d =  check(num, size, penalty, 'protein')
print '                 With Gaps     Without Gaps'
print 'DNA:              ', a,'        ', b, '\n','Protein:          ', c,'         ', d 


    
    

