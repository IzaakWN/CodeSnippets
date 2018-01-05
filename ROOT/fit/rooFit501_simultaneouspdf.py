# ORGANIZATION AND SIMULTANEOUS FITS
# Using simultaneous p.d.f.s to describe simultaneous fits to multiple datasets
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf501_simultaneouspdf.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf501_simultaneouspdf.C.html
#         https://github.com/clelange/roofit/blob/master/rf501_simultaneouspdf.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kDashed
from ROOT import RooRealVar, RooArgSet, RooArgList, RooDataSet, RooGaussian, RooChebychev, RooSimultaneous, RooAddPdf, RooCategory
from ROOT.RooFit import Title, LineColor, LineStyle, Range, Bins, Name, Index, Import, Components, Slice, ProjWData, Cut



def rooFit501():
    
    print ">>> setup model for physics sample..."
    x     = RooRealVar("x","x",-8,8)
    mean  = RooRealVar("mean","mean",0,-8,8)
    sigma = RooRealVar("sigma","sigma",0.3,0.1,10)
    gauss = RooGaussian("gx","gx",x,mean,sigma)
    a0 = RooRealVar("a0","a0",-0.1,-1,1)
    a1 = RooRealVar("a1","a1",0.004,-1,1)
    px = RooChebychev("px","px",x,RooArgList(a0,a1))
    f     = RooRealVar("f","f",0.2,0.,1.)
    model = RooAddPdf("model","model",RooArgList(gauss,px),RooArgList(f))
    
    print ">>> setup model for control sample..."
    # NOTE: sigma is shared with the signal sample model
    mean_ctrl  = RooRealVar("mean_ctrl","mean_ctrl",-3,-8,8)
    gauss_ctrl = RooGaussian("gauss_ctrl","gauss_ctrl",x,mean_ctrl,sigma)
    a0_ctrl = RooRealVar("a0_ctrl","a0_ctrl",-0.1,-1,1)
    a1_ctrl = RooRealVar("a1_ctrl","a1_ctrl",0.5,-0.1,1)
    px_ctrl = RooChebychev("px_ctrl","px_ctrl",x,RooArgList(a0_ctrl,a1_ctrl))
    f_ctrl     = RooRealVar("f_ctrl","f_ctrl",0.5,0.,1.)
    model_ctrl = RooAddPdf("model_ctrl","model_ctrl",RooArgList(gauss_ctrl,px_ctrl),RooArgList(f_ctrl))
    
    
    
    print ">>> generate events for both samples..."
    data      = model.generate(RooArgSet(x),100) # RooDataSet
    data_ctrl = model_ctrl.generate(RooArgSet(x),2000) # RooDataSet
    
    print ">>> create index category and join samples..."
    # Define category to distinguish physics and control samples events
    sample = RooCategory("sample","sample")
    sample.defineType("physics")
    sample.defineType("control")
    
    print ">>> construct combined dataset in (x,sample)..."
    combData = RooDataSet("combData","combined data",RooArgSet(x),Index(sample),Import("physics",data),Import("control",data_ctrl))
    
    print ">>> construct a simultaneous pdf in (x,sample)..."
    # Construct a simultaneous pdf using category sample as index
    simPdf = RooSimultaneous("simPdf","simultaneous pdf",sample)
    
    # Associate model with the physics state and model_ctrl with the control state
    simPdf.addPdf(model,"physics")
    simPdf.addPdf(model_ctrl,"control")
    
    print ">>> perform a simultaneous fit..."
    # Perform simultaneous fit of model to data and model_ctrl to data_ctrl
    simPdf.fitTo(combData)
    
    
    
    print "\n>>> plot model slices on data slices..."
    frame1 = x.frame(Bins(30),Title("Physics sample")) # RooPlot
    combData.plotOn(frame1,Cut("sample==sample::physics"))
    
    # Plot "physics" slice of simultaneous pdf. 
    # NBL You _must_ project the sample index category with data using ProjWData 
    # as a RooSimultaneous makes no prediction on the shape in the index category 
    # and can thus not be integrated
    simPdf.plotOn(frame1,Slice(sample,"physics"),ProjWData(RooArgSet(sample),combData))
    simPdf.plotOn(frame1,Slice(sample,"physics"),Components("px"),ProjWData(RooArgSet(sample),combData),LineStyle(kDashed))
    
    print "\n>>> plot control sample slices..."
    frame2 = x.frame(Bins(30),Title("Control sample")) # RooPlot
    combData.plotOn(frame2,Cut("sample==sample::control"))
    simPdf.plotOn(frame2,Slice(sample,"control"),ProjWData(RooArgSet(sample),combData))
    simPdf.plotOn(frame2,Slice(sample,"control"),Components("px_ctrl"),ProjWData(RooArgSet(sample),combData),LineStyle(kDashed))
    
    print "\n>>> draw on canvas..."
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
    canvas.SaveAs("rooFit501.png")
    


if __name__ == '__main__':
    rooFit501()
    print ">>>\n>>> Done.\n"
    

