# https://docs.python.org/2/library/csv.html

import csv

with open('WriteCSVFilesDefault.csv','w') as f:
    writer = csv.writer(f) # default: dialect=excel?
    writer.writerow(range(5))
    writer.writerow(range(6))
    writer.writerow(["a","ka","pa","sta"])
    f.close()

with open('WriteCSVFilesSemicolon.csv','w') as f:
    writer = csv.writer(f,delimiter=';')
    writer.writerow(range(5))
    writer.writerow(range(6))
    writer.writerow(["a","ka","pa","sta"])
    f.close()

with open('WriteTextFilesTab.txt','w') as f:
    writer = csv.writer(f,delimiter='\t')
    writer.writerow(range(5))
    writer.writerow(range(6))
    writer.writerow(["a","ka","pa","sta"])
    f.close()
