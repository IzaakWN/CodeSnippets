# BASIC ROOFIT FUNCTIONALITY
# Adding boxes with parameters, statistics to RooPlots.
# Decorating RooPlots with arrows, text etc. ...
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf106_plotdecoration.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf106_plotdecoration.C.html

import ROOT
from ROOT import gPad, gStyle, TCanvas, TLegend, TText, TArrow, TFile, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooGaussian, RooArgSet, RooArgList
from ROOT.RooFit import LineColor, Name, Title, Bins, Layout



def rooFit106():
    
    print ">>> setup model..."
    x      = RooRealVar("x","x",-3,3)
    mean   = RooRealVar("mean","mean of gaussian",1,-10,10)
    sigma  = RooRealVar("sigma","width of gaussian",1,0.1,10)
    gauss  = RooGaussian("gauss","gauss",x,mean,sigma)
    data   = gauss.generate(RooArgSet(x),10000) # RooDataSet
    gauss.fitTo(data)
    
    print ">>> plot pdf and data..."
    frame = x.frame(Name("frame"),Title("RooPlot with decorations"),Bins(40)) # RooPlot
    data.plotOn(frame)
    gauss.plotOn(frame)
    
    print ">>> RooGaussian::paramOn - add box with pdf parameters..."
    # https://root.cern.ch/doc/master/classRooAbsPdf.html#aa43b2556a1b419bad2b020ba9b808c1b
    # Layout(Double_t xmin, Double_t xmax, Double_t ymax)
    # left edge of box starts at 20% of x-axis
    gauss.paramOn(frame,Layout(0.55))
    
    print ">>> RooDataSet::statOn - add box with data statistics..."
    # https://root.cern.ch/doc/master/classRooAbsData.html#a538d58020b296a1623323a84d2bb8acb
    # x size of box is from 55% to 99% of x-axis range, top of box is at 80% of y-axis range)
    data.statOn(frame,Layout(0.20,0.55,0.8))
    
    print ">>> add text and arrow..."
    text = TText(2,100,"Signal")
    text.SetTextSize(0.04)
    text.SetTextColor(kRed)
    frame.addObject(text)
    
    arrow = TArrow(2,100,-1,50,0.01,"|>")
    arrow.SetLineColor(kRed)
    arrow.SetFillColor(kRed)
    arrow.SetLineWidth(3)
    frame.addObject(arrow)
    
    print ">>> persist frame with all decorations in ROOT file..."
    file = TFile("rooFit106.root","RECREATE")
    frame.Write()
    file.Close()
    
    # To read back and plot frame with all decorations in clean root session do
    #   [0] TFile f("rooFit106.root")
    #   [1] xframe->Draw()
    
    print ">>> draw functions and toy data on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.05)
    frame.GetYaxis().SetTitleOffset(1.6)
    frame.GetYaxis().SetLabelOffset(0.010)
    frame.GetYaxis().SetTitleSize(0.045)
    frame.GetYaxis().SetLabelSize(0.042)
    frame.GetXaxis().SetTitleSize(0.045)
    frame.GetXaxis().SetLabelSize(0.042)
    frame.Draw()    
    canvas.SaveAs("rooFit106.png")
    


if __name__ == '__main__':
    rooFit106()
    print ">>>\n>>> Done.\n"
    

