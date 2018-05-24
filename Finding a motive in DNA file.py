#the program takes as an arguments a text or fasta file
#containing few sequenses, and a motive, and prints the
#sequence lengths, and whether they contain the motive.

#using a user specified file
print 'please write the name of the file you want to check'
name = raw_input()+'.txt'
fas_file = open(name)
file_contents = fas_file.readlines()
fas_file.close()
print 'please write the motive you are looking for'
motive = raw_input()

print '>gi number       Length    motive \n>---------------------------------\n'

index = 0
length = -12
exist = 0

for i in file_contents:
        if i.startswith(">"):
            if length >0:
                     if exist !=0:
                          print name, '%9i' % length, '      +'
                     else:
                          print name ,'%9i' % length ,'      -'
            name = i[:11]
            index= index +1
            length = -12
            exist = 0
        else:
            length = length + len(i)
            if motive in i:
                exist = 1
if length >0:
        if exist !=0:
            print name ,'%9i' % length,'      +'
        else:
            print name ,'%9i' % length,'      -'
print 'Total of' , index , 'sequence'

 
