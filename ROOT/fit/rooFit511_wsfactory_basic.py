# ORGANIZATION AND SIMULTANEOUS FITS
# Basic use of the 'object factory' associated with a workspace
# to rapidly build pdfs functions and their parameter components
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf511_wsfactory_basic.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf511_wsfactory_basic.C.html
#         https://github.com/clelange/roofit/blob/master/rf511_wsfactory_basic.py

import ROOT
from ROOT import gPad, gDirectory, TCanvas, TLegend, kBlue, kRed, kGreen, kDashed, kDotted, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooWorkspace, RooAbsPdf, RooAbsData
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name, Rename, Components



def rooFit511(compact=kFALSE):
    
    workspace = RooWorkspace("workspace")

    print ">>> creating and adding basic pdfs..."
    # Remake example pdf of tutorial rf502_wspacewrite.C:
    # 
    # Basic pdf construction: ClassName::ObjectName(constructor arguments)
    # Variable construction:  VarName[x,xlo,xhi], VarName[xlo,xhi], VarName[x]
    # pdf addition:           SUM::ObjectName(coef1*pdf1,...coefM*pdfM,pdfN)
    
    if not compact:
        # Use object factory to build pdf of tutorial rooFit502_wspacewrite
        workspace.factory("Gaussian::sig1(x[-10,10],mean[5,0,10],0.5)")
        workspace.factory("Gaussian::sig2(x,mean,1)")
        workspace.factory("Chebychev::bkg(x,{a0[0.5,0.,1],a1[-0.2,0.,1.]})")
        workspace.factory("SUM::sig(sig1frac[0.8,0.,1.]*sig1,sig2)")
        workspace.factory("SUM::model(bkgfrac[0.5,0.,1.]*bkg,sig)")
    else:
        # Use object factory to build pdf of tutorial rf502_wspacewrite but 
        #  - Contracted to a single line recursive expression, 
        #  - Omitting explicit names for components that are not referred to explicitly later
        workspace.factory("SUM::model(bkgfrac[0.5,0.,1.]*Chebychev::bkg(x[-10,10],{a0[0.5,0.,1],a1[-0.2,0.,1.]}),"+\
                          "SUM(sig1frac[0.8,0.,1.]*Gaussian(x,mean[5,0,10],0.5),Gaussian(x,mean,1)))")
    
    print ">>> advanced pdf constructor arguments..."
    # pdf constructor arguments may by any type of RooAbsArg, but also the follow conversion are made:
    #   Double_t     -->  RooConst(...)
    #   {a,b,c}      -->  RooArgSet() or RooArgList() depending on required ctor arg
    #   dataset name -->  RooAbsData reference for any dataset residing in the workspace
    #   enum         -->  any enum label that belongs to an enum defined in the (base) class
    
    print ">>> generate a dummy dataset from 'model' pdf and import it in the workspace..."
    data = workspace.pdf("model").generate(RooArgSet(workspace.var("x")),1000) # RooDataSet
    getattr(workspace,"import")(data,Rename("data"))
    
    print ">>> construct keys pdf..."
    # Construct a KEYS pdf passing a dataset name and an enum type defining the
    # mirroring strategy
    workspace.factory("KeysPdf::k(x,data,NoMirror,0.2)")
    
    print ">>> workspace contents:"
    workspace.Print()
    
    print ">>> save workspace in memory (gDirectory)..."
    gDirectory.Add(workspace)
    


if __name__ == '__main__':
    rooFit511()
    print ">>>\n>>> Done.\n"
    

