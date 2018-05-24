#the program takes as an arguments a DNA file, and a k-mer number,
#and returns the k-mers exist in it.

import operator
#using a user specified file
print 'please write the name of the file you want to check'
name = raw_input()+'.txt'
fas_file = open(name)
file_contents = fas_file.read()
fas_file.close()

d={}
print 'Please enter your k-mer:'
kmer = int(raw_input())
ex=0
length = len(file_contents)-kmer+1
while ex <=length:
    s = file_contents[ex:ex+kmer]
    if s in d:
       d[s] = d[s]+1
    else:
        d[s]=1
    ex= ex+1
keys = [key for key,val in d.iteritems() if val == max(d.values())]
for i in keys:
    print i

  
        
     
