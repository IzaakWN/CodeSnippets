# https://docs.python.org/2/library/optparse.html
# http://www.macworld.com/article/1132219/software-utilities/termfoldercomp.html
# https://automatetheboringstuff.com/chapter7/
# TODO: function to replace patterns https://docs.python.org/2/library/re.html
# TODO: add month and year to fileName
# TODO .bundle

import os, sys
from argparse import ArgumentParser
import re
import time

argv = sys.argv
parser = ArgumentParser(description="Make textfile with hierarchy of subdir for a given dir")
parser.add_argument( "file",
                     type=str, action='store',
                     metavar="DIRECTORY", help="Input directory" )
parser.add_argument( "-o", "--output", dest="fileName",
                     default=None, action='store',
                     metavar="FILE_NAME", help="file name to print subdirs hierarchy" )
parser.add_argument( "-t", "--extensions", dest="extensions",
                     nargs='+', default=None, action='store',
                     metavar="EXT", help="only specified extensions" )
parser.add_argument( "-d","--depth", dest="maxDepth",
                     type=int, default=None, action='store',
                     metavar="MAX_DEPTH", help="set maximum subdir depth" )
parser.add_argument( "-e", "--excludeFiles", dest="excludeFiles",
                     default=False, action='store_true',
                     help="exclude files" )
parser.add_argument( "-a", "--all", dest="showAll",
                     default=False, action='store_true',
                     help="show hidden files and directories" )
args = parser.parse_args()
fileName = args.fileName
extensions = args.extensions
maxDepth = args.maxDepth
includeFiles = not args.excludeFiles
showAll = args.showAll

print args.file

tab = "    "



def replacePattern2(string,pattern,replaceString):

    parts = pattern.split("*")

    a = 0
    for part in parts:
        if part in string[a:]:
            a = sting[a:].index(part)
        else:
            return string



def replacePattern2(string,patterns,replaceString=""):
#    pattern = re.compile (r'\[720.*?BluRay.*?YIFY\]')
#    pattern.findall("lol (2010) [720p foo BluRay YIFY bar]")

    for pattern in patterns:
        pattern = pattern.replace("[","\[").replace("]","\]").replace("*",".*?")
        comp = re.compile(pattern)
        matches = findall(string)
        for match in matches:
            string = string.replace(match,replaceString,1)



def listSubDirs(dir,extensions=[],indent="",depth=0):

    list = os.listdir(dir)
    hierarchy = [ ]
    
    for i in list:
        if i[0] != "." or showAll:
            subdir = dir+"/"+i
            if os.path.isdir(subdir) and not i[-4:] == ".app":
                hierarchy += [ indent+i ]
                if (maxDepth == None or depth < maxDepth):
                    hierarchy += listSubDirs( subdir,
                                              extensions=extensions,
                                              indent=tab+indent,
                                              depth=depth+1 )
            elif includeFiles or i[-4:] == ".app":
                if extensions:
                    for ext in extensions:
                        if ext == i[-len(ext):]:
                            hierarchy += [ indent+i ]
                            break
                else:
                    hierarchy += [ indent+i ]
    
    return hierarchy



def main(dir):

    global fileName
    
    path = "/"
    if "/" in dir:
        if dir[-1] == "/":
            dir = dir[:-1]
        path = dir[:dir.rfind("/")+1]
    
    hierarchy = listSubDirs(dir,extensions=extensions)
    for i in hierarchy:
        print i

    if not fileName:
        t = time.struct_time(time.localtime())
        fileName = "%s hierarchy %i-%i-%i.txt" % (dir.replace(path,""), t.tm_mday, t.tm_mon, t.tm_year)

    file = open(fileName,'write')
    file.write(dir+"\n\n")
    for i in hierarchy:
        file.write(i+"\n")
    print ">>> %s written" % fileName
    file.close()



if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        dir = str(sys.argv[1])
        if os.path.isdir(dir):
            main(dir)
        else:
            if not os.path.isdir(dir):
                print ">>> ERROR: argument is not a directory: %s" % dir
    else:
        print ">>> ERROR: Needs an arguments"
    
    print ">>> done"


