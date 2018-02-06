from DataFormats.FWLite import Events, Handle
from ROOT import TFile, TH1F, TTree, gStyle, TH2F
import math
import numpy as num
from DeltaR import *
import sys



def findCentralJets(leadJets, otherJets ):
    '''Finds all jets between the 2 leading jets, for central jet veto.'''
    if not len(otherJets):
        return []
    
    etamin = leadJets[0].eta()
    etamax = leadJets[1].eta()
    if etamin > etamax:
        etamin, etamax = etamax, etamin
    def isCentral( jet ):
        if jet.pt() < 30.:
            return False
        eta = jet.eta()
        if etamin < eta and eta < etamax:
            return True
        else:
            return False
    centralJets = filter( isCentral, otherJets )
    return centralJets



def p4sumvis(particles):
    
    visparticles = [p for p in particles if abs(p.pdgId()) not in [12, 14, 16]]
    p4 = visparticles[-1].p4() if particles else 0.
    visparticles.pop()
    for p in visparticles:
        p4 += p.p4()
    return p4



def finalDaughters(particle, daughters):
    '''Fills daughters with all the daughters of particle.
    Recursive function.'''
    if particle.numberOfDaughters() == 0:
        daughters.append(particle)
    else:
        foundDaughter = False
        for i in range( particle.numberOfDaughters() ):
            dau = particle.daughter(i)

#            if dau.status() >= 2:
            if dau.status() >= 1:
                daughters = finalDaughters( dau, daughters )
                foundDaughter = True
        if not foundDaughter:
            daughters.append(particle)
    
    return daughters



def tauDecayMode(tau):
    
    unstable = True
    
    dm = 'tau'
    final_daughter = tau
    
    while unstable:
        nod = tau.numberOfDaughters()
        for i in range(nod):
            dau = tau.daughter(i)
            if abs(dau.pdgId()) == 11 and dau.status() == 1:
                dm = 'ele'
                final_daughter = dau
                unstable = False
                break
            elif abs(dau.pdgId()) == 13 and dau.status() == 1:
                dm = 'muon'
                final_daughter = dau
                unstable = False
                break
            elif abs(dau.pdgId()) == 15: #taus may do bremsstrahlung
                dm = 'tau'
                final_daughter = dau
                tau = dau # check its daughters
                break
            elif abs(dau.pdgId()) not in (12, 14, 16):
                unstable = False
                break
            else:
                pass
            
    return final_daughter, dm



def returnDecayMode(decay1, decay2):
    if decay1 == 'ele' and decay2 == 'ele':
        return 5, 'ee'
    elif decay1 == 'muon' and decay2 == 'muon':
        return 3, 'mm'
    elif (decay1 == 'ele' and decay2 == 'muon') or (decay1 == 'muon' and decay2 == 'ele'):
        return 4, 'em'
    elif (decay1 == 'tau' and decay2 == 'ele') or (decay1 == 'ele' and decay2 == 'tau'):
        return 2, 'et'
    elif (decay1 == 'tau' and decay2 == 'muon') or (decay1 == 'muon' and decay2 == 'tau'):
        return 1, 'mt'
    elif decay1 == 'tau' and decay2 == 'tau':
        return 0, 'tt'
    else:
        return -1, 'anything'



gStyle.SetOptStat(11111)
decaydict = {'ele':0, 'muon':1, 'tau':2}

# open file
infile = ""
outfile = ""
location = "root://eoscms.cern.ch//eos/cms/store/cmst3/user/ytakahas/LowMass/DR/"
if len(sys.argv) > 1: infile = location + sys.argv[1]
else: infile = "root://eoscms.cern.ch//eos/cms/store/cmst3/user/ytakahas/LowMass/DR/DR_1.root"
print ">>> get file: \"%s\"" % (infile)
events = Events(infile)

if len(sys.argv) == 3: outfile = TFile(sys.argv[2], 'recreate')
else: outfile = TFile('validation.root', 'recreate')

nbin = 10000

event_tree = TTree('per_event','per_event')
mother_tree = TTree('per_mother','per_mother')
decay_tree = TTree('per_decay','per_decay')

mother_inv = num.zeros(1, dtype=float)
mother_mass = num.zeros(1, dtype=float)
mother_pdg = num.zeros(1, dtype=float)
mother_pt = num.zeros(1, dtype=float)
mother_eta = num.zeros(1, dtype=float)
mother_phi = num.zeros(1, dtype=float)
mother_ndaughter = num.zeros(1, dtype=int)
mother_dphi_ll = num.zeros(1, dtype=float)
mother_deta_ll = num.zeros(1, dtype=float)
mother_dr_ll = num.zeros(1, dtype=float)
mother_dr_tm = num.zeros(1, dtype=float)

decay_mother_m = num.zeros(1, dtype=float)
decay_pdgId = num.zeros(1, dtype=int)
decay_pt = num.zeros(1, dtype=float)
decay_eta = num.zeros(1, dtype=float)
decay_phi = num.zeros(1, dtype=float)
decay_vispt = num.zeros(1, dtype=float)
decay_type = num.zeros(1, dtype=int)

mother_tree.Branch('mother_pdg', mother_pdg, 'mother_pdg/D')
mother_tree.Branch('mother_pt', mother_pt, 'mother_pt/D')
mother_tree.Branch('mother_eta', mother_eta, 'mother_eta/D')
mother_tree.Branch('mother_phi', mother_phi, 'mother_phi/D')
mother_tree.Branch('mother_mass', mother_mass, 'mother_mass/D')
mother_tree.Branch('mother_inv', mother_inv, 'mother_inv/D')
mother_tree.Branch('mother_ndaughter', mother_ndaughter, 'mother_ndaughter/I')
mother_tree.Branch('mother_dphi_ll', mother_dphi_ll, 'mother_dphi_ll/D')
mother_tree.Branch('mother_deta_ll', mother_deta_ll, 'mother_deta_ll/D')
mother_tree.Branch('mother_dr_ll', mother_dr_ll, 'mother_dr_ll/D')
mother_tree.Branch('mother_dr_tm', mother_dr_tm, 'mother_dr_tm/D')

decay_tree.Branch('decay_mother_m', decay_mother_m, 'decay_mother_m/D')
decay_tree.Branch('decay_pdgId', decay_pdgId, 'decay_pdgId/I')
decay_tree.Branch('decay_pt', decay_pt, 'decay_pt/D')
decay_tree.Branch('decay_eta', decay_eta, 'decay_eta/D')
decay_tree.Branch('decay_phi', decay_phi, 'decay_phi/D')
decay_tree.Branch('decay_vispt', decay_vispt, 'decay_vispt/D')
decay_tree.Branch('decay_type', decay_type, 'decay_type/I')

handle  = Handle ('std::vector<reco::GenParticle>')
#label = ("prunedGenParticles")
label = ("genParticles")


def isFinal(p):
    return not (p.numberOfDaughters() == 1 and p.daughter(0).pdgId() == p.pdgId())


evtid = 0
for ev in events:
    
    evtid += 1
    if evtid==100000: break
    
    ev.getByLabel(label, handle)
    gps = handle.product()
    #gps_mother = [p for p in gps if isFinal(p) and abs(p.pdgId()) in [24, 25]]  # H -> tau tau
    gps_mother = [p for p in gps if isFinal(p) and abs(p.pdgId()) in [7000021]] # X -> tau tau 
    
    for p in gps_mother:       
        
        nother = 0
        pair = [ ]
        decaytype = [ ]
        muons = [ ]
        taush = [ ]
        nmuon = 0
        
        for i in range(p.numberOfDaughters()):
            
            tau = p.daughter(i)
            
            #if abs(tau.pdgId()) == 16: continue
            if abs(tau.pdgId()==15):
                while tau.status()!=2:
                    tau = tau.daughter(0)
                    
                if tau.status()!=2:
                    print 'NOT POSSIBLE !!!', tau.status(), tau.pdgId()    
            
            pair.append(tau.p4())
            decay_mother_m[0] = p.mass()
            decay_pdgId[0] = tau.pdgId()
            decay_pt[0] = tau.pt()
            decay_eta[0] = tau.eta()
            decay_phi[0] = tau.phi()
            
            if abs(tau.pdgId())==15: 
                finDaughters = finalDaughters(tau, [ ])
                (daughter,decaymode) = tauDecayMode(tau)
                decay_type[0] = decaydict[decaymode]
                visible_pt = p4sumvis(finDaughters).pt()
                
                #print decaymode, 'vis pt = ', visible_pt , 'tau pt = ', tau.pt()
                if (visible_pt > tau.pt()): print 'Warning! visible_pt > tau.pt()'
                
                decay_vispt[0] = visible_pt
                decaytype.append(decaymode)
                
                # save muons and hadronic taus
                if   decaymode == "muon":   muons.append(daughter)
                elif decaymode == "tau":    taush.append(tau)
                
            decay_tree.Fill()
        
        if(len(pair)==2):
            inv = (pair[0] + pair[1]).mass()
            mother_inv[0] = inv
            mother_dphi_ll[0] = deltaPhi(pair[0].phi(), pair[1].phi())
            mother_deta_ll[0] = pair[0].eta() - pair[1].eta()
            mother_dr_ll[0] = deltaR(pair[0].eta(), pair[0].phi(), pair[1].eta(), pair[1].phi())
            if(len(muons) == 1 and len(taush) == 1):
                mother_dr_tm[0] = deltaR(taush[0].eta(), taush[0].phi(), muons[0].eta(), muons[0].phi())
            else: mother_dr_tm[0] = -9
            
        else:
            mother_inv[0]     = -1
            mother_dphi_ll[0] = -9
            mother_deta_ll[0] = -9
            mother_dr_ll[0]   = -9
            mother_dr_tm[0]   = -9
        
        
        mother_pdg[0]  = p.pdgId()
        mother_mass[0] = p.mass()
        mother_pt[0]   = p.pt()
        mother_eta[0]  = p.eta()
        mother_phi[0]  = p.phi()
        mother_ndaughter[0] = len(pair)
        
        mother_tree.Fill()
        

print evtid, 'events processed'

outfile.Write()
outfile.Close()
