#!/bin/bash

PATH="/pnfs/psi.ch/cms/trivcat/store/user/ineuteli/samples/tt_bbWW_delphes"
MISSING_FILES=""
N=0

for i in {1..300}; do
  FILE="tt_bbWW_$i.root"
  if test ! -e $PATH/$FILE; then
    MISSING_FILES="$MISSING_FILES\n>>>   $FILE"
    let N=N+1
  fi
done

if [[ $N > 0 ]]; then
  echo -e ">>> files missing in $PATH:$MISSING_FILES"
  echo `echo $MISSING_FILES | sed -r 's/.*_([0-9]*)\..*/\1,/g' | tr '\n' ' '`
else
  echo ">>> no missing files!"
fi