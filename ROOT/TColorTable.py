#! /usr/bin/env python
# Author: Izaak Neutelings (June 2018)

import os, sys
from math import ceil, sqrt
# import CMS_lumi as CMS_lumi, tdrstyle as tdrstyle
import ROOT
from ROOT import gROOT, gPad, gStyle, TGaxis,\
                 TCanvas, TBox, TText, TLatex, Double,\
                 TColor, kBlack, kWhite, kGray,\
                 kBlue, kAzure, kCyan, kTeal, kGreen, kSpring, kYellow, kOrange, kRed, kPink, kMagenta, kViolet
ROOT.gROOT.SetBatch(ROOT.kTRUE)

color_dict = {
  'kWhite':   kWhite,   'kBlack':   kBlack,  'kGray':    kGray,
  'kBlue':    kBlue,    'kAzure':   kAzure,  'kCyan':    kCyan,
  'kTeal':    kTeal,    'kGreen':   kGreen,  'kSpring':  kSpring,
  'kYellow':  kYellow,  'kOrange':  kOrange,
  'kRed':     kRed,     'kPink':    kPink,
  'kMagenta': kMagenta, 'kViolet':  kViolet,
}


def makeTColorWheel():
  #canvas = TCanvas("canvas","canvas",100,100,800,800)
  colorWheel = TColorWheel()
  colorWheel.Draw()
  canvas = colorWheel.GetCanvas()
  canvas.SetCanvasSize(1000, 1010)
  canvas.SaveAs("TColorWheel.pdf")


def drawColorTable(clist=range(0,50),nrow=None,ncol=None,tag="",label=False,RBG=False,div=2):
    # https://root.cern.ch/doc/master/src_2TPad_8cxx_source.html#l01611
    
    cmax = 10
    if not ncol:
      ncol = min(cmax,len(clist))
    if not nrow:
      nrow = 1 if len(clist)<=cmax else int(ceil(len(clist)/float(cmax)))
    x1 = y1 = 0.
    x2 = y2 = 20.
    hs = (y2-y1)/nrow
    ws = (x2-x1)/ncol
    if label or RBG:
      width  = 170*ncol
      height = 80*nrow
    else:
      width  = 110*ncol
      height = 80*nrow
    scale  = 400./height
    if 400.<height: scale = sqrt(scale)
    canvas = TCanvas("c","Fill Area colors",0,0,width,height)
    canvas.SetFillColor(0)
    canvas.Clear()
    canvas.Range(x1,y1,x2,y2)
   
    text = TText(0,0,"")
    text.SetTextFont(61)
    text.SetTextSize(0.07*scale)
    text.SetTextAlign(22)   
    box = TBox()
   
    for r in range(0,nrow):
      ylow = y2 - hs*(r+0.1)
      yup  = y2 - hs*(r+0.9)
      for c in range(0,ncol):
        i = ncol*r+c
        if i >= len(clist): break
        xlow = x1 + ws*(c+0.1)
        xup  = x1 + ws*(c+0.9)
        color = clist[ncol*r+c]
        box.SetFillStyle(1001)
        box.SetFillColor(color)
        box.DrawBox(xlow, ylow, xup, yup)
        box.SetFillStyle(0)
        box.SetLineColor(1)
        box.DrawBox(xlow, ylow, xup, yup)
        if color==1: text.SetTextColor(0)
        else:        text.SetTextColor(1)
        name =  "%d"%color
        if (isinstance(label,int) and i%div==label) or label:
          name = getColorString(color)
        if (not isinstance(RBG,bool) and isinstance(RBG,int) and i%div==RBG) or (RBG and not isinstance(label,int)):
          name = getRGBString(color)
        text.DrawText(0.5*(xlow+xup), 0.5*(ylow+yup), name)
      if i >= len(clist): break
    
    canvas.SaveAs("TColorTable%s.png"%tag)
    canvas.SaveAs("TColorTable%s.pdf"%tag)
    


def getColorString(color):
  if gROOT.GetColor(color)!=None:
    name = gROOT.GetColor(color).GetName()
    if name[0]=='k':
      return name
  #imin = -1
  #dmin = 51;
  #cmin = 'kWhite';
  #for colkey, coli in color_dict.iteritems():
  #  diff = color - coli
  #  name = gROOT.GetColor(imin).GetName()
  #  if diff==0:
  #    return colkey; 
  #  if abs(diff)<abs(dmin):
  #    imin = coli
  #    dmin = diff
  #    cmin = colkey;
  #if abs(dmin)<51 and gROOT.GetColor(imin)!=None:
  #  return "%s%+d"%(cmin,dmin)
  return "%s"%color
  
def getRGB(color):
  return color.GetRed(), color.GetGreen(), color.GetBlue()
  
def getRGBString(color):
  if isinstance(color,int):
    color = gROOT.GetColor(color)
  if not color: return "255,255,255"
  print color
  return "%d,%d,%d"%(color.GetRed()*255, color.GetGreen()*255, color.GetBlue()*255)

  
def findClosestExistingColor(*args,**kwargs):
  r,g,b = args[:3] if len(args)>2 else getRGB(gROOT.GetColor(args[0]))
  cmax  = kwargs.get('N',924)
  dmin  = 999
  imin  = -1
  cmin  = None
  color = None
  for i, col in findNonWhiteColors(cmax):
    r2,g2,b2 = getRGB(col)
    rbgdiff  = dRGB(r,g,b,r2,g2,b2)
    if rbgdiff<dmin:
      #print "      (%.3f,%.3f,%.3f) vs. %4d, (%.3f,%.3f,%.3f), %5.4f"%(r,g,b,imin,r2,g2,b2,rbgdiff)
      imin, cmin, dmin = i, col, rbgdiff
  return imin, cmin, dmin
  
def findNonWhiteColors(N=924):
  for i in xrange(0,N):
    color = gROOT.GetColor(i)
    if i==kWhite:
      yield kWhite, color
    if color==None or getRGB(color)==(0.0,0.0,0.0): 
      continue
    yield i, color

def dRGB(r1,g1,b1,r2,g2,b2):
  return sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)



def main():
  
  #makeTColorWheel()
  
  #drawColorTable(range(0,50))
  #drawColorTable([kBlue+i for i in range(-25,25)],tag="_kBlue",label=True)
  #drawColorTable([kRed+i for i in range(-25,25)],tag="_kRed",label=True)
  #drawColorTable([kGreen+i for i in range(-25,25)],tag="_kGreen",label=True)
  #drawColorTable([kAzure+i for i in range(-25,25)],tag="_kAzure",label=True)
  #drawColorTable(range(0,1000),tag="_all",label=True)
  
  HTTcolors = [ TColor.GetColor(155,152,204),  TColor.GetColor(248,206,104),
                TColor.GetColor(135,206,250),  TColor.GetColor(100,182,232),
                TColor.GetColor(155,152,204),  TColor.GetColor(100,222,106),
                TColor.GetColor(100,222,106),  TColor.GetColor(248,206,104),
                TColor.GetColor(140,180,220),  TColor.GetColor(200,140,220),  
                TColor.GetColor(250,202,255),  TColor.GetColor(222,90,106),
                TColor.GetColor(240,175,60),   TColor.GetColor(222,140,106), ]
  drawColorTable(HTTcolors,tag="_HTT",label=True)
  
  colorPairs = [ ]
  for icol in HTTcolors:
    color = gROOT.GetColor(icol)
    imin, cmin, dmin = findClosestExistingColor(icol)
    r1,g1,b1 = getRGB(color)
    r2,g2,b2 = getRGB(cmin)
    #print "%4d, (%.3f,%.3f,%.3f) vs. %4d, (%.3f,%.3f,%.3f), %5.4f"%(icol,r1,g1,b1,imin,r2,g2,b2,dmin)
    colorPairs += [icol,imin]
  drawColorTable(colorPairs,tag="_HTTPairs",label=True)
  drawColorTable(colorPairs,tag="_HTTPairsRBG",label=True,RBG=0)
  


if __name__ == '__main__':
    main()


