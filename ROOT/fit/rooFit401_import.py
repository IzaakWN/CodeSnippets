# LIKELIHOOD AND MINIMIZATION
# Overview of advanced option for importing data from ROOT TTree and THx histograms
# Basic import options are demonstrated in rf102_dataimport.C
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf401_importttreethx.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf401_importttreethx.C.html
#         https://github.com/clelange/roofit/blob/master/rf401_importttreethx.py

import ROOT
from ROOT import gDirectory, gInterpreter, gRandom, gPad, TFile, TH1D, TTree, TCanvas, TLegend,\
                 kBlue, kRed, kGreen, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooAbsReal, RooDataHist, RooGaussian, RooCategory, RooDataSet
from ROOT.RooFit import Title, LineColor, Range, Name, Index, Import, Cut
from array import array


def makeTH1(name,mean,sigma):
    """Create ROOT TH1 filled with a Gaussian distribution"""

    hist = TH1D(name,name,100,-10,10)
    for i in range(1000):
        hist.Fill(gRandom.Gaus(mean,sigma))
    return hist
    


def makeTTree():
    """Create ROOT TTree filled with a Gaussian distribution
       in x and a uniform distribution in y"""
    
    tree = TTree("tree","tree")
    px   = array('d',[0])
    py   = array('d',[0])
    pz   = array('d',[0])
    pi   = array('i',[0])
    tree.Branch("x",px,"x/D")
    tree.Branch("y",py,"y/D")
    tree.Branch("z",pz,"y/D")
    tree.Branch("i",pi,"y/I")
    for i in range(500):
        px[0] = gRandom.Gaus(0,3)
        py[0] = gRandom.Uniform()*30 - 15
        pz[0] = gRandom.Gaus(0,5)
        pi[0] = i%3
        tree.Fill()
    return tree
    


def rooFit601():
    
#     print ">>> setup pdf and likelihood..."
#     x      = RooRealVar("x","x",-20,20)
#     mean   = RooRealVar("mean","mean of g1 and g2",0)
#     sigma1 = RooRealVar("sigma1","width of g1",3)
#     sigma2 = RooRealVar("sigma2","width of g2",4,3.0,6.0) # intentional strong correlations
#     gauss1 = RooGaussian("gauss1","gauss1",x,mean,sigma1)
#     gauss2 = RooGaussian ("gauss2","gauss2",x,mean,sigma2)
#     frac   = RooRealVar("frac","frac",0.5,0.0,1.0)
#     model  = RooAddPdf("model","model",RooArgList(gauss1,gauss2),RooArgList(frac))
    
    print ">>> import multiple TH1 into a RooDataHist..."
    hist1 = makeTH1("hist1",0,3)
    hist2 = makeTH1("hist2",-3,1)
    hist3 = makeTH1("hist3",+3,4)
    
    print ">>> create category observables that serves as index for the ROOT histograms..."
    category = RooCategory("category","category") # RooCategory
    category.defineType("SampleA")
    category.defineType("SampleB")
    category.defineType("SampleC")

    print ">>> create a binned dataset that imports contents of all TH1 mapped by index category..."
    x         = RooRealVar("x","x",-10,10)
    data_hist = RooDataHist("data_hist","data_hist",RooArgList(x),Index(category),Import("SampleA",hist1),Import("SampleB",hist2),Import("SampleC",hist3))
    data_hist.Print()

    # Alternative constructor form for importing multiple histograms
    # TODO: https://github.com/clelange/roofit/blob/master/rf401_importttreethx.py
    # hist_dict = { }
    # hist_dict["SampleA"] = hist1
    # hist_dict["SampleB"] = hist2
    # hist_dict["SampleC"] = hist3
    # datahist2 = RooDataHist("data_hist2","data_hist2",RooArgList(x),category,hist_dict) # RooDataHist
    # datahist2.Print()
    
    gInterpreter.GenerateDictionary("std::pair<std::string, TH1*>", "map;string;TH1.h")
    gInterpreter.GenerateDictionary("std::map<std::string, TH1*>",  "map;string;TH1.h")
    from ROOT import std
    hist_map = std.map('string, TH1*')()
    hist_map.keepalive = list()
    hist_map.insert(hist_map.cbegin(),std.pair("const std::string,TH1*")("SampleA", hist1))
    hist_map.insert(hist_map.cbegin(),std.pair("const std::string,TH1*")("SampleB", hist2))
    hist_map.insert(hist_map.cbegin(),std.pair("const std::string,TH1*")("SampleC", hist3))
    datahist2 = RooDataHist("datahist2", "datahist2", RooArgList(x),category,hist_map)
    datahist2.Print()
    
    
    
    print ">>> importing a TTree into a RooDataSet with cuts..."
    tree = makeTTree()
    y  = RooRealVar("y","y",-10,10)
    z  = RooRealVar("z","z",-10,10)
    dataset = RooDataSet("dataset","dataset",RooArgSet(x,y),Import(tree))
    dataset.Print()
    dataset2 = RooDataSet("dataset2","dataset2",RooArgSet(x,y,z),Import(tree),Cut("y+z<0"))
    dataset2.Print()
        
    print ">>> importing integer TTree branches..."
    i        = RooRealVar("i","i",0,5)
    dataset3 = RooDataSet("dataset3","dataset3",RooArgSet(i,x),Import(tree))
    dataset3.Print()
    
    # Import integer tree branch as RooCategory (only events with i==0 and i==1
    # will be imported as those are the only defined states)
    icategory = RooCategory("icategory","icategory")
    icategory.defineType("State0",0)
    icategory.defineType("State1",1)
    dataset4 = RooDataSet("dataset4","dataset4",RooArgSet(icategory,x),Import(tree))
    dataset4.Print()
    
    
    
    print ">>> import multiple RooDataSets into a RooDataSet..."
    datasetA = dataset2.reduce(RooArgSet(x,y),"z<-5") # RooDataSet
    datasetB = dataset2.reduce(RooArgSet(x,y),"abs(z)<5")
    datasetC = dataset2.reduce(RooArgSet(x,y),"z>5")
    
    print ">>> create a dataset that imports contents of all the above datasets mapped by index category"
    datasetABC = RooDataSet("datasetABC","datasetABC",RooArgSet(x,y),Index(category),Import("SampleA",datasetA),Import("SampleB",datasetB),Import("SampleC",datasetC))
    datasetABC.Print()
      
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
    

