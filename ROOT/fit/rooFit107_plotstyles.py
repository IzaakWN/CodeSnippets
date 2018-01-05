# BASIC ROOFIT FUNCTIONALITY
# Demonstration of various plotting styles of data and functions
# in a RooPlot
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf107_plotstyles.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf107_plotstyles.C.html
#         https://github.com/clelange/roofit/blob/master/rf107_plotstyles.py

import ROOT
from ROOT import gPad, TCanvas, TLegend,\
                 kGray, kBlue, kRed, kGreen, kOrange, kMagenta, kDashed
from ROOT import RooRealVar, RooArgSet, RooArgList, RooAbsData, RooGaussian
from ROOT.RooFit import Name, Title, Bins, Range, LineColor, MarkerColor, FillColor,\
                        DrawOption, LineStyle, DataError, XErrorSize, MoveToBack



def rooFit107():
    
    print ">>> setup model..."
    x      = RooRealVar("x","x",-3,3)
    mean   = RooRealVar("mean","mean of gaussian",1,-10,10)
    sigma  = RooRealVar("sigma","width of gaussian",1,0.1,10)
    gauss  = RooGaussian("gauss","gauss",x,mean,sigma)
    data   = gauss.generate(RooArgSet(x),1000) # RooDataSet
    gauss.fitTo(data)
    
    print ">>> plot pdf and data..."
    frame1 = x.frame(Name("frame1"),Title("Red Curve / SumW2 Histo errors"),Bins(20)) # RooPlot
    frame2 = x.frame(Name("frame2"),Title("Dashed Curve / No XError bars"),Bins(20)) # RooPlot
    frame3 = x.frame(Name("frame3"),Title("Filled Curve / Blue Histo"),Bins(20)) # RooPlot
    frame4 = x.frame(Name("frame4"),Title("Partial Range / Filled Bar chart"),Bins(20)) # RooPlot
    
    print ">>> data plotting styles..."
    data.plotOn(frame1,DataError(RooAbsData.SumW2))
    data.plotOn(frame2,XErrorSize(0))                           # Remove horizontal error bars
    data.plotOn(frame3,MarkerColor(kBlue),LineColor(kBlue))     # Blue markers and error bors
    data.plotOn(frame4,DrawOption("B"),DataError(RooAbsData.None),
                       XErrorSize(0),FillColor(kGray))          # Filled bar chart
    
    print ">>> data plotting styles..."
    gauss.plotOn(frame1,LineColor(kRed))    
    gauss.plotOn(frame2,LineStyle(kDashed))                              # Change line style to dashed
    gauss.plotOn(frame3,DrawOption("F"),FillColor(kOrange),MoveToBack()) # Filled shapes in green color
    gauss.plotOn(frame4,Range(-8,3),LineColor(kMagenta))
    
    print ">>> draw pfds and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1000,1200)
    canvas.Divide(2,2)
    for i, frame in enumerate([frame1,frame2,frame3,frame4],1):
        canvas.cd(i)
        gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.05)
        frame.GetYaxis().SetTitleOffset(1.6)
        frame.GetYaxis().SetLabelOffset(0.010)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.042)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetXaxis().SetLabelSize(0.042)
        frame.Draw()
    canvas.SaveAs("rooFit107.png")
    


if __name__ == '__main__':
    rooFit107()
    print ">>>\n>>> Done.\n"
    

