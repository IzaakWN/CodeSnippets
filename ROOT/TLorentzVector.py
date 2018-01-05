#! /usr/bin/env python
# Author: Izaak Neutelings (November 2017)
# https://root.cern.ch/doc/v606/classTLorentzVector.html

import time
start = time.time()

import ROOT
from ROOT import TLorentzVector
from math import sqrt, exp




def sumTLVs():
    """Test function test behavior of TLorentzVectors."""
    print ">>> create TLVs..."
    
    pt  = [ 40.0, 30.0  ]
    eta = [  1.5, -2.2  ]
    phi = [  0.0,  0.0  ]
    m   = [  4.0,  4.0  ]
    
    tlv1 = TLorentzVector()
    tlv1.SetPtEtaPhiM(pt[0],eta[0],phi[0],m[0])
    tlv2 = TLorentzVector()
    tlv2.SetPtEtaPhiM(pt[1],eta[1],phi[1],m[1])
    
    print ">>> tlv1.SetPtEtaPhiM(%.3g,%.3g,%.3g,%.3g)"%(pt[0],eta[0],phi[0],m[0])
    print ">>> tlv2.SetPtEtaPhiM(%.3g,%.3g,%.3g,%.3g)"%(pt[1],eta[1],phi[1],m[1])



def shiftMET():
    """Test function to see how one can apply a shift to the MET."""
    print ">>> create TLVs..."
    
    shift = 1.05 # 5%
    
    jet1 = TLorentzVector()
    jet2 = TLorentzVector()
    met  = TLorentzVector()
    jet1.SetPtEtaPhiM( 40.0,  1.5,  0.0,  4.0 )
    jet2.SetPtEtaPhiM( 30.0, -2.5,  1.5, 10.0 )
    met.SetPtEtaPhiM(  45.0,  0.0, -2.3,  0.0 )
    printTLV(jet1,jet2,met,names=["tlv1","tlv2","met"],header=True)
    
    # SHIFT JET ENERGY
    jet1_shift = TLorentzVector()
    jet1_shift.SetPtEtaPhiM(shift*jet1.Pt(),jet1.Eta(),jet1.Phi(),shift*jet1.M())
    jet2_shift = TLorentzVector()
    jet2_shift.SetPtEtaPhiM(shift*jet2.Pt(),jet2.Eta(),jet2.Phi(),shift*jet2.M())
    #jet1_shift2 = shift*jet1
    #jet2_shift2 = shift*jet2
    printTLV(jet1_shift,jet2_shift,names=["jet1_shift","jet2_shift"])
    
    # SHIFT MET
    dtlv = TLorentzVector()
    dtlv += (jet1-jet1_shift)
    dtlv += (jet2-jet2_shift)
    printTLV(dtlv,names=["dtlv"])
    
    met_shift1 = met - dtlv
    met_shift2 = TLorentzVector()
    met_shift2.SetPtEtaPhiM(met_shift1.Pt(),0,met_shift1.Phi(),0)
    
    printTLV(met_shift1,met_shift2,names=["met_shift1","met_shift2"])
    
    
    
    
    


def printTLV(*tlvs,**kwargs):
    '''Help function to print all relevant info of the fiven TLV'''
    
    names   = kwargs.get('names',  [ ]  )
    header  = kwargs.get('header', False)
    
    while len(names)<len(tlvs): names.append("")
    if header:
        print ">>> %15s  %8s %8s %8s %8s %8s %8s %8s %8s"%("name","Px","Py","Pz","Pt","E","M","Phi","Eta")
    for name, tlv in zip(names,tlvs):
        print ">>> %15s: %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f"%(name,tlv.Px(),tlv.Py(),tlv.Pz(),tlv.Pt(),tlv.E(),tlv.M(),tlv.Phi(),tlv.Eta())


def main():
    print "\n>>> Hello, world!"
    shiftMET()
    




if __name__ == '__main__':
    main()
    end = time.time()
    print ">>>\n>>> The program lasted %.3f seconds.\n" % (end-start)
