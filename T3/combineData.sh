#! /bin/bash

BASEDIR="/scratch/ineuteli/SFrameAnalysis/AnalysisOutput/"
VETO="_24"
RUN_LABEL="Run2017"
LABEL="_2017" #"_Moriond"
FINAL_LABEL="${LABEL}"

DATA_SET="MuEle"
[[ $1 == *m* ]] && DATA_SET="Mu"
[[ $1 == *e* ]] && DATA_SET="Ele"

echo
echo ">>> working in ${BASEDIR}"
cd ${BASEDIR}

echo
[[ $DATA_SET == *Mu* ]] && echo ">>> hadd SingleMuon" &&
ls -lt SingleMuon/*_${RUN_LABEL}?${LABEL}.root && echo &&
hadd -f SingleMuon/TauTauAnalysis.SingleMuon_${RUN_LABEL}${FINAL_LABEL}.root SingleMuon/TauTauAnalysis.SingleMuon_${RUN_LABEL}?${LABEL}.root ||
echo ">>> Warning! Could not find SingleMuon root files!"
echo
[[ $DATA_SET == *Ele* ]] && echo ">>> hadd SingleElectron" &&
ls -lt SingleElectron/*_${RUN_LABEL}?${LABEL}.root && echo &&
hadd -f SingleElectron/TauTauAnalysis.SingleElectron_${RUN_LABEL}${FINAL_LABEL}.root SingleElectron/TauTauAnalysis.SingleElectron_${RUN_LABEL}?${LABEL}.root ||
echo ">>> Warning! Could not find SingleElectron root files!"
echo

