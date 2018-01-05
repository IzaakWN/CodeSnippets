import ROOT
from ROOT import TCanvas, TGraphErrors, TVectorD
from array import array
from math import sqrt

x = array('d',[ ])
y = array('d',[ ])
y_errors = array('d',[ ])
zeros = array('d',[ ])

for i in range(10):
  x.append(i)
  y.append(sqrt(i))
  y_errors.append(0.2)
  zeros.append(0)

# v_x = TVectorD(len(x),x)
# v_y = TVectorD(len(y),y)
# v_y_errors = TVectorD(len(y_errors),y_errors)
# v_zeros = TVectorD(len(zeros),zeros)

#graph = TGraphErrors(v_x,v_y,v_zeros,v_y_errors)
graph = TGraphErrors(len(x),x,y,zeros,y_errors)

canvas = TCanvas("canvas","canvas",100,100,800,600)
#frame = canvas.DrawFrame(0,0,10,5)
graph.Draw()
#frame.Draw('sameaxis')
canvas.SaveAs("graphWithErrors.png")
canvas.Close()