#! /usr/bin/env python
# Author: Izaak Neutelings (January 2018)
#
# Copy file:
#  https://root.cern.ch/doc/master/classTFile.html#aaf0edbf57091f9d941caf134f1207156
#
# Poisson errors:
#  https://twiki.cern.ch/twiki/bin/view/CMS/StatisticsCommittee
#  https://github.com/DESY-CMS-SUS/cmgtools-lite/blob/8_0_25/TTHAnalysis/python/plotter/mcPlots.py#L70-L102
#  https://github.com/DESY-CMS-SUS/cmgtools-lite/blob/8_0_25/TTHAnalysis/python/plotter/susy-1lep/RcsDevel/plotDataPredictWithSyst.py#L12-L21
#  https://root.cern.ch/doc/master/TH1_8cxx_source.html#l08344

import sys, os
import re
from argparse import ArgumentParser
import ROOT
from ROOT import gPad, gROOT, gStyle, TFile, TVectorD, Math, Double,\
                 TCanvas, TLegend, TLatex, TText,\
                 TH1D, TH1F, TH2F, THStack, TF1, TGraph, TGraphErrors, TGraphAsymmErrors,\
                 kBlack, kRed, kBlue, kAzure, kGreen, kGreen, kYellow, kOrange, kMagenta, kViolet,\
                 kSolid, kDashed, kDotted, kDashDotted
from math import sqrt, log, floor, ceil
ROOT.gROOT.SetBatch(ROOT.kTRUE)
gStyle.SetOptStat(0)

argv = sys.argv
description = '''This script runs combine on data cards, extracts limits from the output and plot them.'''
parser = ArgumentParser(prog="plotLimits",description=description,epilog="Succes!")
parser.add_argument( "-v", "--verbose", dest="verbose", default=False, action='store_true',
                     help="set verbose" )
parser.add_argument( "-f", "--force", dest="force", default=False, action='store_true',
                     help="force overwriting of existing files" )
args = parser.parse_args()

# PLOT OPTIONS
IN_DIR      = "./datacard"
OUT_DIR     = IN_DIR
DIR         = "./output" #"/shome/ineuteli/analysis/CMSSW_7_4_8/src/CombineHarvester/LowMassTauTau/output"
mylabel     = "_Moriond" # ICHEP
force       = args.force
verbosity   = 1*args.verbose

colors = [ kRed+2, kAzure+5, kOrange-5, kGreen+2, kMagenta+2, kYellow+2,
           kRed-7, kAzure-4, kOrange+6, kGreen-2, kMagenta-3, kYellow-2 ] #kViolet
styles = [ kSolid, kDashed, kDashDotted, ] #kDotted



# CHECK Poisson errors
def checkDataPoissonErrors():
    '''Check on behaviour of Poisson errors in histograms.'''
    
    N       = 150
    hist1   = TH1D("data1","kPoisson",N,0,N)
    hist2   = TH1D("data2","#chi^{2} quantile",N,0,N)
    
    for i in xrange(0,N+2):
        y = max(0,i-1) 
        hist1.SetBinContent(i,y)
        hist2.SetBinContent(i,y)
    
    table   = [ ]
    header  = "%22s  %14s  %14s  %14s\n>>>  " % (" ","default".center(14),"kPoisson".center(14),"custom".center(14))
    header += "%4s %7s  %7s   %6s %6s   %6s %6s   %6s %6s" % ("bin","content","sqrt(N)","errLow","errUp","errLow","errUp","errLow","errUp")
    table.append(header)
    
    # FILL table with default errors
    for i in xrange(1,N+1):
        y = hist1.GetBinContent(i)
        table.append("%4d %5d    %7.2f   %6.2f %6.2f"%(
          i,y,sqrt(y),hist1.GetBinErrorLow(i),hist1.GetBinErrorUp(i)))
    
    # GET data Possoin errors
    graph1 = getDataPoissonErrors(hist1,drawZeroBins=True,centerBin=False,kPoisson=True)
    graph2 = getDataPoissonErrors(hist2,drawZeroBins=True,centerBin=False,kPoisson=False)
    
    # FILL table with kPoisson, chi-squared
    for i in xrange(0,N):
        table[i+1] += "   %6.2f %6.2f   %6.2f %6.2f"%(
          graph1.GetErrorYlow(i),graph1.GetErrorYhigh(i),graph2.GetErrorYlow(i),graph2.GetErrorYhigh(i))
    
    # PRINT table
    for line in table:
        print ">>> " + line
    print ">>> "
    
    # GRAPHS
    function = TF1("function1","sqrt(x)",0,N)
    function.SetTitle("#sqrt{N}")
    graphElow1, graphEup1 = makeErrorGraph(graph1)
    graphElow2, graphEup2 = makeErrorGraph(graph2)
    graphElow2.SetTitle("N-[1-F^{-1}_{#chi^{2}}(1-#alpha,2N)]/2")
    graphEup2.SetTitle("[1-F^{-1}_{#chi^{2}}(#alpha,2(N-1))]/2-N")
    graphs   = [function, graphElow1, graphEup1, graphElow2, graphEup2]
    
    # DRAW settings
    W, H = 800, 800
    T, B = 0.04*H, 0.14*H
    L, R = 0.12*W, 0.04*W
    ymax   = function.GetMaximum()*1.16
    width  = 0.25
    legendTextSize = 0.045
    height = 0.066 + len(graphs)*0.066
    x2 = 0.80; x1 = x2 - width
    y1 = 0.16; y2 = y1 + height
    
    # MAIN plot
    canvas = TCanvas("canvas","canvas",100,100,W,H)
    canvas.Divide(2)
    canvas.cd(1)
    gPad.SetPad("pad1","pad1",0,0.37,1,1,0,-1,0)
    gPad.SetTopMargin(  T/H ); gPad.SetBottomMargin( 0.01 )
    gPad.SetLeftMargin( L/W ); gPad.SetRightMargin(  R/W  )
    gPad.SetTickx(0)
    gPad.SetTicky(0)
    gPad.SetGrid()
    
    frame = gPad.DrawFrame(0,0,N,ymax)
    frame.GetYaxis().SetTitleSize(0.055)
    frame.GetXaxis().SetTitleSize(0.058)
    frame.GetXaxis().SetLabelSize(0.050*0)
    frame.GetYaxis().SetLabelSize(0.053)
    frame.GetXaxis().SetLabelOffset(0.012)
    frame.GetXaxis().SetTitleOffset(1.02)
    frame.GetYaxis().SetTitleOffset(1.08)
    frame.GetXaxis().SetNdivisions(505)
    frame.GetXaxis().SetTitle("number of events")
    frame.GetYaxis().SetTitle("error on number of events")
    legend = TLegend(x1,y1,x2,y2)
    
    colors = [ kRed, kBlue, kViolet, kYellow, kGreen ]
    style = kSolid
    for i, graph in enumerate(graphs):
        if i>2: style = kDashed
        graph.SetLineColor(colors[i%len(colors)])
        graph.SetLineStyle(style)
        graph.SetLineWidth(2)
        graph.Draw('L SAME')
        legend.AddEntry(graph,graph.GetTitle(),'L')
    
    gPad.SetTicks(1,1)
    gPad.Modified()
    frame.Draw('SAME AXIS')
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)
    legend.SetTextFont(62)
    legend.SetHeader("method")
    legend.SetTextFont(42)
    legend.Draw()
    
    # RATIO plot
    canvas.cd(2)
    gPad.SetPad("pad2","pad2",0,0,1,0.36,0,-1,0)
    gPad.SetTopMargin(  0.05 ); gPad.SetBottomMargin( 0.24 )
    gPad.SetLeftMargin( L/W  ); gPad.SetRightMargin(  R/W  )
    
    frame_ratio = gPad.DrawFrame(0,0.50,N,1.50)
    frame_ratio.GetYaxis().CenterTitle()
    frame_ratio.GetYaxis().SetTitleSize(0.055*1.79)
    frame_ratio.GetXaxis().SetTitleSize(0.058*1.79)
    frame_ratio.GetXaxis().SetLabelSize(0.052*1.79)
    frame_ratio.GetYaxis().SetLabelSize(0.050*1.79)
    frame_ratio.GetXaxis().SetLabelOffset(0.012)
    frame_ratio.GetXaxis().SetTitleOffset(1.00)
    frame_ratio.GetYaxis().SetTitleOffset(0.63)
    frame_ratio.GetXaxis().SetNdivisions(508)
    frame_ratio.GetYaxis().CenterTitle(True)
    frame_ratio.GetYaxis().SetTitle("ratio")
    frame_ratio.GetXaxis().SetTitle("number of events N")
    frame_ratio.GetYaxis().SetNdivisions(5)
    
    ratios = [ ]
    graphf = makeGraphFromTF1(function,N)
    for i, graph in enumerate(graphs):
        if isinstance(graph,TF1): graph = makeGraphFromTF1(graph,N)
        ratio = makeRatioTGraphs(graph,graphf)
        ratio.SetLineColor(graph.GetLineColor())
        ratio.SetLineStyle(graph.GetLineStyle())
        ratio.SetLineWidth(graph.GetLineWidth())
        ratio.Draw('L SAME')
        ratios.append(ratio)
    
    gPad.SetTicks(1,1)
    gPad.Modified()
    frame_ratio.Draw('sameaxis')
    
    canvas.SaveAs("PoissonError.png")
    canvas.Close()
    


# MAKE graph
def makeErrorGraph(graph):
    '''Make graphs of the low and high error of a given graph.'''
    N = graph.GetN()
    graphElow = TGraph(N)
    graphEup  = TGraph(N)
    graphElow.SetName(  graph.GetName() +"_graphElow"  )
    graphEup.SetName(   graph.GetName() +"_graphEup"   )
    graphElow.SetTitle( graph.GetTitle()+" low error"  )
    graphEup.SetTitle(  graph.GetTitle()+" high error" )
    for i in xrange(0,N):
        x, y = Double(), Double()
        graph.GetPoint(i,x,y)
        graphElow.SetPoint( i, x, graph.GetErrorYlow(i)  )
        graphEup.SetPoint(  i, x, graph.GetErrorYhigh(i) )
    graphElow.SetLineWidth(graph.GetLineWidth())
    graphEup.SetLineWidth(graph.GetLineWidth())
    graphElow.SetLineColor(graph.GetLineColor())
    graphEup.SetLineColor(graph.GetLineColor())
    graphElow.SetLineStyle(graph.GetLineStyle())
    graphEup.SetLineStyle(graph.GetLineStyle())
    graphElow.SetMarkerSize(graph.GetMarkerSize())
    graphEup.SetMarkerSize(graph.GetMarkerSize())
    graphElow.SetMarkerColor(graph.GetMarkerColor())
    graphEup.SetMarkerColor(graph.GetMarkerColor())
    graphElow.SetMarkerStyle(graph.GetMarkerStyle())
    graphEup.SetMarkerStyle(graph.GetMarkerStyle())
    return [ graphElow, graphEup ]
    


# MAKE graph
def makeGraphFromTF1(function,N):
    '''Make graphs from a given function.'''
    a, b  = function.GetXmin(), function.GetXmax()
    graph = TGraph(N)
    graph.SetName(  function.GetName() +"_function"  )
    graph.SetTitle( function.GetTitle() )
    for i in xrange(0,N):
        x = a + i*float(b-a)/N
        y = function.Eval(x)
        graph.SetPoint(i,x,y)
    graph.SetLineWidth(function.GetLineWidth())
    graph.SetLineColor(function.GetLineColor())
    graph.SetLineStyle(function.GetLineStyle())
    graph.SetMarkerSize(function.GetMarkerSize())
    graph.SetMarkerColor(function.GetMarkerColor())
    graph.SetMarkerStyle(function.GetMarkerStyle())
    return graph
    


# MAKE ratio
def makeRatioTGraphs(graph0,graph1,**kwargs):
    """Make a ratio of two TGraphs bin by bin."""
    
    # SETTINGS
    verbose     = kwargs.get('verbose',False)    
    N           = graph0.GetN()
    x0, y0      = Double(), Double()
    x1, y1      = Double(), Double()
    graph_ratio = TGraph()
    
    # CHECK binning hist1
    N1 = graph1.GetN()
    if N != N1:
      print ">>> Warning! makeRatioTGraphs: different number of points: %d != %d!"%(N,N1)
      exit(1)
    
    if verbose:
      print ">>> %3s  %9s %9s %9s %9s %9s"%("i","x0","x1","y0","y1","ratio")
    
    # CALCULATE ratio bin-by-bin
    for i in range(0,N):
        graph0.GetPoint(i,x0,y0)
        graph1.GetPoint(i,x1,y1)
        if x0!=x1:
          print ">>> Warning! makeRatioTGraphs: graphs' points %i have different x values: %.2f vs. %.2f !"%(i,x0,x1)
          exit(0)
        ratio = 0
        if y1:          ratio = y0/y1
        elif y0==y1:    ratio = 1.0
        elif y0>100*y1: ratio = 100.0
        graph_ratio.SetPoint( i, x0, ratio )
        if verbose:
          print ">>> %3s  %9.3f %9.3f %9.3f %9.3f %9.3f"%(i,x0,x1,y0,y1,ratio)
    
    return graph_ratio
    


# GET Poisson Errors
def getDataPoissonErrors(hist, kPoisson=False, drawZeroBins=False, drawXbars=False, centerBin=True):
    '''Make data poisson errors for a histogram with two different methods:
       - TH1.kPoisson
       - chi-squared quantile   
    '''
    # https://github.com/DESY-CMS-SUS/cmgtools-lite/blob/8_0_25/TTHAnalysis/python/plotter/mcPlots.py#L70-L102
    # https://github.com/DESY-CMS-SUS/cmgtools-lite/blob/8_0_25/TTHAnalysis/python/plotter/susy-1lep/RcsDevel/plotDataPredictWithSyst.py#L12-L21
    
    if kPoisson: hist.SetBinErrorOption(TH1D.kPoisson)
    
    Nbins   = hist.GetNbinsX()
    xaxis   = hist.GetXaxis()
    alpha   = (1-0.6827)/2.
    
    graph = TGraphAsymmErrors(Nbins)
    graph.SetName(hist.GetName()+"_graph")
    graph.SetTitle(hist.GetTitle())
    for i in xrange(1,Nbins+1):
        N  = hist.GetBinContent(i)
        if N<=0 and not drawZeroBins: continue
        dN = hist.GetBinError(i)
        yscale = 1
        if centerBin:
            x = xaxis.GetBinCenter(i)
        else:
            x = xaxis.GetBinLowEdge(i)
        if N>0 and dN>0 and abs(dN**2/N-1)>1e-4: # check is error is Poisson
            yscale = (dN**2/N)
            N = (N/dN)**2
        if kPoisson:
            EYlow = hist.GetBinErrorLow(i)
            EYup  = hist.GetBinErrorUp(i)
        else:
            EYlow = (N-Math.chisquared_quantile_c(1-alpha,2*N)/2.) if N>0 else 0
            EYup  = Math.chisquared_quantile_c(alpha,2*(N+1))/2.-N
        y      = yscale*N 
        EXup   = xaxis.GetBinUpEdge(i)-x  if drawXbars else 0
        EXlow  = x-xaxis.GetBinLowEdge(i) if drawXbars else 0
        graph.SetPoint(i-1,x,y)
        graph.SetPointError(i-1,EXlow,EXup,EYlow,EYup)
        #print ">>> getDataPoissonErrors - bin %2d: (x,y) = ( %3.1f - %4.2f + %4.2f, %4.2f - %4.2f + %4.2f )"%(i,x,EXlow,EXup,y,EYlow,EYup)
    graph.SetLineWidth(hist.GetLineWidth())
    graph.SetLineColor(hist.GetLineColor())
    graph.SetLineStyle(hist.GetLineStyle())
    graph.SetMarkerSize(hist.GetMarkerSize())
    graph.SetMarkerColor(hist.GetMarkerColor())
    graph.SetMarkerStyle(hist.GetMarkerStyle())
    return graph
    


# MAIN
def main():
    print ""
    
    checkDataPoissonErrors()
    


if __name__ == '__main__':
    main()
    print ">>>\n>>> done\n"
    

