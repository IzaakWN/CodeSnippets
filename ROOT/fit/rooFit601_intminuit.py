# LIKELIHOOD AND MINIMIZATION
# Interactive minimization with MINUIT
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf602_chi2fit.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf602_chi2fit.C.html
#         https://github.com/clelange/roofit/blob/master/rf602_chi2fit.py

import ROOT
from ROOT import gPad, gDirectory, TCanvas, TLegend, kBlue, kRed, kGreen, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooAbsReal, RooGaussian, RooAddPdf, RooMinuit
from ROOT.RooFit import Title, LineColor, Range, Name



def rooFit601():
    
    print ">>> setup pdf and likelihood..."
    x      = RooRealVar("x","x",-20,20)
    mean   = RooRealVar("mean","mean of g1 and g2",0)
    sigma1 = RooRealVar("sigma1","width of g1",3)
    sigma2 = RooRealVar("sigma2","width of g2",4,3.0,6.0) # intentional strong correlations
    gauss1 = RooGaussian("gauss1","gauss1",x,mean,sigma1)
    gauss2 = RooGaussian ("gauss2","gauss2",x,mean,sigma2)
    frac   = RooRealVar("frac","frac",0.5,0.0,1.0)
    model  = RooAddPdf("model","model",RooArgList(gauss1,gauss2),RooArgList(frac))
    
    print ">>> generate to data..."
    data = model.generate(RooArgSet(x),1000) # RooDataSet
    
    print ">>> construct unbinned likelihood of model wrt data..."
    nll  = model.createNLL(data) # RooAbsReal
    
    print ">>> interactive minimization and error analysis with MINUIT interface object..."
    minuit = RooMinuit(nll)
    
    print ">>> set avtive verbosity for logging of MINUIT parameter space stepping..."
    minuit.setVerbose(kTRUE)
    
    print ">>> call MIGRAD to minimize the likelihood..."
    minuit.migrad()
    
    print "\n>>> parameter values and error estimates that are back propagated from MINUIT:"
    model.getParameters(RooArgSet(x)).Print("s")
    
    print "\n>>> disable verbose logging..."
    minuit.setVerbose(kFALSE)
    
    print ">>> run HESSE to calculate errors from d2L/dp2..."
    minuit.hesse()
    
    print ">>> value of and error on sigma2 (back propagated from MINUIT):"
    sigma2.Print()
    
    print "\n>>> run MINOS on sigma2 parameter only..."
    minuit.minos(RooArgSet(sigma2))
    
    print "\n>>> value of and error on sigma2 (back propagated from MINUIT after running MINOS):"
    sigma2.Print()
    
    print "\n>>> saving results, contour plots..."
    # Save a snapshot of the fit result. This object contains the initial
    # fit parameters, the final fit parameters, the complete correlation
    # matrix, the EDM, the minimized FCN , the last MINUIT status code and
    # the number of times the RooFit function object has indicated evaluation
    # problems (e.g. zero probabilities during likelihood evaluation)
    result = minuit.save() # RooFitResult
    
    # Make contour plot of mx vs sx at 1,2,3 sigma
    frame1 = minuit.contour(frac,sigma2,1,2,3) # RooPlot
    frame1.SetTitle("RooMinuit contour plot")
    
    # Print the fit result snapshot
    result.Print("v")
    
    print "\n>>> change value of \"mean\" parameter..."
    mean.setVal(0.3)
    
    # Rerun MIGRAD,HESSE
    print ">>> rerun MIGRAD, HESSE..."
    minuit.migrad()
    minuit.hesse()
    
    print ">>> value on and error of frac:"
    frac.Print()
    
    print "\n>>> fix value of \"sigma\" parameter (setConstant)..."
    sigma2.setConstant(kTRUE)
    
    print ">>> rerun MIGRAD, HESSE..."
    minuit.migrad()
    minuit.hesse()
    frac.Print()
    
#     print ">>> gDirectory.Print()"
#     gDirectory.Print()
#     print ">>> gDirectory.ls()"
#     gDirectory.ls()
#     print "\n>>> locals"
#     print locals()
#     print "\n>>> globals"
#     print globals()
#     
#     print ">>> delete MINUIT object..."
#     #nll.Delete()
#     #minuit.Delete()
#     for obj in locals():
#         del obj #.Delete()
        
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
    rooFit601()
    print ">>>\n>>> Done.\n"
    

