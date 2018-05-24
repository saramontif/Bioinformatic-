#findind the bases and gc content in a DNA file. 

import random

#using a user specified file
print 'please write the name of the file you want to check'
name = raw_input()+'.txt'
dna_seq_file = open(name)

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
    return d

#printing the frequency 
def print_bases_freq(d):
    if 'file_name' in d:
        print d['file_name']
    else:
        print 'a random file, or a reading name Error'
    print ' a      t      c      g      gc'
    print '%.1f' %d['a'],' ','%.1f'%d['t'],' ', '%.1f'%d['c'],' ', '%.1f' %d['g'] ,' ','%.1f' %d['gc'],'\n'
    return

#creating a random seq, in a given length
def ran_gen(num):
    dna_list = [x for x in ''.join([ 'ACGT' for i in range(num/4)])]
    random.shuffle(dna_list)
    result = ''.join(dna_list)
    return result
  
print_bases_freq(bases_freq(dna_seq_file))
print_bases_freq(bases_freq(ran_gen(2000)))
