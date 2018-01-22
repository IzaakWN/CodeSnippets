#! /bin/bash

OUTPUT="ineuteli/analysis/SFrameAnalysis/AnalysisOutput"
PNFS_OUTPUT="root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/$OUTPUT"

cd "/scratch/$OUTPUT"
FILES=""
FILES0=`ls */*.root`
IGNORE="EES TES LTF"
SELECT=""
GREP=""

for pattern in $IGNORE; do
  FILES0=`ls $FILES0 | grep -v $pattern`
done

[[ ! $SELECT ]] && FILES=$FILES0
for pattern in $SELECT; do
  FILES+=" "`ls $FILES0 | grep $pattern`
done

i=0
N=`echo $FILES | wc -w`
for f in $FILES; do
  i=$((i+1))
  COMMAND="xrdcp -f $f ${PNFS_OUTPUT}/$f"
  echo
  echo ">>> ${i}/${N}: ${f}"
  echo ">>> $COMMAND"
  $COMMAND
done
echo

