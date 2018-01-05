# BASIC ROOFIT FUNCTIONALITY
# Interpreted functions and pdfs
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf103_interprfuncs.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/htmldoc/tutorials/roofit/rf103_interprfuncs.C.html
#         https://github.com/clelange/roofit/blob/master/rf103_interprfuncs.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooDataHist, RooRealVar, RooGenericPdf, RooFormulaVar, RooArgList, RooArgSet, RooGaussian
from ROOT.RooFit import LineColor, Title, Binning, Import, RooConst, Save



def rooFit103():
    
    print ">>> construct generic pdf from interpreted expression..."
    # To construct a proper p.d.f, the formula expression is explicitly normalized internally
    # by dividing  it by a numeric integral of the expresssion over x in the range [-20,20]
    x      = RooRealVar("x","x",-20,20)
    alpha  = RooRealVar("alpha","alpha",5,0.1,10) ;
    genpdf = RooGenericPdf("genpdf","genpdf","(1+0.1*abs(x)+sin(sqrt(abs(x*alpha+0.1))))",RooArgList(x,alpha))
    
    print ">>> generate and fit toy data...\n"
    data = genpdf.generate(RooArgSet(x),10000) # RooDataSet
    genpdf.fitTo(data)
    frame1 = x.frame(Title("Interpreted expression pdf")) # RooPlot
    data.plotOn(frame1,Binning(40))
    genpdf.plotOn(frame1)
    
    
    
    print "\n>>> construct standard pdf with formula replacing parameter..."
    mean2 = RooRealVar("mean2","mean^2",10,0,200)
    sigma = RooRealVar("sigma","sigma",3,0.1,10)
    mean  = RooFormulaVar("mean","mean","sqrt(mean2)",RooArgList(mean2))
    gaus2 = RooGaussian("gaus2","gaus2",x,mean,sigma)
    
    print ">>> generate and fit toy data...\n"
    gaus1 = RooGaussian("gaus1","gaus1",x,RooConst(10),RooConst(3)) ;
    data2 = gaus1.generate(RooArgSet(x),1000) # RooDataSet
    result = gaus2.fitTo(data2,Save()) # RooFitResult
    result.Print()
    frame2 = x.frame(Title("Tailored Gaussian pdf")) # RooPlot
    data2.plotOn(frame2,Binning(40))
    gaus2.plotOn(frame2)
    
    
    
    print "\n>>> draw pfds and fits on canvas..."
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
    canvas.SaveAs("rooFit103.png")
    


if __name__ == '__main__':
    rooFit103()
    print ">>>\n>>> Done.\n"
    

