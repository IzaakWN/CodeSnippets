# ORGANIZATION AND SIMULTANEOUS FITS
# Creating and writing a workspace
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf502_wspacewrite.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf502_wspacewrite.C.html
#         https://github.com/clelange/roofit/blob/master/rf502_wspacewrite.py

import ROOT
from ROOT import gPad, gDirectory, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList, RooWorkspace, RooGaussian, RooChebychev, RooAddPdf
from ROOT.RooFit import Title, LineColor, Range, Name



def rooFit502():
    
    print ">>> setup model components..."
    x      = RooRealVar("x","x",0,10)
    mean   = RooRealVar("mean","mean of gaussians",5,0,10)
    sigma1 = RooRealVar("sigma1","width of gaussians",0.5)
    sigma2 = RooRealVar("sigma2","width of gaussians",1)
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)
    a0  = RooRealVar("a0","a0",0.5,0.,1.)
    a1  = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg = RooChebychev("bkg","Background",x,RooArgList(a0,a1))

    print ">>> sum model components..."
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),RooArgList(sig1frac))
    bkgfrac  = RooRealVar("bkgfrac","fraction of background",0.5,0.,1.)
    model    = RooAddPdf("model","g1+g2+a",RooArgList(bkg,sig),RooArgList(bkgfrac))
    
    print ">>> generate data..."
    data    = model.generate(RooArgSet(x),1000) # RooDataSet
    
    
    
    print ">>> create workspace, import data and model..."
    workspace = RooWorkspace("workspace","workspace") # empty RooWorkspace
    getattr(workspace, 'import')(model) # import model and all its components
    getattr(workspace, 'import')(data)  # import data
    #workspace.import(model) # causes synthax error in python
    #workspace.import(data)  # causes synthax error in python
    
    print "\n>>> print workspace contents:"
    workspace.Print()
    
    print "\n>>> save workspace in file..."
    workspace.writeToFile("rooFit502_workspace.root")
    
    print ">>> save workspace in memory (gDirectory)..."
    gDirectory.Add(workspace)
    # Workspace will remain in memory after macro finishes
    


if __name__ == '__main__':
    rooFit502()
    print ">>>\n>>> Done.\n"
    

