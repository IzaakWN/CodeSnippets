#! /usr/bin/env python
# Author: Izaak Neutelings (June 2018)
# https://ineuteli.web.cern.ch/ineuteli/public/smear/
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
import time
start = time.time()

from math import sqrt, log, log10, floor, ceil
from ROOT import gRandom, gPad, TCanvas, TLegend, TH1F, TF1, TGraphAsymmErrors, TLine,\
                 kRed, kGreen, kBlue, kOrange
colors  = [ kRed, kBlue, kGreen, kOrange ]


def smear(mu,sigma0,smearfactor,N=100000,lcut=None,ucut=None,nbins=80):
    print ">>> smearing for N(%s,%s) with a factor of %s"%(mu,sigma0,smearfactor)
    
    xmin, xmax = mu-sigma0*5, mu+sigma0*4
    xtitle     ="x variable"
    ytitle     = "events"
    title      = "Gauss(%s,%s)"%(mu,"#sigma")
    canvasname = "smear_%.1f-%.1f_by_%.2f"%(mu,sigma0,smearfactor)
    if lcut!=None:
      canvasname += "_gt%.1f"%(lcut)
    if ucut!=None:
      canvasname += "_lt%.1f"%(ucut)
    canvasname = canvasname.replace('.','p')
    
    # HISTS
    sigma1     = sigma0*(1+smearfactor)
    histname0  = "unsmeared"
    histname1  = "smeared"
    histtitle0 = "unsmeared, #sigma_{0} = %s"%(sigma0)
    histtitle1 = "smeared, #sigma_{new} = %s"%(sigma1)
    hist0      = TH1F(histname0,histtitle0,nbins,xmin,xmax)
    hist1      = TH1F(histname1,histtitle1,nbins,xmin,xmax)
    
    # FIT FUNCTIONS
    xminf      = xmin if lcut==None else lcut
    xmaxf      = xmax if ucut==None else ucut
    gaus0      = TF1("gaus0","gaus",xminf,xmaxf)
    gaus1      = TF1("gaus1","gaus",xminf,xmaxf)
    gaus0.SetTitle("%s fit"%histname0)
    gaus1.SetTitle("%s fit"%histname1)
    gaus0.SetParameters(N,mu,sigma0)
    gaus1.SetParameters(N,mu,sigma1)
    #gaus0.SetParLimits(2,sigma0*0.9,sigma0*1.1)
    #gaus1.SetParLimits(2,sigma1*0.9,sigma1*1.1)
    hists      = [ (hist0,gaus0), (hist1,gaus1) ]
    
    # SMEAR & FILL
    print ">>>   generating %s events..."%(N)
    #sigma1 = smearfactor
    #sigma1 = (smearfactor**2)/2.
    #sigma1 = sqrt(2.*(smearfactor))
    #sigma1 = sqrt(-2.*log(smearfactor))
    #sigma1 = 1./(2*smearfactor**2)
    sigma2 = sqrt(sigma1**2-sigma0**2)
    print ">>>   sigma1 = %.3f"%(sigma1)
    for i in xrange(N):
      xval0 = gRandom.Gaus(mu,sigma0)
      if lcut!=None and xval0<lcut: continue
      if ucut!=None and xval0>ucut: continue
      #rand  = gRandom.Gaus(1,smearfactor)
      #xval1 = xval0 * rand
      #rand  = gRandom.Gaus(0,1+smearfactor) 
      #xval1 = xval0 + rand
      rand  = gRandom.Gaus(0,1)
      xval1 = xval0 + sigma2*rand
      hist0.Fill(xval0)
      if lcut!=None and xval1<lcut: continue
      if ucut!=None and xval1>ucut: continue
      hist1.Fill(xval1)
    
    ymin, ymax = 0, 1.14*max(hist0.GetMaximum(),hist1.GetMaximum())
    rmin, rmax = 0.60, 1.40
    
    # CANVAS
    lmargin, rmargin = 0.14, 0.04
    canvas = TCanvas("canvas","canvas",100,100,800,800)
    canvas.Divide(2)
    
    # MAIN plot
    canvas.cd(1)
    gPad.SetPad("pad1","pad1",0,0.33,1,1,0,-1,0)
    gPad.SetFillColor(0)
    gPad.SetBorderMode(0)
    gPad.SetFrameFillStyle(0)
    gPad.SetFrameBorderMode(0)
    gPad.SetTopMargin(  0.06 ); gPad.SetBottomMargin( 0.02 )
    gPad.SetLeftMargin( lmargin ); gPad.SetRightMargin( rmargin )
    gPad.SetGrid()
    gPad.cd()
    
    textsize   = 0.050
    x1, width  = 0.18, 0.25
    y1, height = 0.89, textsize*1.08*5
    legend = TLegend(x1,y1,x1+width,y1-height)
    legend.SetTextSize(textsize)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetFillColor(0)
    legend.SetTextFont(62)
    legend.SetHeader(title)
    legend.SetTextFont(42)
    
    frame = gPad.DrawFrame(xmin,ymin,xmax,ymax)
    frame.GetYaxis().SetTitleSize(0.070)
    frame.GetXaxis().SetTitleSize(0.070)
    frame.GetXaxis().SetLabelSize(0.000)
    frame.GetYaxis().SetLabelSize(0.060)
    frame.GetXaxis().SetTitleOffset(1.00)
    frame.GetYaxis().SetTitleOffset(1.06)
    frame.GetXaxis().SetNdivisions(508)
    frame.GetXaxis().SetTitle(xtitle)
    frame.GetYaxis().SetTitle(ytitle)
    
    # DRAW & FIT
    print ">>>   fitting..."
    fits = [ ]
    for i, (hist,gaus) in enumerate(hists):
      color = colors[i%len(colors)]
      hist.SetLineColor(color)
      hist.SetLineWidth(2)
      hist.SetLineStyle(1)
      gaus.SetLineColor(color+1)
      gaus.SetLineWidth(2)
      gaus.SetLineStyle(2)
      hist.Fit(gaus.GetName(),'0','',xminf,xmaxf)
      hist.Draw('SAME')
      gaus.Draw('SAME')
      gtitle = "#sigma_{fit} = %.3f"%(gaus.GetParameter(2)) #gaus.GetTitle()
      legend.AddEntry(hist, hist.GetTitle(), 'l')
      legend.AddEntry(gaus, gtitle, 'l')
    print ">>>   real unsmeared sigma:    %5.3f"%(sigma0)
    print ">>>   fitted unsmeared sigma:  %5.3f"%(gaus0.GetParameter(2))
    print ">>>   real smear factor:       %5.3f"%(smearfactor)
    print ">>>   fitted smeared sigma:    %5.3f"%(gaus1.GetParameter(2))
    
    legend.Draw()
    frame.Draw('SAMEAXIS')
    gPad.Modified()
    
    # RATIO plot
    canvas.cd(2)
    gPad.SetPad("pad2","pad2",0,0,1,0.32,0,-1,0)
    gPad.SetTopMargin(  0.04 );    gPad.SetBottomMargin( 0.29 )
    gPad.SetLeftMargin( lmargin ); gPad.SetRightMargin( rmargin )
    
    rframe = gPad.DrawFrame(xmin,rmin,xmax,rmax)
    rframe.GetYaxis().CenterTitle()
    rframe.GetXaxis().SetTitleSize(0.144)
    rframe.GetYaxis().SetTitleSize(0.140)
    rframe.GetXaxis().SetLabelSize(0.130)
    rframe.GetYaxis().SetLabelSize(0.120)
    rframe.GetXaxis().SetLabelOffset(0.012)
    rframe.GetXaxis().SetTitleOffset(0.85)
    rframe.GetYaxis().SetTitleOffset(0.53)
    rframe.GetXaxis().SetNdivisions(508)
    rframe.GetYaxis().CenterTitle(True)
    rframe.GetYaxis().SetTitle("ratio")
    rframe.GetXaxis().SetTitle(xtitle)
    rframe.GetYaxis().SetNdivisions(5)
    
    # RATIO
    ratios = [ ]
    for i, (hist,gaus) in enumerate(hists):
      #if i==0: continue
      #ratio = hist.Clone(hist.GetName()+"_ratio")
      #ratio.Divide(hist0)
      ratio = divideHists(hist,hist0,name=hist.GetName()+"_ratio")
      ratio.Draw('HISTSAME')
      ratios.append(ratio)
      #ratiof = createTH1FromTF1(gaus,nbins,xmin,xmax)
      #ratiof.Divide(hist0)
      ratiof = divideTF1ByTH1(gaus,hist0,name=gaus.GetName()+"_ratio")
      ratiof.Draw('HISTSAME')
      ratios.append(ratiof)
      print ratiof
    #line = TLine(xmin,1.,xmax,1.)
    #line.SetLineColor(hist0.GetLineColor())
    #line.SetLineWidth(hist0.GetLineWidth())
    #line.SetLineStyle(1)
    #line.Draw('SAME')
    
    gPad.SetGrid()
    gPad.Modified()
    rframe.Draw('sameaxis')
    
    canvas.SaveAs(canvasname+".png")
    canvas.SaveAs(canvasname+".pdf")
    canvas.Close()
    print ">>> "
    


def createTH1FromTF1(func,nbins,xmin,xmax):
    hist = TH1F("hist_"+func.GetName(),func.GetTitle(),nbins,xmin,xmax)
    for i in xrange(0,nbins+2):
      xval = hist.GetBinCenter(i)
      yval = func.Eval(xval)
      hist.SetBinContent(i,yval)
    hist.SetLineColor(func.GetLineColor())
    hist.SetLineWidth(func.GetLineWidth())
    hist.SetLineStyle(func.GetLineStyle())
    #hist.SetLineStyle(func.GetLineStyle())
    return hist
    

def divideHists(histnom,histden,**kwargs):
    """Make ratio of two histograms."""
    nbins = histnom.GetNbinsX()
    name  = kwargs.get('name',           "ratio"   )
    title = kwargs.get('title',          "ratio"   )
    ratio = histnom.Clone(name)
    ratio.Reset()
    ratio.SetTitle(title)
    for i in xrange(0,nbins+2):
      binnom = histnom.GetBinContent(i)
      binden = histden.GetBinContent(i)
      errnom = histnom.GetBinError(i)
      if binden!=0:
        ratio.SetBinContent(i,binnom/binden)
        ratio.SetBinError(i,errnom/binden)
      elif binnom==binden:
        ratio.SetBinContent(i,1.)
        ratio.SetBinError(i,0)
      else:
        ratio.SetBinContent(i,999989)
        ratio.SetBinError(i,0)
    return ratio
    

def divideTF1ByTH1(funcnom,histden,**kwargs):
    """Make ratio of two histograms."""
    nbins = histden.GetNbinsX()
    name  = kwargs.get('name',           "ratio"   )
    title = kwargs.get('title',          "ratio"   )
    ratio = histden.Clone(name)
    ratio.Reset()
    ratio.SetTitle(title)
    ratio.SetLineColor(funcnom.GetLineColor())
    ratio.SetLineWidth(funcnom.GetLineWidth())
    ratio.SetLineStyle(funcnom.GetLineStyle())
    for i in xrange(0,nbins+2):
      xval   = histden.GetBinCenter(i)
      binnom = funcnom.Eval(xval)
      binden = histden.GetBinContent(i)
      if binden!=0:
        ratio.SetBinContent(i,binnom/binden)
      elif binnom==binden:
        ratio.SetBinContent(i,1.)
      else:
        ratio.SetBinContent(i,999989)
      ratio.SetBinError(i,0)
    return ratio


def main():
    
    N     = 1000000
    nbins = 80
    lcut  = None #-1.5
    ucut  = None #+1.5
    smear(0,1,0.01,N,lcut,ucut,nbins)
#     smear(0,1,0.05,N,lcut,ucut,nbins)
#     smear(0,1,0.10,N,lcut,ucut,nbins)
    smear(0,1,0.20,N,lcut,ucut,nbins)
    smear(0,1,0.50,N,lcut,ucut,nbins)
#     smear(0,2,0.10,N)
#     smear(0,2,0.20,N)
#     smear(0,2,0.50,N)
    


if __name__ == '__main__':
    print
    main()
    end = time.time()
    print ">>> Done after %.2f seconds.\n" % (end-start)


