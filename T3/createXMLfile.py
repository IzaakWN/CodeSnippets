#! /usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#* @Project: creating XML files for SFrame
#* @author Clemens Lange    <clange@physik.uzh.ch>        - UZH
#*
#***************************************************************************

# NOTE: if there are a lot of corrupt files, and the connection is slow, consider
# replacing "return 255" by "continue" in  ../SFrame/python/SFrameHelpers.py

# Get text file with full paths of ntuples (18/02/2017):
example = """
Examples:
 
 \033[1mTier 3 PNFS\033[0m:
   PNFS="/pnfs/psi.ch/cms/trivcat/store/t3groups/uniz-higgs/Summer16/Ntuple_80_20170206"
   ls -d $PNFS/DY*/*/*/* > dirs_DY.txt
   ls -d $PNFS/*/*/*/* > dirs.txt
   ./createXMLfile.py dirs.txt -o xmls_Moriond
 
 \033[1mTier 2 PNFS\033[0m:
   PNFS="gsiftp://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/ytakahas/Ntuple_Moriond17"
   uberftp -ls $PNFS/DY*/*/* | awk '{print $8}' > dirs_T2_DY.txt
   uberftp -ls $PNFS/*/*/* | awk '{print $8}' > dirs_T2.txt
   ./createXMLfile.py dirs_T2.txt -o xmls_Moriond_T2 -s PSI-T2
 
 \033[1mSplit files\033[0m (to run in parallel):
   cat dirs.txt | wc -l
   ./createXMLfile.py dirs.txt --split 2
 
 \033[1mPrint out xml file names\033[0m formatted for copy-pasting into job options files:
   cd xmls_Moriond/
   ls *.xml | xargs -I@ echo \\"@\\",
"""
#cat dirs.txt | wc -l
#split -l 200 dirs.txt dirs_split -d

import os
import sys
import re
import optparse
import thread
import subprocess
import math

# parse the command line
parser=optparse.OptionParser(usage="%prog SAMPLELISTFILE") #epilog
parser.add_option("-e", "--example", action="store_true",
                dest="example", default=False,
                help="Print example usage")
parser.add_option("-v", "--verbose", action="store_true",
                dest="verbose", default=False,
                help="Verbose output [default = %default]")
parser.add_option("-s", "--site", action="store",
                dest="site", default="PSI",
                help="Grid site [default = %default]")
parser.add_option("-x", "--xrootd", action="store_true",
                dest="useXrootd", default=False,
                help="Use Xrootd [default = %default]")
parser.add_option("-t", "--tree", action="store",
                dest="treeName", default="ntuplizer/tree",
                help="Tree to be scanned by SFrame for number of input events [default = %default]")
parser.add_option("-m", "--maxFiles", action="store",
                dest="maxFiles", default="500",
                help="Maximum number of files [default = %default]")
parser.add_option("-o", "--outDir", action="store",
                dest="outDir", default="xmls",
                help="Output directory for xml files [default = %default]")
parser.add_option("-f", "--no-failed", action="store_false",
                dest="writeFailed", default=True,
                help="Do not write corrupt root files to a txt file")
parser.add_option("-d", "--split", action="store",
                dest="nSplit", default="1",
                help="Number of parts a given file needs to be split into [default = %default]")
(options, args) = parser.parse_args()
if options.example or len(args) is not 1:
  parser.print_help()
  print example
  if len(args) is not 1:
    parser.error("No input given. Please provide a file with a name list.")
  exit(0)

print
sampleListName = args[0]
site=options.site
verbose=options.verbose
useXrootd=options.useXrootd
treeName=options.treeName
maxFiles_original=int(options.maxFiles)
nSplit=int(options.nSplit)
outDir=options.outDir
writeFailed=options.writeFailed
if verbose:
  print "Site:",site

dCacheInstances={}
#Xrootd and dcap prefixes
dCacheInstances["PSI"]=["root://t3dcachedb.psi.ch:1094/", "dcap://t3se01.psi.ch:22125/"]
dCacheInstances["PSI-T3"]=dCacheInstances["PSI"]
dCacheInstances["T3"]=dCacheInstances["PSI"]
dCacheInstances["PSI-T2"]=["root://storage01.lcg.cscs.ch/", "root://storage01.lcg.cscs.ch/"] # PSI Tier 2
dCacheInstances["T2"]=dCacheInstances["PSI-T2"]
if site not in dCacheInstances:
  print "ERROR! Site \"%s\" not registered as a dCacheInstances! Please use one of the following options with the -s flag:\n"%site+\
        '\n'.join([ "%12s:  %s"%(k,', '.join(v)) for k,v in sorted(dCacheInstances.items()) ]) + '\n'
  sys.exit(1)


def main():
  
  if nSplit>1:
    splitSampleListFile(sampleListName,nChunks=nSplit)
    return
  
  nSamples = 0
  with open(sampleListName) as sampleList:
    nSamples = len([l for l in sampleList if not (l.startswith("#") or l.isspace())])
  
  with open(sampleListName) as sampleList:
    
    print "  Creating XML files in         %s," % (outDir)
    print "  with root files on the        %s storage element," % ("PSI-T3" if "T2" not in site else site)
    print "  in the directories listed in  %s.\n" % (sampleListName)
    
    if not os.path.exists(outDir):
      print "Creating output directory", outDir
      os.makedirs(outDir)
  
    # LOOP over all samples
    iSample = 0
    for sample in sampleList:
      if sample.startswith("#") or sample.isspace():
        continue
      print "- "*10
      iSample+=1
      sample = sample.strip("\n")
      sampleName = (sample.strip("/")).rsplit("/",1)[1]
      sampleName_file=(sample.strip("/")).rsplit("/",3)[1]
      sampleName_file+="_"+sampleName
      print "Sample %d/%d: %s in location: %s producing file with list %s" %(iSample,nSamples,sampleName,sample,sampleName_file )
      fileList=[]
      
      # CHECK directory existence
      if not isDir(sample):
        print sample,"is not a directory."
        if "lcg.cscs.ch" in sample and "T2" not in site:
          print "Please use the \"-s PSI-T2\" option if you samples are on PSI-T2!"
      else:
        prefix = ""
        if (sample.startswith("/pnfs")):
          if (site not in dCacheInstances):
            print "Gridsite doesn't have dCache instances defined."
            sys.exit(1)
          if (useXrootd):
            prefix = dCacheInstances[site][0]
          else:
            prefix = dCacheInstances[site][1]
        if verbose:
          print "Using prefix:",prefix
        
        # GET root files
        for subdir, files in getFiles(sample):
          for file in files:
            if (file.find(".root") >= 0):
              path = prefix + os.path.join(sample, subdir, file)
              if (verbose): print path
              if "fail" in path.lower() or "corrupt" in path.lower(): continue
              fileList.append(path)
        print "Processing %d files"%len(fileList)
        nFiles=int(math.ceil(len(fileList)/float(maxFiles_original)))
        
        # SPLIT files list
        if (nFiles > 1):
          maxFiles = int(math.ceil(len(fileList)/float(nFiles)))
          print "Splitting file into %d subfiles of max. %d input files each" %(nFiles, maxFiles)
        else:
          maxFiles = int(maxFiles_original)
        if (len(fileList) == 0):
          print "No files found."
        
        # LOOP over XML files
        for i in range(nFiles):
          if (nFiles > 1):
            outName = "%s_%d" %(sampleName_file, i)
          else:
            outName = sampleName_file
          csvList = ""
          firstFileIndex=i*maxFiles
          lastFileIndex=min((i+1)*maxFiles,len(fileList))
          nRootFiles=lastFileIndex-firstFileIndex
          for fileIndex in range(firstFileIndex,lastFileIndex):
            csvList = csvList+fileList[fileIndex]+","
          csvList = csvList.strip(",")
          
          # MAKE XML file
          failedRootFiles=[ ]
          retryXMLFile=True
          while retryXMLFile:
            retryXMLFile=False
            lock=thread.allocate_lock()
            lock.acquire()
            commandMC="sframe_input.py -r -d -o %s/%s.xml %s -t %s" %(outDir, outName, csvList, treeName)
            if verbose: print commandMC
            processMC=subprocess.Popen(commandMC, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            lock.release()
            output=processMC.stdout.read()
            if verbose: print output
            
            # CHECK output
            nWrittenRootFiles=output.count(".root")
            newFailedRootFiles=[ ]
            for line in output.split("\n"):
              
              # CHECK for failed files
              if "error" in line.lower():
                for rootfile in csvList.split(','):
                  if rootfile in line:
                    nWrittenRootFiles -= 2 # ".root" in processing and error message
                    newFailedRootFiles.append(rootfile)
                    csvList=csvList.replace(rootfile,'').replace(",,",',') # remove failed file from list
                    retryXMLFile=True
                    #print "  \033[1mWarning! File %s (%s.xml): ignoring corrupt file (%s) and retrying!\033[0m" % (i+1,outName,rootfile)
                #else:
                  #print "  \033[1m\033[91mERROR!%s!\033[0m" % line.replace(" *ERROR*","").replace("*ERROR*","")
                  #if ".root" in line: nWrittenRootFiles-=line.count(".root")+1
              
              # FINAL succes
              if "events processed" in line:
                retryXMLFile=False
                print "  File %s: %s (%s files)" % (i+1,line.replace("\n",""),nWrittenRootFiles)
            
            # RETRY ?
            if len(newFailedRootFiles):
              failedRootFiles+=newFailedRootFiles
              if retryXMLFile:
                print "  \033[1mWarning! File %s: Ignoring %s corrupt file%s and retrying!\033[0m" % (i+1,len(newFailedRootFiles),plural(newFailedRootFiles))
                continue
              else:
                print "  \033[1mWarning! File %s: Ignoring %s corrupt file%s!\033[0m" % (i+1,len(newFailedRootFiles),plural(newFailedRootFiles))
            
            # NO RETRY
            outerr=processMC.stderr.read()
            if outerr: print "sframe_input.py gave an error:\n%s" % (outerr)
            if nWrittenRootFiles != nRootFiles:
              print "  \033[1mWarning! File %s contains fewer root files (%s) than expected (%s)! (%s.xml)\033[0m" % (i+1,nWrittenRootFiles,nRootFiles,outName)
              if verbose:
                for j, file in enumerate(csvList.split(',')): print "%3s: %s" % (j,file)
            
          # LOG failed files
          if len(failedRootFiles) and writeFailed: writeFailedRootFiles(failedRootFiles,i,outDir,outName)
        
  print "- "*10



def getFiles(samplepath):
  '''Generator to loop over files in some directory.'''
  if "T2" in site:
    lock=thread.allocate_lock()
    lock.acquire()
    commandLS="uberftp -ls -r gsiftp://storage01.lcg.cscs.ch/%s | awk '{print $8}' | grep .root"%(samplepath) # | sort -V
    if verbose: print commandLS
    processLS=subprocess.Popen(commandLS, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    lock.release()
    subdirs_dict={}
    #output=processLS.stdout #(stdout,stderr) = processLS.communicate()
    for line in processLS.stdout:
      if line.find(".root") <= 0: continue
      subdirs_dict.setdefault(os.path.dirname(line),[]).append(os.path.basename(line.strip()))
    for subdir,files in subdirs_dict.items():
      if verbose: print "subdir=%s, files=%s" % (subdir,files)
      yield (subdir,files)
  else:
    for subdir,dirs,files in os.walk(samplepath):
      if verbose: print "subdir=%s, files=%s" % (subdir,files)
      yield (subdir,files)
  


def isDir(samplepath):
  '''Help function check the existence of a directory.'''
  if "T2" in site:
    lock=thread.allocate_lock()
    lock.acquire()
    commandLS="uberftp -ls gsiftp://storage01.lcg.cscs.ch/%s"%(samplepath)
    if verbose: print "\n",commandLS
    processLS=subprocess.Popen(commandLS, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    lock.release()
    (stdout,stderr) = processLS.communicate() #output=processLS.stderr.read()
    if verbose: print "isDir: stdout: %s"%stdout
    if verbose: print "isDir: stderr: %s"%stderr
    return "No match for" not in stderr
  else:
    return os.path.isdir(samplepath)
  


def writeFailedRootFiles(failedRootFiles,i,outDir,outName):
  '''Write names of root files that could not be opened to a log file.'''
  outDirFailed=outDir #.strip("/")+"_failed"
  outNameFailed=outName+"_failed"
  if not os.path.exists(outDirFailed):
    print "Creating output directory", outDirFailed
    os.makedirs(outDirFailed)
  with open("%s/%s.txt"%(outDirFailed,outNameFailed),'w') as file:
    for rootfile in failedRootFiles:
      file.write("%s\n"%rootfile)
  with open("%s/%s.xml"%(outDir,outName),'a') as file:
    file.write("<!-- Warning! Ignored %s corrupted file%s, see %s.txt -->\n\n" % (len(failedRootFiles),plural(failedRootFiles),outNameFailed))
  print "  \033[1mWarning! File %s: Written %s corrupt root file%s to %s.txt in %s\033[0m" % (i+1, len(failedRootFiles),plural(failedRootFiles),outNameFailed,outDirFailed)
  


def splitSampleListFile(filename,nChunks=2):
  '''Split txt file into some number of file with an equal number of lines.'''
  if not os.path.exists(filename):
    print "%s does not exist!"%(filename)
    exit(1)
  list = [ ]
  with open(filename,'r') as file:
    list  = [ s for s in file if not s.startswith("#") and not s.isspace() ]
  nChunks = min(len(list),nChunks)
  length  = int(len(list)/nChunks)
  k, m    = divmod(len(list), nChunks)
  for i in xrange(nChunks):
    subfilename = filename.replace(".txt","_split%d.txt"%(i+1))
    with open(subfilename,'w') as subfile:
      print "Made \"%s\""%(subfilename)
      for s in list[i*k+min(i,m):(i+1)*k+min(i+1,m)]: subfile.write(s)
  


def plural(list,y=False):
  '''Make plural if there is more than one element in the list.'''
  if len(list) > 1:
      if y: return "ies"
      else: return "s"
  else:
      if y: return "y"
      else: return ""
  


if __name__ == "__main__":
  main()
  print
  

