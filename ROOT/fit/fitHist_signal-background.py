# Example of signal + background fit with using plainly TF1 and TH1::Fit
# where the signal model is a gaussian function and the background model
# is either a function or histogram.
#
# Author: Izaak Neutelings (August 2017)
# After:  $ROOTSYS/tutorials/fit/fithist.C by Rene Brun
# https://root.cern.ch/root/html/tutorials/fit/fithist.C.html
# https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html
# https://root.cern.ch/doc/master/classTFormula.html
# https://root.cern.ch/doc/master/classTF1.html

import ROOT
from ROOT import TFile, TF1, TH1F, TCanvas, kBlack, kBlue, kRed, kViolet, kGreen
from math import exp

# globally defined TF1 for ftotal
background = None



def histgen():
    """Generate the histogram background and save it to a file
       background taken as linearly decreasing"""
    
    file = TFile("fitHist.root","recreate")
    
    # "real" background
    f_background = TF1("fB","pol1",0,10)
    f_background.SetParameters(5,-0.5)
    f_background.Write()
    histB1 = TH1F("background_data","real, linear background",50,0,10)
    histB1.FillRandom("fB",10000)
    histB1.Write()
    
    # "simulated" background template
    histB2 = TH1F("background_MC","simulated, linear background",50,0,10)
    histB2.FillRandom("fB",60000)
    histB2.Scale(histB1.Integral()/histB2.Integral())
    histB2.Write()
    
    # superimpose a gaussian signal to the background
    f_signal = TF1("fS","gaus",0,10)
    f_signal.SetParameters(1,6,0.5)
    f_signal.Write()
    histS = TH1F("signal_data","real signal",50,0,10)
    histD = TH1F("data","data",50,0,10)
    histS.FillRandom("fS",1000)
    histD.Add(histB1)
    histD.Add(histS)
    histD.Write()



def ftotal(var, par):
    """Parametrized function of signal (function) + background (histogram)"""
    x  = var[0]
    bin = background.GetXaxis().FindBin(x)
    br  = par[0]*background.GetBinContent(bin)
    #br  = par[3]+par[4]*x
    arg = (x-par[2])/par[3]
    sr  = par[1]*exp(-0.5*arg*arg)
    return sr + br



def main():
    """Fit function ftotal to signal + background"""
    
    global f_background, background
    histgen()
    
    file = TFile("fitHist.root")
    background = file.Get("background_MC")
    data = file.Get("data")
    
    print ">>> define fit functions..."
    ftot1 = TF1("ftot1","pol1(0)+gaus(2)",0,10,4)   # function  as background template
    ftot2 = TF1("ftot2",ftotal,0,10,4)              # histogram as background template
    norm  = data.GetMaximum()
    # pol1   = [0]+[1]*x
    # gaus   = [0]*exp(-0.5*((x-[1])/[2])**2)
    # ftotal = [0]*hist + [1]*exp(-0.5*((x-[2])/[3])**2)
    ftot1.SetParNames("A","B","N","mu","sigma")
    ftot2.SetParNames("M","N","mu","sigma")
    ftot1.SetParameters(1.5*norm, -40,0.5*norm,5,0.2) # start values to help fit
    ftot2.SetParameters(1.5*norm,     0.5*norm,5,0.2) # start values to help fit
    ftot1.SetParLimits(0,       0,1000)         # set limits on parameter 1
    ftot1.SetParLimits(2,0.1*norm,norm)         # set limits on parameter 2
    ftot2.SetParLimits(1,0.1*norm,norm)         # set limits on parameter 1
    print norm
    
    print ">>> fit..."
    canvas = TCanvas("canvas","canvas",100,100,800,600)
    ftot1.SetLineColor(kGreen+1)
    ftot2.SetLineColor(kViolet)
    ftot1.SetLineWidth(2)
    ftot2.SetLineWidth(2)
    data.SetLineColor(kBlack)
    data.SetMarkerSize(0.6)
    data.SetMarkerStyle(8)
    data.Draw("E1")
    data.Fit( ftot1, "B")
    data.Fit("ftot2","B+")  # use + to add second fit function to histogram
    #ftot1.Draw("same")
    #ftot2.Draw("same")
    
    print ">>> draw signal and background components..."
    fB = TF1("fB","pol1",0,10,4)
    fS = TF1("fS","gaus",0,10,4)
    par = ftot1.GetParameters()
    fB.SetParameters(par[0],par[1])
    fS.SetParameters(par[2],par[3],par[4])
    fB.SetLineColor(kBlue)
    fS.SetLineColor(kRed)
    fB.SetLineStyle(2)
    fS.SetLineStyle(2)
    fB.Draw("same")
    fS.Draw("same")
    canvas.SaveAs("fitHist.png")




if __name__ == '__main__':
    print "\n>>>"
    main()
    print ">>>\n>>> Done.\n"


