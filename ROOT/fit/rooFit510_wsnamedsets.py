# ORGANIZATION AND SIMULTANEOUS FITS
# Working with named parameter sets and parameter snapshots in workspaces
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf510_wsnamedsets.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf510_wsnamedsets.C.html
#         https://github.com/clelange/roofit/blob/master/rf510_wsnamedsets.py

import ROOT
from ROOT import gPad, gDirectory, TFile, TCanvas, TLegend,\
                 kBlue, kRed, kGreen, kDashed, kDotted, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooDataSet, RooAbsData, RooWorkspace,\
                 RooGaussian, RooChebychev, RooAddPdf, RooAbsPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name, Components, PrintLevel




def fillWorkspace(workspace):
    
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
    
    print ">>> import model into workspace..."
    getattr(workspace,'import')(model) # import model and all its components
    #workspace.import(model) # causes synthax error in python
    
    
    
    print "\n>>> encode definition of parameters and observables in workspace..."
    # Define named sets "parameters" and "observables", which list which variables should
    # be considered parameters and observables by the users convention
    # 
    # Variables appearing in sets _must_ live in the workspace already, or the autoImport
    # flag of defineSet must be set to import them on the fly. Named sets contain only
    # references to the original variables, therefore the value of observables in named
    # sets already reflect their 'current' value
    params = model.getParameters(RooArgSet(x)) # RooArgSet
    workspace.defineSet("parameters",RooArgSet(params))
    workspace.defineSet("observables",RooArgSet(x))
    
    
    
    # Encode reference value for parameters in workspace:
    # Define a parameter 'snapshot' in the pdf
    # Unlike a named set, a parameter snapshot stores an independent set of values for
    # a given set of variables in the workspace. The values can be stored and reloaded
    # into the workspace variable objects using the loadSnapshot() and saveSnapshot()
    # methods. A snapshot saves the value of each variable, any errors that are stored
    # with it as well as the 'Constant' flag that is used in fits to determine if a 
    # parameter is kept fixed or not.
    
    print ">>> generate and fit data..."
    # Do a dummy fit to a (supposedly) reference dataset here and store the results
    # of that fit into a snapshot
    refData = model.generate(RooArgSet(x),10000) # RooDataSet
    model.fitTo(refData,PrintLevel(-1))
    
    print "\n>>> save fit results into a snapshot in the workspace..."
    # The kTRUE flag imports the values of the objects in (*params) into the workspace
    # If not set, the present values of the workspace parameters objects are stored
    workspace.saveSnapshot("reference_fit",params,kTRUE)
    
    print ">>> make another fit with the signal component forced to zero..."
    bkgfrac.setVal(1)
    bkgfrac.setConstant(kTRUE)
    bkgfrac.removeError()
    model.fitTo(refData,PrintLevel(-1))
    
    print "\n>>> save new fit parameters in different snapshot..."
    workspace.saveSnapshot("reference_fit_bkgonly",params,kTRUE)
    


def rooFit510():
    
    print ">>> create and fill workspace..."
    workspace = RooWorkspace("workspace") # RooWorkspace
    fillWorkspace(workspace)
    
    print ">>>\n>>> retrieve model from workspace..."
    # Exploit convention encoded in named set "parameters" and "observables"
    # to use workspace contents w/o need for introspected
    model = workspace.pdf("model") # RooAbsPdf
    
    print ">>> generate and fit data in given observables"
    data = model.generate(workspace.set("observables"),1000) # RooDataSet
    model.fitTo(data)
    
    print ">>> plot model and data of first observables..."
    frame1 = workspace.set("observables").first().frame() # RooPlot
    data.plotOn(frame1 ,Name("data"),Binning(50))
    model.plotOn(frame1,Name("model"))
    
    print ">>> overlay plots with reference parameters as stored in snapshots..."
    workspace.loadSnapshot("reference_fit")
    model.plotOn(frame1,LineColor(kRed),Name("model_ref"))
    workspace.loadSnapshot("reference_fit_bkgonly")
    model.plotOn(frame1,LineColor(kRed),LineStyle(kDashed),Name("bkg_ref"))
    
    print "\n>>> draw on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    legend = TLegend(0.2,0.8,0.4,0.6)
    legend.SetTextSize(0.032)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.5)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend.AddEntry("data",     "data",               'LEP')
    legend.AddEntry("model",    "model",              'L')
    legend.AddEntry("model_ref","model fit",          'L')
    legend.AddEntry("bkg_ref",  "background only fit",'L')
    legend.Draw()
    canvas.SaveAs("rooFit510.png")
    
    # Print workspace contents
    workspace.Print()
    
    # Workspace will remain in memory after macro finishes
    gDirectory.Add(workspace)
    


if __name__ == '__main__':
    rooFit510()
    print ">>>\n>>> Done.\n"
    

