# Simple example of generating a histogram from a gaussian function
# and fitting it
#
# Author: Izaak Neutelings (August 2017)
# https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html
# https://root.cern.ch/doc/master/classTFormula.html
# https://root.cern.ch/doc/master/classTF1.html

import ROOT
from ROOT import TF1, TH1F, TCanvas, TLegend, kBlack, kBlue, kRed, kViolet, kGreen
from math import exp

print ">>> generating signal..."
function1 = TF1("f1","gaus",0,10)
function1.SetParameters(1,2,0.5)
hist = TH1F("signal","signal",50,0,5)
hist.FillRandom("f1",1000)

print ">>> make fit functions..."
# pol1  = [0]+[1]*x+[2]*x**2
# gaus  = [0]*exp(-0.5*((x-[1])/[2])**2)
norm = hist.GetMaximum()
function2 = TF1("f2","gaus",0,10)
function3 = TF1("f3","pol2",0,10)
function2.SetParNames("N","mu","sigma")
function3.SetParNames("C","B","A")
function2.SetParameters(1.3*norm,    1,  0.4)  # start values to help fit
function3.SetParameters(-3*norm,4*norm,-norm)  # start values to help fit
function2.SetParLimits(0, 0.2*norm,  1.5*norm) # set limits on parameter 1
function3.SetParLimits(1, 0.5*norm, 10.0*norm) # set limits on parameter 1
function3.SetParLimits(2,-1.4*norm, -0.6*norm) # set limits on parameter 2

print ">>> fit and draw..."
canvas = TCanvas("canvas","canvas",100,100,800,600)
function2.SetLineColor(kRed)
function3.SetLineColor(kBlue)
function2.SetLineWidth(2)
function3.SetLineWidth(2)
hist.SetLineColor(kBlack)
hist.SetMarkerSize(0.6)
hist.SetMarkerStyle(8)
hist.Draw("E1")
hist.Fit("f2","B")           # "B" to override default limits values
hist.Fit(function3,"B+","",  # use + to add second fit function to histogram
                    1.1,2.9) # fit for subrange
hist.Fit("gaus","B+")        # default gaussian
function4 = hist.GetFunction("gaus")
function4.SetLineColor(kGreen)
function4.SetLineStyle(6)
function4.SetLineWidth(2)
legend = TLegend(0.6,0.6,0.8,0.42)
legend.SetTextSize(0.032)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(hist,"data",'LEP')
legend.AddEntry(function2,"custom gaussian",'L')
legend.AddEntry(function4,"default gaussian",'L')
legend.AddEntry(function3,"polynomial",'L')
legend.Draw()
canvas.SaveAs("fit.png")

