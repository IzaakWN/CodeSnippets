# BASIC ROOFIT FUNCTIONALITY
# Calculating chi^2 from histograms and curves in RooPlots, 
# making histogram of residual and pull distributions
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf109_chi2residpulls.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf109_chi2residpull.C.html
#         https://github.com/clelange/roofit/blob/master/rf109_chi2residpull.py

import ROOT
from ROOT import gPad, gStyle, TCanvas, TLegend, TLine, kBlue, kRed, kGreen, kYellow, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooAbsData
from ROOT.RooFit import Title, LineColor, Bins, RooConst, DataError



def rooFit109():
    
    print ">>> setup model..."
    x     = RooRealVar("x","x",-10,10)
    sigma = RooRealVar("sigma","sigma",3,0.1,10)
    mean  = RooRealVar("mean","mean",0,-10,10)
    gauss = RooGaussian("gauss","gauss",x,RooConst(0),sigma) # RooConst(0) gives segfaults
    data  = gauss.generate(RooArgSet(x),100000) # RooDataSet
    #sigma = 3.15 # overwrites RooRealVar with a float
    sigma.setVal(3.15)
    
    print ">>> plot data and slightly distorted model..."
    frame1 = x.frame(Title("Data with distorted Gaussian pdf"),Bins(40)) # RooPlot
    data.plotOn(frame1,DataError(RooAbsData.SumW2))
    gauss.plotOn(frame1)
    
    print ">>> calculate chi^2..."
    # Show the chi^2 of the curve w.r.t. the histogram
    # If multiple curves or datasets live in the frame you can specify
    # the name of the relevant curve and/or dataset in chiSquare()
    print ">>>   chi^2 = %.2f" % frame1.chiSquare()
    
    print ">>> construct histograms with the residuals and pull of the data wrt the curve"
    hresid = frame1.residHist() # RooHist
    hpull  = frame1.pullHist() # RooHist
    frame2 = x.frame(Title("Residual Distribution")) # RooPlot
    frame2.addPlotable(hresid,"P")
    frame3 = x.frame(Title("Pull Distribution")) # RooPlot
    frame3.addPlotable(hpull,"P")
    
    
    
    print ">>> draw functions and toy data on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,2000,400)
    canvas.Divide(3)
    for i, frame in enumerate([frame1,frame2,frame3],1):
        canvas.cd(i)
        gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.04)
        frame.GetYaxis().SetTitleOffset(1.5)
        frame.GetYaxis().SetLabelOffset(0.010)
        frame.GetYaxis().SetTitleSize(0.045)
        frame.GetYaxis().SetLabelSize(0.042)
        frame.GetXaxis().SetTitleSize(0.045)
        frame.GetXaxis().SetLabelSize(0.042)
        frame.Draw()
    canvas.SaveAs("rooFit109.png")
    canvas.Close()
        
    # ratio/pull/residual plot
    print ">>> draw with pull plot..."
    canvas = TCanvas("canvas","canvas",100,100,1000,1000)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetPad("pad1","pad1",0,0.33,1,1,0,-1,0)
    gPad.SetTopMargin(0.10); gPad.SetBottomMargin(0.03)
    gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.04)
    gPad.SetBorderMode(0)
    gStyle.SetTitleFontSize(0.062)
    frame1.GetYaxis().SetTitle("Events / %.3g GeV"%frame1.getFitRangeBinW())
    frame1.GetYaxis().SetTitleSize(0.059)
    frame1.GetYaxis().SetTitleOffset(1.21)
    #frame1.GetYaxis().SetLabelOffset(0.010)
    frame1.GetXaxis().SetLabelSize(0); frame1.GetYaxis().SetLabelSize(0.045)
    frame1.Draw()
    canvas.cd(2)
    gPad.SetPad("pad2","pad2",0,0,1,0.33,0,-1,0)
    gPad.SetTopMargin(0.01); gPad.SetBottomMargin(0.30)
    gPad.SetLeftMargin(0.14); gPad.SetRightMargin(0.04)
    gPad.SetBorderMode(0)
    gPad.SetGridy(kTRUE)
    line1 = TLine(frame3.GetXaxis().GetXmin(),0,frame3.GetXaxis().GetXmax(),0)
    line2 = TLine(frame3.GetXaxis().GetXmin(),0,frame3.GetXaxis().GetXmax(),0)
    line1.SetLineColor(0) # white to clear dotted grid lines
    line2.SetLineColor(12) # dark grey
    line2.SetLineStyle(2)
    frame3.SetTitle("")
    frame3.GetYaxis().SetTitle("pull")
    frame3.GetXaxis().SetTitle("#Deltam^{2}_{ll} [GeV]")
    frame3.GetXaxis().SetTitleSize(0.13);   frame3.GetYaxis().SetTitleSize(0.12)
    frame3.GetXaxis().SetTitleOffset(1.0);  frame3.GetYaxis().SetTitleOffset(0.58)
    frame3.GetXaxis().SetLabelSize(0.10);   frame3.GetYaxis().SetLabelSize(0.10)
    frame3.GetXaxis().SetLabelOffset(0.02); frame3.GetYaxis().SetLabelOffset(0.01)
    frame3.GetYaxis().SetRangeUser(-5,5)
    frame3.GetYaxis().CenterTitle(True)
    frame3.GetYaxis().SetNdivisions(505)
    frame3.Draw("")
    line1.Draw("SAME")
    line2.Draw("SAME")
    frame3.Draw("SAME")
    canvas.SaveAs("rooFit109_ratiolike.png")
    canvas.Close()
    


if __name__ == '__main__':
    rooFit109()
    print ">>>\n>>> Done.\n"
    

