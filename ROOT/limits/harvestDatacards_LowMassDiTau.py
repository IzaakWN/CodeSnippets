#!/usr/bin/env python

from argparse import ArgumentParser
import CombineHarvester.CombineTools.ch as ch
from CombineHarvester.CombineTools.ch import CombineHarvester, MassesFromRange, SystMap, BinByBinFactory, CardWriter, SetStandardBinNames
import CombineHarvester.CombinePdfs.morphing as morphing
from CombineHarvester.CombinePdfs.morphing import BuildRooMorphing
from ROOT import RooWorkspace, TFile, RooRealVar
import ROOT
import os, sys

argv = sys.argv
description = '''This script makes datacards with CombineHarvester.'''
parser = ArgumentParser(prog="LowMassDiTau_Harvester",description=description,epilog="Succes!")
parser.add_argument( "-f", "--filelabel", dest="filelabel", type=str, default="", action='store',
                     metavar="FILELABEL", help="label for a file" )
parser.add_argument( "-m", "--mutau",     dest="doMutau",  default=False, action='store_true',
                                          help="run mutau" )
parser.add_argument( "-e", "--etau",      dest="doEtau",   default=False, action='store_true',
                                          help="run etau" )
parser.add_argument( "-v", "--verbose",   dest="verbose",  default=False, action='store_true',
                                          help="set verbose" )
args = parser.parse_args()

DIR_datacards   = "/shome/ineuteli/analysis/CMSSW_7_4_8/src/CombineHarvester/LowMassTauTau/datacards"
doMutau         = args.doMutau
doEtau          = args.doEtau
verbosity       = args.verbose
noShapes        = True #and False



def harvest(**kwargs):
    # http://cms-analysis.github.io/CombineHarvester/intro1.html
    # http://cms-analysis.github.io/CombineHarvester/python-interface.html
    # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/HTT.cpp
    # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc
    # vi ~/../ytakahas/work/Combination/CMSSW_7_4_8/src/CombineHarvester/TES/morph.py
    # bin 1: category_1_2
    # bin 2: category_2_2
    # combine -M Asymptotic -m 28 xtt_mt_1-13TeV-28.txt
    # combine -M ProfileLikelihood -m 28 --significance xtt_mt_1-13TeV-28.txt -t 10000 --expectSignal=1
    
    # SIGNAL mass & strength
    mass        = kwargs.get('mass',28)
    mass0       = kwargs.get('mass0',mass)
    filelabel   = kwargs.get('filelabel',"")
    label       = kwargs.get('label',"")
    signal      = "XTT-M%s" % (mass)
    if "bbA" in filelabel:
      signal    = "ATT-M%s" % (mass)
    
    channels = ['mt','et',] #'em']
    if doMutau and 'mt' not in channels: channels.append('mt')
    if doEtau  and 'et' not in channels: channels.append('et')
    processes = {   'signal'    : [ signal ],
                    'TT'        : [ 'TTT', 'TTJ', 'TTL' ], # Warning! emu only has TT
                    'DY'        : [ 'ZTT',  'ZJ',  'ZL' ],
                    'leptons_lt': [ 'ZL', 'ZJ', 'TTJ', 'VV'],
                    'leptons_em': [ 'ZTT', 'TT',  'VV'],
                    'VV'        : [  'WW',  'WZ',  'ZZ' ], # not needed as dibosons are already added into 'VV'
                }
    processes['background'] = { 'lt_noQCD': processes['TT'] + processes['DY'] + [ 'W', 'VV', 'ST'        ],
                                'mt':       processes['TT'] + processes['DY'] + [ 'W', 'VV', 'ST', 'QCD' ],
                                'et':       processes['TT'] + processes['DY'] + [ 'W', 'VV', 'ST', 'QCD' ],
                                'em_noQCD':          ['TT'] +          ['DY'] + [ 'W', 'VV', 'ST'        ],
                                'em':                ['TT'] +          ['DY'] + [ 'W', 'VV', 'ST', 'QCD' ],
                                }
    categories = [( 1, "category_1_2" ),
                  ( 2, "category_2_2" ),]
    if "bbA"  in filelabel: categories = [( 1, "category_bbA" ),]
    if "dphi" in filelabel: categories = [( 2, "category_2_2" ),]
    #masses = MassesFromRange("24-32:5")
    
    # HARVESTER
    harvester = CombineHarvester()
    for channel in channels:
        harvester.AddObservations( [str(mass)], ["xtt"], ["13TeV"], [channel], categories)
        harvester.AddProcesses(    [str(mass)], ["xtt"], ["13TeV"], [channel], processes['signal'],              categories, True )
        harvester.AddProcesses(    [str(mass)], ["xtt"], ["13TeV"], [channel], processes['background'][channel], categories, False)
        #harvester.AddProcesses(    ["*"], ["xtt"], ["13TeV"], [channel], processes['signal'],     categories, True)
    
    
    # NUISSANCE PARAMETERS
    print green(">>> defining nuissance parameters ...")
    nuissances = [
    
        # efficiencies
        ( ['mt','et',    ], [signal, 'ZTT', 'ZJ', 'ZL',  'VV', 'ST'],       'CMS_lumi',                             'lnN',   1.026  ),
        ( [          'em'], [signal, 'DY',               'VV', 'ST'],       'CMS_lumi',                             'lnN',   1.026  ),
        ( ['mt',         ], [signal, 'ZL',  'ZJ', 'TTJ', 'VV'],             'CMS_eff_m',                            'lnN',   1.02   ), # MU
        ( [          'em'], [signal, 'DY',        'TT',  'VV'],             'CMS_eff_m',                            'lnN',   1.02   ), # MU, emu only has 'TT'
        ( [     'et',    ], [signal, 'ZL',  'ZJ', 'TTJ', 'VV'],             'CMS_eff_e',                            'lnN',   1.02   ), # ELE
        ( [          'em'], [signal, 'DY',        'TT',  'VV'],             'CMS_eff_e',                            'lnN',   1.02   ), # ELE
        ( ['mt','et',    ], [signal, 'ZTT','TTT'],                          'CMS_eff_t',                            'lnN',   1.04   ), # TAU,   correlated
        ( ['mt','et',    ], [signal, 'ZTT','TTT'],                          'CMS_eff_t_$CHANNEL',                   'lnN',   1.03   ), # TAU, uncorrelated
        ( ['mt','et',    ], [signal]+processes['background']['lt_noQCD'],   'CMS_eff_trigger_$CHANNEL',             'lnN',   1.02   ), # trigger
        ( [          'em'], [signal]+processes['background']['em_noQCD'],   'CMS_eff_trigger_$CHANNEL',             'lnN',   1.02   ), # trigger
        
        # normalizations
        ( ['mt','et','em'], processes['DY'],                                'CMS_norm_DY',                          'lnN',   1.30   ),
        ( ['mt','et','em'], ['VV'],                                         'CMS_norm_VV',                          'lnN',   1.10   ),
        ( ['mt','et',    ], processes['TT'],                                'CMS_norm_TT',                          'lnN',   1.10   ),
        ( [          'em'],          ['TT'],                                'CMS_norm_TT',                          'lnN',   1.10   ), # emu only has 'TT'
        ( ['mt','et','em'], ['W'],                                          'CMS_norm_W',                           'lnN',   1.10   ),
        
        # QCD estimation
        ( ['mt','et','em'], ['QCD'],                                        'QCD_Yield_$CHANNEL_$ERA',              'lnN',   1.20   ),
        ( ['mt','et','em'], ['W'],                                          'QCD_extrap_$CHANNEL_$ERA',             'shape', 1.00   ),
        
        # energy scales
        ( ['mt','et',    ], [signal,'ZTT', 'TTT'],                          'CMS_xtt_shape_t_$CHANNEL_$ERA',        'shape', 1.00   ), # TES # don't split in DM
        ( [     'et',    ], [signal,'ZL',  'TTL'],                          'CMS_xtt_shape_e_$CHANNEL_$ERA',        'shape', 1.00   ), # EES
        ( [          'em'], [signal,'DY',  'TT' ],                          'CMS_xtt_shape_e_$CHANNEL_$ERA',        'shape', 1.00   ), # EES
        ( ['mt','et',    ], [signal]+processes['background']['lt_noQCD'],   'CMS_xtt_j_$CHANNEL_$ERA',              'lnN',   1.04   ), # JEC
        ( [          'em'], [signal]+processes['background']['em_noQCD'],   'CMS_xtt_j_$CHANNEL_$ERA',              'lnN',   1.04   ), # JEC
        ( ['mt','et',    ], [signal]+processes['background']['lt_noQCD'],   'CMS_xtt_UncEn_$CHANNEL_$ERA',          'lnN',   1.04   ), # Unclustering energy
        ( [          'em'], [signal]+processes['background']['em_noQCD'],   'CMS_xtt_UncEn_$CHANNEL_$ERA',          'lnN',   1.04   ), # Unclustering energy
        ( ['mt','et',    ], ['ZL'],                                         'CMS_xtt_ZLShape_$CHANNEL_$ERA',        'shape', 1.00   ), # LTF ES
        
        # b tag weight
        ( ['mt','et',    ], [signal]+processes['background']['lt_noQCD'],   'CMS_xtt_tag_b_$ERA',                   'lnN',   1.02   ), # ltau, heavy flavor
        ( [          'em'], [signal]+processes['background']['em_noQCD'],   'CMS_xtt_tag_b_$ERA',                   'lnN',   1.02   ), # emu,  heavy flavor
        ( ['mt','et',    ], [signal, 'W', 'VV', 'ST'] + processes['DY'],    'CMS_xtt_mistag_b_$ERA',                'lnN',   1.02   ), # ltau, light flavor, no TT
        ( [          'em'], [signal, 'W', 'VV', 'ST',             'DY'],    'CMS_xtt_mistag_b_$ERA',                'lnN',   1.02   ), # emu,  light flavor, no TT
        
        # fake tau rates
        ##( ['mt','et',    ], ['ZL'],                                         'CMS_norm_ZL',                          'lnN',   1.10   ), # 
        ##( [          'em'], ['DY'],                                         'CMS_norm_ZL',                          'lnN',   1.10   ), # 
        ( ['mt',         ], ['ZL','TTL'],                                   'CMS_mToTauFake',                       'lnN',   1.25   ), # LTF norm
        ( [     'et',    ], ['ZL','TTL'],                                   'CMS_eToTauFake',                       'lnN',   1.12   ), # LTF norm
        ( ['mt','et',    ], ['ZJ','TTJ'],                                   'CMS_jetToTauFake',                     'lnN',   1.20   ), # LTF norm
        
        # pt reweighting
        ( ['mt','et','em'], processes['TT'],                                'CMS_xtt_ttbarShape_$CHANNEL_$ERA',     'shape', 1.00   ), # TT pt reweighting
        ( ['mt','et','em'],          ['TT'],                                'CMS_xtt_ttbarShape_$CHANNEL_$ERA',     'shape', 1.00   ), # TT pt reweighting
        ( ['mt','et',    ], processes['DY'],                                'CMS_xtt_dyShape_$CHANNEL_$ERA',        'shape', 1.00   ), # Z  pt reweighting
        ( [          'em'],          ['ZTT'],                               'CMS_xtt_dyShape_$CHANNEL_$ERA',        'shape', 1.00   ), # Z  pt reweighting
        
    ]
    
    
    for channels0, processes0, parameter, shape, shift in nuissances:
        if noShapes and 'shape' in shape: continue
        harvester.cp().channel(channels0).process(processes0).AddSyst(harvester, parameter, shape, SystMap()(shift))
    
    # luminosity
#     #harvester.cp().process(processes['signal']+processes['background']
#     #                ).AddSyst(harvester, "CMS_eff", 'lnN', SystMap()(1.062))
#     harvester.cp().process(processes['signal']+['ZTT', 'ZJ', 'ZL', 'VV', 'ST']
#                    ).AddSyst(harvester, "CMS_lumi", 'lnN', SystMap()(1.026))
    
    # lepton efficiencies
#     harvester.cp().channel(['mt']
#                  ).process(processes['signal']+processes['leptons_lt']
#                  ).AddSyst(harvester, "CMS_eff_m", 'lnN', SystMap()(1.02))
#     harvester.cp().channel(['et']
#                  ).process(processes['signal']+processes['leptons_lt']
#                  ).AddSyst(harvester, "CMS_eff_e", 'lnN', SystMap()(1.02))
#     harvester.cp().channel(['em']
#                  ).process(processes['signal']+processes['leptons_lt']
#                  ).AddSyst(harvester, "CMS_eff_m", 'lnN', SystMap()(1.02))
#     harvester.cp().channel(['em']
#                  ).process(processes['signal']+processes['leptons_lt']
#                  ).AddSyst(harvester, "CMS_eff_e", 'lnN', SystMap()(1.02))
#     harvester.cp().channel(['mt','et']
#                  ).process(processes['signal']+['ZTT','TTT']
#                  ).AddSyst(harvester, "CMS_eff_t", 'lnN', SystMap()(1.04)) # correlated
#     for ch in ['mt','et']:
#         harvester.cp().channel([ch]
#                  ).process(processes['signal']+['ZTT','TTT']
#                  ).AddSyst(harvester, "CMS_eff_t_%s"%ch, 'lnN', SystMap()(1.03)) # uncorrelated
#     for ch in ['mt','et','em']:
#         harvester.cp().channel([ch]
#                  ).process(processes['signal']+processes['background']
#                  ).AddSyst(harvester, "CMS_eff_trigger_%s"%ch, 'lnN', SystMap()(1.02)) # uncorrelated
    
    # normalization
#     harvester.cp().channel(['mt'] #'et','em']
#                  ).process(processes['DY']
#                  ).AddSyst(harvester, "CMS_norm_DY", 'lnN', SystMap()(1.10))
#     harvester.cp().process(['VV'] #['WW','WZ','ZZ']
#                  ).AddSyst(harvester, "CMS_norm_VV", 'lnN', SystMap()(1.10))
#     harvester.cp().channel(['mt','et']
#                  ).process(['TTT','TTJ','TTL']
#                  ).AddSyst(harvester, "CMS_norm_tt", 'lnN', SystMap()(1.10))
#     harvester.cp().channel(['em']
#                  ).process(['TT'] # emu
#                  ).AddSyst(harvester, "CMS_norm_tt", 'lnN', SystMap()(1.10))
#     harvester.cp().process(['W']
#                  ).AddSyst(harvester, "CMS_norm_W",  'lnN', SystMap()(1.10))
    
    # systematic uncertainty
#     harvester.cp().process(['QCD']
#                  ).AddSyst(harvester, "QCD_Yield_$CHANNEL_$ERA", 'lnN', SystMap()(1.30))
#     harvester.cp().process(['W']
#                 ).AddSyst(harvester, "QCD_extrap_$CHANNEL_$ERA", 'shape', SystMap()(1.10))
    
    # TES
#     harvester.cp().channel(['mt','et']
#                  ).process(processes['signal']+['ZTT', 'TTT']
#                  ).AddSyst(harvester, "CMS_xtt_shape_t_$CHANNEL_$ERA", 'shape', SystMap()(1.00))
     
    # EES
#     harvester.cp().channel(['et']
#                  ).process(processes['signal']+processes['background']
#                  ).AddSyst(harvester, "CMS_shape_e_$CHANNEL_$ERA", 'shape', SystMap()(1.00))
    
    # JES
#     harvester.cp().channel(['et']
#                  ).process(processes['signal']+processes['background']
#                  ).AddSyst(harvester, "CMS_shape_j_$CHANNEL_$ERA", 'shape', SystMap()(1.00))
    
    # LTF
#     harvester.cp().channel(['mt','et']
#                  ).process(['ZL']
#                  ).AddSyst(harvester, "CMS_xtt_ZLShape_$CHANNEL_$ERA", 'shape', SystMap()(1.00))
#     harvester.cp().process(['ZL']
#                  ).AddSyst(harvester, "CMS_norm_ZL", 'lnN', SystMap()(1.03))
    
    # top reweighting
#     harvester.cp().channel(['mt','et']
#                  ).process(processes['TT']
#                  ).AddSyst(harvester, "CMS_xtt_ttbarShape_$CHANNEL_$ERA", 'shape', SystMap()(1.00))
    
    # Z pt reweighting
#     harvester.cp().channel(['mt','et']
#                  ).process(processes['DY']
#                  ).AddSyst(harvester, "CMS_xtt_dyShape_$CHANNEL_$ERA", 'shape', SystMap()(1.00))
    
    # EXTRACT SHAPES
    print green(">>> extracting shapes...")
    for channel in channels:
        filename = "%s/xtt_%s.inputs-LowMassDiTau-13TeV-%s%s.root" % (DIR_datacards,channel,mass0,filelabel)
        print ">>>   file %s" % (filename)
        harvester.cp().channel([channel]).backgrounds().ExtractShapes( filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")
        harvester.cp().channel([channel]).signals().ExtractShapes(     filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC") #$MASS
    
    # BIN STUFF
    print green(">>> generating bin by bin...")
    bbb_factory = BinByBinFactory()
    bbb_factory.SetAddThreshold(0.1)
    bbb_factory.SetMergeThreshold(0.5)
    bbb_factory.SetFixNorm(True)
    bbb_factory.MergeBinErrors(harvester.cp().backgrounds())
    bbb_factory.AddBinByBin(harvester.cp().backgrounds(), harvester)
    
    # NUISANCE PARAMETER GROUPS
    print green(">>> setting nuisance parameter groups...")
    harvester.SetGroup( "all",      [ ".*" ])
    harvester.SetGroup( "lumi",     [ "CMS_lumi" ])
    harvester.SetGroup( "eff",      [ "CMS_eff.*" ])
    harvester.SetGroup( "norm",     [ "CMS_norm_.*" ])
    harvester.SetGroup( "LTF",      [ "CMS_xtt_ZLShape_.*" ])
    harvester.SetGroup( "TES",      [ "CMS_xtt_shape_t_.*" ])
    harvester.SetGroup( "TTpt",     [ "CMS_xtt_ttbarShape_.*" ])
    harvester.SetGroup( "Zpt",      [ "CMS_xtt_dyShape_.*" ])
    harvester.SetGroup( "QCD",      [ "QCD_.*" ])
    #harvester.SetGroup(     "syst", [ ".*" ])
    #harvester.RemoveGroup(  "syst", [ "lumi_.*" ])
    
    # BIN NAMES
    print green(">>> setting format bin names...")
    SetStandardBinNames(harvester)  # formats every entry as {analysis}_{channel}_{bin_id}_{era}
    print green(">>> generating bin names...")
    bins = harvester.bin_set()      # generate set of bin names
    
    # PRINT
    if verbosity>0:
        print green("\n>>> print observation...\n")
        harvester.PrintObs()
        print green("\n>>> print processes...\n")
        harvester.PrintProcs()
        print green("\n>>> print systematics...\n")
        harvester.PrintSysts()
        print green("\n>>> print parameters...\n")
        harvester.PrintParams()
        print "\n"
    
    # WRITER
    print green(">>> writing datacards...")
    MASS = "$MASS"
    #if mass0 != mass:
    MASS = str(mass)
    datacardtxt  = "$TAG/$ANALYSIS_$CHANNEL-$BINID%s-$ERA-%s.txt"              % (filelabel,MASS)
    datacardroot = "$TAG/$ANALYSIS_$CHANNEL%s.input-LowMassDiTau-$ERA-%s.root" % (filelabel,MASS)
    print ">>>   %s"%(datacardtxt)
    print ">>>   %s"%(datacardroot)
    writer = CardWriter( datacardtxt, datacardroot)
    # writer.SetVerbosity(1)
    writer.WriteCards("output/", harvester)
    writer.SetWildcardMasses([ ])
    #for channel in harvester.channel_set():
    #    writer.WriteCards("output/" + channel, harvester.cp().channel([channel]))
    #output = TFile("output/xtt.input.root", 'RECREATE')
    
    #GetObservedRate() will sum the event yields of all remaining Observation objects
    #print ">>> Total observed rate: %s" % harvester.GetObservedRate()
    


def green(string,**kwargs): return "\x1b[0;32;40m%s\033[0m"%string
    


def main():
    
    filelabel = args.filelabel
    masses    = [28]
    if "bbA" in filelabel:
      masses    = range(25,71,5)
    else:
      masses    = [20,28,40,50,60,70]
    
    # NO MASS SCAN
    #harvest(mass0=28,filelabel=args.filelabel)
    
    # MASS SCAN
    for mass in masses:
      harvest(mass=mass,mass0=28,filelabel=filelabel)
    



if __name__ == '__main__':
    main()
    print ">>>\n>>> done\n"
    

