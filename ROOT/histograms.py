import time
start = time.time()

from math import floor, ceil
from ROOT import gRandom, TFile, TTree, TH1D, TObject, TCanvas, kRed, kGreen
import numpy # or use array



def writeHistogramsToFileTest():
    print ">>> write a root file with a histogram."

    
    filein = TFile("tree.root", "read")
    fileout = TFile("test.root", "recreate")
    tree = filein.Get("dir1/tree2")
    
    hist1 = TH1D("hist1","hist1",100,0,40)
    tree.Draw("normal5 >> hist1")
    
    hist2 = TH1D("hist2","hist2",100,0,40)
    hist2.SetLineColor(kRed)
    tree.Draw("normal5 + 5 >> hist2")
    
    # ...
    
    canvas = TCanvas("canvas","canvas",100,100,600,800)
    hist1.Draw()
    hist2.Draw("same")
    # ...
    
    canvas.SaveAs("test.png")
    
    fileout.Write()
    fileout.Close()
    canvas.Close()



def writeHistogramToFile(filename,name,Nbins=600,option='recreate',N=10000):
    print ">>> write a root file with a histogram."

    f = TFile(filename, option)
    h1 = TH1D(name,"Hists be histin'",Nbins,-4,8)

    for i in xrange(N):
        h1.Fill(gRandom.Gaus(2,2))

    f.Write()
    f.Close()


def reBinStandard(h0,Nbins1):

    Nbins0 = h0.GetNbinsX()
    name0 = h0.GetName()
    name1 = "%s_%s-default" % (name0,Nbins1)
    rebin_factor = Nbins0 / Nbins1

    h1 = h0.Rebin(rebin_factor,name1)
    #h1 = h0.Clone()
    #h1.SetName("%s_%s" % (name,Nbins1))
    #h1.Rebin(NBins1)
    Nbins1 = h1.GetNbinsX()
    print ">>>> Rebinned  %s (%s bins) to %s (%s bins) (factor %s)" % (name0,Nbins0,name1,Nbins1,rebin_factor)

    return h1



def reBinExact(h0,Nbins1):
    
    Nbins0 = h0.GetNbinsX()
    name0 = h0.GetName()
    name1 = "%s_%s-exact" % (name0,Nbins1)
    rebin_factor = Nbins0 / float(Nbins1)
    title1 = h0.GetTitle()
    a = h0.GetXaxis().GetXmin()
    b = h0.GetXaxis().GetXmax()
    h1 = TH1D(name1,title1,Nbins1,a,b)
    
    # under and overflow
    h1.SetBinContent(0,h1.GetBinContent(0))
    h1.SetBinContent(Nbins1+1,h1.GetBinContent(Nbins0+1))

    # everything else
    bin0_last = 1
    fraction_low = 1
    for bin1 in range(1,Nbins1+1):
        
        low1 = h1.GetXaxis().GetBinLowEdge(bin1)
        wid1 = h1.GetXaxis().GetBinWidth(bin1)
        upp1 = low1+wid1
        
        bin0 = h0.FindBin(upp1)
        low0 = h0.GetXaxis().GetBinLowEdge(bin0)
        wid0 = h0.GetXaxis().GetBinWidth(bin0)
        upp0 = low0+wid0
        fraction_upp =  ( upp1 - low0 ) / wid0
        
        #print "\n>>>>> bin1 = %s,  bin0 = %s " % (bin1, bin0)
        #print ">>>>> low1 = %5.3g, upp1 = %5.3g, wid1 = %5.3g" % (low1, upp1, wid1)
        #print ">>>>> low0 = %5.3g, upp0 = %5.3g, wid0 = %5.3g" % (low0, upp0, wid0)
        #print ">>>>> fraction_low = %s, fraction_upp = %s" % (fraction_low,fraction_upp)
        if   upp1 < low0:
            if abs(low0-upp1) < 0.00001: upp1 = low0
            else: print ">>>>> Warning! upp1 = %5.10g < low0 = %5.10g" % (upp1, low0)
        elif upp0 < upp1:
            if abs(upp1-upp0) < 0.00001: upp1 = upp0
            else: print ">>>>> Warning! upp0 = %5.10g < upp1 = %5.10g" % (upp0, upp1)
        #else: print ">>>>> low0 = %s, upp1 = %s, upp0 = %s, wid0 = %s" % (low0, upp1, upp0, wid0)
        fraction_upp =  ( upp1 - low0 ) / wid0
        
        # split first bin  with weight determined by overlap of bins
        binc1 = floor(h0.GetBinContent(bin0_last) * fraction_low)
        #print ">>> floor(h0.GetBinContent(bin0_last) * fraction_low) = %s" % floor(h0.GetBinContent(bin0_last) * fraction_low)
        
        # bins inbetween   without any weights
        for bin in range(bin0_last+1,bin0):
            binc1 += h0.GetBinContent(bin)
            #print ">>> h0.GetBinContent(bin) = %s" % h0.GetBinContent(bin)
            
        # split last bin   with weight determined by overlap of bins
        if bin0 is not Nbins0+1:
            binc1 += ceil(h0.GetBinContent(bin0) * fraction_upp)
            #print ">>> ceil(h0.GetBinContent(bin0) * fraction_upp) = %s" % ceil(h0.GetBinContent(bin0) * fraction_upp)

        h1.SetBinContent(bin1,binc1)
        bin0_last = bin0
        fraction_low = 1 - fraction_upp

    print ">>>> Rebinned  %s (%s bins) to %s (%s bins) (exact factor %5.4g)" % (name0,Nbins0,name1,Nbins1,rebin_factor)

    return h1



def reBinHistToFile(filename,name0,Nbins1,replace=False,exact=False):
    print ">>> rebin histogram"
    # https://root.cern.ch/doc/master/classTH1.html#aff6520fdae026334bf34fa1800946790

    f = TFile(filename,'update')
    
    h0 = f.Get(name0)
    Nbins0 = h0.GetNbinsX()
    
    if Nbins1 < 0:
        print ">>> Warning! Could not rebin: new binning (%s) is incorrect format" % (Nbins1)
        return 0
    if Nbins0 < Nbins1:
        print ">>> Warning! Could not rebin: binning of original histogram (%s) is smaller than the new binning (%s)" % (Nbins0,Nbins1)
        return 0

    name1 = "%s_%s-exact" % (name0,Nbins1)
    rebin_factor = Nbins0 / float(Nbins1)
    print ">>>> Rebinning %s (%s bins) to %s (%s bins) (exact factor %5.4g)" % (name0,Nbins0,name1,Nbins1,rebin_factor)

    if exact:
        h1 = reBinExact(h0,Nbins1)
    else:
        h1 = reBinStandard(h0,Nbins1)

    f.Write("",TObject.kOverwrite)
    f.Close()



def printHistogram(filename,name):
    print ">>> print contents of histogram %s from file %s" % (name,filename)

    f = TFile(filename,'read')
    h = f.Get(name)
    for bin in range(h.GetNbinsX()+2):
        print ">>>> bin %s: %15.5g" % (bin,h.GetBinContent(bin))
    f.Close()



def main():
    print "Hello, world!"
    
    filename = "histograms.root"
    name = "normal_5"

    writeHistogramsToFileTest()
    
#     writeHistogramToFile(filename,name,Nbins=5)
#     reBinHistToFile(filename,name,3,exact=True)
#     reBinHistToFile(filename,name,3)
#     name = "normal_600"
#     writeHistogramToFile(filename,name,Nbins=600,N=10000,option='update')
#     reBinHistToFile(filename,name,25,exact=True)
#     reBinHistToFile(filename,name,25)
#     reBinHistToFile(filename,name,30,exact=True)
#     reBinHistToFile(filename,name,30)
#     reBinHistToFile(filename,name,35,exact=True)
#     reBinHistToFile(filename,name,35)
#     reBinHistToFile(filename,name,52,exact=True)
#     reBinHistToFile(filename,name,52)
#     reBinHistToFile(filename,name,55,exact=True)
#     reBinHistToFile(filename,name,55)
#    printHistogram(filename,name)


if __name__ == '__main__':
    main()
    end = time.time()
    print "\nThe program lasted %.2f seconds.\n" % (end-start)


