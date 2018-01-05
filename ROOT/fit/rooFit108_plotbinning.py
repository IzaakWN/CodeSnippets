# BASIC ROOFIT FUNCTIONALITY
# Plotting unbinned data with alternate and variable binnings
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf108_plotbinning.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf108_plotbinning.C.html
#         https://github.com/clelange/roofit/blob/master/rf108_plotbinning.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList, RooGaussModel, RooBMixDecay, RooCategory, RooBinning
from ROOT.RooFit import Title, LineColor, Range, Binning, Asymmetry



def rooFit108():
    
    print ">>> setup model - a B decay with mixing..."
    dt  = RooRealVar("dt","dt",-20,20)
    dm  = RooRealVar("dm","dm",0.472)
    tau = RooRealVar("tau","tau",1.547)
    w   = RooRealVar("w","mistag rate",0.1)
    dw  = RooRealVar("dw","delta mistag rate",0.)
    
    # Build categories - possible values states
    # https://root.cern/doc/v610/classRooCategory.html
    mixState = RooCategory("mixState","B0/B0bar mixing state")
    mixState.defineType("mixed",-1)
    mixState.defineType("unmixed",1)
    tagFlav  = RooCategory("tagFlav","Flavour of the tagged B0")
    tagFlav.defineType("B0",1)
    tagFlav.defineType("B0bar",-1)
    
    # Build a gaussian resolution model
    dterr   = RooRealVar("dterr","dterr",0.1,1.0)
    bias1   = RooRealVar("bias1","bias1",0)
    sigma1  = RooRealVar("sigma1","sigma1",0.1)
    gm1     = RooGaussModel("gm1","gauss model 1",dt,bias1,sigma1)
    
    # Construct Bdecay (x) gauss
    # https://root.cern/doc/v610/classRooBMixDecay.html
    bmix    = RooBMixDecay("bmix","decay",dt,mixState,tagFlav,tau,dm,w,dw,gm1,RooBMixDecay.DoubleSided)
    
    print ">>> sample data from data..."
    data    =  bmix.generate(RooArgSet(dt,mixState,tagFlav),2000) # RooDataSet
    
    print ">>> show dt distribution with custom binning..."
    # Make plot of dt distribution of data in range (-15,15) with fine binning for dt>0
    # and coarse binning for dt<0
    tbins = RooBinning(-15,15)  # Create binning object with range (-15,15)
    tbins.addUniform(60,-15,0)  # Add 60 bins with uniform spacing in range (-15,0)
    tbins.addUniform(15,0,15)   # Add 15 bins with uniform spacing in range (0,15)
    dtframe = dt.frame(Range(-15,15),Title("dt distribution with custom binning")) # RooPlot
    data.plotOn(dtframe,Binning(tbins))
    bmix.plotOn(dtframe)
    
    # NB: Note that bin density for each bin is adjusted to that of default frame
    # binning as shown in Y axis label (100 bins --> Events/0.4*Xaxis-dim) so that
    # all bins represent a consistent density distribution
    
    
    
    print ">>> plot mixstate asymmetry with custom binning..."
    # Make plot of dt distribution of data asymmetry in 'mixState' with variable binning 
    abins = RooBinning(-10,10)  # Create binning object with range (-10,10)
    abins.addBoundary(0)        # Add boundaries at 0
    abins.addBoundaryPair(1)    # Add boundaries at (-1,1)
    abins.addBoundaryPair(2)    # Add boundaries at (-2,2)
    abins.addBoundaryPair(3)    # Add boundaries at (-3,3)
    abins.addBoundaryPair(4)    # Add boundaries at (-4,4)
    abins.addBoundaryPair(6)    # Add boundaries at (-6,6)
    aframe = dt.frame(Range(-10,10),Title("MixState asymmetry distribution with custom binning")) # RooPlot
    
    # Plot mixState asymmetry of data with specified customg binning
    data.plotOn(aframe,Asymmetry(mixState),Binning(abins))
    
    # Plot corresponding property of pdf
    bmix.plotOn(aframe,Asymmetry(mixState))
    
    # Adjust vertical range of plot to sensible values for an asymmetry
    aframe.SetMinimum(-1.1)
    aframe.SetMaximum( 1.1)
    
    # NB: For asymmetry distributions no density corrects are needed (and are thus not applied)
    
    
    
    print "\n>>> draw on canvas..."
    canvas = TCanvas("canvas","canvas",100,100,1400,600)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    dtframe.GetYaxis().SetLabelOffset(0.008)
    dtframe.GetYaxis().SetTitleOffset(1.6)
    dtframe.GetYaxis().SetTitleSize(0.045)
    dtframe.GetXaxis().SetTitleSize(0.045)
    dtframe.Draw()
    canvas.cd(2)
    gPad.SetLeftMargin(0.15); gPad.SetRightMargin(0.02)
    aframe.GetYaxis().SetLabelOffset(0.008)
    aframe.GetYaxis().SetTitleOffset(1.6)
    aframe.GetYaxis().SetTitleSize(0.045)
    aframe.GetXaxis().SetTitleSize(0.045)
    aframe.Draw()
    canvas.SaveAs("rooFit108.png")
    


if __name__ == '__main__':
    rooFit108()
    print ">>>\n>>> Done.\n"
    

