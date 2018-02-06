# Author: Izaak Neutelings (Januari 2016)
import os, sys
import time



def color(string,**kwargs):
    """Color"""
    # http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    text_color_dict = { "black"     : "0;30;",  "red"       : "1;31;",
                        "green"     : "0;32;",  "yellow"    : "1;33;", "orange"    : "1;33;",
                        "blue"      : "1;34;",  "purple"    : "0;35;",
                        "magenta"   : "1;36;",  "grey"      : "0;37;",  }
    background_color_dict = {   "black"     : "40", "red"       : "41",
                                "green"     : "42", "yellow"    : "43", "orange"    : "43",
                                "blue"      : "44", "purple"    : "45",
                                "magenta"   : "46", "grey"      : "47", }                  
    color_code = text_color_dict[kwargs.get('color',"red")] + background_color_dict[kwargs.get('background',"black")]
    return kwargs.get('prepend',"") + "\x1b[%sm%s\033[0m" % ( color_code, string )



def warning(string,**kwargs):
    return color("Warning! "+string, color="yellow", prepend=">>> "+kwargs.get('prepend',""))


 
def error(string,**kwargs):
    return color("ERROR! "+string, color="red", prepend=">>> "+kwargs.get('prepend',""))



def main():

    print color(">>> Hello World!",color="magenta")
    print color("I am old.",color="grey", prepend=">>> ")
    print warning("This is a drill.")
    print error("This is also a drill.")



if __name__ == '__main__':
    
    print " "
    main()
    print ">>>\n>>> done\n"


