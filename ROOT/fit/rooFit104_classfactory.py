# BASIC ROOFIT FUNCTIONALITY
# The class factory for functions and pdfs
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf104_classfactory.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/htmldoc/tutorials/roofit/rf104_classfactory.C.html
#         https://github.com/clelange/roofit/blob/master/rf104_classfactory.py

import ROOT
from ROOT import gPad, gROOT, TCanvas, TLegend,\
                 kBlue, kRed, kGreen, kTRUE, kFALSE
from ROOT import RooClassFactory, RooRealVar, RooArgSet, RooArgList
from ROOT.RooFit import LineColor, Title, Binning



def rooFit104():
    
    print ">>> RooClassFactory::makePdf - write class (\"MyPdfV1\") skeleton code..."
    # Write skeleton p.d.f class with variable x,a,b
    # To use this class, 
    #   - Edit the file MyPdfV1.cxx and implement the evaluate() method in terms of x,a and b
    #   - Compile and link class with '.x MyPdfV1.cxx+'
    RooClassFactory.makePdf("MyPdfV1","x,A,B")
    
    print ">>> write class (\"MyPdfV2\") with added initial value expression..."
    # Write skeleton pdf class with variable x,a,b and given formula expression 
    # To use this class, 
    #   - Compile and link class with '.x MyPdfV2.cxx+'
    RooClassFactory.makePdf("MyPdfV2","x,A,B","","A*fabs(x)+pow(x-B,2)")
    
    print ">>> write class (\"MyPdfV3\") with added analytical integral expression..."
    # Write skeleton p.d.f class with variable x,a,b, given formula expression _and_
    # given expression for analytical integral over x
    # To use this class, 
    #   - Compile and link class with '.x MyPdfV3.cxx+'
    RooClassFactory.makePdf("MyPdfV3","x,A,B","","A*fabs(x)+pow(x-B,2)",kTRUE,kFALSE,
                   "x:(A/2)*(pow(x.max(rangeName),2)+pow(x.min(rangeName),2))+(1./3)*(pow(x.max(rangeName)-B,3)-pow(x.min(rangeName)-B,3))")
    
    print ">>> compile and load \"MyPdfV3\" class..."
    gROOT.ProcessLineSync(".x MyPdfV3.cxx+")
    #MyPdfV3 = gROOT.LoadClass("MyPdfV3.cxx+") # TClass
    #print ">>> type(%s) = %s" % ("MyPdfV3",type(MyPdfV3))
    from ROOT import MyPdfV3
    
    print ">>> generate and fit data with \"MyPdfV3\" class...\n"
    a      = RooRealVar("a","a",1)
    b      = RooRealVar("b","b",2,-10,10)
    x      = RooRealVar("x","x",-10,10)
    pdf    = MyPdfV3("pdf","pdf",x,a,b)
    frame1 = x.frame(Title("Compiled class MyPdfV3")) # RooPlot
    data   = pdf.generate(RooArgSet(x),1000) # RooDataSet
    pdf.fitTo(data)
    data.plotOn(frame1,Binning(40))
    pdf.plotOn(frame1)
    
    
    
    print "\n>>> RooClassFactory::makePdfInstance - generate a pdf instance directly..."
    # The RooClassFactory::makePdfInstance() function performs code writing, compiling, linking
    # and object instantiation in one go and can serve as a straight replacement of RooGenericPdf
    y      = RooRealVar("y","y",-20,20)
    alpha  = RooRealVar("alpha","alpha",5,0.1,10)
    genpdf = RooClassFactory.makePdfInstance("GenPdf","(1+0.1*fabs(y)+sin(sqrt(fabs(y*alpha+0.1))))",RooArgList(y,alpha)) # RooAbsPdf

    print ">>> generate and fit data with pdf instance...\n"
    data2  = genpdf.generate(RooArgSet(y),10000) # RooDataSet
    genpdf.fitTo(data2)
    frame2 = y.frame(Title("Compiled version of pdf of rf103")) # RooPlot
    data2.plotOn(frame2,Binning(50))
    genpdf.plotOn(frame2)
    
    
    
    print "\n>>> draw pdfs and fits on canvas..."
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
    canvas.SaveAs("rooFit104.png")
    


if __name__ == '__main__':
    rooFit104()
    print ">>>\n>>> Done.\n"
    

