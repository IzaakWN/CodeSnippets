# ADDITION AND CONVOLUTION
# Extended maximum likelihood fit with alternate range definition
# for observed number of events.
#
#   pdf = f_bkg * bkg(x,a0,a1) + (1-fbkg) * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf204_extrangefit.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf204_extrangefit.C.html
#         https://github.com/clelange/roofit/blob/master/rf204_extrangefit.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kDashed, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooAbsReal, RooGaussian, RooChebychev, RooExtendPdf, RooAddPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name, Save, Extended, Components, Normalization



def rooFit204():
    
    print ">>> setup model signal components: gaussians..."
    x      = RooRealVar("x","x",0,10)
    mean   = RooRealVar("mean","mean of gaussian",5)
    sigma1 = RooRealVar("sigma1","width of gaussians",0.5)
    sigma2 = RooRealVar("sigma2","width of gaussians",1)
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),RooArgList(sig1frac))
    
    print ">>> setup model background components: Chebychev polynomial..."
    a0  = RooRealVar("a0","a0",0.5,0.,1.)
    a1  = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg = RooChebychev("bkg","Background",x,RooArgList(a0,a1))
    
    print ">>> construct extended components with specified range..."
    # Define signal range in which events counts are to be defined
    x.setRange("signalRange",5,6)
    
    # Associated nsig/nbkg as expected number of events with sig/bkg _in_the_range_ "signalRange"
    nsig = RooRealVar("nsig","number of signal events in signalRange",    500,0.,10000) 
    nbkg = RooRealVar("nbkg","number of background events in signalRange",500,0,10000) 
    esig = RooExtendPdf("esig","extended signal pdf",    sig,nsig,"signalRange") 
    ebkg = RooExtendPdf("ebkg","extended background pdf",bkg,nbkg,"signalRange") 
    
    print ">>> sum extended components..."
    # Construct sum of two extended p.d.f. (no coefficients required)
    model = RooAddPdf("model","(g1+g2)+a",RooArgList(ebkg,esig))
    
    print ">>> sample data, fit model..."
    data = model.generate(RooArgSet(x),1000) # RooDataSet 
    result = model.fitTo(data,Extended(kTRUE),Save()) # RooFitResult
    
    print "\n>>> fit result:"
    result.Print()
    
    
    
    print "\n>>> plot everything..."
    frame1 = x.frame(Title("Fitting a sub range")) # RooPlot
    data.plotOn(frame1,Binning(50),Name("data"))
    model.plotOn(frame1,LineColor(kBlue),Name("model"))
    argset1 = RooArgSet(bkg)
    model.plotOn(frame1,Components(argset1),LineStyle(kDashed),LineColor(kBlue),Name("bkg"),Normalization(1.0,RooAbsReal.RelativeExpected))
    #model.plotOn(frame1,Components(argset1),LineStyle(kDashed),LineColor(kRed),Name("bkg2"))
    
    print ">>> draw on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    legend = TLegend(0.2,0.85,0.4,0.7)
    legend.SetTextSize(0.032)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.4)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend.AddEntry("data",   "data",           'LEP')
    legend.AddEntry("model",  "fit",            'L')
    legend.AddEntry("bkg",    "background only",'L')
    #legend.AddEntry("bkg2",   "background only (no extended norm)",'L')
    legend.Draw()
    canvas.SaveAs("rooFit204.png")
    


if __name__ == '__main__':
    rooFit204()
    print ">>>\n>>> Done.\n"
    

