import time
start = time.time()

from ROOT import TFile, gDirectory
# You probably also want to import TH1D,
# unless you're not making any histograms.
from ROOT import TH1D, TH2D, TVirtualPad, TCanvas, TMath, gStyle



###  ___ SET-UP ___ ###

# Open the file. Note that the name of your file outside this class
# will probably NOT be experiment.root.

myfile = TFile('experiment.root')

# Retrieve the n-tuple of interest. In this cae, the n-tuple's name is
# "tree1". You may have to use the TBrowser to find the name of the
# n-tuple that someone gives you.
mychain = gDirectory.Get( 'tree1' )
entries = mychain.GetEntriesFast()

lol = TCanvas("lol","The histograms of Analyze Ville, North Pyhton.")
lol.Divide(2,2,0.01,0.01)

# ebeam histogram
ebeamHist = TH1D("ebeam","Histogram of ebeam",100,149.2,150.8)
ebeamHist.GetXaxis().SetTitle("ebeam [GeV]")
ebeamHist.GetYaxis().SetTitle("number of events")
    
# chi2 histogram
chi2Hist = TH1D("chi2","Histogram of chi2",100,0,20)
chi2Hist.GetXaxis().SetTitle("chi2")
chi2Hist.GetYaxis().SetTitle("number of events")

# chi2-ebeam histogram
cveHist = TH2D("cve","Scatterplot of chi2 vs. ebeam",100,0.3,1.7,100,149.2,150.8)
cveHist.GetXaxis().SetTitle("chi2")
cveHist.GetYaxis().SetTitle("ebeam [GeV]")
    
#chi2-theta histogram
cvtHist = TH2D("cvt","Scatterplot of chi2 vs. theta",100,0.3,19,100,-0.005,.3)
cvtHist.GetXaxis().SetTitle("chi2")
cvtHist.GetYaxis().SetTitle("theta [radians]")



###  ___ LOOP ___ ###
pzcount=0
for jentry in xrange( entries ):
    # Get the next tree in the chain and verify.
    ientry = mychain.LoadTree( jentry )
    if ientry < 0:
        break
     
    # Copy next entry into memory and verify.
    nb = mychain.GetEntry( jentry )
    if nb <= 0:
        continue

    # Use the values directly from the tree. This is an example using a
    # variable "vertex". This variables does not exist in the example
    # n-tuple experiment.root, to force you to think about what you're
    # doing.
    # myValue = mychain.vertex
    # myHist.Fill(myValue)

    chi2 = mychain.chi2
    chi2Hist.Fill(chi2)

    px = mychain.px
    py = mychain.py
    pz = mychain.pz
    ebeam = mychain.ebeam
    pt = TMath.Sqrt(px*px + py*py)   # Exercise 5
    theta = TMath.ATan2(pt,pz)       # Exercise 7

    ebeamHist.Fill(ebeam)      # ebeam
    chi2Hist.Fill(chi2)        # chi2
    cveHist.Fill(chi2,ebeam)   # chi2 vs. ebeam
#    cvtHist.Fill(chi2,theta)   # chi2 vs. theta

    if pz<145:
        pzcount=pzcount+1

    if (chi2<1.5 and theta<0.15):
        cvtHist.Fill(chi2,theta)



###  ___ WRAP UP ___ ###

# ebeam
lol.cd(1)
ebeamHist.Draw("E")
ebeamHist.Fit("gaus")
gStyle.SetOptFit()

# chi2
lol.cd(2)
chi2Hist.Draw("E")
chi2Hist.Fit("gaus")
gStyle.SetOptFit()
    
# chi2 vs. ebeam
lol.cd(3)
cveHist.Draw()
    
# chi2 vs. theta
lol.cd(4)
cvtHist.Draw()
    
lol.Update()

print "\nThere are",pzcount,"events with pz<145."

end = time.time()
print "\nThe program lasted",end-start,"wseconds.\n"
