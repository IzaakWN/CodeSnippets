# ORGANIZATION AND SIMULTANEOUS FITS
# Illustration of operator expressions and expression-based
# basic pdfs in the workspace factory syntax
#
# Author: Izaak Neutelings (September 2017)
# After:  $ROOTSYS/tutorials/roofit/rf512_wsfactory_oper.C by Wouter Verkerke (2008)
#         https://root.cern.ch/root/html/tutorials/roofit/rf512_wsfactory_oper.C.html
#         https://github.com/clelange/roofit/blob/master/rf512_wsfactory_oper.py

import ROOT
from ROOT import gPad, gDirectory, TCanvas, TLegend, kBlue, kRed, kGreen
from ROOT import RooRealVar, RooArgSet, RooArgList, RooWorkspace, RooGaussian, RooChebychev, RooAddPdf
from ROOT.RooFit import Title, LineColor, Range, Name



def rooFit502():
    
    print ">>> create workspace..."
    workspace = RooWorkspace("workspace","workspace")
    
    print ">>> create typedef (shorthands)..."
    workspace.factory("$Typedef(Gaussian,Gaus)")
    workspace.factory("$Typedef(Chebychev,Cheby)")
    
    
    
    print ">>> operator pdf examples..."

    print ">>>   SUM (coef1*pdf1,pdf2)         - pdf addition"
    workspace.factory("SUM::summodel( f[0,1]*Gaussian::gx(x[-10,10],m[0],1.0), Chebychev::ch(x,{0.1,0.2,-0.3}) )")
    
    print ">>>   SUM (yield1*pdf1,yield2*pdf2) - extended pdf addition"
    workspace.factory("SUM::extsummodel( Nsig[0,1000]*gx, Nbkg[0,1000]*ch )")
    
    print ">>>   PROD ( pdf1, pdf2 )           - pdf multiplication"
    # PDF multiplication is done with PROD ( pdf1, pdf2 ) 
    workspace.factory("PROD::gxz( gx, Gaussian::gz(z[-10,10],0,1) )")
    
    print ">>>   PROD ( pdf1|obs, pdf2 )       - conditional p.d.f multiplication"
    workspace.factory("Gaussian::gy( y[-10,10], x, 1.0 )")
    workspace.factory("PROD::gxycond( gy|x, gx )")
    
    print ">>>   NCONV (obs,pdf1,pdf2)         - numeric convolution"
    print ">>>   FCONV (obs,pdf1,pdf2)         - fft convolution"
    workspace.factory("FCONV::lxg( x, Gaussian::g(x,mg[0],1), Landau::lc(x,0,1) )")
    
    print ">>>   SIMUL( index, state1=pdf1, state2=pdf2,...) - simultaneous pdfs are constructed"
    workspace.factory("SIMUL::smodel( c[A=0,B=1], A=Gaussian::gs(x,m,s[1]), B=Landau::ls(x,0,1) )")
    
    
    
    print ">>> operator function examples..."
    
    print ">>>   prod (func1, func2,...)       - function multiplication"
    workspace.factory("prod::uv(u[10],v[10])")
    
    print ">>>   sum (func1, func2,...)        - function addition"
    workspace.factory("sum::uv2(u,v)")
    
    
    
    print ">>> interpreted and compiled expression based pdfs..."
    print ">>>   create a RooGenericPdf interpreted pdf by using single quotes to pass the expression string argument"
    workspace.factory("EXPR::G('x*x+1',x)")
    
    # Create a custom compiled p.d.f similar to the above interpreted p.d.f.
    # The code required to make this p.d.f. is automatically embedded in the workspace
    workspace.factory("CEXPR::GC('x*x+a',{x,a[1]})")
    
    # Compiled and interpreted functions (rather than pdfs) can be made with the lower case 
    # 'expr' and 'cexpr' types
    
    
    
    print ">>> print workspace contents:"
    workspace.Print()
    
    print "\n>>> save workspace in memory..."
    gDirectory.Add(workspace)
    # Workspace will remain in memory after macro finishes
    


if __name__ == '__main__':
    rooFit502()
    print ">>>\n>>> Done.\n"
    

