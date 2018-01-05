#! /usr/bin/env python
# Author: Izaak Neutelings (March 2015)

import time
start = time.time()

from ROOT import gRandom, TFile, TTree, TH1D ,TObject
from array import array
import numpy # alternative to array

# Add branch to existing tree:
#    https://rootree.cern.ch/phpBB3/viewtopic.php?t=9661
#
# Write directories into root files:
#    https://rootree.cern.ch/root/html/tutorials/io/dirs.C.html


def writeTree():
    print ">>> Writing a tree."
    
    # make new root file with new tree
    file = TFile("tree.root", 'recreate')
    tree = TTree("tree_name", "tree title")
    
    # create 1 dimensional float arrays as fill variables, in this way the float array serves
    # as a pointer which can be passed to the branch
    n = array('d',[0])
    u = array('d',[0])
    
    # using numpy instead of array class (note python's float datatype corresponds to C++ doubles):
    #n = numpy.zeros(1, dtype=float)
    #u = numpy.zeros(1, dtype=float)
    
    # create the branches and assign the fill-variables to them as doubles (D)
    tree.Branch("normal", n, 'normal/D')
    tree.Branch("uniform", u, 'uniform/D')
    
    # create some random numbers, assign them into the fill variables and call Fill()
    for i in xrange(10000):
        n[0] = gRandom.Gaus()
        u[0] = gRandom.Uniform()
        tree.Fill()

    # write the tree into the output file and close the file
    file.Write()
    file.Close()



def addBranch():
    print ">>> Add branch."

    # reopen tree file
    file = TFile("tree.root",'update')
    tree = file.Get("tree_name")
    
    # make new variable
    n = array('d',[0])
    #n = numpy.zeros(1, dtype=float)
    b = tree.Branch("normal2", n, 'normal2/D')
    
    # fill the branch
    N = tree.GetEntries()
    for i in xrange(N):
        tree.GetEntry(i)
        n[0] = gRandom.Gaus(3,2)
        b.Fill()

    # overwrite the tree in the output file and close the file
    file.Write("",TFile.kOverwrite)
    file.Close()



def addHist():
    print ">>> Add histograms to a tree and one to a new branch."

    # reopen tree file
    file = TFile("tree.root",'update')
    tree = file.Get("tree_name")
    
    # make new histogram
    hist = TH1D("normal3","Haters be histin'",50,-2,6)

    # fill histogram
    for i in xrange(10000):
        hist.Fill(gRandom.Gaus(2,2))

    file.Write("",TObject.kOverwrite)
    file.Close()



def addHistToDirectory():
    print ">>> Add histogram to directory."

    # reopen tree file
    file = TFile("tree.root",'update')
    
    # make directory if it does not exist
    dir = file.GetDirectory("dir1")
    if not dir:
        print ">>>   created dir1"
        dir = file.mkdir("dir1")
    
    # make this directory the current one: everything you write will be saved here
    dir.cd()
    
    # declare histogram
    hist = TH1D("normal4","Hist in folder",50,-1,9)
    
    # write histogram
    for i in xrange(10000):
        hist.Fill(gRandom.Gaus(4,3))

    file.Write("",TFile.kOverwrite)
    file.Close()



def addBranchToDirectory():
    print ">>> Add branch to directory."
    
    file = TFile("tree.root",'update')
    
    # make directory if it does not exist
    dir = file.GetDirectory("dir1")
    if not dir:
        print ">>>   created dir1"
        dir = file.mkdir("dir1")
    
    # make this directory the current one: everything you write will be saved here
    dir.cd()
    
    # make new tree with a branch
    tree = TTree("tree2", "tree2")
    n = array('d',[0])
    #n = numpy.zeros(1, dtype=float)
    tree.Branch("normal5", n, 'normal5/D')
    
    # fill tree
    for i in xrange(10000):
        n[0] = gRandom.Gaus(3,2)
        tree.Fill()

    file.Write("",TFile.kOverwrite)
    file.Close()



def loopThroughTree():
    print ">>> Loop through tree."

    file = TFile("tree.root",'read')
    tree = file.Get("tree_name")
    
    # loop over tree in the easiest way
    i = 0
    for event in tree:
        if (i%2000) == 0:
            print ">>>   event %5i: n = %5.2f" % (i,tree.normal)
            print ">>>   event %5i: u = %5.2f" % (i,tree.uniform)
        i += 1
    print ">>>   event %5i: n = %5.2f" % (i,tree.normal)
    print ">>>   event %5i: u = %5.2f" % (i,tree.uniform)
    
    # alternatively
    # N = tree.GetEntries()
    # for i in xrange(N):
    #     if (i%2000) == 0:
    #         tree.GetEntry(i)
    #         print ">>>   event %5i: n = %5.2f" % (i,tree.normal)
    #         print ">>>   event %5i: u = %5.2f" % (i,tree.uniform)
    #     i += 1
    # print ">>>   event %5i: n = %5.2f" % (i,tree.normal)
    # print ">>>   event %5i: u = %5.2f" % (i,tree.uniform)
    
    file.Close()



def main():
    print "\n>>> Hello, world!"
    writeTree()
    addBranch()
    addBranchToDirectory()
    addHist()
    addHistToDirectory()
    loopThroughTree()



if __name__ == '__main__':
    main()
    end = time.time()
    print ">>>\n>>> The program lasted %.3f seconds.\n" % (end-start)
