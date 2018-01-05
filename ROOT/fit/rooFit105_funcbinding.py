# BASIC ROOFIT FUNCTIONALITY
# Demonstration of binding ROOT Math functions as RooFit functions and pdfs
#
#           !!! DOES NOT WORK IN PYROOT !!!
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf105_funcbinding.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/htmldoc/tutorials/roofit/rf105_funcbinding.C.html
#         https://github.com/clelange/roofit/blob/master/rf105_funcbinding.py

import ROOT
from ROOT import gPad, TMath, Math, TF1, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooAbsReal, RooArgSet, RooArgList, RooCFunction1Binding
from ROOT.RooFit import LineColor, Title, bindPdf, bindFunction



def rooFit105():
    
    print ">>> bind TMath::Erf C function..."
    x   = RooRealVar("x","x",-3,3)
    #print ">>> type(%s) = %s" % ("TMath.Erf",type(TMath.Erf))
    
    fa1 = TF1("fa2","TMath::Erf(x)",0,10);
    erf = bindFunction(fa1,x) # RooAbsReal
    #erf = bindFunction("erf",TMath.Erf,RooArgList(x)) # RooAbsReal
    erf.Print()
    frame1 = x.frame(Title("TMath::Erf bound as RooFit function")) # RooPlot
    erf.plotOn(frame1)
    
    
    
    print ">>> bind ROOT::Math::beta_pdf C pdf..."
    x2   = RooRealVar("x2","x2",0,0.999)
    a    = RooRealVar("a","a",5,0,10)
    b    = RooRealVar("b","b",2,0,10)
    print ">>> type(%s) = %s" % ("Math.beta_pdf",type(Math.beta_pdf))
    #beta = bindPdf("beta",Math.beta_pdf,RooArgList(x2,a,b)) # RooAbsPdf
    beta = bindPdf("beta",Math.beta_pdf,x2,a,b) # RooAbsPdf
    beta.Print()
    
    print ">>> generate and fit data...\n"
    data = beta.generate(x2,10000) # RooDataSet
    beta.fitTo(data)
    frame2 = x2.frame(Title("ROOT::Math::Beta bound as RooFit pdf")) # RooPlot
    data.plotOn(frame2)
    beta.plotOn(frame2)
    
    
    
    print ">>> bind ROOT::TF1 as RooFit function..."
    fa3  = TF1("fa3","sin(x)/x",0,10)
    x3   = RooRealVar("x3","x3",0.01,20)
    rfa1 = bindFunction(fa3,RooArgList(x3)) # RooAbsReal
    rfa1.Print()
    frame3 = x3.frame(Title("TF1 bound as RooFit function")) # RooPlot
    rfa1.plotOn(frame3)
    
    
    
    print ">>> draw functions and toy data on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1800,600)
    canvas.Divide(3)
    for i, frame in enumerate([frame1,frame2,frame3],1):
        canvas.cd(i)
        gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.05)
        frame.GetYaxis().SetTitleOffset(1.6)
        frame.GetYaxis().SetLabelOffset(0.010)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.042)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetXaxis().SetLabelSize(0.042)
        frame.Draw()
    canvas.SaveAs("rooFit105.png")
    


if __name__ == '__main__':
    rooFit105()
    print ">>>\n>>> Done.\n"
    

