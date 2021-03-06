# ORGANIZATION AND SIMULTANEOUS FITS
# Reading and using a workspace
# Note: The input file for this macro is generated by rf502_wspaceread.C
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf503_wspaceread.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf503_wspaceread.C.html
#         https://github.com/clelange/roofit/blob/master/rf503_wspaceread.py

import ROOT
from ROOT import gPad, TFile, TCanvas, TLegend, kBlue, kRed, kGreen, kDashed, kDotted
from ROOT import RooRealVar, RooArgSet, RooArgList, RooWorkspace, RooAbsPdf, RooAbsData
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name, Components



def rooFit503():
    
    print ">>> open and workspace file, list its contents and get workspace object..."
    file = TFile("rooFit502_workspace.root")
    file.ls()
    workspace = file.Get("workspace") # RooWorkspace
    
    print "\n>>> retrieve pdf, data from workspace..."
    x = workspace.var("x") # RooRealVar
    model = workspace.pdf("model") # RooAbsPdf
    data = workspace.data("modelData")
    
    print ">>> print model tree:..."
    model.Print("t")
    
    print "\n>>> fit model to data..."
    model.fitTo(data)
    frame1 = x.frame(Title("Model and data read from workspace")) # RooPlot
    
    print ">>> plot everything..."
    data.plotOn(frame1, Name("data"),Binning(40))
    model.plotOn(frame1,Name("model"))
    model.plotOn(frame1,Components("bkg"),     LineStyle(kDashed),Name("bkg"))
    model.plotOn(frame1,Components("bkg,sig2"),LineStyle(kDotted),Name("bkgsig2"))
    
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
    legend.AddEntry("data",   "data",                 'LEP')
    legend.AddEntry("model",  "model",                'L')
    legend.AddEntry("bkg",    "background only",      'L')
    legend.AddEntry("bkgsig2","background + signal 2",'L')
    legend.Draw()
    canvas.SaveAs("rooFit503.png")
    


if __name__ == '__main__':
    rooFit503()
    print ">>>\n>>> Done.\n"
    

