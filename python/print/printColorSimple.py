# Author: Izaak Neutelings (Februari 2018)

import os, sys
import time

def green(string,**kwargs):   return "\x1b[0;32;40m%s\033[0m"%string
def error(string,**kwargs):   print ">>> \033[1m\033[91m%sERROR! %s\033[0m"%(kwargs.get('pre',""),string)
def warning(string,**kwargs): print ">>> \033[1m\033[93m%sWarning!\033[0m\033[93m %s\033[0m"%(kwargs.get('pre',""),string)

def main():
    print green(">>> Hello World!",color="magenta")
    print green("I am old.",color="grey", prepend=">>> ")
    warning("This is a drill.")
    error("This is also a drill.")

if __name__ == '__main__':    
    print " "
    main()
    print ">>>\n>>> done\n"


