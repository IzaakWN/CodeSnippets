# https://docs.python.org/3/tutorial/inputoutput.html
# http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python


# CREATE
file = open("test.txt", 'w')
file.write("Hello World! This my first line!")
file.write(" And this is a new sentence!")
file.write("\nAnd this is a new line.")
file.close()

# READ
file = open("test.txt", 'r')
print file.read()
file.close()

# EDIT
file = open("test.txt", 'r+')
for line in file:
    print line
file.write("\nEDIT: new line!")
file.close()