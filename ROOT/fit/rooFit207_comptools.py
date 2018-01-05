# ADDITION AND CONVOLUTION
# Tools and utilities for manipulation of composite objects
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf207_comptools.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf207_comptools.C.html
#         https://github.com/clelange/roofit/blob/master/rf207_comptools.py

import ROOT
from ROOT import gPad, TCanvas, TLegend, kBlue, kRed, kGreen, kTRUE, kFALSE
from ROOT import RooRealVar, RooArgSet, RooArgList, RooDataSet,\
                 RooGaussian, RooChebychev, RooExponential, RooAddPdf, RooCustomizer
from ROOT.RooFit import Title, LineColor, Range, Name



def rooFit207():
    
    print ">>> setup model signal components: gaussians..."
    x     = RooRealVar("x","x",0,10)
    mean  = RooRealVar("mean","mean of gaussians",5)
    sigma = RooRealVar("sigma","width of gaussians",0.5)
    sig   = RooGaussian("sig","Signal",x,mean,sigma)
    
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
    
    # Create dummy dataset that has more observables than the above pdf
    y    = RooRealVar("y","y",-10,10)
    data = RooDataSet("data","data",RooArgSet(x,y))
    
    # Basic information requests:"
    print ">>> get list of observables of pdf in context of a dataset..."
    # Observables are define each context as the variables
    # shared between a model and a dataset. In this case
    # that is the variable 'x'
    model_obs = model.getObservables(data) # RooArgSet
    model_obs.Print('v')
    
    print "\n>>> get list of parameters..."
    # Get list of parameters, given list of observables
    model_params = model.getParameters(RooArgSet(x)) # RooArgSet
    print ">>> model_params.getStringValue(\"a0\") = %s" % (model_params.getStringValue("a0"))
    print ">>> model_params.getRealValue(\"a0\")   = %s" % (model_params.getRealValue("a0"))
    print ">>> model_params.find(\"a0\").GetName() = %s" % (model_params.find("a0").GetName())
    print ">>> model_params.find(\"a0\").getVal()  = %s" % (model_params.find("a0").getVal())
#     print ">>> for param in model_params:"
#     for param in model_params.():
#     print ">>>   %s"%(model_params.first())
#     print ">>>   %s"%(model_params.first())
#     model_params.selectByName("a*").Print('v')
    model_params.Print('v')
    
    print "\n>>> get list of parameters of a dataset..."
    # Gives identical results to operation above
    model_params2 = model.getParameters(data) # RooArgSet
    model_params2.Print()
    
    print "\n>>> get list of components..."
    # Get list of component objects, including top-level node
    model_comps = model.getComponents() # RooArgSet
    model_comps.Print('v')
    
    
    
    print "\n>>> modifications to structure of composites..."
    sigma2 = RooRealVar("sigma2","width of gaussians",1)
    sig2   = RooGaussian("sig2","Signal component 1",x,mean,sigma2)
    sig1frac = RooRealVar("sig1frac","fraction of component 1 in signal",0.8,0.,1.)
    sigsum   = RooAddPdf("sigsum","sig+sig2",RooArgList(sig,sig2),RooArgList(sig1frac))
    
    print ">>> construct a customizer utility to customize model..."
    cust = RooCustomizer(model,"cust")
    
    print ">>> instruct the customizer to replace node 'sig' with node 'sigsum'..."
    cust.replaceArg(sig,sigsum)

    # Build a clone of the input pdf according to the above customization
    # instructions. Each node that requires modified is clone so that the
    # original pdf remained untouched. The name of each cloned node is that
    # of the original node suffixed by the name of the customizer object  
    #
    # The returned head node own all nodes that were cloned as part of
    # the build process so when cust_clone is deleted so will all other
    # nodes that were created in the process.
    cust_clone = cust.build(kTRUE) # RooAbsPdf
    
    # Print structure of clone of model with sig->sigsum replacement.
    cust_clone.Print("t")
    
    # delete clone
    del cust_clone
    


if __name__ == '__main__':
    rooFit207()
    print ">>>\n>>> Done.\n"
    

