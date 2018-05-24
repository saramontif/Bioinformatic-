#finding a word frequency in a DNA file.

#using a user specified file
print 'please write the name of the file you want to check'
name = raw_input()+'.txt'
dna_seq_file = open(name)
print 'please write the word you want to calculate'
word = str(raw_input())

#the bases frequency function (using both file and string, reading line by line)
def bases_freq(dna_seq_file):
    d={}
    ex=0
    le=0
    gc_content = 0
    for line in dna_seq_file:
        if line[:1]== '>':
            file_name = line
            name='file_name'
            d[name]= file_name 
        else:
            line = line.lower()
            length = len(line)
            while ex <length:
                n = line[ex:ex+1]
                if n!= '':
                    if n!= '\n':
                        le=le+1
                        if n in d:
                            d[n] = d[n]+1
                        else:
                            d[n]=1
                ex= ex+1
        ex=0
    for i in d:
        if i is not 'file_name':
            d[i]= float(d[i]*100)/le
    for i in d:
        if i=='g' or i =='c':
            gc_content = gc_content + d[i]
    gc='gc'
    d[gc]=gc_content
    leg='length'
    d[leg]=le
    dna_seq_file.seek(0,0)
    return d

#word occurance counting function
def count(dna_seq_file, word):
    d={}
    c={}
    kmer = len(word)
    ex=0
    le=0
    for line in dna_seq_file:
        length = len(line)
        ex=0
        line = line.lower()
        while ex <=length:
            s = line[ex:ex+kmer]
            if s in d:
               d[s] = d[s]+1
            else:
               d[s]=1
            ex= ex+1
    dna_seq_file.seek(0,0)
    c = bases_freq(dna_seq_file)
    le = c['length']
    c = d[word]
    content = float(c)/(le-1)
    return content

#the representation frequency function
def representation(word, dna_seq_file):
    d = bases_freq(dna_seq_file)
    length = len(word)
    lis=[]
    fmult = 1.0
    p = 0.0
    num = 0.0
    fword = count(dna_seq_file, word)
    for i in range(length):
        n = word[i:i+1]
        num = d[n]/100
        lis.append(num)
    for i in lis:
        fmult = fmult*i
    p = fword/fmult
    if 'file_name' in d:
        print d['file_name']
    print word, ' representation: ', p
    return p

representation(word, dna_seq_file)



