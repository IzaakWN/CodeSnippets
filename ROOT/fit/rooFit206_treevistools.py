# ADDITION AND CONVOLUTION
# Tools for visualization of RooAbsArg expression trees
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf206_treevistools.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf206_treevistools.C.html
#         https://github.com/clelange/roofit/blob/master/rf206_treevistools.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kDashed, kDotted
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussian, RooChebychev, RooExponential, RooAddPdf
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Binning, Name, Components



def rooFit206():
    
    print ">>> setup model signal components: gaussians..."
    x      = RooRealVar("x","x",0,10)
    mean   = RooRealVar("mean","mean of gaussians",5)
    sigma1 = RooRealVar("sigma1","width of gaussians",0.5)
    sigma2 = RooRealVar("sigma2","width of gaussians",1)
    sig1   = RooGaussian("sig1","Signal component 1",x,mean,sigma1)
    sig2   = RooGaussian("sig2","Signal component 2",x,mean,sigma2)
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sig      = RooAddPdf("sig","Signal",RooArgList(sig1,sig2),RooArgList(sig1frac))
    
    print ">>> setup model background components: Chebychev polynomial plus exponential..."
    a0    = RooRealVar("a0","a0",0.5,0.,1.)
    a1    = RooRealVar("a1","a1",-0.2,0.,1.)
    bkg1  = RooChebychev("bkg1","Background 1",x,RooArgList(a0,a1))
    alpha = RooRealVar("alpha","alpha",-1)
    bkg2  = RooExponential("bkg2","Background 2",x,alpha)
    bkg1frac = RooRealVar("bkg1frac","fraction of component 1 in background",0.2,0.,1.)
    bkg      = RooAddPdf("bkg","Signal",RooArgList(bkg1,bkg2),RooArgList(bkg1frac))
    
    print ">>> sum signal and background component..."
    bkgfrac = RooRealVar("bkgfrac","fraction of background",0.5,0.,1.)
    model   = RooAddPdf("model","g1+g2+a",RooArgList(bkg,sig),RooArgList(bkgfrac))
    
    print ">>> composite tree in ASCII:"
    model.Print("t")
    
    print "\n>>> write to txt file"
    model.printCompactTree("","rooFit206_asciitree.txt")
    
    print ">>> draw composite tree graphically..."
    # Print GraphViz DOT file with representation of tree
    model.graphVizTree("rooFit206_model.dot")
    
    # Make graphic output file with one of the GraphViz tools
    # (freely available from www.graphviz.org)
    #
    # 'Top-to-bottom graph'
    # unix> dot -Tgif -o rooFit206_model_dot.gif rooFit206_model.dot
    #
    # 'Spring-model graph'
    # unix> fdp -Tgif -o rooFit206_model_fdp.gif rooFit206_model.dot
    
    
    
    print ">>> plot everything..."
    data   = model.generate(RooArgSet(x),1000) # RooDataSet
    frame1 = x.frame(Title("Component plotting of pdf=(sig1+sig2)+(bkg1+bkg2)")) # RooPlot
    data.plotOn(frame1, Name("data"),Binning(40))
    model.plotOn(frame1,Name("model"))
    argset1 = RooArgSet(bkg)
    argset2 = RooArgSet(bkg2)
    argset3 = RooArgSet(bkg,sig2)
    model.plotOn(frame1,Components(argset1),LineColor(kRed),                   Name("bkg"))
    model.plotOn(frame1,Components(argset2),LineStyle(kDashed),LineColor(kRed),Name("bkg2")) 
    model.plotOn(frame1,Components(argset3),LineStyle(kDotted),                Name("bkgsig2"))
    
    print "\n>>> draw pfds and fits on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    legend = TLegend(0.22,0.85,0.4,0.65)
    legend.SetTextSize(0.032)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    frame1.GetYaxis().SetLabelOffset(0.008)
    frame1.GetYaxis().SetTitleOffset(1.6)
    frame1.GetYaxis().SetTitleSize(0.045)
    frame1.GetXaxis().SetTitleSize(0.045)
    frame1.Draw()
    legend.AddEntry("data",   "data",    'LEP')
    legend.AddEntry("model",  "model",   'L')
    legend.AddEntry("bkg",    "bkg",     'L')
    legend.AddEntry("bkg2",   "bkg2",    'L')
    legend.AddEntry("bkgsig2","bkg,sig2",'L')
    legend.Draw()
    canvas.SaveAs("rooFit206.png")
    


if __name__ == '__main__':
    rooFit206()
    print ">>>\n>>> Done.\n"
    

