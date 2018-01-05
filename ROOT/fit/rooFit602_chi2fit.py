# LIKELIHOOD AND MINIMIZATION
# Setting up a chi^2 fit to a binned dataset
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf601_intminuit.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf601_intminuit.C.html
#         https://github.com/clelange/roofit/blob/master/rf601_intminuit.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooChebychev, RooAddPdf, RooChi2Var
from ROOT.RooFit import Title, LineColor, Range, Name



def rooFit602():
    
    print ">>> setup model..."
    x      = RooRealVar("x","x",0,10)
    mean   = RooRealVar("mean","mean of gaussian",5)
    sigma1 = RooRealVar("sigma1","width of gaussian",0.5)
    sigma2 = RooRealVar("sigma2","width of gaussian",1)
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)
    a0     = RooRealVar("a0","a0",0.5,0.,1.)
    a1     = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg    = RooChebychev("bkg","Background",x,RooArgSet(a0,a1))
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),sig1frac)
    bkgfrac = RooRealVar("bkgfrac","fraction of background",0.5,0.,1.)
    model   = RooAddPdf("model","g1+g2+a",RooArgList(bkg,sig),bkgfrac)
    
    print ">>> create binned dataset..."
    data = model.generate(RooArgSet(x),10000) # RooDataSet
    hist = data.binnedClone() # RooDataHist
    
    # Construct a chi^2 of the data and the model.
    # When a p.d.f. is used in a chi^2 fit, the probability density scaled
    # by the number of events in the dataset to obtain the fit function
    # If model is an extended p.d.f, the expected number events is used
    # instead of the observed number of events.
    model.chi2FitTo(hist)

    # NB: It is also possible to fit a RooAbsReal function to a RooDataHist
    # using chi2FitTo(). 

    # Note that entries with zero bins are _not_ allowed 
    # for a proper chi^2 calculation and will give error
    # messages
    data_small = date.reduce(EventRange(1,100)) # RooDataSet
    hist_small = data_small.binnedClone() # RooDataHist
    chi2_lowstat("chi2_lowstat","chi2",model,hist_small)
    print ">>> chi2_lowstat.getVal() = %s" % chi2_lowstat.getVal()
    
#     print "\n>>> draw pfds and fits on canvas..."
#     canvas = TCanvas("canvas","canvas",100,100,1400,600)
#     canvas.Divide(2)
#     canvas.cd(1)
#     gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
#     frame1.GetYaxis().SetLabelOffset(0.008)
#     frame1.GetYaxis().SetTitleOffset(1.6)
#     frame1.GetYaxis().SetTitleSize(0.045)
#     frame1.GetXaxis().SetTitleSize(0.045)
#     frame1.Draw()
#     canvas.cd(2)
#     gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
#     frame2.GetYaxis().SetLabelOffset(0.008)
#     frame2.GetYaxis().SetTitleOffset(1.6)
#     frame2.GetYaxis().SetTitleSize(0.045)
#     frame2.GetXaxis().SetTitleSize(0.045)
#     frame2.Draw()
#     canvas.SaveAs("rooFit201.png")
    


if __name__ == '__main__':
    rooFit602()
    print ">>>\n>>> Done.\n"
    

