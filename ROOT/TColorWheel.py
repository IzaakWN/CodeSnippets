from ROOT import TCanvas, TColorWheel

#canvas = TCanvas("canvas","canvas",100,100,800,800)
colorWheel = TColorWheel()
colorWheel.Draw()
canvas = colorWheel.GetCanvas()
canvas.SetCanvasSize(1000, 1010)
canvas.SaveAs("TColorWheel.pdf")