# Author: Izaak Neutelings (June 2017)
from ROOT import TFile, TTree, gRandom, gDirectory
from array import array


def writeTree()
  print gDirectory.GetName()
  print gDirectory.ls()
  file = TFile("treeParticles.root", 'recreate')
  tree = TTree("tree_name", "tree title")
  
  nevts = 100
  Nmax = 10
  nParticles = array( 'i', [ 0 ] )
  pt = array( 'd', Nmax*[ 0. ] )
  tree.Branch( 'nParticles', nParticles, 'nParticles/I' )
  tree.Branch( 'pt', pt, 'pt[nParticles]/D' )
  
  for i in xrange(nevts):
    nParticles[0] = int(gRandom.Uniform()*10)
    for j in range(nParticles[0]):
       pt[j] = gRandom.Gaus(20,2)
    tree.Fill()
  
  tree.Draw("pt[0] >> h(100,0,10)")
  hist = gDirectory.Get("h")
  print gDirectory.GetName()
  print gDirectory.ls()
  print hist
  print type(hist)
  
  file.Write()
  file.Close()
  

def main():
  print "\n>>> Hello, world!"
  writeTree()
  

if __name__ == '__main__':
  main()
  end = time.time()
  print ">>>\n>>> The program lasted %.3f seconds.\n" % (end-start)
  