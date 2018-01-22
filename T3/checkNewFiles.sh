#! /bin/bash

BASEDIR="/scratch/ineuteli/SFrameAnalysis/AnalysisOutput"
LABEL="Moriond"
VETO="(EES|TES|LTF)"

echo ">>> PWD: $BASEDIR"
cd $BASEDIR
ls -hlr --sort=time */*root | grep $LABEL | grep -Pv $VETO | \
  while read c1 c2 c3 c4 c5 c6 c7 c8 c9; do
    printf "%4s %3s %s %5s %s\n" $c7 $c6 $c8 $c5 $c9;
  done

