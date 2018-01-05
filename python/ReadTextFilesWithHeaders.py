# Parsing a tab delimited file into separate lists or strings
# http://stackoverflow.com/questions/7605374/parsing-a-tab-delimited-file-into-separate-lists-or-strings

import csv

names=[]
ages=[]
with open('ReadTextFilesWithHeaders.txt','r') as f:
    reader = csv.reader(f,delimiter='\t')
    header = next(reader)
    for name,age in reader:
        names.append(name)
        ages.append(age)

print header
# ['Name', 'Age']
print header[0]
# Name
print names
# ['Mark', 'Matt', 'John', 'Jason', 'Matt', 'Frank', 'Frank', 'Frank', 'Frank']
print ages
# ['32', '29', '67', '45', '12', '11', '34', '65', '78']
print names[0]
# Mark
print ages[2:4]
# ['67', '45']


