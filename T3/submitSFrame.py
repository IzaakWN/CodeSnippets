#!/usr/bin/env python

# -*- coding: utf-8 -*-
#***************************************************************************
#* @Project: submission tool for SFrame
#*
#* @author Sascha Mehlhase  <sascha.mehlhase@desy.de>      - DESY
#* @author Clemens Lange    <clemens.lange@desy.de>        - DESY
#*
#***************************************************************************
#


sFrameExecutable="sframe_main"

import os
import sys
import glob
import optparse
import tempfile
import platform
from copy import deepcopy

# check for python version
if platform.python_version() < "2.5.1":
  print "FATAL: you need a newer python version"
  sys.exit()

from multiprocessing import Process
import thread
import subprocess
import time
import shutil
import socket
starttime=time.time()
startdate=time.strftime("%a %d/%m/%Y %H:%M:%S",time.gmtime())
succesRates=[ ]


class runCommand(Process):
  def __init__(self, baseName, subJob):
    Process.__init__(self)
    self.cmd="date; %s ../%s%s.xml; date; ls -lh; mv %s.root %s%s.root; ls -lh; date" %(sFrameExecutable, baseName, subJob, baseName, baseName, subJob)
    self.baseName=baseName
    self.subJob=subJob
  def run(self):
    lock=thread.allocate_lock()
    lock.acquire()
    subProcess=subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    subProcessStatus=subProcess.poll()
    if subProcessStatus==1:
      print "job '%s' failed" %(self.cmd, subProcessStatus)
      lock.release()
      sys.exit()
    else:
      print "job '%s %s' starting ..." %(self.baseName, self.subJob)
      lock.release()
      logFile=open(self.baseName+self.subJob+'.log', 'w')
      logFile.write(subProcess.stdout.read())
      logFile.write("###################### STDERR ####################\n")
      logFile.write(subProcess.stderr.read())
      logFile.close()
      time.sleep(1)
      print "job '%s %s' finished" %(self.baseName, self.subJob)



class XmlTemplate(object):
  """Class to parse and create XML file"""
  def __init__(self, xmlTemplateFileName, jobConfig, jobName, outputLevel, loadLibs, loadPacks, cycleName, runMode, proofServer, proofWorkdir, postFix, inputTrees, outputTrees, userItems):
    self.template=open(xmlTemplateFileName, 'r').read()
    self.template=self.template.replace('JOBCONFIG', jobConfig)
    self.template=self.template.replace('JOBNAME', jobName)
    self.template=self.template.replace('OUTPUTLEVEL', outputLevel)
    loadLibsFull=""
    for l in loadLibs:
      loadLibsFull+="  <Library Name=\""+l+"\" />\n"
    self.template=self.template.replace('LIBRARIES', loadLibsFull)
    loadPacksFull=""
    for l in loadPacks:
      loadPacksFull+="  <Package Name=\""+l+"\" />\n"
    self.template=self.template.replace('PACKAGES', loadPacksFull)
    self.template=self.template.replace('CYCLENAME', cycleName)
    self.template=self.template.replace('RUNMODE', runMode)
    self.template=self.template.replace('PROOFSERVER', proofServer)
    self.template=self.template.replace('PROOFWORKDIR', proofWorkdir)
    self.template=self.template.replace('OUTPUTDIR', "./")
    self.template=self.template.replace('POSTFIX', postFix)
    # header and footer
    self.inputDataHeader="    <InputData Lumi=\"DATALUMI\" Type=\"TYPE\" Version=\"VERSION\" NEventsMax=\"NEVENTSMAX\" NEventsSkip=\"NEVENTSSKIP\" SkipValid=\"SKIPVALID\" >\n"
    self.inputDataFooter=""
    for f in inputTrees:
      self.inputDataFooter+="      <InputTree Name=\""+f+"\" />\n"
    for f in outputTrees:
      self.inputDataFooter+="      <OutputTree Name=\""+f+"\" />\n"
    self.inputDataFooter+="    </InputData>\n"
    userItemsFull=""
    for l in userItems:
      if len(l)!=2:
        continue
      userItemsFull+="      <Item Name=\""+str(l[0])+"\" Value=\""+str(l[1])+"\" />\n"
    self.template=self.template.replace('USERITEMS', userItemsFull)

  def getInputDataHeader(self):
    return self.inputDataHeader

  def getInputDataFooter(self):
    return self.inputDataFooter

  def replace(self, old, new):
    self.template=self.template.replace(old, new)

  def write(self, outputFileName):
    self.outFile=open(outputFileName, 'w')
    self.outFile.write(self.template)
    self.outFile.close()
  


class BatchScript(object):
  """Class to create batch script"""
  def __init__(self, useHost, useOS, path2sframe, useEnv, cmssw, hCPU, hVMEM, cycleName, tempDirLog):
    self.addhost=""
    self.addOS=""
    if not useHost=="":
      self.addhost="#$ -l hostname=HOST\n"
    if not useOS=="":
      self.addOS="#$ -l os=OSYSTEM\n"
    self.batchScript="#!/bin/zsh\n#$ -S /bin/zsh\n#$ -l h_cpu=HCPU\n#$ -l h_vmem=HVMEM\n%s#$ -j y\n#$ -N NAME\n#$ -o STDOUT\n" %(self.addhost +self.addOS)
    self.batchScript+="date\n"
    self.batchScript+="hostname\n"
    self.batchScript+="uname -a\n"
    #self.batchScript+="df -h\n"
    self.batchScript+="cd %s/..\n" %(path2sframe)
    # setup ROOT and python
    if (socket.gethostname()).find("psi.ch") >=0:
      if not useEnv:
        #self.batchScript+="source /swshare/psit3/etc/profile.d/cms_ui_env.sh\n"
        # self.batchScript+="source /swshare/cms/cmsset_default.sh\n"
        self.batchScript+='cd /swshare/ROOT/root_v5.34.18_slc6_amd64_py26_pythia6; export LD_LIBRARY_PATH=/swshare/ROOT/pythia6/pythia6:; source bin/thisroot.sh; cd -'
    if useEnv:
      envVariables= ['ROOTSYS', 'LD_LIBRARY_PATH', 'PYTHONPATH', 'PATH' ] 
      for envVar in envVariables:
        self.batchScript+="export %s=%s\n" %(envVar, os.environ[envVar])
    else:
      self.batchScript+="cd %s/../%s/src\n" %(path2sframe, cmssw)
      self.batchScript+="eval `scramv1 runtime -sh`\n"
      self.batchScript+="cd ../..\n"
    
    # self.batchScript+="export DCACHE_CLIENT_ACTIVE=1\n"
    self.batchScript+="cd %s\n" %(path2sframe)
    self.batchScript+="source setup.sh\n"
    self.batchScript+="echo $PYTHONPATH\n"
    
    self.batchScript+="env\n"
    self.batchScript+="echo Using SFrame in ${SFRAME_DIR}\n"
    
    self.batchScript=self.batchScript.replace("HCPU", hCPU)
    self.batchScript=self.batchScript.replace("HVMEM", hVMEM)
    self.batchScript=self.batchScript.replace("HOST", useHost)
    self.batchScript=self.batchScript.replace("OSYSTEM", useOS)
  
  def addLine(self, lineString):
    self.batchScript+=lineString
    
  def replace(self, old, new):
    self.batchScript=self.batchScript.replace(old, new)

  def write(self, outputFileName):
    self.outFile=open(outputFileName, 'w')
    self.outFile.write(self.batchScript)
    self.outFile.close()




#  listOfJobs.append([str(dataSets[i][0]), str(dataSets[i][1][j]), baseName, subJob, "",tempDirSh,tempDirRoot,tempDirLog])
def getDataset(job):
  return job[0]

def getSubset(job):
  return job[1]

def getBasename(job):
  return job[2]

def getSubjobString(job):
  return job[3]

def getFinished(job):
  return job[4]=="."

def getTempDirSh(job):
  return job[5]

def getTempDirRoot(job):
  return job[6]

def getTempDirLog(job):
  return job[7]

def getCycleName(job):
  return getBasename(job)+getSubjobString(job)



#runningJob = [ qid, cylceName=basename+subjobstring ]
def getJobFromId(runningJob, listOfJobs):
  for l in listOfJobs:
    if runningJob[1]==getCycleName(l): return l
  return []



# build in an automated resubmit for Eqw jobs at some point
def waitForBatchJobs(runningJobs, listOfJobs, userName, timeCheck):
  print "waiting for %d job(s) in the queue" %(len(runningJobs))
  nJobs = len(runningJobs)
  skip  = 5 if nJobs<400 else 10
  skip2 = 5 if nJobs>400 else 1
  while not len(runningJobs)==0:
    time.sleep(float(timeCheck))
    queryString="qstat -u %s | grep %s | awk {\'print $1\'}" %(userName, userName)
    lock=thread.allocate_lock()
    lock.acquire()
    compileProcess=subprocess.Popen(queryString, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    compileProcess.wait()
    lock.release()
    jobList = compileProcess.stdout.read()
    jobList = jobList.split("\n")
    for j in runningJobs:
      jobId=j[0]
      if (jobId not in jobList):
        for l in listOfJobs:
          if j[1]==(l[2]+l[3]):
            l[4]="."
        runningJobs.remove(j)
        nRunningJobs = len(runningJobs)
        if ((nRunningJobs%skip )==0 or not(nJobs*0.25<nRunningJobs<nJobs*0.75)) and\
           ((nRunningJobs%skip2)==0 or not(nJobs*0.07<nRunningJobs<nJobs*0.93)):
          print "waiting for %d job(s) in the queue" %(len(runningJobs))
      #else:
      #  #store job usage info in seperate file, dump into log at the end
      #  queryString   = "qstat -j " + jobId + " | grep usage"
      #  lock=thread.allocate_lock()
      #  lock.acquire()
      #  usageProcess  = subprocess.Popen(queryString, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      #  usageProcess.wait()
      #  lock.release()
      #  usageOutput   = usageProcess.stdout.read()
      #  job       = getJobFromId(j, listOfJobs)
      #  usageFile = getTempDirLog(job) + "/" + getCycleName(job) + ".tmp"  
      #  open(usageFile,'a').write(usageOutput)



def checkRunningJobs(runningJobs, listOfJobs, timeCheck):
  time.sleep(float(timeCheck))
  for r in runningJobs:
    if not r[0].is_alive():
      for l in listOfJobs:
        if r[1]==(l[2]+l[3]):
          l[4]=r[2]
      runningJobs.remove(r)



def checkCompletion(dataSets, listOfJobs, outDir, cycleName, postFix,keepTemp):
  for d in dataSets:
    checkReady=True
    mergeFiles=""
    mergeDebug=""
    fileBaseName=""
    fileBaseNameRoot=""
    fileToMerge=""
    for l in listOfJobs:
      #print "l[6] %s ,l[1] %s, l[2] %s ,l[3] %s ,d[0] %s = l[0] %s ,l[4] %s , fileBaseNameRoot %s ," %(l[6],l[1],l[2],l[3],d[0], l[0],l[4],fileBaseNameRoot)
      if l[0]==d[0] and not l[4]=="" :
        fileBaseName=l[6]
        fileBaseNameRoot=l[6]+"/"+l[2]
        fileBaseNameLog=l[7]+"/"+l[2]
        #fileBaseName=l[4]+"/"+(l[2].split("_subjob"))[0]
        mergeDebug+="\n###### %s %s ######\n" %(fileBaseNameLog, l[3])
        mergeDebug+="\n###### %s %s ######\n" %(fileBaseNameRoot, l[3])
        mergeDebug+=open(fileBaseNameLog+l[3]+".log").read()
        #dump usage info into log
        #usageFile=fileBaseNameLog+l[3]+".tmp"
        #if os.path.exists(usageFile):
        #  mergeDebug+=open(usageFile).read()
        #  os.system("rm -f " +usageFile)
        mergeFiles+=fileBaseNameRoot+l[3]+".root "
        fileToMerge=fileBaseNameRoot.partition("pythia8")[0]+fileBaseNameRoot.partition("pythia8")[1]+'*'
        fileToMerge=fileToMerge.partition("Run2016")[0]+fileToMerge.partition("Run2016")[1]+'*'
        fileToMerge=fileToMerge.partition("madgraph")[0]+fileToMerge.partition("madgraph")[1]+'*'
        
        # print "l[6] %s ,l[1] %s, l[2] %s ,l[3] %s , fileBaseNameRoot %s ," %(l[6],l[1],l[2],l[3],fileBaseNameRoot)
      elif l[0]==d[0] and l[4]=="":
        checkReady=False
    if checkReady:
      print "\n%s is ready, start merging and copying" %(d[0])
      #print "outDir %s ,  cycleName %s,  d[0] %s, postFix %s, "%(outDir , cycleName, d[0], postFix)
      mergeFileBaseName="%s/%s.%s%s" %(outDir , cycleName, d[0], postFix)
      if keepTemp:
        mergeCmd="hadd -f %s.root %s " %(mergeFileBaseName, mergeFiles)
      else:
        #mergeCmd="hadd -f %s.root %s && rm -rf %s" %(mergeFileBaseName, mergeFiles, mergeFiles)
        fileToMerge=fileBaseNameRoot.partition("pythia8")[0]+fileBaseNameRoot.partition("pythia8")[1]+'*'
        fileToMerge=fileToMerge.partition("Run2016")[0]+fileToMerge.partition("Run2016")[1]+'*'
        fileToMerge=fileToMerge.partition("madgraph")[0]+fileToMerge.partition("madgraph")[1]+'*'
        mergeCmd='hadd -f %s.root %s.root && rm -rf %s.root'  %(mergeFileBaseName,  fileToMerge,  fileToMerge)
        #mergeCmd_mt = 'hadd -f %s/%s_mutau.root %s/%s_mutau*.root && rm -rf %s/%s_mutau*.root'  %(outDir, d[0], fileBaseName, d[0], fileBaseName, d[0])
        #mergeCmd_et = 'hadd -f %s/%s_eletau.root %s/%s_eletau*.root && rm -rf %s/%s_eletau*.root'  %(outDir, d[0], fileBaseName, d[0], fileBaseName, d[0])
        print "mergeCmd is\n%s \n" %mergeCmd
        #print "mergeCmd_private_mt is %s " %mergeCmd_mt
        #print "mergeCmd_private_et is %s " %mergeCmd_et
      while "**" in fileToMerge: fileToMerge=fileToMerge.replace("**",'*')
      
      # LS
      lock=thread.allocate_lock()
      lock.acquire()
      lsCmd="date; ls -lh %s*" %(fileToMerge)
      subProcess=subprocess.Popen(lsCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      #subProcess.wait()
      mergeDebug+="\n###### merging ######\n"
      lsDebug=lsCmd+"\n"
      lsDebug+=subProcess.stdout.read()
      lsDebug+=subProcess.stderr.read()
      lock.release()
      
      # COUNT
      global succesRates
      WARNING='\033[1m\033[93m'
      END='\033[0m'
      nMergeFiles=len(glob.glob("%s*.root"%fileToMerge))
      nMergeJobs=len([ j for j in listOfJobs if j[0]==d[0] ])
      nFiles=len(glob.glob("%s/*.root"%l[6]))
      nJobs=len(listOfJobs)
      countCmd ="number of files to merge / number of jobs: %3d/%3d\n(%s.root)" % (nMergeFiles,nMergeJobs,'/'.join((fileToMerge.split('/')[-2:])))
      #countCmd+="\nnumber of all root files / number of all jobs: %3d/%d\n(%s/*.root)" % (nFiles,   nJobs,     '/'.join((l[6].split('/')[-1:])))
      countDebug="" if os.path.exists(l[6]) else "Warning! %s does not exist!"%l[6]
      lsDebug+="\n"+countCmd+"\n"+countDebug
      mergeDebug+="\n"+lsDebug
      mergeDebug+="\n"+mergeCmd
      succesRates.append("  %4d /%3d %s"%(nMergeFiles,nMergeJobs,d[0])) # global list
      print WARNING+countCmd+END
      print WARNING+countDebug+END
      
      # MERGE
      lock=thread.allocate_lock()
      lock.acquire()
      outFile=open(mergeFileBaseName+'.log', 'w')
      if not 'No such file or directory' in lsDebug:
        subProcess=subprocess.Popen(mergeCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #subProcess.wait()
        mergeDebug+=subProcess.stdout.read()
        mergeDebug+=subProcess.stderr.read()

        #subProcess_mt = subprocess.Popen(mergeCmd_mt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ##subProcess.wait()
        #mergeDebug += subProcess_mt.stdout.read()
        #mergeDebug += subProcess_mt.stderr.read()

        #subProcess_et = subprocess.Popen(mergeCmd_et, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ##subProcess.wait()
        #mergeDebug += subProcess_et.stdout.read()
        #mergeDebug += subProcess_et.stderr.read()
      else:
        mergeDebug+="FATAL: Missing root files. No merging!"
        
      # WRITE
      outFile.write(mergeDebug)
      outFile.close()
      if subProcess.poll()==1:
        print "ERROR"
      lock.release()
      dataSets.remove(d)
      print "%s finished merging and copying" %(d[0])



def getFileLumi(inputline):
  lumi_start=inputline.find("\"", inputline.find("Lumi="))+1
  lumi_end=inputline.find("\"", lumi_start)
  return float(inputline[lumi_start:lumi_end])



def main():
  # parse the command line
  parser=optparse.OptionParser(usage="%prog -j jobOption.py")
  parser.add_option("-j", "--jobOptions", dest="jobOptions",
                    action="store", default="Datasets.py",
                    help="joboptions to process [default = %default]")
  parser.add_option("--keepTemp", action="store_true",
                    dest="keepTemp", default=False,
                    help="keep temporary directory [default = %default]")
  parser.add_option("--fixTemp", action="store_true",
                    dest="fixTemp", default=False,
                    help="use only given temporary directory [default = %default]")
  parser.add_option("-m", "--mergeOnly", action="store_true",
                    dest="mergeOnly", default=False,
                    help="do not run jobs but merge files in path2tmpsh [default = %default]")
  parser.add_option("--nobatch", action="store_false",
                    dest="useBatch", default=True,
                    help="do not run on batch system [default = %default]")
  parser.add_option("--batchCompile", action="store_true",
                    dest="batchCompile", default=False,
                    help="do compile on batch farm [default = %default]")
  parser.add_option("--path2tmplog", action="store",
                    dest="path2tmplog", default="...",
                    help="set temporary log directory [default = %default]")
  parser.add_option("--path2tmpsh", action="store",
                    dest="path2tmpsh", default="...",
                    help="set temporary script directory [default = %default]")
  parser.add_option("--path2tmproot", action="store",
                    dest="path2tmproot", default="...",
                    help="set temporary root output file directory [default = %default]")
  parser.add_option("--path2tmp", action="store",
                    dest="path2tmp", default="...",
                    help="set temporary directory [default = %default]")
  parser.add_option("--nosandbox", action="store_false",
                    dest="useSandbox", default=True,
                    help="do not use sandbox [default = %default]")
  parser.add_option("-e", "--useEnvironment", dest="useEnv",
                    action="store_true", default=False,
                    help="get ROOT and python setup from environment [default = %default]")
  parser.add_option("-c", "--usecmssw", dest="cmssw",
                    action="store", default="CMSSW_7_3_0",
                    help="CMSSW version to use for ROOT/python setup [default = %default]")
  parser.add_option("-s", "--syst", dest="systematics",
                    action="store", default="",
                    help="systematics string [default = %default]")
  parser.add_option("--dccp", dest="usedccp",
                    action="store_true", default=False,
                    help="copy files from dCache before running [default = %default]")

  (options, args)=parser.parse_args()
  jobOptions=options.jobOptions
  useEnv=options.useEnv
  cmssw=options.cmssw
  Systematics=options.systematics
  usedccp=options.usedccp

  # check for jobOptions file
  if not os.access(jobOptions,os.R_OK):
    print "FATAL: jobOptions not accessible!"
    sys.exit()

  # parse jobOptions file
  jobOptionsFile=open(jobOptions, 'r')
  command=""
  for i in [o for o in jobOptionsFile.readlines()]: #parse
    if "#End" in i : break
    command+=i
  jobOptionsFile.close()
  exec command

  # check for sframe environment
  if not 'SFRAME_DIR' in os.environ:
    print "FATAL: sframe environment not sourced"
    sys.exit()

  path2sframe=os.environ['SFRAME_DIR']
  userName=os.environ['USER']
  
  os.system('date')
  # set jobconfig file
  if not "jobConfig" in dir():
    jobConfig=path2sframe+'/user/config/JobConfig.dtd'
  print "%-30s : jobConfig='%s'" %("job config file", jobConfig)
  print "%-30s : jobOptions='%s'" %("job option file", jobOptions)

  # check jobconfig file
  if not os.access(jobConfig, os.R_OK):
    print "FATAL: jobConfig missing"
    sys.exit()

  # check for job name
  if not "jobName" in dir():
    print "Specify jobName under jobName="
    sys.exit()

  # set libraries
  if not "loadLibs" in dir():
    loadLibs=["libGenVector", "libGraf", "libSFramePlugIns", "libSFrameUser"]
  print "%-30s : loadLibs=%s" %("libraries", loadLibs)

  # set packages
  if not "loadPacks" in dir():
    loadPacks=["SFrameCore.par", "SFramePlugIns.par", "SFrameUser.par"]
  print "%-30s : loadPacks=%s" %("packages", loadPacks)

  # set input trees
  if not "inputTrees" in dir():
    inputTrees=["physics"]
  print "%-30s : inputTrees=%s" %("input trees", inputTrees)

  #set output trees
  if not "outputTrees" in dir():
    outputTrees=[]
  print "%-30s : outputTrees=%s" %("output trees", outputTrees)

  # set user items
  if not "userItems" in dir():
    userItems=[
              ["TriggerTreeString", "TriggerTree"],
              ["RecoTreeString", "RecoTree"],
              ["InfoTreeString", "InfoTree"],
              ]
  print "%-30s : userItems=%s" %("user items", userItems)

  # check cycle name
  if not "cycleName" in dir():
    print "FATAL: cycleName missing"
    sys.exit()

  # check path to temp directory
  if not "path2tmp" in dir():
    path2tmp="/tmp"
  if not options.path2tmp=="...":
    path2tmp=options.path2tmp
  path2tmp=os.path.expandvars(path2tmp)
  print "%-30s : path2tmp='%s'" %("temp directory", path2tmp)

  if not "path2tmplog" in dir():
    path2tmplog=path2tmp
  if not options.path2tmplog=="...":
    path2tmplog=options.path2tmplog
  path2tmplog=os.path.expandvars(path2tmplog)
  print "%-30s : path2tmplog='%s'" %("temp log directory", path2tmplog)

  if not "path2tmproot" in dir():
    path2tmproot=path2tmp
  if not options.path2tmproot=="...":
    path2tmproot=options.path2tmproot
  path2tmproot=os.path.expandvars(path2tmproot)
  print "%-30s : path2tmproot='%s'" %("temp root directory", path2tmproot)

  if not "path2tmpsh" in dir():
    path2tmpsh=path2tmp
  if not options.path2tmpsh=="...":
    path2tmpsh=options.path2tmpsh
  path2tmpsh=os.path.expandvars(path2tmpsh)
  print "%-30s : path2tmpsh='%s'" %("temp sh directory", path2tmpsh)

  # keep temporary directory
  if not "keepTemp" in dir():
    keepTemp=False
  if options.keepTemp:
    keepTemp=options.keepTemp
  print "%-30s : keepTemp=%s" % ("temporary directory behaviour", str(keepTemp))

  # use only given temporary directory 
  if not "fixTemp" in dir():
    fixTemp=False
  if options.fixTemp:
    fixTemp=options.fixTemp
  if fixTemp:
    keepTemp=True
  print "%-30s : fixTemp=%s" % ("use only path2tmp (no deletion)", str(fixTemp))

  # dont clean tmp 
  if not "cleanTmp" in dir():
    cleanTmp=True

  # no job submission, merging only
  if not "mergeOnly" in dir():
    mergeOnly=False
  if options.mergeOnly:
    mergeOnly=options.mergeOnly
  if mergeOnly:
    keepTemp=True
    fixTemp=True
    useBatch=False #FIXME need this?
  print "%-30s : mergeOnly=%s" % ("only merge files in path2tmp", str(mergeOnly))
  
  # set output level
  if not "outputLevel" in dir():
    outputLevel="INFO"
  print "%-30s : outputLevel='%s'" %("output level", outputLevel)

  # set run mode
  if not "runMode" in dir():
    runMode="LOCAL"
  print "%-30s : runMode='%s'" %("run mode", runMode)

  # set proof server
  if not "proofServer" in dir():
    proofServer="lite"
  print "%-30s : proofServer='%s'" %("PROOF server", runMode)

  # set proof work dir
  if not "proofWorkdir" in dir():
    proofWorkdir=""
  proofWorkdir=os.path.expandvars(proofWorkdir)
  print "%-30s : proofWorkdir='%s'" %("PROOF working directory", proofWorkdir)

  # set output directory dir
  if not "outDir" in dir():
    outDir=os.getcwd()
  outDir=os.path.expandvars(outDir)
  print "%-30s : outDir='%s'" %("output directory", outDir)
  if not os.path.exists(outDir):
    print "WARNING: output directory ",outDir," does not exist. Creating it."
    os.system("mkdir -p "+ outDir )
    #sys.exit()

  # set postfix
  if not "postFix" in dir():
    postFix=""
  print "%-30s : postFix='%s'" %("postfix", postFix)

  # set target lumi
  if not "targetLumi" in dir():
    targetLumi=1.
  print "%-30s : targetLumi=%s" %("target lumi", targetLumi)

  # set xml template
  if not "xmlTemplate" in dir():
    xmlTemplate="submitSFrame.xml"
  print "%-30s : xmlTemplate='%s'" %("xml template", xmlTemplate)

  # check xml template
  if not os.access(xmlTemplate, os.R_OK):
    print "FATAL: xml template missing"
    sys.exit()

  # check path to xml files
  if not "path2xml" in dir():
    print "FATAL: path2xml missing"
    sys.exit()
  path2xml=os.path.expandvars(path2xml)
  print "%-30s : path2xml=%s" %("path to xml files", path2xml)

  # check number of files per job
  if not "nFiles" in dir():
    nFiles=10
  print "%-30s : nFiles=%d" %("number of files per job", nFiles)

  # check number of files per job
  if not "nMaxFilesDataset" in dir():
    nMaxFilesDataset=-1
  print "%-30s : nMaxFilesDataset=%d" %("max number of files per dataset", nMaxFilesDataset)

  # set maximum number of events
  if not "nEventsMax" in dir():
    nEventsMax=-1
  #if not nFiles==-1:
    #nEventsMax=-1
  print "%-30s : nEventsMax=%s" %("max number of events per file", nEventsMax)

  # check if input is data for later weighting
  if not "isData" in dir():
    isData=False
  print "%-30s : isData=%s" %("input is data: ", str(isData))

  # set number of events to be skipped
  if not "nEventsSkip" in dir():
    nEventsSkip=0
  if not nFiles==-1:
    nEventsSkip=0
  print "%-30s : nEventsSkip=%s" %("events to skip", nEventsSkip)

  # set whether validation to be skipped
  if not "skipValid" in dir():
    skipValid=True
  print "%-30s : skipValid=%s" %("skip validation", skipValid)

  # set number of parallel processes
  if not "nProcesses" in dir():
    nProcesses="3"
  print "%-30s : nProcesses=%s" %("number of parallel processes", nProcesses)


  # using sandbox
  if not "useSandbox" in dir():
    useSandbox=False
  if options.useSandbox:
    useSandbox=options.useSandbox
  print "%-30s : useSandbox=%s" % ("sandbox", str(useSandbox))

  # running batch mode
  if not "useBatch" in dir():
    useBatch=False
  if options.useBatch:
    useBatch=options.useBatch
  print "%-30s : useBatch=%s" % ("batch mode", str(useBatch))

  # compiling in batch mode
  if not "batchCompile" in dir():
    batchCompile=False
  if options.batchCompile:
    batchCompile=options.batchCompile
  print "%-30s : batchCompile=%s" % ("batch compile", str(batchCompile))

  # additional compile commands
  if not "compilePacks" in dir():
    compilePacks=[]
  print "%-30s : compilePacks=%s" % ("additional packages to compile", compilePacks)

  # set hard CPU limit
  if not "hCPU" in dir():
    hCPU="00:30:00"
  print "%-30s : hCPU=%s" %("hard CPU limit", hCPU)

  # set hard VMEM limit
  if not "hVMEM" in dir():
    hVMEM="1500M"
  print "%-30s : hVMEM=%s" %("hard VMEM limit", hVMEM)

  # set job submission destination host
  if not "useHost" in dir():
    useHost=""
  if not useHost=="":
    print "Sending jobs to host: %s" %(useHost)

  if not "useOS" in dir():
    useOS=""
  if not useOS=="":
    print "Using OS: %s" %(useOS)

  # check data
  if not "dataSets" in dir():
    print "FATAL: data sets not set"
    sys.exit()

  # set delay for process check
  if not "timeCheck" in dir():
    timeCheck="30"
  print "%-30s : timeCheck=%s" %("delay for process check", timeCheck)

  if not "rootSetup" in dir():
    rootSetup="default"
  print "%-30s : rootSetup=%s" % ("Setup script for ROOT/Python", rootSetup)
  
  if not "runningJobsLimit" in dir():
    runningJobsLimit=-1
  print "%-30s : runningJobsLimit=%d" %("limit for running jobs", runningJobsLimit)
  if usedccp:
    print "%-30s : usedccp=%s" % ("use DCCP", str(usedccp))
  
  
  # create genXmlTemplate steering file
  genXmlTemplate = XmlTemplate(xmlTemplate, jobConfig, jobName, outputLevel, loadLibs, loadPacks, cycleName, runMode, proofServer, proofWorkdir, postFix, inputTrees, outputTrees, userItems)
  
  currentDir=os.getcwd()
  if fixTemp:
    if(path2tmplog):
      tempDirLog=path2tmplog
    else:
      tempDirLog=path2tmp
    if(path2tmproot):
      tempDirRoot=path2tmproot
    else:
      tempDirRoot=path2tmp
    if(path2tmpsh):
      tempDirSh=path2tmpsh
    else:
      tempDirSh=path2tmp
    
    os.system( "mkdir -p " + tempDirLog )
    os.system( "mkdir -p " + tempDirRoot )
    os.system( "mkdir -p " + tempDirSh )
  else:
    tempDirLog=tempfile.mkdtemp(prefix="sframe_%s_log_"%jobName, dir=path2tmplog)
    tempDirRoot=tempfile.mkdtemp(prefix="sframe_%s_root_"%jobName, dir=path2tmproot)
    tempDirSh=tempfile.mkdtemp(prefix="sframe_%s_sh_"%jobName, dir=path2tmpsh)
  
  if (useSandbox):
    analysisDir = (path2sframe.rstrip("/")).rstrip("SFrame")
    print "creating sandbox archive of %s and moving it to %s" %(analysisDir, tempDirSh)
    os.chdir( "%s" %(analysisDir) )
    os.system( "tar czf SFrameSandbox.tar.gz SFrame" )
    os.system( "mv SFrameSandbox.tar.gz %s" %(tempDirSh) )
    print "sandbox creation finished!"

  print "using temporary directories\n  %s (scripts)\n  %s (root)\n  %s (log)" %(tempDirSh,tempDirRoot,tempDirLog)
  os.chdir(tempDirSh)

  # clean up for new run
  if not mergeOnly and cleanTmp:
    os.system( "rm -f %s*.xml %s*.sh %s*.log %s*.root" % ((cycleName,)*4) )

  # create xml files and list of jobs to run
  listOfJobs=[]
  # loop over final data sets
  nJobs = 0
  for i in range(len(dataSets)):
    # loop over sub sets
    iFilesPerDataset=0
    for j in range(len(dataSets[i][1])):
      sampleLumi=0.
      add2dataSet=[]
      #enable .xml in jo for convenient copy/paste 
      if dataSets[i][1][j][-4:]=='.xml': dataSets[i][1][j]=dataSets[i][1][j][:-4] 
      inFileName=path2xml+'/'+str(dataSets[i][1][j])+'.xml'
      if not os.access(inFileName, os.R_OK):
        print inFileName+" not found, skipping it ..."
        continue
      fileNames=[]
      inFile=open(inFileName, 'r')
      line=inFile.readline()
      while line and (nMaxFilesDataset<0 or iFilesPerDataset<nMaxFilesDataset):
        if (line.strip()).startswith("<In FileName"):
          iFilesPerDataset+=1
          fileNames.append("      "+line)
          sampleLumi+=getFileLumi(line)
        line=inFile.readline()
      inputDataHeader=genXmlTemplate.getInputDataHeader()
      inputDataFooter=genXmlTemplate.getInputDataFooter()
      inFileText=""
      # print "sampleLumi=%f %s" %(sampleLumi, str(dataSets[i][1][j]))
      # print "targetLumi=%f" %(targetLumi)
      subsampleLumi=0.
      for fN in range(0, len(fileNames)):
        inFileText+=fileNames[fN]
        subsampleLumi+=getFileLumi(fileNames[fN])
        if fN==len(fileNames)-1 or (not nFiles==-1 and fN%nFiles==nFiles-1):
          subsampleTargetLumi=subsampleLumi*targetLumi/sampleLumi
          #print "  subsampleLumi=%f" %(subsampleLumi)
          #print "  subsampleTargetLumi=%f" %(subsampleTargetLumi)
          subJob=""
          if (not nFiles==-1 and fN%nFiles==nFiles-1):
            subJob="subjob"+str(fN/nFiles+1)
          inFileText=inputDataHeader+inFileText
          inFileText+=inputDataFooter
          if isData:
            inFileText=inFileText.replace("DATALUMI", str(subsampleTargetLumi))
          else:
            inFileText=inFileText.replace("DATALUMI", str(0.))
          inFileText=inFileText.replace("TYPE", str(dataSets[i][0]))
          inFileText=inFileText.replace("VERSION", str(dataSets[i][1][j]))
          inFileText=inFileText.replace("NEVENTSMAX", str(nEventsMax))
          inFileText=inFileText.replace("NEVENTSSKIP", str(nEventsSkip))
          inFileText=inFileText.replace("SKIPVALID", str(skipValid))
          thisXmlTemplate=deepcopy(genXmlTemplate)
          thisXmlTemplate.replace('TARGETLUMI', str(subsampleTargetLumi))
          thisXmlTemplate.replace("INPUTDATA", inFileText)
          baseName=cycleName+"."+str(dataSets[i][0])+"."+str(dataSets[i][1][j])+postFix
          thisXmlTemplate.write(baseName+subJob+'.xml')
          listOfJobs.append([str(dataSets[i][0]), str(dataSets[i][1][j]), baseName, subJob, "",tempDirSh,tempDirRoot,tempDirLog])
          nJobs+=1
          inFileText=""
          subsampleLumi=0.
      inFile.close()

  if useBatch:
    if batchCompile:
      print "running in batch mode ..."
      print "test compile ..."
      runningJobs=[]
      
      compileScript = BatchScript(useHost, useOS, path2sframe, useEnv, cmssw, hCPU, hVMEM, cycleName, tempDirLog)
      
      compileScript.replace("NAME", cycleName)
      compileScript.replace("STDOUT", tempDirLog+"/compile.log")
      #adding additional compilation commands
      compileScript.add("make distclean\n")
      compileScript.add("make\n")
      for c in compilePacks:
        compileScript.add("cd " +path2sframe+ "/" +c+ "\n")
        compileScript.add("make distclean && make\n")
      compileScript.add("cd %s\n" %(path2sframe))
      
      compileScript.write("compileJob.sh")
      
      lock=thread.allocate_lock()
      lock.acquire()
      compileProcess=subprocess.Popen("qsub compileJob.sh", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      compileProcess.wait()
      #runningJobs.append(cycleName)
      compileProcessStatus=compileProcess.poll()
      if compileProcessStatus==1:
        lock.release()
        sys.exit()
      else:
        lock.release()
        submitOut = compileProcess.stdout.read()
        runningJobs.append([submitOut.split(" ")[2], cycleName])
      waitForBatchJobs(runningJobs, listOfJobs, userName, timeCheck)

    print "sending jobs ..."
    runningJobs=[]
    iJobs=0
    skip=1
    if   len(listOfJobs)>=1000: skip = 100
    elif len(listOfJobs)>= 500: skip =  50
    elif len(listOfJobs)>= 160: skip =  20
    elif len(listOfJobs)>=  50: skip =  10
    elif len(listOfJobs)>=  20: skip =   5
    for j in listOfJobs:
      
      batchScript = BatchScript(useHost, useOS, path2sframe, useEnv, cmssw, hCPU, hVMEM, cycleName, tempDirLog)
      
      if (useSandbox):
        batchScript.add("cp %s/SFrameSandbox.tar.gz ${TMPDIR}\n" %(tempDirSh)) #copy sandbox archive to work dir
        tmppath2sframe = "${TMPDIR}/SFrame" # change sframe path to new location
        batchScript.addLine("cd ${TMPDIR}\n")
        batchScript.addLine("echo \"Creating soft-links\"\n")
        batchScript.addLine("for i in `ls -d %s*`; do ln -s $i; done;\n" %((path2sframe.rstrip("/")).rstrip("SFrame"))) #link SFrame installation to tmpdir
        batchScript.addLine("rm SFrame\n")
        batchScript.addLine("echo \"Unpacking Sandbox\"\n")
        batchScript.addLine("tar xzf SFrameSandbox.tar.gz\n")
        batchScript.addLine("ls -l\n")
        batchScript.addLine("cd %s\n" %(tmppath2sframe))
      else:
        batchScript.addLine("cd %s\n" %(path2sframe))
      
      batchScript.addLine("cd $TMPDIR\n")
      batchScript.addLine("cp -f %s .\n" %(tempDirSh+"/"+j[2]+j[3]+".xml"))
      
      # dccp and replace xml
      if (usedccp):
        batchScript.addLine("echo \"########## Copying files from dCache ############\"\n")
        batchScript.addLine("for i in `cat %s.xml | grep \"dcap://\" | awk '{ print $2; }'`; do LENGTH=(${#i}-1); DCAPFILE=`echo $i[11,$LENGTH]`; LOCALFILE=`basename $DCAPFILE`; echo dccp $DCAPFILE .; dccp $DCAPFILE .; ls $LOCALFILE; DCAPPATH=`dirname $DCAPFILE`; sed -i.bak 's|'\"$DCAPPATH\"'/||g' %s.xml; done; \n" %((j[2]+j[3]),(j[2]+j[3])))
        batchScript.addLine("echo \"######## Done copying files from dCache #########\"\n")
      
      batchScript.addLine("echo \"##################################################\"\n")
      batchScript.addLine("cat %s\n" %(j[2]+j[3]+".xml"))
      batchScript.addLine("echo \"##################################################\"\n")
      batchScript.addLine("date\n")
      batchScript.addLine("/usr/bin/time -v sframe_main %s\n" %(j[2]+j[3]+".xml"))
      batchScript.addLine("date\n")
      batchScript.addLine("echo \"##################################################\"\n")
      batchScript.addLine("echo $PWD\n")
      batchScript.addLine("ls -lh\n")
      batchScript.addLine("echo \"##################################################\"\n")
      batchScript.addLine("echo \"cp -f %s %s/%s\"\n" %(j[2]+".root", tempDirRoot, j[2]+j[3]+".root"))
      batchScript.addLine("cp -f %s %s/%s\n" %(j[2]+".root", tempDirRoot, j[2]+j[3]+".root"))
      #batchScript.addLine("cp -f %s %s/%s\n" %("Myroot_mutau.root",  tempDirRoot, j[0]+"_mutau_"+j[3]+".root"))
      #batchScript.addLine("cp -f %s %s/%s\n" %("Myroot_eletau.root", tempDirRoot, j[0]+"_eletau_"+j[3]+".root"))
      
      batchScript.replace("HCPU", hCPU)
      batchScript.replace("HVMEM", hVMEM)
      batchScript.replace("HOST", useHost)
      batchScript.replace("OSYSTEM", useOS)
      batchScript.replace("NAME", j[2]+j[3])
      batchScript.replace("STDOUT", tempDirLog+"/"+j[2]+j[3]+".log")
      
      batchScript.write(j[2]+j[3]+'.sh')
      
      lock=thread.allocate_lock()
      lock.acquire()
      nameOfJob=j[2]+j[3]
      nameOfJob=nameOfJob.split('.')[1]+nameOfJob.split('.')[2]
      runProcess=subprocess.Popen("qsub -q all.q -notify -N %s %s.sh" %(nameOfJob, j[2]+j[3]), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      runProcess.wait()
      #runningJobs.append(j[2]+j[3])
      runProcessStatus=runProcess.poll()
      if runProcessStatus==1:
        print "Error code %d when running\n   qsub -notify -N %s %s.sh\nExiting!" %(runProcessStatus, nameOfJob, j[2]+j[3])
        lock.release()
        sys.exit()
      else:
        lock.release()
        submitOut = runProcess.stdout.read()
        runningJobs.append([submitOut.split(" ")[2], j[2]+j[3]])
      if not (iJobs%skip):
        print "submitting job %d of %d"%(iJobs,nJobs),
        while runningJobsLimit>0:
          #subProcess=subprocess.Popen('qstat -u $USER | awk \'{print $5}\' | grep r |wc -l' , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
          #nRunning=int(subProcess.stdout.read())
          subProcess=subprocess.Popen('qstat -u $USER | wc -l' , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
          nSubmitted=int(subProcess.stdout.read())-2
          #print " submitted:",nSubmitted
          if nSubmitted<runningJobsLimit: break
          print "|",
          time.sleep(float(timeCheck*2))
        print
        
      iJobs+=1
    waitForBatchJobs(runningJobs, listOfJobs, userName, timeCheck)
    while not len(dataSets)==0:
      print "\nwaiting for %d data sets to finish" %(len(dataSets))
      checkCompletion(dataSets, listOfJobs, outDir, cycleName, postFix,keepTemp)
      time.sleep(float(timeCheck))
  elif not mergeOnly:
    # process list of jobs
    runningJobs=[]
    for j in listOfJobs:
      while not len(runningJobs)<int(nProcesses):
        checkRunningJobs(runningJobs, listOfJobs, timeCheck)
      jobDir=tempfile.mkdtemp(dir=tempDirSh, prefix=(j[2]+j[3])+"_")
      os.chdir(jobDir)
      runningJobs.append([runCommand(j[2], j[3]), (j[2]+j[3]), jobDir])
      runningJobs[-1][0].start()
      os.chdir(tempDirSh)
      checkCompletion(dataSets, listOfJobs, outDir, cycleName, postFix,keepTemp)
    while not len(runningJobs)==0:
      checkRunningJobs(runningJobs, listOfJobs, timeCheck)
    while not len(dataSets)==0:
      print "\nwaiting for %d data sets to finish" %(len(dataSets))
      checkCompletion(dataSets, listOfJobs, outDir, cycleName, postFix,keepTemp)
      time.sleep(float(timeCheck))
  else:
    runningJobs=[]
    for j in listOfJobs:
      runningJobs.append(["-1",j[2]+j[3]])
    waitForBatchJobs(runningJobs, listOfJobs, userName, 0)
    checkCompletion(dataSets, listOfJobs, outDir, cycleName, postFix,keepTemp)
  
  os.chdir(currentDir)
  if not keepTemp:
    print "\nremoved temporary directory with scripts and root file:"
    print  "  %s" % ('/'.join((tempDirSh.split('/')[-1:])))
    print  "  %s" % ('/'.join((tempDirRoot.split('/')[-1:])))
    print "kept temporary directory with log files:"
    print  "  %s" % ('/'.join((tempDirLog.split('/')[-1:])))
    shutil.rmtree(tempDirSh)
    shutil.rmtree(tempDirRoot)
  
  if "postExec" in dir():
    print "Executing:\n%s \n\n" % postExec
    exec postExec
  
  accountTime(jobOptions,jobName,nJobs)
  
  print "\nTschoe!\n"
  


def partitionFileNames(fileBaseNameRoot):
  """Help function to convert root file basename to a file name pattern for merging with hadd."""
  
  # fileToMerge=fileBaseNameRoot.partition("pythia8")[0]+fileBaseNameRoot.partition("pythia8")[1]+'*'
  # fileToMerge=fileToMerge.partition("Run2016")[0]+fileToMerge.partition("Run2016")[1]+'*'
  # fileToMerge=fileToMerge.partition("Run2017")[0]+fileToMerge.partition("Run2017")[1]+'*'
  # fileToMerge=fileToMerge.partition("Run2018")[0]+fileToMerge.partition("Run2018")[1]+'*'
  # fileToMerge=fileToMerge.partition("madgraph")[0]+fileToMerge.partition("madgraph")[1]+'*'
  
  fileToMerge = fileBaseNameRoot
  for token in [ "pythia8", "madgraph", "Run2016", "Run2017", "Run2018" ]:
    part        = fileToMerge.partition(token)
    letters     = dataSetLetters(part[2])
    fileToMerge = part[0]+part[1]+letters+'*'
  
  while "**" in fileToMerge: fileToMerge=fileToMerge.replace("**",'*')
  return fileToMerge
  


def dataSetLetters(string):
  """"Help function to find dataset letter(s) (ABCDE) at the beginning of a string"""
  letters = ""
  dataSetLetters = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'H', 'I', 'J', 'K' ]
  if len(string)>0:
    for character in string:
      #print "%s <-> %s"%(character,dataSetLetters)
      if len(dataSetLetters)==0: break
      for i, letter in enumerate(dataSetLetters):
        if character == letter:
          letters += letter
          dataSetLetters = dataSetLetters[i+1:]
          break
      else: break # stop once no other letter was found
  return letters
  


def accountTime(jobOptions,jobName,nJobs):
  """Append summary to a log file."""
  
  logdir="nohup"
  makeDirectory(logdir)
  filepath="%s/submitSFrame.log"%logdir
  new = not os.path.exists(filepath)
  
  global succesRates, starttime, startdate
  succesRates = "succes rate(s):\n" + '\n'.join(sorted(succesRates)) + '\n'
  minutes, seconds = divmod(time.time()-starttime,60)
  hours, minutes   = divmod(minutes,60)
  
  with open(filepath,"a") as file:
    if new: file.write("# log file of submitSFrame.py\n\n")
    file.write("%s: %s\n" % (jobName, jobOptions.split('/')[-1]))
    file.write("number of jobs: %s\n" % (nJobs))
    file.write(succesRates)
    file.write("start: %s\n" % (startdate))
    file.write("done:  %s\n" % (time.strftime("%a %d/%m/%Y %H:%M:%S",time.gmtime())))
    file.write("took:  %d hours, %d minutes and %.1f seconds\n" % (hours,minutes,seconds))
    file.write("\n")
  print "\nDone after %d hours, %d minutes and %.1f seconds." % (hours,minutes,seconds)
  


def makeDirectory(DIR):
  """Make directory if it does not exist."""
  if not os.path.exists(DIR):
    os.makedirs(DIR)
    #print ">>> made directory " + DIR
    


if __name__ == "__main__":
  main()
