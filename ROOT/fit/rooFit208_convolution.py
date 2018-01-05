# ADDITION AND CONVOLUTION
# One-dimensional numeric convolution
# NOTE: ROOT needs to be compiled with --enable-fftw3
# 
#   pdf = landau(t) (x) gauss(t)
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf208_convolution.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf208_convolution.C.html
#         https://github.com/clelange/roofit/blob/master/rf208_convolution.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kDashed
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooLandau, RooFFTConvPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name



def rooFit208():
    
    print ">>> setup component pdfs..."
    t      = RooRealVar("t","t",-10,30) ;
    ml     = RooRealVar("ml","mean landau",5.,-20,20)
    sl     = RooRealVar("sl","sigma landau",1,0.1,10)
    landau = RooLandau("lx","lx",t,ml,sl)
    mg     = RooRealVar("mg","mg",0)
    sg     = RooRealVar("sg","sg",2,0.1,10)
    gauss  = RooGaussian("gauss","gauss",t,mg,sg)
    
    
    
    print ">>> construct convolution pdf..."
    # Set #bins to be used for FFT sampling to 10000
    t.setBins(10000,"cache")
    
    # Construct landau (x) gauss
    convolution = RooFFTConvPdf("lxg","landau (X) gauss",t,landau,gauss)
    
    print ">>> sample, fit and plot convoluted pdf..."
    data = convolution.generate(RooArgSet(t),10000) # RooDataSet
    convolution.fitTo(data)
    
    
    
    print "\n>>> plot everything..."
    frame1 = t.frame(Title("landau #otimes gauss convolution")) # RooPlot
    data.plotOn(frame1,Binning(50),Name("data"))
    convolution.plotOn(frame1,Name("lxg"))
    gauss.plotOn(frame1, LineStyle(kDashed),LineColor(kRed),  Name("gauss"))
    landau.plotOn(frame1,LineStyle(kDashed),LineColor(kGreen),Name("landau"))
    
    print "\n>>> draw pfds and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    legend = TLegend(0.6,0.8,0.8,0.6)
    legend.SetTextSize(0.032)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.5)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend.AddEntry("data",  "data",       'LEP')
    legend.AddEntry("lxg",   "convolution",'L')
    legend.AddEntry("landau","landau",     'L')
    legend.AddEntry("gauss", "gauss",      'L')
    legend.Draw()
    canvas.SaveAs("rooFit208.png")
    


if __name__ == '__main__':
    rooFit208()
    print ">>>\n>>> Done.\n"
    

