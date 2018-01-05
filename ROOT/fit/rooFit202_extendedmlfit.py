# ADDITION AND CONVOLUTION
# Setting up an extended maximum likelihood fit
#
#   pdf = f_bkg * bkg(x,a0,a1) + (1-fbkg) * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf202_extendedmlfit.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf202_extendedmlfit.C.html
#         https://github.com/clelange/roofit/blob/master/rf202_extendedmlfit.py
#
# See also RooFit chapter 3 "Signal and Background - Composite models"
#         https://root.cern.ch/download/doc/RooFit_Users_Manual_2.91-33.pdf

import ROOT
from ROOT import gPad, TCanvas, TLegend,\
                 kBlue, kRed, kGreen, kOrange, kMagenta, kPink, kAzure, kDashed, kDotted, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooChebychev, RooAbsReal, RooExtendPdf, RooAddPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name, Components, Normalization, Extended



def rooFit202():
    
    print ">>> setup model component: gaussian signals and Chebychev polynomial background..."
    x      = RooRealVar("x","x",0,10)
    mean   = RooRealVar("mean","mean of gaussian",5)
    sigma1 = RooRealVar("sigma1","width of gaussian",0.5)
    sigma2 = RooRealVar("sigma2","width of gaussian",1.0)    
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)

    a0  = RooRealVar("a0","a0",0.5,0.,1.)
    a1  = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg = RooChebychev("bkg","Background",x,RooArgList(a0,a1))
    
    # Sum the signal components into a composite signal p.d.f.
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),RooArgList(sig1frac))
    
    
    
    print ">>>\n>>> METHOD 1"
    print ">>> construct extended composite model..."
    # Sum the composite signal and background into an extended pdf nsig*sig+nbkg*bkg
    nsig  = RooRealVar("nsig","number of signal events",500,0.,10000)
    nbkg  = RooRealVar("nbkg","number of background events",500,0,10000)
    model = RooAddPdf("model","(g1+g2)+a",RooArgList(bkg,sig),RooArgList(nbkg,nsig))
    
    print ">>> sample, fit and plot extended model...\n"
    # Generate a data sample of expected number events in x from model
    #   nsig + nbkg = model.expectedEvents()
    # NOTE: since the model predicts a specific number events, one can
    #       omit the requested number of events to be generated
    # Introduce Poisson fluctuation with Extended(kTRUE)
    data = model.generate(RooArgSet(x),Extended(kTRUE)) # RooDataSet
    
    # Fit model to data, extended ML term automatically included
    # NOTE: Composite extended pdfs can only be successfully fit if the extended likelihood
    #       term -log(Poisson(Nobs,Nexp)) is included in the minimization because they have
    #       one extra degree of freedom in their parameterization that is constrained by
    #       this extended term. If a pdf is capable of calculating an extended term (i.e.
    #       any extended RooAddPdf), the extended term is AUTOMATICALLY included in the
    #       likelihood calculation. Override this behaviour with Extended():
    #           Extended(kTRUE)  ADD extended likelihood term
    #           Extended(kFALSE) DO NOT ADD extended likelihood 
    #model.fitTo(data,Extended(kTRUE))
    model.fitTo(data)
    
    
    
    print "\n>>> plot data, model and model components..."
    # Plot data and PDF overlaid, use expected number of events for pdf projection
    # normalization, rather than observed number of events, data.numEntries()
    frame1 = x.frame(Title("extended ML fit example")) # RooPlot
    data.plotOn(frame1,Binning(30),Name("data"))
    model.plotOn(frame1,Normalization(1.0,RooAbsReal.RelativeExpected),Name("model"))
    
    # Overlay the background components of model
    # NOTE: By default, the pdf is normalized to event count of the last dataset added
    #       to the plot frame. Use "RelativeExpected" to normalize to the expected
    #       event count of the pdf instead
    argset1 = RooArgSet(bkg)
    argset2 = RooArgSet(sig1)
    argset3 = RooArgSet(sig2)
    argset4 = RooArgSet(bkg,sig2)
    model.plotOn(frame1,Components(argset1),LineStyle(kDashed),LineColor(kBlue),   Normalization(1.0,RooAbsReal.RelativeExpected),Name("bkg"))
    #model.plotOn(frame1,Components(argset1),LineStyle(kDashed),LineColor(kBlue),  Name("bkg2"))
    model.plotOn(frame1,Components(argset2),LineStyle(kDotted),LineColor(kMagenta),Normalization(1.0,RooAbsReal.RelativeExpected),Name("sig1"))
    model.plotOn(frame1,Components(argset3),LineStyle(kDotted),LineColor(kPink),   Normalization(1.0,RooAbsReal.RelativeExpected),Name("sig2"))
    model.plotOn(frame1,Components(argset4),LineStyle(kDashed),LineColor(kAzure-4),Normalization(1.0,RooAbsReal.RelativeExpected),Name("bkgsig2"))
    
    
    
    print "\n>>> structure of composite pdf:"
    model.Print("t") # "tree" mode
    
    print "\n>>> parameters:"
    params = model.getVariables() # RooArgSet
    params.Print("v")
    params.Print()
    
    print "\n>>> params.find(\"...\").getVal():"
    print ">>>   sigma1   = %.2f" % params.find("sigma1").getVal()
    print ">>>   sigma2   = %.2f" % params.find("sigma2").getVal()
    print ">>>   nsig     = %6.2f,  sig1frac = %5.2f" % (params.find("nsig").getVal(),params.find("sig1frac").getVal())
    print ">>>   nbkg     = %6.2f" % params.find("nbkg").getVal()
    
    print ">>>\n>>> components:"
    comps   = model.getComponents() # RooArgSet
    sig     = comps.find("sig")     # RooAbsArg
    sigVars = sig.getVariables()    # RooArgSet
    sigVars.Print()
    
    
    
    print ">>>\n>>> METHOD 2"
    print ">>> construct extended components first..."
    # Associated nsig/nbkg as expected number of events with sig/bkg
    nsig = RooRealVar("nsig","number of signal events",500,0.,10000)
    nbkg = RooRealVar("nbkg","number of background events",500,0,10000)
    esig = RooExtendPdf("esig","extended signal pdf",    sig,nsig)
    ebkg = RooExtendPdf("ebkg","extended background pdf",bkg,nbkg)
    
    print ">>> sum extended components without coefficients..."
    # Construct sum of two extended p.d.f. (no coefficients required)
    model2 = RooAddPdf("model2","(g1+g2)+a",RooArgList(ebkg,esig))
    
    # METHOD 2 is functionally completely equivalent to METHOD 1.
    # Its advantage is that the yield parameter is associated to the shape pdf
    # directly, while in METHOD 1 the association is made after constructing
    # a RooAddPdf. Also, class RooExtendPdf offers extra functionality to
    # interpret event counts in a different range.
    
    print ">>> plot model..."
    model2.plotOn(frame1,LineStyle(kDashed),LineColor(kRed),Normalization(1.0,RooAbsReal.RelativeExpected),Name("model2"))
    
    
    
    print ">>> draw on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    legend = TLegend(0.2,0.85,0.4,0.65)
    legend.SetTextSize(0.032)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.4)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend.AddEntry("data",   "data",                      'LEP')
    legend.AddEntry("model",  "composite model",           'L')
    legend.AddEntry("model2", "composite model (method 2)",'L')
    legend.AddEntry("bkg",    "background only",           'L')
    #legend.AddEntry("bkg2",   "background only (no extended norm)", 'L')
    legend.AddEntry("sig1",   "signal 1",                  'L')
    legend.AddEntry("sig2",   "signal 2",                  'L')
    legend.AddEntry("bkgsig2","background + signal 2",     'L')
    legend.Draw()
    canvas.SaveAs("rooFit202.png")
    
    


if __name__ == '__main__':
    rooFit202()
    print ">>>\n>>> Done.\n"
    

