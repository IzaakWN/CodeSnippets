# BASIC ROOFIT FUNCTIONALITY
# Examples on normalization of pdfs, integration of pdfs,
# construction of cumulative distribution functions from pdfs
# in one dimension
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf110_normintegration.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf110_normintegration.C.html
#         https://github.com/clelange/roofit/blob/master/rf110_normintegration.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooLinearVar, RooAbsReal
from ROOT.RooFit import LineColor, Title, RooConst, NormSet, Range, Name, Normalization
from math import sqrt, pi



def rooFit110():
    
    print ">>> setup  model..."
    x     = RooRealVar("x","x",-10,10)
    mean  = RooConst(-2)
    sigma = RooConst(3)
    gauss = RooGaussian("gauss","gauss",x,mean,sigma)
    frame1 = x.frame(Title("Gaussian pdf")) # RooPlot
    gauss.plotOn(frame1)
    
    print ">>> retrieve raw & normalized values of RooFit pdfs...\n>>>"
    # Return 'raw' unnormalized value of gauss
    print ">>>   raw value:          gauss.getVal( )  = %.3f" % gauss.getVal() + " depends on x range"
    print ">>>   normalization:      gauss.getVal(x)  = %.3f" % gauss.getVal(RooArgSet(x))
    print ">>>   normalization:     gauss.getNorm(x)  = %.3f" % gauss.getNorm(RooArgSet(x))
    print ">>>                  1/(sigma*sqrt(2*pi))  = %.3f" % (1/(sigma.getValV()*sqrt(2*pi)))
    # Create object representing integral over gauss
    # which is used to calculate  gauss_Norm[x] == gauss / gauss_Int[x]
    igauss = gauss.createIntegral(RooArgSet(x)) # RooAbsReal
    print ">>>   integral:          igauss.getVal( )  = %.3f" % igauss.getVal()
    print ">>>                      igauss.getVal(x)  = %.3f" % igauss.getVal(RooArgSet(x))
    print ">>>                    1/igauss.getVal(x)  = %.3f" % (1/igauss.getVal(RooArgSet(x)))
    print ">>>       gauss.getVal()/igauss.getVal(x)  = %.3f" % (gauss.getVal()/igauss.getVal(RooArgSet(x)))
    # maximum
    print ">>>   maximum:         gauss.getMaxVal(x)  = %.3f" % gauss.getMaxVal(RooArgSet(x))
    print ">>>                       gauss.getMax(0)  = %.3f" % gauss.maxVal(0)
    print ">>>                       gauss.getMax(1)  = %.3f" % gauss.maxVal(1)
    print ">>>           gauss.asTF(x).GetMaximumX()  = %.3f" % gauss.asTF(RooArgList(x)).GetMaximumX()
    print ">>>            gauss.asTF(x).GetMaximum()  = %.3f" % gauss.asTF(RooArgList(x)).GetMaximum()
    xmaxVal = gauss.asTF(RooArgList(x)).GetMaximumX()
    xmax = RooRealVar("x_max","x_max",xmaxVal)
    x.setVal(xmaxVal)
    print ">>>                    gauss.getVal(    )  = %.3f" % gauss.getVal()
    print ">>>                    gauss.getVal(xmax)  = %.3f" % gauss.getVal(RooArgSet(x))
    print ">>>                    gauss.getVal(xmax)  = %.3f" % gauss.getVal(RooArgSet(xmax))
    
    print ">>> plot"
    frame2 = x.frame(Title("integral of Gaussian pdf")) # RooPlot
    line1 = RooLinearVar("line1","line1",x,RooConst(0),RooConst(gauss.getVal()))
    line2 = RooLinearVar("line2","line2",x,RooConst(0),RooConst(gauss.getVal(RooArgSet(x))))
    igauss.plotOn(frame2,LineColor(kBlue), Name(igauss.GetName()))
    line1.plotOn( frame2,LineColor(kRed),  Name(line1.GetName()))
    line2.plotOn( frame2,LineColor(kGreen),Name(line2.GetName()))
    
    print ">>>\n>>> integrate normalized pdf over subrange..."
    # Define a range named "signal" in x from -5,5
    x.setRange("signal",-5,5)
    
    # Create an integral of gauss_Norm[x] over x in range "signal"
    # This is the fraction of of p.d.f. gauss_Norm[x] which is in
    # the range named "signal"
    igauss_sig = gauss.createIntegral(RooArgSet(x),NormSet(RooArgSet(x)),Range("signal")) # RooAbsReal
    print ">>>   gauss_Int[x|signal]_Norm[x] = %.2f" % igauss_sig.getVal()
    
    print ">>> construct cumulative distribution function from pdf..."
    # Create the cumulative distribution function of
    # gauss, i.e. calculate Int[-10,x] gauss(x') dx'
    gauss_cdf = gauss.createCdf(RooArgSet(x)) # RooAbsReal
    frame3 = x.frame(Title("cdf of Gaussian pdf")) # RooPlot
    gauss_cdf.plotOn(frame3)
    
    print ">>> draw functions on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,2000,400)
    legend = TLegend(0.6,0.6,0.8,0.42)
    legend.SetTextSize(0.032)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    canvas.Divide(3)
    for i, frame in enumerate([frame1,frame2,frame3],1):
        canvas.cd(i)
        gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.04)
        frame.GetYaxis().SetTitleOffset(1.6)
        frame.GetYaxis().SetLabelOffset(0.010)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.042)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetXaxis().SetLabelSize(0.042)
        frame.Draw()
        if i is 2:
            legend.AddEntry(line1.GetName(), " gauss.getVal( )",'L')
            legend.AddEntry(line2.GetName(), " gauss.getVal(x)",'L')
            legend.AddEntry(igauss.GetName(),"igauss.getVal( )",'L')
            legend.Draw()
    canvas.SaveAs("rooFit110.png")
    


if __name__ == '__main__':
    rooFit110()
    print ">>>\n>>> Done.\n"
    

