from ROOT import TFile, TTree, TH1F, gDirectory

def printGDirectory():
    print ">>> gDirectory.GetName()\n%s" % gDirectory.GetName()
    print ">>> gDirectory.pwd()"
    gDirectory.pwd()
    print ">>> gDirectory.ls()"
    gDirectory.ls()
    print

print "\ndefault"
printGDirectory()

print ">>> creating a file with some contents"
file = TFile("test.root","recreate")
tree = TTree("tree","tree")
hist = TH1F("hist","hist",100,0,100)
dir1 = file.mkdir("dir1")
printGDirectory()

print ">>> gDirectory.Delete(\"hist\")"
gDirectory.Delete("hist")
printGDirectory()

print ">>> dir1.cd()"
dir1.cd()
printGDirectory()

print ">>> file.Close()"
file.Close()
printGDirectory()