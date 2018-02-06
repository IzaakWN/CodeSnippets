#! /usr/bin/env python
# Author: Izaak Neutelings (2016)

import time
start = time.time()
import os, sys #, ROOT
from ROOT import TFile, TTree, TObject
#import numpy # to set branch addres
from math import log, pow, floor

# https://root.cern.ch/root/html/tutorials/tree/copytree.C.html
# https://root.cern.ch/root/html/tutorials/tree/copytree3.C.html
# to get branch channel with string "channel": getattr(oldtree,"channel")

# /scratch/ineuteli/SFrameAnalysis/AnalysisOutput/
# /shome/ineuteli/analysis/SFrameAnalysis/AnalysisOutput/

# TODO: method for adding variables (weights, jpt, etc.) to tree.

mylabel     = "_Moriond"
DIR         = "."
doLFT       = True #and False
doEES       = True #and False
doTES       = True and False
doNominal   = True #and False
testRun     = True and False
verbosity   = 0


# CUTS
isocuts   = "iso_cuts==1"
isocuts_relaxed = "iso_1<0.5" #&& (iso_2_medium==1 || iso_2==1)"
vetos     = "lepton_vetos==0"
ptcut     = "(pt_1>26||(channel==1 && pt_1>23))"
triggers  = "abs(eta_1)<2.1 && (( %s && (triggers==1||triggers==3))||(triggers>1))" % ptcut



    ###############
    # checkEvents #
    ###############

def checkEvents(oldfilename, treenames, **kwargs):
    """Check number of events in trees."""
    start_here  = time.time()
    verbosity   = kwargs.get('verbosity',0)
    treelabel   = kwargs.get('treelabel',"")
        
    # TREENAME
    treename = ""
    if isinstance(treenames,str): treenames = [treenames]
    if len(treenames) == 1:       treename  = "_%s"%treenames[0]
    print ">>> checking tree(s) %s from file \"%s\""%(treenames,oldfilename)
    
    # FILE
    oldfile     = TFile(oldfilename)
    
    # PRINT
    printVerbose(">>>   file in:    \"%s\"" % (oldfilename),verbosity)
    
    for oldtreename in treenames:
        if oldtreename: oldtreename += treelabel
        oldtree     = oldfile.Get(oldtreename)
        if not oldtree:
            print warning("Could not find tree \"%s\" => ignoring" % (oldtreename),pre="  ")
            continue
        print ">>>    %s has %5i entries" % (oldtreename,oldtree.GetEntries())
    oldfile.Close()
    
    print ">>> took %.2f seconds." % (time.time()-start_here)
    print ">>> "
    


    ###########
    # cutTree #
    ###########

def cutTree(oldfilename, treenames, **kwargs):
    """Extract tree from file and save in new one."""
    start_here  = time.time()
    verbosity   = kwargs.get('verbosity',0)
        
    # TREENAME
    treename = ""
    if isinstance(treenames,str): treenames = [treenames]
    if len(treenames) == 1:       treename  = "_%s"%treenames[0]
    print ">>> extracting tree(s) from file"
    N           = kwargs.get('N',-1)
    
    # CUTS
    cuts        = kwargs.get('cuts',"channel>0")
    if isinstance(cuts,str):      cuts = [cuts]*len(treenames)
    if len(treenames)!=len(cuts): print warning("cutTree: len(treenames)!=len(cuts)")
    
    # FILE OPTIONS
    newfilename = kwargs.get('newfilename',False)
    update      = kwargs.get('update',False) # update file
    if not newfilename:
        if update: newfilename = oldfilename
        else:      newfilename = oldfilename.replace(".root","%s_string.root"%(treename))
    copycontents = kwargs.get('copy',False) and oldfilename!=newfilename # copy all contents of oldfile to newfile
    option      = 'read' if copycontents else ('update' if update else 'recreate')
    option      = kwargs.get('option',option)
    label       = kwargs.get('label',"_cut" if (oldfilename==newfilename) else "")
    
    # FILE
    oldfile     = TFile(oldfilename)
    if copycontents: succes = oldfile.Cp(newfilename,True)
    newfile     = TFile(newfilename,'update')
    
    # PRINT
    printVerbose(">>>   file in:    \"%s\"" % (oldfilename),verbosity)
    printVerbose(">>>   file out:   \"%s\"" % (newfilename),verbosity)
    printVerbose(">>>   tree label: \"%s\"" % (label),verbosity)
    printVerbose(">>>   settings:   update=%s, option=\"%s\", copycontents=%s" % (update,option,copycontents),verbosity)
    
    for treename, cut in zip(treenames,cuts):
        oldtree     = oldfile.Get(treename)
        newtreename = treename+label
        if treename != newtreename and oldfile.Get(newtreename):
            print warning("There already exists a tree of name \"%s\" => ignoring" % (newtreename),pre="  ")
            continue
        if verbosity>0:
            print ">>>   copying tree \"%s\" into \"%s\" with cuts" % (treename,newtreename)
            print ">>>     \"%s\"" % (cut),verbosity
        else: print ">>>   copying tree \"%s\" into \"%s\"" % (treename,newtreename)
        newtree     = None
        maxmessage  = ""
        if N>0:
            newtree    = oldtree.CopyTree(cut,"",N)
            maxmessage = " (max %i)"%N
        else:
            newtree = oldtree.CopyTree(cut)
        #newtree.SetName(newtreename)
        newtree.Write(newtreename,TObject.kOverwrite)
        print ">>>   extraction done: %i%s of %i entries copied" % (newtree.GetEntries(),maxmessage,oldtree.GetEntries())
    
    print ">>>   writing and closing new file: %s" % (newfilename)  
    #newfile.Write(TObject.kOverwrite)
    newfile.Close()
    oldfile.Close()
    
    print ">>> took %.2f seconds." % (time.time()-start_here)
    print ">>> "
    




    ########
    # main #
    ########

def main():
    """Main method: list files and which trees to extract."""
    
    # FILES
    files = [
        ( "LowMass",         "LowMass_20GeV_DiTauResonance" ),
        ( "LowMass",         "LowMass_28GeV_DiTauResonance" ),
        ( "LowMass",         "LowMass_40GeV_DiTauResonance" ),
        ( "LowMass",         "LowMass_50GeV_DiTauResonance" ),
        ( "LowMass",         "LowMass_60GeV_DiTauResonance" ),
        ( "LowMass",         "LowMass_70GeV_DiTauResonance" ),
#         ( "SingleMuon",      "SingleMuon_Run2016"           ),
#         ( "SingleElectron",  "SingleElectron_Run2016"       ),
#         ( "TT", "TT_TuneCUETP8M1"                           ),
#         ( "TT", "TTJets_DiLept"                             ),
#         ( "TT", "TTJets_SingleLeptonFromT"                  ),
#         ( "TT", "TTJets_SingleLeptonFromTbar"               ),
#         ( "DY", "DYJetsToLL_M-10to50_TuneCUETP8M1"          ),
#         ( "DY", "DY1JetsToLL_M-10to50_TuneCUETP8M1"         ),
#         ( "DY", "DY2JetsToLL_M-10to50_TuneCUETP8M1"         ),
#         ( "DY", "DY3JetsToLL_M-10to50_TuneCUETP8M1"         ), 
#         ( "DY", "DYJetsToLL_M-50_TuneCUETP8M1"              ), 
#         ( "DY", "DY1JetsToLL_M-50_TuneCUETP8M1"             ),
#         ( "DY", "DY2JetsToLL_M-50_TuneCUETP8M1"             ),
#         ( "DY", "DY3JetsToLL_M-50_TuneCUETP8M1"             ),
#         ( "DY", "DY4JetsToLL_M-50_TuneCUETP8M1"             ),
#         ( "WJ", "WJetsToLNu_TuneCUETP8M1"                   ), 
#         ( "WJ", "W1JetsToLNu_TuneCUETP8M1"                  ),
#         ( "WJ", "W2JetsToLNu_TuneCUETP8M1"                  ),
#         ( "WJ", "W3JetsToLNu_TuneCUETP8M1"                  ),
#         ( "WJ", "W4JetsToLNu_TuneCUETP8M1"                  ),
#         ( "WW", "WWTo1L1Nu2Q_13TeV_nlo"                     ),
#         ( "WZ", "WZTo3LNu_TuneCUETP8M1_13TeV_nlo"           ),
#         ( "WZ", "WZTo1L1Nu2Q_13TeV_nlo"                     ),
#         ( "WZ", "WZTo2L2Q_13TeV_nlo"                        ),
#         ( "WZ", "WZJToLLLNu_nlo"                            ),
#         ( "VV", "VVTo2L2Nu_13TeV_nlo"                       ),
#         ( "ZZ", "ZZTo2L2Q_13TeV_nlo"                        ),
#         ( "ZZ", "ZZTo4L_13TeV_nlo"                          ),
#         ( "ST", "ST_tW_top_5f_inclusiveDecays"              ),
#         ( "ST", "ST_tW_antitop_5f_inclusiveDecays"          ),
#         ( "ST", "ST_t-channel_top_4f_inclusiveDecays"       ),
#         ( "ST", "ST_t-channel_antitop_4f_inclusiveDecays"   ),
        ( "HTT",  "GluGluHToTauTau_M125"                    ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-25"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-30"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-35"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-40"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-45"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-50"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-55"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-60"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-65"           ),
        ( "SUSY", "SUSYGluGluToBBa1ToTauTau_M-70"           ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-15"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-20"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-25"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-30"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-35"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-40"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-45"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-50"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-55"  ),
#         ( "SUSY", "SUSYGluGluToHToAA_AToBB_AToTauTau_M-60"  ),
#         ( "SUSY", "SUSYVBFToHToAA_AToBB_AToTauTau_M-20"     ),
#         ( "SUSY", "SUSYVBFToHToAA_AToBB_AToTauTau_M-40"     ),
#         ( "SUSY", "SUSYVBFToHToAA_AToBB_AToTauTau_M-60"     ),
#         ( "VBF",  "VBFHToTauTau_M125_13TeV_powheg_pythia8"  ),
    ]
    
    
    # SHIFTS
    newfiles = [ ]
    if doEES:
      for subdir,filename in files:
        if subdir not in ["SingleMuon","SingleMuon","MuonEG","data"]:
          newfiles.append((subdir,filename+"_EES0p99"))
          newfiles.append((subdir,filename+"_EES1p01"))
    if doTES:
      for subdir,filename in files:
        if subdir in ["DY","TT","LowMass","SUSY"]:
          newfiles.append((subdir,filename+"_TES0p97"))
          newfiles.append((subdir,filename+"_TES1p03"))
    if doLFT:
      for subdir,filename in files:
        if subdir in ["DY"]:
          newfiles.append((subdir,filename+"_LTF0p97"))
          newfiles.append((subdir,filename+"_LTF1p03"))
    if doNominal: files += newfiles
    else:         files  = newfiles
    
    
    # CHANNEL & TREENAMES
    channels  = [   "mutau",
                    "etau"
    ]
    treenames = ["tree_%s"%c for c in channels]
    
    
    nFiles    = len(files)
    Nmax      = -1 #000000
    #cuts      = "channel>0 && abs(eta_1)<2.1 && %s && %s" % (isocuts,vetos)
    cuts      = "channel>0 && abs(eta_1)<2.1 && %s && %s" % (isocuts_relaxed,vetos) # RELAXED #triggers
    #OUTDIR    = "%s/trimmed"%DIR; ensureDirectory(OUTDIR)
    for i, (subdir, sample) in enumerate(files):
        print ">>> %i/%i files: %s"%(i+1,nFiles,sample)
        oldfilename = "%s/%s/TauTauAnalysis.%s%s.root" % (DIR,subdir,sample,mylabel)
        #newdir      = "%s/%s"%(OUTDIR,subdir); ensureDirectory(newdir)
        #newfilename = "%s/TauTauAnalysis.%s%s.root" % (newdir,sample,mylabel)
        if os.path.isfile(oldfilename):
            if testRun:
                print oldfilename
                continue
            #cutTree(oldfilename,treenames,cuts=cuts,newfilename=newfilename,copycontents=True) # make new file, copy all contents of old file
            #cutTree(oldfilename,treenames,cuts=cuts,update=True,verbosity=verbosity) # update old file: add new cut tree
            cutTree(oldfilename,treenames,cuts=cuts,update=True,verbosity=verbosity,label="_cut_relaxed") # RELAXED
        else: print warning("%s does not exist!"%oldfilename,pre="  ")+"\n>>> "
    




    ##################
    # Help functions #
    ##################

def ensureDirectory(DIR):
    """Make directory if it does not exist."""
    
    if not os.path.exists(DIR):
        os.makedirs(DIR)
        print ">>> made directory " + DIR

def green(string,**kwargs):   return "\x1b[0;32;40m%s\033[0m"%string
def error(string,**kwargs):   print ">>> %s\033[1m\033[91mERROR! %s\033[0m"%(kwargs.get('pre',""),string)
def warning(string,**kwargs): print ">>> %s\033[1m\033[93mWarning!\033[0m\033[93m %s\033[0m"%(kwargs.get('pre',""),string)

def printVerbose(string,verbosity,**kwargs):
    """Print string if verbosity is true or verbosity int is lager than given level."""
    level = kwargs.get('level',False)
    if level:
        if verbosity>=level: print string
    elif verbosity: print string

def makeThreshold(n,**kwargs):
    """Help function to find a good stepsize for read out when looping over a large number N.
       In a for loop with index i, you could do a print out like:
         if i % threshold == 0: print "some progress message" """
    max_digits = kwargs.get('max',6)
    #                      floor(log(N/10.0,10))        stepsize = (number of digits in N) - 2
    #              max(0.0,floor(log(N/10.0,10)))       make sure it is at least 0
    #        min(6,max(0.0,floor(log(N/10.0,10))))      set maximum step size to 10^6 (otherwise one has to wait too long for an update)
    # pow(10,min(6,max(0.0,floor(log(N/10.0,10)))))     make treshold a power of 10
    return pow(10,min(max_digits,max(0.0,floor(log(n/10.0,10)))))
    




if __name__ == '__main__':
    print
    main()
    end = time.time()
    print ">>>\n>>> done in %.2f seconds\n" % (end-start)
    

