# BASIC ROOFIT FUNCTIONALITY
# Numerical 1st, 2nd and 3rd order derivatives wrt observables and parameters
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf111_derivatives.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf111_derivatives.C.html
#         https://github.com/clelange/roofit/blob/master/rf111_derivatives.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kOrange, kMagenta
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian
from ROOT.RooFit import Title, LineColor, Range, Name, Normalization



def rooFit111():
    
    print ">>> setup model..."
    x     = RooRealVar("x","x",-10,10)
    mean  = RooRealVar("mean","mean of gaussian",1,-10,10)
    sigma = RooRealVar("sigma","width of gaussian",1,0.1,10)
    gauss = RooGaussian("gauss","gaussian PDF",x,mean,sigma)
    
    print ">>> create and plot derivatives wrt x..."
    dgdx   = gauss.derivative(x,1) # RooAbsReal
    d2gdx2 = gauss.derivative(x,2) # RooAbsReal
    d3gdx3 = gauss.derivative(x,3) # RooAbsReal
    
    print ">>> plot gaussian and its first two derivatives..."
    frame1 = x.frame(Title("d^{n}(Gauss)/dx^{n}")) # RooPlot
    norm1  = 10 
    gauss.plotOn( frame1,LineColor(kBlue),   Name(gauss.GetName()), Normalization(norm1))
    dgdx.plotOn(  frame1,LineColor(kMagenta),Name("dgdx"))
    d2gdx2.plotOn(frame1,LineColor(kRed),    Name("d2gdx2"))
    d3gdx3.plotOn(frame1,LineColor(kOrange), Name("d3gdx3"))
    
    
        
    print ">>> create and plot derivatives wrt sigma..."
    dgds   = gauss.derivative(sigma,1) # RooAbsReal
    d2gds2 = gauss.derivative(sigma,2) # RooAbsReal
    d3gds3 = gauss.derivative(sigma,3) # RooAbsReal
    
    print ">>> plot gaussian and its first two derivatives..."
    frame2 = sigma.frame(Title("d^{n}(Gauss)/d(sigma)^{n}"),Range(0.,2.)) # RooPlot
    (norm2,norm21,norm22) = (8000,15,5)
    gauss.plotOn( frame2,LineColor(kBlue),   Name(gauss.GetName()), Normalization(norm2))
    dgds.plotOn(  frame2,LineColor(kMagenta),Name("dgds"),          Normalization(norm21))
    d2gds2.plotOn(frame2,LineColor(kRed),    Name("d2gds2"),        Normalization(norm22))
    d3gds3.plotOn(frame2,LineColor(kOrange), Name("d3gds3"))
    
    print ">>> draw pdfs and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1400,600)
    legend1 = TLegend(0.22,0.85,0.4,0.65)
    legend2 = TLegend(0.60,0.85,0.8,0.65)
    for legend in [legend1,legend2]:
        legend.SetTextSize(0.032)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.6)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend1.AddEntry(gauss.GetName(),"gaussian G (#times%s)"%norm1, 'L')
    legend1.AddEntry("dgdx",         "d(G)/dx",                     'L')
    legend1.AddEntry("d2gdx2",       "d^{2}(G)/dx^{2}",             'L')
    legend1.AddEntry("d3gdx3",       "d^{3}(G)/dx^{3}",             'L')
    legend1.Draw()
    canvas.cd(2)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame2.GetYaxis().SetLabelOffset(0.008)
    frame2.GetYaxis().SetTitleOffset(1.6)
    frame2.GetYaxis().SetTitleSize(0.045)
    frame2.GetXaxis().SetTitleSize(0.045)
    frame2.Draw()
    legend2.AddEntry(gauss.GetName(),"gaussian G (#times%s)"%norm2,      'L')
    legend2.AddEntry("dgds",         "d(G)/ds (#times%s)"%norm21,        'L')
    legend2.AddEntry("d2gds2",       "d^{2}(G)/ds^{2} (#times%s)"%norm22,'L')
    legend2.AddEntry("d3gds3",       "d^{3}(G)/ds^{3}",                  'L')
    legend2.Draw()
    canvas.SaveAs("rooFit111.png")
    
    

if __name__ == '__main__':
    rooFit111()
    print ">>>\n>>> Done.\n"
    

