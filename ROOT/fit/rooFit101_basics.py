# BASIC ROOFIT FUNCTIONALITY
# Fitting, plotting, toy data generation on one-dimensional pdf
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf101_basics.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/htmldoc/tutorials/roofit/rf101_basics.C.html
#         https://github.com/clelange/roofit/blob/master/rf101_basics.py

import ROOT
from ROOT import gPad, TF1, TH1F, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooGaussian
from ROOT.RooFit import LineColor, Title, Binning



def rooFit101():
    
    print ">>> build gaussian pdf..."
    x     = RooRealVar("x","x",-10,10)
    mean  = RooRealVar("mean","mean of gaussian",1,-10,10)
    sigma = RooRealVar("sigma","width of gaussian",1,0.1,10)
    gauss = RooGaussian("gauss","gaussian PDF",x,mean,sigma)
    
    print ">>> plot pdf..."
    frame1 = x.frame(Title("Gaussian pdf")) # RooPlot
    #xframe.SetTitle("Gaussian pdf")
    gauss.plotOn(frame1)
    
    print ">>> change parameter value and plot..."
    sigma.setVal(3)
    gauss.plotOn(frame1,LineColor(kRed))
    
    print ">>> generate events..."
    data = gauss.generate(RooArgSet(x),10000) # RooDataSet
    frame2 = x.frame()
    data.plotOn(frame2,Binning(40))
    gauss.plotOn(frame2)
    
    print ">>> fit gaussian...\n"
    gauss.fitTo(data)
    mean.Print()
    sigma.Print()
    
    print "\n>>> draw pdfs and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1400,600)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.6)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    canvas.cd(2)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame2.GetYaxis().SetLabelOffset(0.008)
    frame2.GetYaxis().SetTitleOffset(1.6)
    frame2.GetYaxis().SetTitleSize(0.045)
    frame2.GetXaxis().SetTitleSize(0.045)
    frame2.Draw()
    canvas.SaveAs("rooFit101.png")
    


if __name__ == '__main__':
    rooFit101()
    print ">>>\n>>> Done.\n"
    

