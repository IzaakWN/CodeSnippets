# ADDITION AND CONVOLUTION
# Fitting and plotting in sub ranges 
#
#   pdf = f_bkg * bkg(x,a0,a1) + (1-fbkg) * (f_sig1 * sig1(x,m,s1 + (1-f_sig1) * sig2(x,m,s2)))
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf203_ranges.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf203_ranges.C.html
#         https://github.com/clelange/roofit/blob/master/rf203_ranges.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kTRUE, kFALSE, kDashed
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooPolynomial, RooAddPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Save, Name, RooConst



def rooFit203():
    
    print ">>> setup model..."
    x     = RooRealVar("x","x",-10,10)
    mean  = RooRealVar("mean","mean of gaussian",0,-10,10)
    gauss = RooGaussian("gauss","gaussian PDF",x,mean,RooConst(1))
    
    # Construct px = 1 (flat in x)
    px    = RooPolynomial("px","px",x)
    
    # Construct model = f*gx + (1-f)px
    f     = RooRealVar("f","f",0.,1.)
    model = RooAddPdf("model","model",RooArgList(gauss,px),RooArgList(f))
    data  = model.generate(RooArgSet(x),10000) # RooDataSet
    
    print ">>> fit to full data range..."
    result_full = model.fitTo(data,Save(kTRUE)) # RooFitResult
    
    print "\n>>> fit \"signal\" range..."
    # Define "signal" range in x as [-3,3]
    x.setRange("signal",-3,3)
    result_sig = model.fitTo(data,Save(kTRUE),Range("signal")) # RooFitResult
    
    print "\n>>> plot and print results..."
    # Make plot frame in x and add data and fitted model
    frame1 = x.frame(Title("Fitting a sub range")) # RooPlot
    data.plotOn(frame1,Name("data"))
    model.plotOn(frame1,Range("Full"),LineColor(kBlue),Name("model")) # Add shape in full ranged dashed
    model.plotOn(frame1,LineStyle(kDashed),LineColor(kRed),Name("model2")) # By default only fitted range is shown
    
    print "\n>>> result of fit on all data:"
    result_full.Print()
    
    print "\n>>> result of fit in in signal region (note increased error on signal fraction):"
    result_sig.Print()
    
    
    
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
    legend.AddEntry("data",   "data",              'LEP')
    legend.AddEntry("model",  "fit (full range)",  'L')
    legend.AddEntry("model2", "fit (signal range)",'L')
    legend.Draw()
    canvas.SaveAs("rooFit203.png")
    


if __name__ == '__main__':
    rooFit203()
    print ">>>\n>>> Done.\n"
    

