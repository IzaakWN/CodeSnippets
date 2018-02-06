#! /usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#* @Project: add XML files for SFrame
#* @author Izaak Neutelings <iwn_@uzh.ch> - UZH
#***************************************************************************

import os, sys
import time
import glob
import re
import math
import optparse

# parse the command line
parser=optparse.OptionParser(usage="%prog SAMPLELISTFILE") #epilog
parser.add_option("-v", "--verbose", action="store_true",
                dest="verbose", default=False,
                help="Verbose output [default = %default]")
parser.add_option("-o", "--outDir", action="store",
                dest="outDir", default="TES",
                help="Output directory for merged xml file [default = %default]")
(options, args) = parser.parse_args()

print
verbose        = options.verbose
outDir         = options.outDir  



def main():
    
    nFiles = 0
    shifts = [ ]
    
    for shift in frange(0.0,0.06001,0.002):
        shifts.append(( "TES", "TESshift", shift, [ "Background_DY.py", ] )) #"Background_TT.py"
    #files = glob.glob("./*.py")
    
    if outDir: ensureDirectory(outDir)
    
    for shiftname, shiftvar, shiftvalue, shiftfiles in shifts:
      if float(shiftvalue)==0.0: continue
      
      labelShiftDn    = ("%s%.3f"%(shiftname,1.-shiftvalue)).replace('.','p')
      labelShiftUp    = ("%s%.3f"%(shiftname,1.+shiftvalue)).replace('.','p')
      shiftvalue      = "%.3f"%shiftvalue
      
      for fileInName in shiftfiles:
        
        # CHECK
        if not os.path.exists(fileInName):
          print "  Error! \"%s\" does not exists!\n"%(fileInName)
          exit(1)
        
        # INPUT files
        with open(fileInName,'r') as fileIn:
          #print ">>>\n>>> %s: %s"%(shiftname,fileInName)
          
          postFixpattern  = '.*postFix.*=.*"([^"]*)"'
          valuepattern    = ('\[.*%s.*,.*"(\d\.\d+)".*\]'%(shiftvar)) #re.escape
          fileShiftDnName = fileInName.replace('.py',"_%s.py"%(labelShiftDn))
          fileShiftUpName = fileInName.replace('.py',"_%s.py"%(labelShiftUp))
          if outDir:
            fileShiftDnName = "%s/%s"%(outDir,fileShiftDnName)
            fileShiftUpName = "%s/%s"%(outDir,fileShiftUpName)
          
          for sign, fileOutName, shiftlabel in [('-',fileShiftDnName,labelShiftDn),('',fileShiftUpName,labelShiftUp)]:
            print ">>>\n>>> %s"%(fileOutName)
            
            # READ input xml file
            foundPostFixLine = False
            foundValueLine   = False
            with open(fileOutName,'w') as fileOut:
              fileIn.seek(0)
              for line in fileIn:
                #if "[" in line: print line.replace('\n','')
                postFixmatches = re.findall(postFixpattern,line)
                valuematches   = re.findall(valuepattern,line)
                
                if postFixmatches:
                    postFixmatch = postFixmatches[0]
                    if len(postFixmatches)>1:
                        print ">>> ERROR! Two matches for \"postFix\" in file \"%s\":\n>>>   \"%s\"!"%(fileInName,line)
                        exit(1)
                    if foundPostFixLine:
                        print ">>> ERROR! Reoccuring \"postFix\" in file \"%s\":\n>>>   \"%s\"!"%(fileInName,line)
                        exit(1)
                    foundPostFixLine = True
                    oldpattern = '(.*postFix.*=.*)"%s"(.*)'%(postFixmatch)
                    newpattern = '%s"_%s%s"%s'%(r"\1",shiftlabel,postFixmatch,r"\2")
                    oldline    = line.replace('\n','')
                    line       = re.sub(oldpattern,newpattern,line)
                    newline    = line.replace('\n','')
                    print ">>>   %22s  ->  %s"%(oldline.lstrip(' '),newline.lstrip(' '))
                
                if valuematches:
                    matchedvalue = valuematches[0]
                    if len(valuematches)>1:
                        print ">>> ERROR! Two matches for \"%s\" in file \"%s\":\n>>>   \"%s\"!"%(shiftvar,fileOutName,line)
                        exit(1)
                    if foundValueLine:
                        print ">>> ERROR! Reoccuring \"%s\" in file \"%s\":\n>>>   \"%s\"!"%(shiftvar,fileOutName,line)
                        exit(1)
                    if float(matchedvalue)!=0.00:
                        print ">>> Warning! \"%s\"'s value \"%s\"!=0.00 in file \"%s\":\n>>>   \"%s\"!"%(shiftvar,shiftvalue,fileOutName,line)
                    foundValueLine = True
                    oldpattern = '(\[.*"%s".*,.*)"%s"(.*\])'%(shiftvar,matchedvalue)
                    newpattern = '%s"%s"%s'%(r"\1",sign+shiftvalue,r"\2")
                    oldline    = line.replace('\n','')
                    line       = re.sub(oldpattern,newpattern,line)
                    newline    = line.replace('\n','')
                    print ">>>   %22s  ->  %s"%(oldline.lstrip(' '),newline.lstrip(' '))
                    
                fileOut.write(line)
              nFiles += 1
    print ">>>\n>>> number of files = %d"%nFiles  
        

def frange(start, stop, step):
    """Yield values in a range between start and stop, with  linearly spaced steps"""
    x = start
    while x <= stop:
      yield x
      x += step


def ensureDirectory(DIR):
    """Make directory if it does not exist."""
    if not os.path.exists(DIR):
        os.makedirs(DIR)
        print ">>> made directory " + DIR
    


if __name__ == "__main__":
  main()
  print ">>> \n"


