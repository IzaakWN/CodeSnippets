# ADDITION AND CONVOLUTION
# Working a with a p.d.f. with a convolution operator in terms
# of a parameter
# NOTE: ROOT needs to be compiled with --enable-fftw3
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf211_paramconv.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf211_paramconv.C.html
#         https://github.com/clelange/roofit/blob/master/rf211_paramconv.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooGenericPdf, RooFFTConvPdf
from ROOT.RooFit import Title, LineColor, Range, Binning, Bins, Name, YVar, ConditionalObservables, Verbose



def rooFit211():
    
    print ">>> setup model components..."
    x      = RooRealVar("x","x",-10,10)
    mean   = RooRealVar("mean","mean",-3,3)
    sigma  = RooRealVar("sigma","sigma",0.5,0.1,10)
    modelx = RooGaussian("gx","gx",x,mean,sigma)
    a          = RooRealVar("a","a",2,1,10) ;
    model_mean = RooGenericPdf("model_mean","abs(mean)<a",RooArgList(mean,a))
    
    print ">>> construct convolution pdf..."
    x.setBins(1000,"cache")
    mean.setBins(50,"cache")
    model = RooFFTConvPdf("model","model",mean,modelx,model_mean)
    
    print ">>> configure convolution to construct a 2-D cache..."
    # Configure convolution to construct a 2-D cache in (x,mean)
    # rather than a 1-d cache in mean that needs to be recalculated
    # for each value of x
    model.setCacheObservables(RooArgSet(x))
    model.setBufferFraction(1.0)
    
    print ">>> integrate model over mean projModel = Int model dmean..."
    projModel = model.createProjection(RooArgSet(mean)) # RooAbsPdf
    
    print ">>> generate and fit toy data..."
    data = projModel.generateBinned(RooArgSet(x),1000) # RooDataHist
    projModel.fitTo(data,Verbose())
    
    print "\n>>> plot data and fitted pdf..."
    frame1 = x.frame(Bins(10)) # RooPlot
    data.plotOn(frame1) #,Binning(30)
    projModel.plotOn(frame1)
    
    print ">>> create a 2D histogram of the model(x;mean)..."
    hist = model.createHistogram("hist",x,Binning(50),YVar(mean,Binning(50)),ConditionalObservables(RooArgSet(mean))) # TH1
    hist.SetTitle("histogram of model(x|mean)")
    hist.SetLineColor(kBlue)
    
    print ">>> draw on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1200,600)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.6)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    canvas.cd(2)
    gPad.SetLeftMargin(0.20); gPad.SetRightMargin(0.02)
    hist.GetYaxis().SetLabelOffset(0.008)
    hist.GetYaxis().SetTitleOffset(1.6)
    hist.GetZaxis().SetTitleOffset(2.4)
    hist.GetYaxis().SetTitleSize(0.045)
    hist.GetXaxis().SetTitleSize(0.045)
    hist.Draw("surf")
    canvas.SaveAs("rooFit211.png")
    


if __name__ == '__main__':
    rooFit211()
    print ">>>\n>>> Done.\n"
    

