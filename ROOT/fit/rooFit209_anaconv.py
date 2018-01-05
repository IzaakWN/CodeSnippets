# ADDITION AND CONVOLUTION
# Decay function p.d.fs with optional B physics 
# effects (mixing and CP violation) that can be
# analytically convolved with e.g. Gaussian resolution 
# functions
# 
#   pdf1 = decay(t,tau) (x) delta(t)
#   pdf2 = decay(t,tau) (x) gauss(t,m,s)
#   pdf3 = decay(t,tau) (x) (f*gauss1(t,m1,s1) + (1-f)*gauss2(t,m1,s1))
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf209_anaconv.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf209_anaconv.C.html
#         https://github.com/clelange/roofit/blob/master/rf209_anaconv.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList
from ROOT.RooFit import Title, LineColor, Range, Name



def rooFit209():
    
#     print ">>> setup model..."
#     x     = RooRealVar("x","x",-10,10)
#     mean  = RooRealVar("mean","mean of gaussian",1,-10,10)
#     sigma = RooRealVar("sigma","width of gaussian",1,0.1,10)
#     gauss = RooGaussian("gauss","gaussian PDF",x,mean,sigma)
#     
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
    rooFit209()
    print ">>>\n>>> Done.\n"
    

