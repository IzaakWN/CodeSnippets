# BASIC ROOFIT FUNCTIONALITY
# Importing data from ROOT TTrees and THx histograms
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf101_dataimport.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/htmldoc/tutorials/roofit/rf102_dataimport.C.html
#         https://github.com/clelange/roofit/blob/master/rf102_dataimport.py

import ROOT
from ROOT import gPad, gRandom, TH1D, TTree, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooDataHist, RooDataSet, RooRealVar, RooArgList, RooArgSet, RooAbsData, RooGaussian
from ROOT.RooFit import LineColor, Title, Import, DataError, Binning
from array import array



def makeTH1():
    """Create ROOT TH1 filled with a Gaussian distribution"""

    hist = TH1D("hist","hist",25,-10,10)
    for i in range(500):
        hist.Fill(gRandom.Gaus(0,3))
    return hist
    


def makeTTree():
    """Create ROOT TTree filled with a Gaussian distribution in x
       and a uniform distribution in y"""
    
    tree = TTree("tree","tree")
    px   = array('d',[0])
    py   = array('d',[0])
    tree.Branch("px",px,"px/D")
    tree.Branch("py",py,"py/D")
    for i in range(500):
        px[0] = gRandom.Gaus(0,3)
        py[0] = gRandom.Uniform()*30 - 15
        tree.Fill()
    return tree
    


def rooFit102():
    
    print ">>> import TH1 into RooDataHist..."
    hist  = makeTH1()
    x     = RooRealVar("x","x",-10,10)
    data_hist = RooDataHist("data_hist","data_hist",RooArgList(x),Import(hist))
    
    print ">>> plot and fit RooDataHist...\n"
    mean   = RooRealVar("mean","mean of gaussian",1,-10,10)
    sigma  = RooRealVar("sigma","width of gaussian",1,0.1,10)
    gauss  = RooGaussian("gauss","gaussian PDF",x,mean,sigma)
    gauss.fitTo(data_hist)
    frame1 = x.frame(Title("Imported TH1 with Poisson error bars")) # RooPlot
    data_hist.plotOn(frame1)
    gauss.plotOn(frame1)
    
    print "\n>>> plot and fit RooDataHist with internal errors..."
    # If histogram has custom error (i.e. its contents is does not originate from a
    # Poisson process but e.g. is a sum of weighted events) you can create data with
    # symmetric 'sum-of-weights' error instead (i.e. same error bars as shown by ROOT)
    frame2 = x.frame(Title("Imported TH1 with internal errors"))
    data_hist.plotOn(frame2,DataError(RooAbsData.SumW2))
    gauss.plotOn(frame2)
    
    # Please note that error bars shown (Poisson or SumW2) are for visualization only,
    # the are NOT used in a maximum likelihood (ML) fit
    #
    # A (binned) ML fit will ALWAYS assume the Poisson error interpretation of data
    # (the mathematical definition  of likelihood does not take any external definition
    # of errors). Data with non-unit weights can only be correctly fitted with a chi^2
    # fit (see rf602_chi2fit.C)
    
    
    
    print ">>> import TTree into RooDataHist..."
    # Construct unbinned dataset importing tree branches x and y matching between
    # branches and RooRealVars is done by name of the branch/RRV 
    # 
    # Note that ONLY entries for which x,y have values within their allowed ranges as 
    # defined in RooRealVar x and y are imported. Since the y values in the import tree
    # are in the range [-15,15] and RRV y defines a range [-10,10] this means that the
    # RooDataSet below will have less entries than the TTree 'tree'
    tree     = makeTTree()
    px       = RooRealVar("px","px",-10,10)
    py       = RooRealVar("py","py",-10,10)
    data_set = RooDataSet("data_set","data_set",RooArgSet(px,py),Import(tree))
    data_set.Print()
    frame3 = py.frame(Title("Unbinned data shown in default frame binning"))
    frame4 = py.frame(Title("Unbinned data shown with custom binning"))
    data_set.plotOn(frame3)             # default frame binning of 100 bins
    data_set.plotOn(frame4,Binning(20)) # custom binning choice
    
    
    
    print ">>> draw pfds and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1000,1200)
    canvas.Divide(2,2)
    for i, frame in enumerate([frame1,frame2,frame3,frame4],1):
        canvas.cd(i)
        gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.05)
        frame.GetYaxis().SetTitleOffset(1.6)
        frame.GetYaxis().SetLabelOffset(0.010)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.042)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetXaxis().SetLabelSize(0.042)
        frame.Draw()
    canvas.SaveAs("rooFit102.png")
    


if __name__ == '__main__':
    rooFit102()
    print ">>>\n>>> Done.\n"
    

