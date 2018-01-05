from ROOT import TFile, TTree, gRandom, gDirectory
from array import array


print gDirectory.GetName()
print gDirectory.ls()

file = TFile("treeParticles.root", 'recreate')
tree = TTree("tree_name", "tree title")

Nmax = 10
nParticles = array( 'i', [ 0 ] )
pt = array( 'd', Nmax*[ 0. ] )
tree.Branch( 'nParticles', nParticles, 'nParticles/I' )
tree.Branch( 'pt', pt, 'pt[nParticles]/D' )

for i in xrange(100):
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