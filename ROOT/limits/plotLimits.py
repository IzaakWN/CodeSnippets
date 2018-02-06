#!/usr/bin/env python
# https://wiki.physik.uzh.ch/cms/limits:brazilianplotexample

import sys, os
import re
from argparse import ArgumentParser
import subprocess
import PlotTools.CMS_lumi as CMS_lumi
import PlotTools.tdrstyle as tdrstyle
from PlotTools.PrintTools import color
import numpy as np
from array import array
import ROOT
from ROOT import gPad, gROOT, gStyle, TFile, TVectorD, Double,\
                 TCanvas, TLegend, TLatex, TText,\
                 TH1F, TH2F, THStack, TF1, TGraph, TGraphErrors, TGraphAsymmErrors,\
                 kBlack, kRed, kBlue, kAzure, kGreen, kGreen, kYellow, kOrange, kMagenta, kViolet,\
                 kSolid, kDashed, kDotted, kDashDotted
from math import log, floor, ceil
ROOT.gROOT.SetBatch(ROOT.kTRUE)
gStyle.SetOptStat(0)

argv = sys.argv
description = '''This script runs combine on data cards, extracts limits from the output and plot them.'''
parser = ArgumentParser(prog="plotLimits",description=description,epilog="Succes!")
# parser.add_argument( "-S", "--S_exp", dest="S_exp", default=-1, type=int, action='store',
#                      metavar="CHANNEL", help="run only for this channel" )
parser.add_argument( "-e", "--etau", dest="etau", default=False, action='store_true',
                     help="run only for the etau channel" )
parser.add_argument( "-m", "--mutau", dest="mutau", default=False, action='store_true',
                     help="run only for the mutau channel" )
args = parser.parse_args()

# PLOT OPTIONS
DIR                 = "./output" #"/shome/ineuteli/analysis/CMSSW_7_4_8/src/CombineHarvester/LowMassTauTau/output"
PLOTS_DIR            = "./plots"
mylabel             = "_Moriond" # ICHEP
verbosity           = 1

# CMS style
lumi = 35.9 #12.9
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Preliminary"
CMS_lumi.cmsTextSize  = 0.65
CMS_lumi.lumiTextSize = 0.60
CMS_lumi.relPosX = 0.105
CMS_lumi.outOfFrame = True
CMS_lumi.lumi_13TeV = "%s fb^{-1}" % lumi
tdrstyle.setTDRStyle()

colors = [ kBlack,
           kRed+2, kAzure+5, kOrange-5, kGreen+2, kMagenta+2, kYellow+2,
           kRed-7, kAzure-4, kOrange+6, kGreen-2, kMagenta-3, kYellow-2 ] #kViolet
styles = [ kSolid, kDashed, kDashDotted, ] #kDotted

label_dict = {
    'mt-1': "#mu#tau: 1b1f",
    'mt-2': "#mu#tau: 1b1c",
    'et-1': "e#tau: 1b1f",
    'et-2': "e#tau: 1b1c",
    'em-1': "e#mu: 1b1f",
    'em-2': "e#mu: 1b1c",
    'combined': "combined",
    'mt-1_bbA': "#mu#tau: 1 b tag",
    'et-1_bbA': "e#tau: 1 b tag",
    'mt-1_bbA_Opt': "#mu#tau: 1 b tag, D_{#zeta}>-40, m_{T}<40",
    'et-1_bbA_Opt': "e#tau: 1 b tag, D_{#zeta}>-40, m_{T}<40",
    'combined_bbA': "combined: 1 b tag",
    'combined_bbA_Opt': "combined: 1 b tag, D_{#zeta}>-40, m_{T}<40",
}
label_dict_split = {
    'mt-1': "#splitline{ #mu#tau}{1b1f}",
    'mt-2': "#splitline{ #mu#tau}{1b1c}",
    'et-1': "#splitline{  e#tau}{1b1f}",
    'et-2': "#splitline{  e#tau}{1b1c}",
    'em-1': "#splitline{  e#mu}{1b1f}",
    'em-2': "#splitline{  e#mu}{1b1c}",
    'combined': "combined",
    'mt-1_Opt': "#splitline{  #splitline{ #mu#tau}{1b1f}}{opt}",
    'mt-2_Opt': "#splitline{  #splitline{ #mu#tau}{1b1f}}{opt}",
    'mt-1_noOpt': "#splitline{  #splitline{ #mu#tau}{1b1f}}{no opt}",
    'mt-2_noOpt': "#splitline{  #splitline{ #mu#tau}{1b1f}}{no opt}",
}

# number of MC events, for normalization:
N_tot = 1998200 #497595
# MC_dict = { 'et-1' : 166,
#             'et-2' : 257,
#             'mt-1' : 493,
#             'mt-2' : 818,
#             'em-1' : 194,
#             'em-2' : 322, }
# MC_dict["combined"] = sum([v for k,v in MC_dict.iteritems()])
ymax = 25





# GET OUTPUT FILENAME
def getOutputFilename(label,mass,**kwargs):
    '''Get formatted output filename.'''
    verbosity       = kwargs.get('verbosity',0)
    DATACARD_DIR    = kwargs.get('DIR',DIR)
    method          = kwargs.get('method',"Asymptotic")
    extralabel      = kwargs.get('extralabel',"")
    filename = "%s/higgsCombine.%s%s.%s.mH%s.root" % (DIR,label,extralabel,method,mass)
    if verbosity>0: print ">>>   getFilename: %s" % (filename) 
    return filename





# EXECUTE datacards
def executeDataCards(labels,**kwargs):
    '''Run combine tool with datacard.'''
    if not isinstance(labels,list): labels = [labels]
    mass        = kwargs.get('mass',28)
    dir         = kwargs.get('DIR',".")
    masses      = kwargs.get('masses',[mass])
    bins        = kwargs.get('bins',[ ])
    method      = kwargs.get('method',"Asymptotic")
    options     = kwargs.get('options',"-t -1")
    extralabel  = kwargs.get('extralabel',"")
    
    for mass in masses:
        for label in labels:
            datacard = "%s/xtt_%s-13TeV-%s.txt" % (dir,label,mass)
            combine_command = "cd output && combine -M %s -m %s -n .%s%s %s %s" % (method,mass,label,extralabel,datacard,options) # --expectSignal=%s
            print color(combine_command,color="magenta",prepend="\n>>> ")
            p = subprocess.Popen(combine_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines(): print line.rstrip("\n")
            print ">>> higgsCombine.%s.%s.mH%s.root created" % (label,method,mass)
            retval = p.wait() # wait for child process to terminate

            



# EXECUTE datacards
def executeDataCardsPValue(labels,**kwargs):
    '''Run combine tool with datacard to calculate the p-value.'''
    # https://raw.githubusercontent.com/nucleosynthesis/HiggsAnalysis-CombinedLimit/combine_tutorial_SWAN/combine_tutorials_2016/combine_intro/run_hgg_pvalue.sh
    oldmethod       = kwargs.get('method',"ProfileLikelihood")
    oldoptions      = kwargs.get('options',"")
    oldextralabel   = kwargs.get('extralabel',"")
    dir             = kwargs.get('DIR',".")
    kwargs["method"] = "ProfileLikelihood"
    for label in labels:
        # expected
        kwargs["extralabel"] = oldextralabel + ".SignifExp"
        kwargs["options"]    = "--signif --expectSignal=1 --pvalue -t -1"
        executeDataCards(label,**kwargs)
        # observed
        kwargs["extralabel"] = oldextralabel + ".SignifObs"
        kwargs["options"]    = "--signif --pvalue"
        executeDataCards(label,**kwargs)
        




# GET LIMITS from datacards
def getLimits(filename,**kwargs):
    '''Get limits from file.'''
    brazilian   = kwargs.get('brazilian',True)
    scale       = kwargs.get('scale',1)
    file        = TFile(filename)
    tree        = file.Get("limit")
    limits      = [ ]
    if brazilian:
        for quantile in tree: limits.append(tree.limit * scale)
        print ">>>   %s: %s" % (filename.replace(DIR+"/",""),["%.2f"%l for l in limits])
        return limits[:6]
    else:
        tree.GetEntry(0)
        limit = tree.limit*scale
        print ">>>   %s: %s" % (filename.replace(DIR+"/",""),"%.5f"%limit)
        return limit # for p-value
    




# PLOT boxes
def plotBoxes(labels,**kwargs):
    '''Plot boxes.'''
    print color("plotBoxes()",color="magenta",prepend=">>>\n>>> ")
    # https://wiki.physik.uzh.ch/cms/limits:brazilianplotexample
    # https://root.cern.ch/doc/master/classTHistPainter.html#HP07
    # text label https://root.cern.ch/root/roottalk/roottalk98/0616.html
    #            https://root.cern.ch/phpBB3/viewtopic.php?t=18534
    #            https://root.cern.ch/doc/master/classTGaxis.html#GA10a
    # boxes https://root.cern.ch/doc/master/classTGraphPainter.html#GP03b
    
    # MASS
    mass    = kwargs.get('mass',28)
    green   = TGraphAsymmErrors()
    yellow  = TGraphAsymmErrors()
    limit   = TGraphAsymmErrors()
    labels  = labels[::-1] # reverse order: top to bottom
    width   = 0.2
    
    (down,up)   = (1000,0)
    labels      = [ "mt-2",   "mt-2", "mt-1",   "mt-1", ]
    extralabels = [ "_noOpt", "_Opt", "_noOpt", "_Opt", ]
    for i, (label,extralabel) in enumerate(zip(labels,extralabels)):        
        filename = getOutputFilename(label,mass,extralabel=extralabel)
        limits   = getLimits(filename)
        limit.SetPoint(  i,limits[2],i+1 )
        green.SetPoint(  i,limits[2],i+1 ) # -/+ 1 sigma
        yellow.SetPoint( i,limits[2],i+1 ) # -/+ 2 sigma
        limit.SetPointError(  i,                  0,                  0,width,width ) # -/+ 1 sigma
        green.SetPointError(  i,limits[2]-limits[1],limits[3]-limits[2],width,width ) # -/+ 1 sigma
        yellow.SetPointError( i,limits[2]-limits[0],limits[4]-limits[2],width,width ) # -/+ 2 sigma
        if down > limits[0]: down = limits[0]
        if   up < limits[4]: up   = limits[4]
    labels  = [ "mt-2_label", "mt-2", "mt-1_label", "mt-1", ]
    
    N       = len(labels)
    canvas  = TCanvas("canvas","canvas",100,100,800,600)
    canvas.SetTopMargin(0.08)
    canvas.SetBottomMargin(0.12)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.04)
    canvas.SetGrid(1,0)
    #canvas.SetTicks(1,0)
    #canvas.SetLogx()
    green.SetFillColor(kGreen+1)
    yellow.SetFillColor(kOrange)
    limit.SetLineWidth(2)
    
    frame = TH2F("frame","frame",200,down-(up*0.1),up*1.1,2*(N+1),0,N+1) #canvas.DrawFrame(0.001,0,10,N+1)
    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetLabelSize(0.0)#8)
    frame.GetXaxis().SetLabelSize(0.045)
    frame.GetXaxis().SetTitleOffset(1.14)
    frame.GetYaxis().SetNdivisions(N+1,0,0,False) # ndiv = N1 + 100*N2 + 10000*N3
    #frame.GetXaxis().CenterTitle(True)
    xtitle = "95% upper limit on #sigma#timesBR(X#rightarrow#tau#tau) [pb]"
    frame.GetXaxis().SetTitle(xtitle)
    
    #frame.GetXaxis().SetRangeUser(0,up*1.10)
    #frame.SetMinimum(0)
    #frame.SetMaximum(up*1.10) #ymax)
    #frame.GetYaxis().SetLimits(0,N+1)
    frame.Draw("AXIS")
    yellow.Draw("2 SAME")
    green.Draw("2 SAME")
    limit.Draw("P SAME")
    
    labelfontsize = 0.042
    text = TLatex()
    text.SetTextSize(labelfontsize)
    text.SetTextAlign(23)
    text.SetTextFont(42)
    
    #labelfontwidth = labelfontsize*stringWidth(*[label_dict_split[k] for k in label_dict_split])
    #xtext = frame.GetXaxis().GetXmin()-frame.GetXaxis().GetXmax()*0.04 # manual
    xtext = marginCenter(canvas,frame.GetXaxis()) # automatic
    for i, label in enumerate(labels):
        bin = frame.GetYaxis().FindBin(i+1)
        ytext = frame.GetYaxis().GetBinCenter(bin)
        #print "(x,y)=(%s,%s)"%(xtext,ytext)
        text.DrawLatex(xtext,ytext,label_dict_split[label]+"  ")
        # limit.GetYaxis().SetBinLabel(bin-1,label_dict_split[label])
    
    #frame.GetYaxis().LabelsOption('H') # draw horizontal
    #gPad.Modified()
    #gPad.Update()
    CMS_lumi.CMS_lumi(canvas,13,0)
    
    print " "
    canvas.SaveAs("%s/upperLimitBoxes.png" % (PLOTS_DIR))
    canvas.SaveAs("%s/upperLimitBoxes.pdf" % (PLOTS_DIR))
    canvas.Close()
    




# PLOT upper limits
def plotUpperLimits(labels,masses,**kwargs):
    print color("plotUpperLimits()",color="magenta",prepend=">>>\n>>> ")
    # https://raw.githubusercontent.com/nucleosynthesis/HiggsAnalysis-CombinedLimit/combine_tutorial_SWAN/combine_tutorials_2016/combine_intro/plotPvalue.py
    
    # SIGNAL strength & mass
    extralabel = kwargs.get('extralabel',"")
    
    # LOOP over LABELS
    for label in labels:
        print color("plotUpperLimits - %s" % (label),color="grey",prepend="\n>>> ")
        
        N       = len(masses)
        yellow  = TGraph(2*N)    # yellow band
        green   = TGraph(2*N)    # green band
        median  = TGraph(N)      # median line
        
        up2s    = [ ]
        down2s  = [ ]
        for i, mass in enumerate(masses):
            filename = getOutputFilename(label,mass,extralabel=extralabel)
            limits   = getLimits(filename)
            yellow.SetPoint(    i,    mass, limits[4] ) # + 2 sigma
            green.SetPoint(     i,    mass, limits[3] ) # + 1 sigma
            median.SetPoint(    i,    mass, limits[2] ) # median
            green.SetPoint(  2*N-1-i, mass, limits[1] ) # - 1 sigma
            yellow.SetPoint( 2*N-1-i, mass, limits[0] ) # - 2 sigma
            down2s.append(limits[0])
            up2s.append(limits[4])
        
        ymax    = max(up2s)*1.20
        ymin    = min(down2s)
        doLog   = ymin and ymax/min(down2s)>4
        xtitle  = "m_{X} [GeV]"
        ytitle  = "95% upper limit on #sigma#timesBR(X #rightarrow #tau#tau) [pb]"
        if "bbA" in extralabel:
          xtitle = "m_{A} [GeV]"
          ytitle = "95% upper limit on #sigma#timesBR(A #rightarrow #tau#tau) [pb]"
        
        W, H = 800, 600
        T, B = 0.08*H, 0.12*H
        L, R = 0.12*W, 0.04*W
        canvas = TCanvas("canvas","canvas",100,100,W,H)
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetTopMargin(  T/H ); canvas.SetBottomMargin( B/H )
        canvas.SetLeftMargin( L/W ); canvas.SetRightMargin(  R/W )
        canvas.SetTickx(0)
        canvas.SetTicky(0)
        canvas.SetGrid()
        canvas.cd()
        if doLog:
          ymin = 0.1  #10**(floor(log(ymin,10))-1)
          ymax = 1000 #10**(ceil(log(ymax,10))+1)
          #ymin, ymax = 0.1, 1000
          canvas.SetLogy()
        else:
          ymin *= 0 if ymin>0 else 1.20
        
        frame = canvas.DrawFrame(min(masses),ymin,max(masses),ymax)
        frame.GetYaxis().SetTitleSize(0.055)
        frame.GetXaxis().SetTitleSize(0.055)
        frame.GetXaxis().SetLabelSize(0.044)
        frame.GetYaxis().SetLabelSize(0.044)
        frame.GetXaxis().SetLabelOffset(0.010)
        frame.GetXaxis().SetTitleOffset(1.04)
        frame.GetYaxis().SetTitleOffset(1.08)
        frame.GetXaxis().SetNdivisions(508)
        frame.GetYaxis().CenterTitle(True)
        frame.GetYaxis().SetTitle(ytitle)
        frame.GetXaxis().SetTitle(xtitle)
        
        yellow.SetFillColor(kOrange)
        yellow.SetLineColor(kOrange)
        yellow.SetFillStyle(1001)
        yellow.Draw('F')
        
        green.SetFillColor(kGreen+1)
        green.SetLineColor(kGreen+1)
        green.SetFillStyle(1001)
        green.Draw('Fsame')
        
        median.SetLineColor(1)
        median.SetLineWidth(2)
        median.SetLineStyle(2)
        median.Draw('Lsame')
        
        CMS_lumi.CMS_lumi(canvas,13,0)
        gPad.SetTicks(1,1)
        gPad.Modified()
        frame.Draw('sameaxis')
        
        width  = 0.28
        height = 0.20
        #x1 = 0.16; x2 = x1 + width # Left
        x2 = 0.80; x1 = x2 - width # Right
        x2 = x1 + width
        
        y1 = 0.68
        y2 = y1 + height
        legend = TLegend(x1,y1,x2,y2)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.040)
        legend.SetTextFont(62)
        legend.SetHeader("%s" % (label_dict[label+extralabel]))
        legend.SetTextFont(42)
        legend.AddEntry(median, "Asymptotic CL_{s} expected",'L')
        legend.AddEntry(green,  "#pm 1 std. deviation",'f')
        #legend.AddEntry(green, "Asymptotic CL_{s} #pm 1 std. deviation",'f')
        legend.AddEntry(yellow, "#pm 2 std. deviation",'f')
        #legend.AddEntry(green, "Asymptotic CL_{s} #pm 2 std. deviation",'f')
        legend.Draw()
        
        print " "
        canvas.SaveAs("%s/upperLimit-%s%s.png" % (PLOTS_DIR,label,extralabel))
        canvas.SaveAs("%s/upperLimit-%s%s%s.pdf" % (PLOTS_DIR,label,extralabel))
        canvas.Close()
    




# COMPARE upper limits
def compareUpperLimits(labels,masses,filelabels,**kwargs):
    print color("compareUpperLimits()",color="magenta",prepend=">>>\n>>> ")
    
    # SIGNAL strength & mass
    extralabel = kwargs.get('extralabel',"")
    plotlabel  = kwargs.get('plotlabel',"")
    
    # LOOP over LABELS
    for label in labels:
      print color("plotUpperLimits - %s" % (label),color="grey",prepend="\n>>> ")
      
      ymax    = -99999
      ymin    =  99999
      medians = [ ]
      
      for filelabel, title in filelabels:
          N      = len(masses)
          median = TGraph(N) # median line
          median.SetTitle(title)
          medians.append(median)
          for i, mass in enumerate(masses):
              filename = getOutputFilename(label,mass,extralabel=filelabel)
              limits   = getLimits(filename)
              median.SetPoint( i, mass, limits[2] ) # median
              if limits[2]>ymax: ymax = limits[2]
              if limits[2]<ymin: ymin = limits[2]
      
      median0 = medians[0]
      doLog   = ymin and ymax/ymin>6
      ymax    = ymax*1.40
      xtitle  = "m_{X} [GeV]"
      ytitle  = "95% upper limit on #sigma#timesBR(X #rightarrow #tau#tau) [pb]"
      if "bbA" in filelabels[0][0]:
        xtitle = "m_{A} [GeV]"
        ytitle = "95% upper limit on #sigma#timesBR(A #rightarrow #tau#tau) [pb]"
      
      W, H = 800, 800
      T, B = 0.10*H, 0.16*H
      L, R = 0.12*W, 0.04*W
      
      # MAIN plot
      canvas = TCanvas("canvas","canvas",100,100,W,H)
      canvas.Divide(2)
      canvas.cd(1)
      gPad.SetPad("pad1","pad1",0,0.37,1,1,0,-1,0)
      gPad.SetTopMargin(  T/H ); gPad.SetBottomMargin( 0.01 )
      gPad.SetLeftMargin( L/W ); gPad.SetRightMargin(  R/W )
      gPad.SetTickx(0)
      gPad.SetTicky(0)
      gPad.SetGrid()
      if doLog:
        ymin = 10**(floor(log(ymin,10)))
        ymax = 10**(ceil(log(ymax,10)))
        gPad.SetLogy()
      else:
        ymin *= 0 if ymin>0 else 1.20
      
      width  = 0.25
      height = 0.05+len(medians)*0.05
      #x1 = 0.16; x2 = x1 + width # Left
      x2 = 0.70; x1 = x2 - width # Right
      x2 = x1 + width
      y1 = 0.86
      y2 = y1 - height
      legend = TLegend(x1,y1,x2,y2)
      
      frame = gPad.DrawFrame(min(masses),ymin,max(masses),ymax)
      frame.GetYaxis().CenterTitle()
      frame.GetYaxis().SetTitleSize(0.055)
      frame.GetXaxis().SetTitleSize(0.058)
      frame.GetXaxis().SetLabelSize(0.050*0)
      frame.GetYaxis().SetLabelSize(0.053)
      frame.GetXaxis().SetLabelOffset(0.012)
      frame.GetXaxis().SetTitleOffset(1.02)
      frame.GetYaxis().SetTitleOffset(1.08)
      frame.GetXaxis().SetNdivisions(508)
      frame.GetYaxis().CenterTitle(True)
      frame.GetYaxis().SetTitle(ytitle)
      frame.GetXaxis().SetTitle(xtitle)
      
      option = 'L'
      for i, median in enumerate(medians):
          median.SetLineColor(colors[i%len(colors)])
          median.SetLineStyle(styles[i%len(styles)])
          median.SetLineWidth(2 if styles[i%len(styles)]!=kDotted else 3)
          median.Draw('L')
          legend.AddEntry(median, median.GetTitle(),'L')
          if i==0: option+=' SAME'
      
      CMS_lumi.CMS_lumi(gPad,13,0)
      gPad.SetTicks(1,1)
      gPad.Modified()
      frame.Draw('sameaxis')
      
      legend.SetFillStyle(0)
      legend.SetBorderSize(0)
      legend.SetTextSize(0.041)
      legend.SetTextFont(62)
      legend.SetHeader("%s" % (label_dict[label+extralabel]))
      legend.SetTextFont(42)
      legend.Draw()
      
      # RATIO plot
      canvas.cd(2)
      gPad.SetPad("pad2","pad2",0,0,1,0.36,0,-1,0)
      gPad.SetTopMargin(  0.05 ); gPad.SetBottomMargin( 0.24 )
      gPad.SetLeftMargin( L/W  ); gPad.SetRightMargin(  R/W  )
      
      frame_ratio = gPad.DrawFrame(min(masses),0.36,max(masses),1.20)
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
      frame_ratio.GetXaxis().SetTitle(xtitle)
      frame_ratio.GetYaxis().SetNdivisions(5)
      
      option = 'L'
      ratios = [ ]
      for i, median in enumerate(medians):
          ratio = makeRatioTGraphs(median,median0)
          ratio.SetLineColor(median.GetLineColor())
          ratio.SetLineStyle(median.GetLineStyle())
          ratio.SetLineWidth(median.GetLineWidth())
          ratio.Draw('L')
          ratios.append(ratio)
          if i==1: option+=' SAME'
        
      gPad.SetTicks(1,1)
      gPad.Modified()
      frame_ratio.Draw('sameaxis')
      
      print " "
      canvas.SaveAs("%s/upperLimit-%s%s_compare.png" % (PLOTS_DIR,label,plotlabel))
      canvas.SaveAs("%s/upperLimit-%s%s_compare.pdf" % (PLOTS_DIR,label,plotlabel))
      canvas.Close()



 
# PLOT p values
def plotPValues(labels,masses0,**kwargs):
    print color("plotPValues()",color="magenta",prepend=">>>\n>>> ")
    
    # SIGNAL strength & mass
    bins    = kwargs.get('bins',[ ])
    ymin    = 0.00005
    
    # LOOP over LABELS
    for label in labels:
        print color("plotPValues - %s" % (label),color="grey",prepend="\n>>> ")
        
        masses      = array('d',[ ])
        zeros       = array('d',[ ])
        limitObs    = array('d',[ ])
        limitExps = [ ]
                
        up2s    = [ ]
        for i, mass in enumerate(masses0):
            bin = -1
            if bins: bin = bins[i]
            filename = getOutputFilename(label,mass,method="ProfileLikelihood",bin=bin,extralabel=".SignifObs")
            limitObs.append(getLimits(filename,brazilian=False))
            masses.append(mass)
            zeros.append(0.0)
        
        v_masses    = TVectorD(len(masses),masses)
        v_zeros     = TVectorD(len(zeros),zeros)
        v_limitObs  = TVectorD(len(limitObs),limitObs)
        v_limitExps = [ ]
        for limitExp in limitExps:
            v_limitExps.append(TVectorD(len(limitExp),limitExp))
        
        W = 800
        H  = 600
        T = 0.08*H
        B = 0.12*H
        L = 0.12*W
        R = 0.04*W
        canvas = TCanvas("canvas","canvas",100,100,W,H)
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin( L/W )
        canvas.SetRightMargin( R/W )
        canvas.SetTopMargin( T/H )
        canvas.SetBottomMargin( B/H )
        canvas.SetTickx(0)
        canvas.SetTicky(0)
        canvas.SetGrid()
        canvas.SetLogy() # log
        canvas.cd()
        
        frame = canvas.DrawFrame(1.4,0.001, 4.1, 10)
        frame.GetYaxis().CenterTitle()
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetLabelSize(0.04)
        frame.GetYaxis().SetLabelSize(0.04)
        frame.GetYaxis().SetTitleOffset(1.14)
        frame.GetXaxis().SetNdivisions(508)
        frame.GetYaxis().CenterTitle(False)
        frame.GetYaxis().SetTitle("local p-value")
        #frame.GetYaxis().SetTitle("95% upper limit on #sigma / #sigma_{SM}")
        frame.GetXaxis().SetTitle("X#rightarrow#tau#tau mass [GeV]")
        frame.SetMinimum(ymin)
        frame.SetMaximum(1.5)
        frame.GetXaxis().SetLimits(min(masses),max(masses))
        
        latex = TLatex()
        latex.SetTextSize(0.4*canvas.GetTopMargin())
        latex.SetTextColor(2)
        f1 = TF1("f1","0.15866",min(masses),max(masses))
        f1.SetLineColor(2)
        f1.SetLineWidth(2)
        f1.Draw("lsame")
        latex.DrawLatex(min(masses)+1, 0.15866*1.1,"1#sigma")
        f2 = TF1("f2","0.02275",min(masses),max(masses))
        f2.SetLineColor(2)
        f2.SetLineWidth(2)
        f2.Draw("lsame")
        latex.DrawLatex(min(masses)+1, 0.02275*1.1,"2#sigma")
        f3 = TF1("f3","0.0013499",min(masses),max(masses))
        f3.SetLineColor(2)
        f3.SetLineWidth(2)
        f3.Draw("lsame")
        latex.DrawLatex(min(masses)+1, 0.0013499*1.1,"3#sigma")
        
        graph_limitExps = [ ]
        colors = [4,2,3,6,7,8]
        for i, v_limitExp in enumerate(v_limitExps):
            graph_limitExps.append(TGraphAsymmErrors(v_masses,v_limitExp,v_zeros,v_zeros,v_zeros,v_zeros))
            graph_limitExps[-1].SetLineColor(colors[i])
            graph_limitExps[-1].SetLineWidth(2)
            graph_limitExps[-1].SetLineStyle(2)
            graph_limitExps[-1].Draw("Lsame")
        
        graph_limitObs = TGraphAsymmErrors(v_masses,v_limitObs,v_zeros,v_zeros,v_zeros,v_zeros)
        graph_limitObs.SetLineColor(1)
        graph_limitObs.SetLineWidth(2)
        graph_limitObs.Draw("Csame")
        
        CMS_lumi.CMS_lumi(canvas,13,0)
        gPad.SetTicks(1,1)
        frame.Draw('sameaxis')
        
        x1 = 0.62
        x2 = x1 + 0.24
        y1 = 0.15
        y2 = y1 + 0.20
        legend = TLegend(x1,y1,x2,y2)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.041)
        legend.SetTextFont(42)
        legend.SetHeader("%s" % (label_dict[label]))
        legend.AddEntry(graph_limitObs, "observed",'L') #p-value
        legend.Draw("same")                                           
        gPad.RedrawAxis()
        
        print " "
        canvas.SaveAs("%s/p-value-local-%s.png" % (PLOTS_DIR,label))
        canvas.SaveAs("%s/p-value-local-%s.pdf" % (PLOTS_DIR,label))
        canvas.Close()



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
          print ">>> Warning! makeRatioTGraphs: graphs' %i points have different x values: %.2f vs. $.2f !"%(x0,x1)
          exit(0)
        ratio = 0
        if y1:          ratio = y0/y1
        elif y0==y1:    ratio = 1.0
        elif y0>100*y1: ratio = 100.0
        graph_ratio.SetPoint( i, x0, ratio )
        if verbose:
          print ">>> %3s  %9.3f %9.3f %9.3f %9.3f %9.3f"%(i,x0,x1,y0,y1,ratio)
    
    return graph_ratio

# GET string width
def stringWidth(*strings0):
    """Make educated guess on the maximum length of a string."""
    strings = list(strings0)
    for string in strings0:
      matches = re.search(r"#splitline\{(.*?)\}\{(.*?)\}",string) # check splitline
      if matches:
        while string in strings: strings.pop(strings.index(string))
        strings.extend([matches.group(1),matches.group(2)])
      matches = re.search(r"[_^]\{(.*?)\}",string) # check subscript/superscript
      if matches:
        while string in strings: strings.pop(strings.index(string))
        strings.append(matches.group(1)+matches.group(2))
      string = string.replace('#','')
    return max([len(s) for s in strings])

# CALCULATE the center of the margin
def marginCenter(canvas,axis,side='left',shift=7):
    """Calculate the center of the right margin in units of a given axis"""
    range    = axis.GetXmax() - axis.GetXmin()
    rangeNDC = 1 - canvas.GetRightMargin() - canvas.GetLeftMargin()
    center   = axis.GetXmin() - canvas.GetLeftMargin()*range/2/rangeNDC
    if side == "right":
      center = axis.GetXmin() - canvas.GetRightMargin()*range/2/rangeNDC
    if shift:
        if center>0: center*=(1+shift/100.0)
        else:        center*=(1-shift/100.0) 
    return center
        
# ENSURE dir
def ensureDirectory(dir):
    """Make directory if it does not exist."""
    if not os.path.exists(dir):
        os.makedirs(dir)
        print ">>> made directory %s" % dir





def main():
    print ""
    
    ensureDirectory(DIR)
    ensureDirectory(PLOTS_DIR)
    
    doSUSY_bbA          = True #and False
    createDataCards     = True and False # not necessary when doLimits.sh was run
    useBinScan          = True and False
    doBoxes             = True and False
    doMassScan          = True and False
    compareMassScan     = True and not doMassScan #and False
    doPValue            = True and False
    
    labels     = ["mt-1","mt-2","et-1","et-2","combined"]
    masses     = [20, 28, 40, 50, 60, 70]
    filelabels = [ ]
    extralabel = ""
    plotlabel  = ""
    
    if doSUSY_bbA:
      labels     = ["mt-1","et-1","combined",]
      masses     = range(25,71,5)
      extralabel = "_bbA" #_Opt"
      plotlabel  = extralabel
      filelabels = [ ("_bbA1",          "1 b tag"                             ),
                     ("_bbA2",          "#geq 1 b tag"                        ),
                     ("_bbA_fj",        "1 b tag, no veto on |#eta|>2.4 jets" ),
                     ("_bbA_pt20_j30",  "1 b tag, p_{T}>20 GeV, other jets p_{T}<30 GeV" ),
                     ("_bbA_pt20_j20",  "1 b tag, p_{T}>20 GeV, other jets p_{T}<20 GeV" ),
                     #("_bbA_pt20_j20",  "1 b tag, p_{T}>20 GeV"               ),
                     ("_bbA_mt40",      "1 b tag, m_{T}<40 GeV"               ),
                     ("_bbA_Dzeta-40",  "1 b tag, D_{#zeta}>-40 GeV"          ),
                   ]
#       for x in [80,70,60,50,40,30]: filelabels.append(("_bbA_Dzeta-%d"%x,"1 b tag, D_{#zeta}>-%d"%x)); plotlabel = "_bbA_Dzeta"
#       for x in [80,70,60,50,40,30]: filelabels.append(("_bbA_met%d"%x,   "1 b tag, MET<%d"%x       )); plotlabel = "_bbA_met"
#       for x in [80,70,60,50,40,30,20]: filelabels.append(("_bbA_mt%d"%x, "1 b tag, m_{T}<%d"%x     )); plotlabel = "_bbA_mt"
#       for x in [80,70,60,50,40,30]: filelabels.append(("_bbA_Dzeta-40_mt%d"%x, "1 b tag, D_{#zeta}>-40, m_{T}<%d"%x )); plotlabel  = "_bbA_Dzeta_mt"
    elif compareMassScan:
      extralabel = ""
      filelabels = [ ("_noOpt",         "no optimization"                       ),
                     #("_dphi2p0",       "#Delta#phi_{qb,ll}>2.0"                ),
                     ("_mt60",         "m_{T}<60"                               ),
                     #("_dphi2p0_met60", "#Delta#phi_{qb,ll}>2.0, MET<60"        ),
                   ]
#       for x in [2.3,2.2,2.1,2.0,1.9,1.8]: filelabels.append((("_dphi%s"%x).replace('.','p'),"#Delta#phi_{qb,ll}>%s"%x)); plotlabel  = "_dphi"
#       for x in [80,70,60,50,40]: filelabels.append(("_met%s"%x,"MET<%s"%x)); plotlabel = "_met"
#       for x in [80,70,60,50,40]: filelabels.append(("_mt%s"%x,"m_{T}<%s"%x)); plotlabel = "_mt"
#       for x in [80,70,60,50,40]: filelabels.append(("_dphi2p0_met%s"%x,"#Delta#phi_{qb,ll}>2.0, MET<%s"%x)); plotlabel = "_dphi_met"
#       for x in [80,70,60,50,40]: filelabels.append(("_met60_mt%s"%x,"#Delta#phi_{qb,ll}>2.0, MET<60, m_{T}<%s"%x)); plotlabel = "_dphi_met_mt"
#       for x in [80,70,60,50,40]: filelabels.append(("_met60_mt%s"%x,"MET<60, m_{T}<%s"%x)); plotlabel = "_met_mt"
      for x in [80,70,60,50,40]: filelabels.append(("_mt60_met%s"%x,"m_{T}<60, MET<%s"%x)); plotlabel = "_mt_met"
      if   "dphi"   in plotlabel: labels = ["mt-2","et-2"]
      elif "met_mt" in plotlabel: labels = ["mt-1","et-1"]
    
    
    bins = [ ]
    binWidth = 5.0
    if useBinScan:
      bins   = range(1,21)
      masses = [binWidth/2.0*i for i in bins] # use bin center as mass point
    
    if  args.mutau: labels = [l for l in labels if "mt" in l]
    elif args.etau: labels = [l for l in labels if "et" in l]
    
    if doBoxes and len(labels)>2:
        if createDataCards: executeDataCards(labels,mass=28)
        plotBoxes(labels,mass=28)
    
    if doMassScan:
        if createDataCards: executeDataCards(labels,masses=masses,extralabel=extralabel)
        plotUpperLimits(labels,masses,extralabel=extralabel)
    
    if compareMassScan and filelabels:
        if createDataCards: executeDataCards(labels,masses=masses)
        compareUpperLimits(labels,masses,filelabels,extralabel=extralabel,plotlabel=plotlabel)
    
    if doPValue:
        if createDataCards: executeDataCardsPValue(labels,masses=masses,bins=bins)
        plotPValues(labels,masses,bins=bins)
    



if __name__ == '__main__':
    main()
    print ">>>\n>>> done\n"

