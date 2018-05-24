import sys

#using a user specified file, and a frame length
print 'please write the name of the file you want to check'
name = raw_input()+'.txt'
dna = open(name)
print 'please write the frame length you want'
frame_length = raw_input()

#the nocleotides - amino acids dictionary
code = {"TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L",
    "TCT":"S", "TCC":"s", "TCA":"S", "TCG":"S",
    "TAT":"Y", "TAC":"Y", "TAA":"STOP", "TAG":"STOP",
    "TGT":"C", "TGC":"C", "TGA":"STOP", "TGG":"W",
    "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L",
    "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P",
    "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
    "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R",
    "ATT":"I", "ATC":"I", "ATA":"I", "ATG":"M",
    "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T",
    "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K",
    "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R",
    "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V", 
    "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A",
    "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E",
    "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G"}

# a function which gets a file and sends
# it to the ORF finding function, as a 6 different ORFs
def divide(dna, code, frame_length):
    seq=''
    name=''
    for line in dna:
        line = line.rstrip()
        if line[0] == '>':
            words=line.split()
            name=words[0][1:]
        else:
            seq = seq + line
    seq.upper()
    #sending the first 3 ORF
    for i in {0,1,2}:
        translate(seq, name,+(i+1), ORF(seq,i,code),frame_length)
    #sending the 3 reverse-complement orfs
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    reverse_complement = "".join(complement.get(base, base) for base in reversed(seq))
    for i in {0,1,2}:
        translate(reverse_complement, name,-(i+1),ORF(reverse_complement,i,code),frame_length)
    return

#the ORF function, which gets a dna string and the code
def ORF(dna, frame, code):
    length = len(dna)
    stop_codons = ['TGA', 'TAG', 'TAA']
    start_codon = ['ATG']
    starts = []
    stops = []
    num_starts=0
    num_stops=0
    #finding the start&stop codons and saving their places
    for i in range(frame,length,3):
        codon=dna[i:i+3]
        if codon in start_codon:
            starts += str(i+1).splitlines()
        if codon in stop_codons:
            stops += str(i+1).splitlines()
    for line in stops:
        num_stops += 1
    for line in starts:
        num_starts += 1 
    orffound = {}
    #if the number of stop codons and start condos are greater\equal to 1
    #if the start codon comes first, we know there is at least 1 ORF
    #it turned out to be a very long code, but the only shorter methods was to use a library
    if num_stops >=1 and num_starts >=1: 
        orfs = True
        stop_before = 0
        start_before = 0
        if num_starts > num_stops:
            num_runs = num_starts
        if num_stops > num_starts:
            num_runs = num_stops
        if num_starts == num_stops:
            num_runs = num_starts
        stop_prev = 0
        start_prev = 0
        counter = 0
         
        for position_stop in stops:
            position_stop = int(position_stop.rstrip()) +2
            for position_start in starts:
                position_start = position_start.rstrip()
                
                if int(position_start) < int(position_stop) and int(position_stop) > int(stop_prev) and int(position_start) > int(stop_prev):
                    counter += 1
                    nameorf = "orf"+str(counter)
                    stop_prev = int(position_stop)
                    tart_prev = int(position_start)
                    sizeorf = int(position_stop) - int(position_start) + 1
                    orffound[nameorf] = position_start,position_stop,sizeorf  
                else: 
                    pass
    else:
        orfs = False
    return orffound

#tge printing function, which also translating the seq
def translate(seq, name, frame, d,frame_length):
    for i in d.items():
        numorf = i[0]
        startorf=d[numorf][0]
        stoporf=d[numorf][1]
        lengthorf=d[numorf][2]
        if lengthorf>=int(frame_length):
            print name,"frame",frame,"start",startorf,"stop",stoporf,"length",lengthorf, seq[int(startorf)-1:int(startorf)+6], seq[int(stoporf)-6:int(stoporf)]
            print seq[int(startorf)-1:int(stoporf)]
            c=[]
            for j in range(int(startorf)-1,int(stoporf), 3):
                codon= seq[j:j+3]
                if codon in code:
                    c += code[codon]
            print c
            c=[]
    return

divide(dna, code, frame_length)

dna.close()
     
        






