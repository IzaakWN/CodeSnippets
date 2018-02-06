#! /usr/bin/env python
# /shome/ineuteli/production/MG5_aMC_v2_5_4/ExRootAnalysis/ExRootLHEFConverter
# xrdcp -f root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/ineuteli/samples/...

import os, sys
import re
from math import sqrt, pi
import PlotTools.CMS_lumi as CMS_lumi
import PlotTools.tdrstyle as tdrstyle
import ROOT
from ROOT import gROOT, gSystem, gPad, gStyle, gRandom, gDirectory, gSystem, TGaxis,\
                 TFile, TTree, TH1F, TH1D, TH2F, THStack, TCanvas, TLegend,\
                 TText, TLatex, TLorentzVector,\
                 kBlue, kAzure, kRed, kGreen, kYellow, kOrange, kMagenta
from argparse import ArgumentParser
#import os; os.getenv('DYLD_LIBRARY_PATH')
gSystem.Load("/shome/ineuteli/production/MG5_aMC_v2_5_4/ExRootAnalysis/libExRootAnalysis.so")
ROOT.gROOT.SetBatch(ROOT.kTRUE)
gStyle.SetOptStat(0)
TGaxis.SetExponentOffset(-0.060,0.005,'y')

argv = sys.argv
usage = '''This script makes plots for root files from LHE files.'''
parser = ArgumentParser(prog="checkLHE",description=usage,epilog="Succes!")
parser.add_argument( "-N", "--max-events", dest="Nmax", type=int, default=-1, action='store',
                     metavar="N_EVENTS_MAX", help="maximum number of events per root file.")
args = parser.parse_args()

Nmax        = int(args.Nmax)    # maximum number of events
LHE_DIR     = "lhe_files_noDRcut"
OUT_DIR     = "plotsLHE"
plotslabel  = "_dRgt0.4"

# CMS style
lumi                  = 35.9 # 12.9
CMS_lumi.cmsText      = "CMS"
CMS_lumi.extraText    = "Preliminary"
CMS_lumi.cmsTextSize  = 0.65
CMS_lumi.lumiTextSize = 0.60
CMS_lumi.relPosX      = 0.105
CMS_lumi.outOfFrame   = True
CMS_lumi.lumi_13TeV   = "%s fb^{-1}" % lumi
tdrstyle.setTDRStyle()

colors = [ kRed+1, kAzure+5, kGreen+2, kOrange+1, kMagenta-3, kYellow+1,
           kRed-9, kAzure-4, kGreen-2, kOrange+6, kMagenta+3, kYellow+2 ]



def makeLaTeX(string):
    """Replace LaTeX patterns."""
    
    if "tau" in string:
        string = string.replace("tau","#tau")
    if "mu" in string:
        string = string.replace("mu","#mu")
    if "eta" in string:
        string = string.replace("eta","#eta")
    if '_' in string:
        #string = string.replace('_',"_{") + '}'
        string = re.sub(r"_([^{}\(\)<>=\ ]+)",r"_{\1}",string).replace('{t}','{T}')
    if "dR" in string:
        string = string.replace("dR","#DeltaR")
    if "pt" in string:
        string = string.replace("pt","p_{T}")
    
    return string
    
def deltaPhi(phi1,phi2):
    """Returns difference between two given phi coordinates."""
    dphi = phi2-phi2
    while dphi > pi: dphi -= 2*pi
    while dphi > pi: dphi += 2*pi
    return dphi
    
def deltaR(eta1,phi1,eta2,phi2):
    """Returns DeltaR between two given (eta,phi) coordinates."""
    deta = abs(eta2-eta1)
    dphi = deltaPhi(phi1,phi2)
    return sqrt(deta**2 + dphi**2)
    
def pt(particle):
    """Returns pt for TRootLHEFParticle particle from ExRootAnalysis"""
    return sqrt(particle.Px**2 + particle.Py**2)
    


def makeHistsFromLHETree(tree,**kwargs):
    """Loops over LHE trees and fill histograms."""
    
    label       = kwargs.get('label',"")
    nEventsRun  = 0
    nNoXboson   = 0
    
    hists               = { }
    hists["dR_tautau"]  = TH1F("dR_tautau"+label,   "dR_tautau",          100,  0,   4)
    hists["dR_bX"]      = TH1F("dR_bX"+label,       "dR_bX",               70,  0,   7)
    hists["m_tautau"]   = TH1F("m_tautau"+label,    "m_tautau",           100,  0, 100)
    hists["m_bX"]       = TH1F("m_bX"+label,        "m_bX",              1400,  0,1400)
    hists["eta_bquark"] = TH1F("eta_bquark"+label,  "b quark eta",         30, -5,   5)
    hists["eta_lquark"] = TH1F("eta_lquark"+label,  "light quark eta",     30, -5,   5)
    hists["pt_bquark"]  = TH1F("pt_bquark"+label,   "b quark pt",          50,  0, 500)
    hists["pt_lquark"]  = TH1F("pt_lquark"+label,   "light quark pt",      30,  0, 120)
    hists["eta_tau1"]   = TH1F("eta_tau1"+label,    "leading tau eta",     30, -5,   5)
    hists["eta_tau2"]   = TH1F("eta_tau2"+label,    "subleading tau eta",  30, -5,   5)
    hists["pt_tau1"]    = TH1F("pt_tau1"+label,     "leading tau pt",      60,  0, 300)
    hists["pt_tau2"]    = TH1F("pt_tau2"+label,     "subleading tau pt",   60,  0, 300)
    
    for ievent, event in enumerate(tree,1):
      #print ">>> event %d"%(ievent)
      if Nmax>0 and Nmax<ievent: break
      
      taus    = [ ]
      bquarks = [ ]
      lquarks = [ ]
      Xbosons = [ ]
      Bprimes = [ ]
      mothers = [ 6000007 ]
      #print ">>>   %5s %8s %8s %8s"%("index","PID","M1","M1.PID")
      for iparticle, particle in enumerate(event.Particle,1):
        PID       = abs(particle.PID)
        mother    = event.Particle[particle.Mother1] if particle.Mother1>-1 else None
        motherPID = abs(mother.PID) if mother else "x"
        #print ">>>   %5d %8d %8d %8s"%(iparticle,particle.PID,particle.Mother1,mother.PID if mother else "x")
        if PID==15: # 7000021
          taus.append(particle)
        elif PID==7000021:
          Xbosons.append(particle)
        elif not mother:
          mothers.append(PID)
        elif motherPID in mothers:
          #print ">>> PID=%d, M1=%d"%(PID,event.Particle[particle.Mother1].PID)
          if PID<5:
            lquarks.append(particle)
          elif PID==5:
            bquarks.append(particle)
      
      if len(taus)==2:
        tau1, tau2 = taus
        tlv1 = TLorentzVector(tau1.Px,tau1.Py,tau1.Pz,tau1.E)
        tlv2 = TLorentzVector(tau2.Px,tau2.Py,tau2.Pz,tau2.E)
        dR   = tlv1.DeltaR(tlv2)
        if dR<0.4: continue
        hists["dR_tautau"].Fill( dR              )
        hists["m_tautau"].Fill(  (tlv1+tlv2).M() )
        hists["eta_tau1"].Fill( tau1.Eta )
        hists["pt_tau1"].Fill(  pt(tau1) )
        hists["eta_tau2"].Fill( tau2.Eta )
        hists["pt_tau2"].Fill(  pt(tau2) )
      else: warning("len(taus)=%d!=2"%(len(taus)),pre="  ")
      
      if len(lquarks)==1:
        hists["eta_lquark"].Fill( lquarks[0].Eta )
        hists["pt_lquark"].Fill(  pt(lquarks[0]) )
      else: warning("len(lquarks)=%d!=1"%(len(lquarks)),pre="  ")
      
      if len(bquarks)==1:
        hists["eta_bquark"].Fill( bquarks[0].Eta )
        hists["pt_bquark"].Fill(  pt(bquarks[0]) )
        if len(Xbosons)==1:
          tlv1 = TLorentzVector(bquarks[0].Px,bquarks[0].Py,bquarks[0].Pz,bquarks[0].E)
          tlv2 = TLorentzVector(Xbosons[0].Px,Xbosons[0].Py,Xbosons[0].Pz,Xbosons[0].E)
          hists["dR_bX"].Fill( tlv1.DeltaR(tlv2) )
          hists["m_bX"].Fill(  (tlv1+tlv2).M()   )
        else:
          if len(Xbosons)==0: nNoXboson += 1
          #warning("len(Xbosons)=%d!=1"%(len(Xbosons)),pre="  ")
      else: warning("len(bquarks)=%d!=1"%(len(bquarks)),pre="  ")
      nEventsRun+=1
    
    if nEventsRun>0 and nNoXboson > 1:
      warning("%d events out of %s (%.1f%%) have no X boson!"%(nNoXboson,nEventsRun,100.0*nNoXboson/nEventsRun),pre="  ")
    
    return hists
    


def compareVarsForLHESamples(filesetname,filenames):
    """Compare shapes of different variables for the same sample file."""
    print ">>>\n>>> compareVarsForSamples()"
    
    treename    = "LHEF"
    dirname     = makeDirectory(OUT_DIR)
    
    files       = [ ]
    hists       = { }
    
    # GET histograms
    for ifile, (filename,filetitle) in enumerate(filenames,1):
        print ">>> %s: %10s, %10s"%(ifile,filename,filetitle)
        file  = TFile("%s/%s"%(LHE_DIR,filename))
        tree  = file.Get(treename)
        print ">>>   %d events"%(tree.GetEntries())
        if hists.get(filetitle,False):
          warning("\"%s\" already exists!"%(filetitle))
        filehists = makeHistsFromLHETree(tree)
        #print filehists
        
        for histkey, hist in filehists.items():
          if histkey not in hists: hists[histkey] = [ ]
          #print ">>>   %-10s - %s"%(histkey,filetitle)
          hists[histkey].append((filetitle,hist))
        files.append(file)
    
    # DRAW
    for histkey, filehists in hists.items():
        
        ymax = 0
        hist1  = None
        width  = 0.30
        legendTextSize = 0.035
        height = 0.05+len(filehists)*0.038
        #x1 = 0.16; x2 = x1 + width # Left
        x2 = 0.84; x1 = x2 - width # Right
        y1 = 0.88; y2 = y1 - height # Top
        if "eta" in histkey:
          x1 = 0.34; x2 = x1 + width # Center
          if "tau" in histkey or "bquark" in histkey:
            y1 = 0.14; y2 = y1 + height # Bottom
        elif "pt_bquark" in histkey:
          if "600" in filesetname or "800" in filesetname:
            x1 = 0.16; x2 = x1 + width # Left
        elif "pt_tau" in histkey:
          if "600" in filesetname or "800" in filesetname:
            x1 = 0.26; x2 = x1 + width # CenterLeft
            y1 = 0.15; y2 = y1 + height # Bottom
        #elif "dR_bX" in histkey:
          #x1 = 0.16; x2 = x1 + width # Left
          #elif "tau" in histkey:
          #  y1 = 0.88; y2 = y1 - height
        elif "m_bX" in histkey:
          if "400" in filesetname or "600" in filesetname or "800" in filesetname:
            x1 = 0.16; x2 = x1 + width # Left
        
        canvas = TCanvas("canvas","canvas",100,100,800,600)
        canvas.SetBottomMargin(0.12)
        canvas.SetRightMargin(0.05)
        canvas.SetLeftMargin(0.12)
        canvas.SetTopMargin(0.08)
        legend = TLegend(x1,y1,x2,y2)
         
        for i, (filetitle,hist) in enumerate(filehists):
            histname    = "%s_%s"%(histkey,i)
            N1          = hist.GetEntries()
            
            # REBIN
            if "m_bX" in histkey:
              if "170" in filesetname:
                hist.GetXaxis().SetRangeUser(120,240)
              elif "400" in filesetname:
                hist.Rebin(7)
                hist.GetXaxis().SetRangeUser(120,600)
              elif "600" in filesetname:
                hist.Rebin(14)
                hist.GetXaxis().SetRangeUser(0,1000)
              elif "800" in filesetname:
                hist.Rebin(20)
                hist.GetXaxis().SetRangeUser(0,1400)
            elif "pt_tau" in histkey:
              if "400" in filesetname:
                hist.Rebin(3)
              elif "600" in filesetname:
                hist.Rebin(3)
              elif "800" in filesetname:
                hist.Rebin(3)
            elif "pt_bquark" in histkey:
              if "170" not in filesetname:
                hist.Rebin(2)
            
            hist.Scale(1/N1)
            #hist.SetBinError(error/N1)
            hmax        = hist.GetMaximum()
            if hmax > ymax:
              ymax = hmax
            hist.SetLineWidth(3)
            hist.SetLineStyle(1+(i-1)%2)
            hist.SetLineColor(colors[i-1])
            hist.SetMarkerSize(0)
            if i==0:
              hist1 = hist
              hist.Draw("hist")
            else:
              hist.Draw("histsame")
            legend.AddEntry(hist,makeLaTeX(filetitle),'l')
        
        hist1.GetXaxis().SetTitle(makeLaTeX(hist1.GetTitle()))
        hist1.GetYaxis().SetTitle("A.U.")
        hist1.GetXaxis().SetTitleSize(0.06)
        hist1.GetYaxis().SetTitleSize(0.06)
        hist1.GetXaxis().SetTitleOffset(0.90)
        hist1.GetYaxis().SetTitleOffset(1.05)
        hist1.GetXaxis().SetLabelSize(0.045)
        hist1.GetYaxis().SetLabelSize(0.045)
        hist1.SetMaximum(ymax*1.10)
        legend.SetTextFont(42)
        legend.SetTextSize(legendTextSize)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.Draw()      
        CMS_lumi.CMS_lumi(gPad,13,0)
        gStyle.SetOptStat(0)
        canvas.SaveAs("%s/%s-%s%s.png" % (dirname,histkey,filesetname,plotslabel))
        #canvas.SaveAs("%s/%s-%s%s.pdf" % (dirname,histkey,filesetname,plotslabel))
        canvas.Close()
    
    for file in files: file.Close()
    


def makeDirectory(DIR):
    """Make directory if it does not exist."""
    
    if not os.path.exists(DIR):
        os.makedirs(DIR)
        print ">>> made directory " + DIR
    return DIR
    
def green(string,**kwargs):   return "\x1b[0;32;40m%s\033[0m"%string
def error(string,**kwargs):   print ">>> \033[1m\033[91m%sERROR! %s\033[0m"%(kwargs.get('pre',""),string)
def warning(string,**kwargs): print ">>> \033[1m\033[93m%sWarning!\033[0m\033[93m %s\033[0m"%(kwargs.get('pre',""),string)



def main():
    print ""
    
    massesX = [ 20, 28, 40, 50, 60, 70 ]
    massesB = [ 170, 400, 600, 800 ] #170, 400, 600, 800 ]
    
    for massB in massesB:
      setname = "B%d"%(massB)
      set = [ ("LowMassDiTau_M-%d_MB-%d.root"%(mX,massB),
               "m_X = %d GeV, m_B' = %d GeV"%(mX,massB)) for mX in massesX]
      compareVarsForLHESamples(setname,set)
    
    print ">>>\n>>> done\n"
    


if __name__ == '__main__':
    main()



