#! /bin/bash

# https://indico.cern.ch/event/577649/contributions/2388797/attachments/1380376/2098158/HComb-Tutorial-Nov16-Impacts.pdf
# -t -1     Asimov dataset (data = background)
# combine -M ProfileLikelihood -m 28 --significance -t -1 --expectSignal=1 $WORKSPACE
# combine -M MaxLikelihoodFit  -m 28 --significance -t -1 --expectSignal=1 $WORKSPACE
# combine $OPTIONS --freezeNuisanceGroups $FREEZE -n $NAME -M MultiDimFit -m $MASS --algo grid --points 50 --redefineSignalPOIs r --setPhysicsModelParameterRanges r=-10,10 --robustFit 1 $WORKSPACE

NAMES=( ) #lumi -norm -eff -TES -LTF -Zpt -TTpt -WJ -QCD)
FREEZES=(`echo ${NAMES[@]} | sed "s/-/,/g"`)
COLORS=(2 4 2 6 8 10 12 14 16 18 3 5 7)
S_EXPS=(    1    ) #  283  )
RANGES=("-5,9" "200,380") # range of signal strength to help combine
#RANGES=("-2,4" "200,380") # range of signal strength to help combine - thesis
CHANNELS="mt et combined"
MASSES="28"
BINS="1 2"
LABEL="" #dphi2p5 #Dzeta-40_mt #_weighted" #_Opt
if [[ $LABEL == *bbA* ]]; then
  MASSES="40"
  BINS="1"
  RANGES=("-80,90" "200,380")
fi
FIGURES=""

# SCRIPTS
DIR="/shome/ineuteli/analysis/CMSSW_7_4_8/src/CombineHarvester/LowMassTauTau"
HARV="./LowMassDiTau_Harvester.py"
WORK="../../../HiggsAnalysis/CombinedLimit/scripts/text2workspace.py"
COMB="../../../HiggsAnalysis/CombinedLimit/scripts/combineCards.py"
IMPA="../../../CombineHarvester/CombineTools/scripts/combineTool.py"
PLOT_PARA="../../../CombineHarvester/CombineTools/scripts/plot1DScan.py"
PLOT_IMPA="../../../CombineHarvester/CombineTools/scripts/plotImpacts.py"
HARV_OPTS="-f \"${LABEL}\""


# MAIN ROUTINE
function main {
  
  cd $DIR
  header "Harvest datacards"
  peval "python $HARV $HARV_OPTS" || exit 1
  cd "$DIR/output"
  
  # LOOP over CHANNEL
  for channel in $CHANNELS; do
    [[ $channel == "#"* ]] && continue
    
    # LOOP over MASSES
    for mass in $MASSES; do
      [[ $mass == "#"* ]] && continue
      
      # LOOP over SIGNAL STRENGTH
      for ((s=0;s<${#S_EXPS[@]};++s)); do
        
        S_EXP=${S_EXPS[s]}
        RANGE=${RANGES[s]}
        METHOD="MultiDimFit" #"MultiDimFit" # "MaxLikelihoodFit"
        PROC_OPTIONS="-m $mass --significance -t -1 --expectSignal=$S_EXP"
        #COMB_OPTIONS="-M MultiDimFit --algo grid --points 30 --redefineSignalPOIs r --setPhysicsModelParameterRanges r=$RANGE $PROC_OPTIONS" #--robustFit 1 --saveWorkspace --setPhysicsModelParameterRanges r=-10,20  --rMin -10 --rMax 30
        #COMB_OPTIONS="-M MaxLikelihoodFit $PROC_OPTIONS"
        #COMB_OPTIONS_SNAP=`echo $COMB_OPTIONS | sed 's/--algo grid/--algo none/'`
        IMPA_OPTIONS="-M Impacts --robustFit 1 $PROC_OPTIONS"
        PLOT_OPTIONS="--logo CMS --logo-sub Preliminary --POI r" # --no-input-label
        
        # LOOP over BINS
        for bin in $BINS; do
            [[ $channel == *combined* ]] && [[ $bin == 2 ]] && continue
            
            SHEADER=""; [ $S_EXP != 1 ] && SHEADER=", signal strength ${S_EXPS[s]}"
            header "${channel}: combine for bin $bin, mass $mass$SHEADER"
            
            BIN_LABEL="${channel}-${bin}"
            [[ $channel == *combined* ]] && BIN_LABEL="$channel"
            [[ $S_EXP ]] && BIN_LABEL+="-S${S_EXP}" # S_EXP can be 0
            [[ $LABEL ]] && BIN_LABEL+="${LABEL}"
            DATACARD="xtt_${BIN_LABEL}-13TeV-${mass}.txt"
            WORKSPACE="xtt_${BIN_LABEL}-13TeV-${mass}.root" #`echo $DATACARD | sed "s/.txt/.root/"`
            FREEZE=""
            NAME=".freeze-"
            OTHERS=""
            
            [[ $channel == *"em"* ]] && [[ $bin == 1 ]] && RANGE="-70,90"
            [[ $channel == *"em"* ]] && [[ $bin == 2 ]] && RANGE="-90,130"
            COMB_OPTIONS="-M MultiDimFit --algo grid --points 30 --redefineSignalPOIs r --setPhysicsModelParameterRanges r=$RANGE $PROC_OPTIONS" #--robustFit 1 --saveWorkspace --setPhysicsModelParameterRanges r=-10,20  --rMin -10 --rMax 30
            
            peval "python $WORK -m $mass $DATACARD -o $WORKSPACE" || exit 1
            echo "$TB2 # best fit - snapshot # $E"
            peval "combine $COMB_OPTIONS --saveWorkspace -n .bestfit-${BIN_LABEL} $WORKSPACE" || exit 1
            echo "$TB2 # statistical - freeze all # $E"
            peval "combine $COMB_OPTIONS --freezeNuisances all -n .stat-${BIN_LABEL} $WORKSPACE" || exit 1
            echo "$TB2 # nominal # $E"
            peval "combine $COMB_OPTIONS -n .nominal-${BIN_LABEL} $WORKSPACE" || exit 1
            
            # FREEZE ONE BY ONE
            for ((j=0;j<${#NAMES[@]};++j)); do
                FREEZE=${FREEZE}${FREEZES[j]}
                NAME=${NAME}${NAMES[j]}
                LABEL=`echo ${FREEZE[j]} | sed "s/,/, /"`
                echo "$TB # freeze $FREEZE # $E"
                peval "combine $COMB_OPTIONS --freezeNuisanceGroups $FREEZE -n $NAME-${BIN_LABEL} $WORKSPACE" || exit 1
                OTHERS="${OTHERS} 'higgsCombine${NAME}-${BIN_LABEL}.${METHOD}.mH${mass}.root:Freeze ${LABEL}:${COLORS[j]}'"
            done
            
            OUTPUT_BESTFIT="higgsCombine.bestfit-${BIN_LABEL}.${METHOD}.mH${mass}.root"
            OUTPUT_STAT="'higgsCombine.stat-${BIN_LABEL}.${METHOD}.mH${mass}.root:Freeze all:2'"
            OUTPUT_NOMINAL="higgsCombine.nominal-${BIN_LABEL}.${METHOD}.mH${mass}.root"
            IMPA_NAME="impacts_${BIN_LABEL}"
            OUTPUT_IMPA="${IMPA_NAME}.json"
            FIG_OUT_DIR0="plots" #"${DIR}/plots_limit"
            FIG_OUT_DIR="../$FIG_OUT_DIR0" #"${DIR}/plots_limit"
            FIG_NAME="parabola_${BIN_LABEL}"
            FIG_NAME_STAT="parabola_stat_${BIN_LABEL}"
            #FIGURES="$FIGURES ${FIG_NAME_STAT}.png" #output/${FIG_NAME}.png
            
            # PLOT PARABOLA
            echo "$TB2 # parabola # $E"
            peval "python $PLOT_PARA $OUTPUT_BESTFIT -o $FIG_OUT_DIR/$FIG_NAME_STAT $PLOT_OPTIONS --others $OUTPUT_STAT --breakdown sys,stat" || exit 1
            [ $? -eq 0 ] && FIGURES="$FIGURES ${FIG_OUT_DIR0}/${FIG_NAME_STAT}.png"
            
            if [[ ${#NAMES} > 0 ]]; then
              peval "python $PLOT_PARA $OUTPUT_NOMINAL -o $FIG_OUT_DIR/$FIG_NAME $PLOT_OPTIONS --others $OTHERS --breakdown $FREEZE,stat" || exit 1
              [ $? -eq 0 ] && FIGURES="$FIGURES ${FIG_OUT_DIR0}/${FIG_NAME}.png"
            fi
            
            # RUN and PLOT IMPACTS
            echo "$TB2 # impacts #"
            peval "python $IMPA $IMPA_OPTIONS --doInitialFit -d $WORKSPACE" || exit 1
            #-o $OUTPUT_IMPA
            peval "python $IMPA $IMPA_OPTIONS --doFits --parallel 4 -d $WORKSPACE" || exit 1
            #-o $OUTPUT_IMPA
            peval "python $IMPA -M Impacts $PROC_OPTIONS -d $WORKSPACE -o $OUTPUT_IMPA" || exit 1
            peval "python $PLOT_IMPA -i $OUTPUT_IMPA -o $FIG_OUT_DIR/$IMPA_NAME"
            [ $? -eq 0 ] && FIGURES="$FIGURES ${FIG_OUT_DIR0}/${IMPA_NAME}.png"
            
        done;
      done;
    done;
  done;

  cd $DIR
  echo "$TB2$E made figures $A $FIGURES $E"
  echo ">>> eog $FIGURES";
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
  echo -e ">>> ${A}$@${E}"
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

