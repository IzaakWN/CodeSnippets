#! /bin/bash

# https://indico.cern.ch/event/577649/contributions/2388797/attachments/1380376/2098158/HComb-Tutorial-Nov16-Impacts.pdf
# -t -1     Asimov dataset (data = background)
# combine -M ProfileLikelihood -m 28 --significance -t -1 --expectSignal=1 $WORKSPACE
# combine -M MaxLikelihoodFit  -m 28 --significance -t -1 --expectSignal=1 $WORKSPACE
# combine $OPTIONS --freezeNuisanceGroups $FREEZE -n $NAME -M MultiDimFit -m $MASS --algo grid --points 50 --redefineSignalPOIs r --setPhysicsModelParameterRanges r=-10,10 --robustFit 1 $WORKSPACE

# SET INPUT
PROCESS="xtt"
CHANNELS="mt et #em"
MASSES="20 #28 #40 #50 #60 #70"
BINS="1 2"
LABEL="_Opt_Asimov" #_Asimov #dphi2p5 #Dzeta-40_mt #_weighted" #_Opt
if [[ $LABEL == *bbA* ]]; then
  MASSES="25 30 35 40 45 50 55 60 65 70"
  BINS="1"
elif [[ $LABEL == *dphi* ]]; then
  BINS="2"
fi

# USER INPUT
DO_COMB=0
while getopts c option; do
  [ ${option} = c ] && DO_COMB=1; # combine cards
done

# SCRIPTS
DIR="/shome/ineuteli/analysis/CMSSW_7_4_8/src/CombineHarvester/LowMassTauTau"
HARV="./harvestDatacards_LowMassDiTau.py"
WORK="text2workspace.py" #"../../../HiggsAnalysis/CombinedLimit/scripts/text2workspace.py"
COMB="combineCards.py" #"../../../HiggsAnalysis/CombinedLimit/scripts/combineCards.py"
HARV_OPTS="-f \"${LABEL}\""
#[[ $CHANNELS == *[^\#]mt* ]]

# MAIN ROUTINE
function main {

  # SETUP CARDS
  cd $DIR
  echo
  #peval "rm -r output/"
  header "Harvest datacards"
  peval "python $HARV $HARV_OPTS" || exit 1
  cd "$DIR/output"

  # LOOP over CHANNEL
  for channel in $CHANNELS; do
    [[ $channel == "#"* ]] && continue
    
    # LOOP over MASSES
    for mass in $MASSES; do
      [[ $mass == "#"* ]] && continue
    
      #PROC_OPTS="-m $mass --expectSignal=1" # --significance
      PROC_OPTS="-m $mass  -t -1 --expectSignal=1" # --significance
      
      # LOOP over BINS
      for bin in $BINS; do
          [[ $bin == "#"* ]] && continue
          header "${channel}: combine for bin $bin, mass $mass"
          
          BIN_LABEL="${channel}-${bin}"
          [[ $LABEL ]] && BIN_LABEL+="${LABEL}"
          DATACARD="xtt_${BIN_LABEL}-13TeV-${mass}.txt"
          WORKSPACE="xtt_${BIN_LABEL}-13TeV-${mass}.root"
        
          peval "$WORK -m $mass $DATACARD -o $WORKSPACE" || exit 1
          echo "$TB # upper limit # $E"
          peval "combine -M Asymptotic -n .${BIN_LABEL} $PROC_OPTS $WORKSPACE" || exit 1 #FitDiagnostics
          #echo "$TB # upper limit #"
          #peval "combine -M ProfileLikelihood -n .${BIN_LABEL} $PROC_OPTS $WORKSPACE"
          #echo "$TB # upper limit #"
          #peval "combine -M MaxLikelihoodFit -n .${BIN_LABEL} $PROC_OPTS $WORKSPACE"

      done
    done
  done;
  
  
  
  [ $DO_COMB -lt 1 ] && return 0 # skip unless -c flag
  cd "$DIR/output"
  for mass in $MASSES; do
    [[ $mass == "#"* ]] && continue
    header "combined: running combine for all bins, mass $mass"
    
    BIN_LABEL="combined"
    BIN_LABELS="*[^combined]"
    DATACARD="xtt_${BIN_LABEL}${LABEL}-13TeV-${mass}.txt"
    DATACARDS="xtt_${BIN_LABELS}${LABEL}-13TeV-${mass}.txt"
    WORKSPACE="xtt_${BIN_LABEL}${LABEL}-13TeV-${mass}.root"
    PROC_OPTS="-m $mass -t -1 --expectSignal=1"
    
    #DATACARDS=`ls $DATACARDS | grep -v combined`
    peval "$COMB $DATACARDS > $DATACARD"
    peval "$WORK -m $mass $DATACARD -o $WORKSPACE"
    echo "$TB # upper limit # $E"
    peval "combine -M Asymptotic -n .${BIN_LABEL}${LABEL} $PROC_OPTS $WORKSPACE"

  done;
}



# PRINT
A="$(tput setab 0)$(tput setaf 7)"
R="$(tput setab 0)$(tput bold)$(tput setaf 1)"
E="$(tput sgr0)"
TB=">>>
>>>$A"
TB2=" 

>>>$A"

function peval {
  echo -e ">>> $(tput setab 0)$(tput setaf 7)$@$(tput sgr0)"
  eval "$@";
}

function header {
  local HDR="$@"
  local BAR=`printf '#%.0s' $(seq 1 ${#HDR})`
  echo " "
  echo " "
  echo "$TB     $A####${BAR}####$E"
  echo ">>>     $A#   ${HDR}   #$E"
  echo ">>>     $A####${BAR}####$E"
  echo ">>> ";
}



# RUN
main
echo "$TB done $E"
echo

exit 0
