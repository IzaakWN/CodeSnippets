#! /usr/bin/env python

from ROOT import TColor, TBox, Form

i, j = 0, 0
color = 0
# xlow, ylow, xup, yup, hs, ws
# x1, y1, x2, y2
x1 = y1 = 0
x2 = y2 = 20

gPad.SetFillColor(0)
gPad.Clear()
gPad.Range(x1,y1,x2,y2)

text = TText(0,0,"")
text.SetTextFont(61)
text.SetTextSize(0.07)
text.SetTextAlign(22)

box = TBox()

# Draw color table boxes.
hs = (y2-y1)/Double_t(5)
ws = (x2-x1)/Double_t(10)
for i in range(0,10):
   xlow = x1 + ws*(Double_t(i)+0.1)
   xup  = x1 + ws*(Double_t(i)+0.9)
   for j in range(0,5):
      ylow = y1 + hs*(j+0.1)
      yup  = y1 + hs*(j+0.9)
      color = 10*j + i
      box.SetFillStyle(1001)
      box.SetFillColor(color)
      box.DrawBox(xlow, ylow, xup, yup)
      box.SetFillStyle(0)
      box.SetLineColor(1)
      box.DrawBox(xlow, ylow, xup, yup)
      if color==1: text.SetTextColor(0)
      else:        text.SetTextColor(1)
      text.DrawText(0.5*(xlow+xup), 0.5*(ylow+yup), Form("%d",color))

