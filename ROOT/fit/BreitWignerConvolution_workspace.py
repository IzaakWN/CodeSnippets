#!/usr/bin/python
from ROOT import *

useSingleGaussian = True

workspace = RooWorkspace('etac mass')
#construct double gaussian resolution function and breit wigner
workspace.factory('BreitWigner::breitwigner(x[2.65, 3.25], BreitWignerMean[2.983], BreitWignerWidth[0.0322])')
workspace.var('x').setUnit('GeV/c^{2}')
workspace.factory('Gaussian::gaus1(x, GausMean1[0.006, -0.01, 0.01], GausSigma1[0.003, -0.02, 0.02])')
workspace.factory('expr::GausSigma2(\'GausSigma1*alpha\',GausSigma1,alpha[3., 1., 5.])')
workspace.factory('expr::GausMean2(\'GausMean1 + MeanShift\', GausMean1, MeanShift[0.02, -0.04, 0.04])')
workspace.factory('Gaussian::gaus2(x, GausMean2, GausSigma2)')
workspace.factory('SUM::ResolutionSignal(fracgaus1[0.9, 0.1, 0.99]*gaus1, gaus2)')
#build signal function as convolution of breit-wigner and resolution function
workspace.factory('FCONV::CompleteSignalModel(x, breitwigner, ResolutionSignal)')
workspace.factory('FCONV::OneGaussianSignalModel(x, breitwigner, gaus1)')
#print workspace content
workspace.Print()
#generate data
if useSingleGaussian:
  pdf = workspace.pdf('OneGaussianSignalModel')
else:
  pdf = workspace.pdf('CompleteSignalModel')

datahist = pdf.generate(RooArgSet(workspace.var('x')), 3000)
pdf.fitTo(datahist, RooFit.Strategy(2), RooFit.Minimizer('Minuit2'))

#print data and fit
canvas = TCanvas('canvas', 'canvas')
canvas.cd()
frame = workspace.var('x').frame()
datahist.plotOn(frame)
pdf.plotOn(frame)
frame.Draw()
canvas.Print('DoubleGaussianConvolution.pdf')
