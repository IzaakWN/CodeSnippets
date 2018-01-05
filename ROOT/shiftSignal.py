#!/usr/bin/env python
# https://wiki.physik.uzh.ch/cms/limits:brazilianplotexample

import sys
# import subprocess
# import PlotTools.CMS_lumi as CMS_lumi
# import PlotTools.tdrstyle as tdrstyle
# from PlotTools.PrintTools import color
# import numpy as np
import ROOT
from ROOT import TGraphErrors, TGraphAsymmErrors, TFile, TH1F, TH2F, THStack, TCanvas, TLegend, kGreen, kYellow, kOrange, gPad, gROOT, gStyle
from math import floor, ceil
# ROOT.gROOT.SetBatch(ROOT.kTRUE)
# gStyle.SetOptStat(0)

DIR_datacards   = "/shome/ineuteli/analysis/CMSSW_7_4_7/src/CombineHarvester/LowMassTauTau/datacards"
DIR             = "/shome/ineuteli/analysis/CMSSW_7_4_7/src/CombineHarvester/LowMassTauTau/output"



# EXTRACT bins
def extractBins(oldfilename,**kwargs):
    '''Make new datacards with just one bin.'''
    print ">>>\n>>> extractBins()"
    # smearing: https://root.cern.ch/phpBB3/viewtopic.php?t=7486
    # https://en.wikipedia.org/wiki/Box-Muller_transform
    
    oldfile         = TFile(oldfilename, 'READ')
    oldhistograms   = oldfile.GetListOfKeys() 
    nBins = oldfile.Get("TTT").GetNbinsX()
    print ">>> nBins = %s" % nBins
    bins = range(1,nBins)
    
    for bin in bins:
        #newfilename = oldfilename.replace(".root","_B%s.root"%bin)
        #oldfile = TFile(oldfilename, 'RECREATE')
        
        for histkey in oldhistograms:
            print ">>> %s" % histkey
            
        #newfile.Close()
        
    oldfile.Close()
        
        
        
def main():
    print ""
    
    channels = ['mt', 'et']
    filenames = [ ]
    
    for channel in channels:
        filenames.append("%s/xtt_%s.inputs-LowMassDiTau-13TeV-28.root" % (DIR_datacards,channel))
    
    for filename in filenames:
        print ">>> filename = %s" % filename
        shiftSignal(filename)
    
    
    
    
    
if __name__ == '__main__':
    main()
    print ">>>\n>>> done\n"

