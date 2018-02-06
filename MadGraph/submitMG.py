#! /usr/bin/env python
# 
# Creating dir:
#   uberftp t3se01.psi.ch 'mkdir /pnfs/psi.ch/cms/trivcat/store/user/ineuteli/samples/LowMassDiTau_madgraph'
# 
# Multicore jobs:
#   to submit multicore job:    qsub -pe smp 8 ...
#   in mg_configuration.txt:    run_mode=2 # multicore
#                               nb_core=8
#   note it might wait longer in queue
# 
# https://wiki.chipp.ch/twiki/bin/view/CmsTier3/Tier3Policies#Batch_system_policies
# 
# Luca vs. Izaak
#   https://www.diffchecker.com/JSVEi5qL

import os, sys
import subprocess
import time
from optparse import OptionParser

argv = sys.argv
usage = \
    '''This script will Delphes for differect samples'''
parser = OptionParser(usage=usage,epilog="Succes!")

parser.add_option("-t", "--test", dest="test", default=False, action='store_true',
                  help="run test sample(s)")
parser.add_option("-d", "--do-not-submit", dest="submit", default=True, action='store_false',
                  help="do not submit job to batch")
parser.add_option("-m", "--mock-submit", dest="submit", default=True, action='store_false',
                  help="do not submit job to batch (mock submit)")
parser.add_option("-N", "--n-events", dest="n_events", default=-1, action='store',
                  help="number of event to be generated in each job")
parser.add_option("-c", "--n-cores", dest="n_cores", default=2, action='store',
                  help="number of core in each job")
(opts, args) = parser.parse_args(argv)
# if len(argv) == 1:
#     parser.print_help()
#     sys.exit()

WORKPATH    = "/shome/ineuteli/production/MG5_aMC_v2_5_4"
DATAPATH    = "root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/ineuteli/samples/"
samples     = ["LowMassDiTau"]      # "LowMassDiTau8TeV", "LowMassDiMuon8TeV", "LowMassDiMuon"
queue       = "short.q"             # all.q (10h), short.q (90 min.)
n_cores     = opts.n_cores          # "nb_core" in input/mg5_configuration.txt should be the same number!
n_events    = opts.n_events         # number of events to be generated
masses      = [ 50, 60 ] #20, 28, 40 ] #40, 50, 60, 70 ] # leave empty if you do not want to change the mass
massesB     = [ 300 ]          # leave empty if you do not want to change the mass
pt_l_min    = 18                    # minimum pt of first two leptons
first_index =  1
last_index  =  6
indices     = range( first_index, last_index + 1 )



def main():
    global samples, n_cores, n_events, masses, massesB, pt_l_min, indices
    
    if opts.test:
      queue    = "debug.q"
      n_events = 100
      indices  = [4,5]
    
    if len(masses)==0:
      masses = [ -1 ] # no change of mass
    
    if len(massesB)==0:
      massesB = [ -1 ] # no change of mass
    
    # ensure directory
    REPORTDIR = "%s/submitMG"%(WORKPATH)
    if not os.path.exists(REPORTDIR):
      os.makedirs(REPORTDIR)
      print ">>> made directory %s\n>>>"%(REPORTDIR)
    
    for sample in samples:
      for massB in massesB:
        for mass in masses:
          for index in indices:
            submitSample(sample,index,M=mass,MB=massB,N=n_events,ptlmin=pt_l_min)
            print ">>> "



def submitSample(sample,index,M=-1,MB=-1,N=-1,ptlmin=-1):
    jobname = "%s"%(sample)
    options = ""
    if M>0:
      jobname = "%s_M-%s"%(jobname,M)
      options = "%s -M %s"%(options,M)
    if MB>0:
      jobname = "%s_MB-%s"%(jobname,MB)
      options = "%s -B %s"%(options,MB)
    if ptlmin>0:
      jobname = "%s_FilterLep%s"%(jobname,ptlmin)
      options = "%s -l %s"%(options,ptlmin)
    if N>0:
      options = "%s -N %s"%(options,N)
    if n_cores>0:
      options = "%s -c %s"%(options,n_cores)
    jobname = "%s_%d"%(jobname,index)
    options = options.lstrip(' ')
    command = "qsub -q %s -pe smp %d -N %s submitMG.sh %s %s %s" % (queue,n_cores,jobname,sample,index,options)
    print ">>> %s"%(command.replace(jobname,"\033[;1m%s\033[0;0m"%jobname,1))
    if not opts.submit: return
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    os.system(command)
    


def printColums(list):
    N = len(list)
    if N%4: list.extend( [" "]*(4-N%4) ); N = len(list)
    for row in zip(list[:N/4],list[N/4:N/2],list[N/2:N*3/4],list[N*3/4:]):
        print ">>> %18s %18s %18s %18s" % row
    


def proceed(prompt=">>> proceed?",proceed_message=">>> proceeding...",stop_message=">>> stop"):
    proceed_ = False
    while True:
        answer = raw_input(prompt+" (y or n) ").lower()
        if answer.lower() in [ 'y', 'ye', 'yes', 'yeah', 'yep', 'jep' ]:
            print proceed_message
            proceed_ = True
            break
        elif answer.lower() in [ 'n', 'no', 'na', 'nah', 'nee', 'neen', 'nop' ]:
            print stop_message
            proceed_ = False
            break
        else:
            print ">>> incorrect input"
            continue
    return proceed_
    


if __name__ == '__main__':
    print "\n>>> "
    main()
    print ">>> done\n"


