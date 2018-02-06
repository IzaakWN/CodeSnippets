#! /bin/bash


DIRS=`ls -d LowMassDiTau_M-*_MB-*_*`

for dir in $DIRS; do

  printf "\n>>> $dir\n"  
  OUT="$dir/$dir.lhe"
  ls $dir/*lhe > list.txt
  ./mergeLheFiles list.txt $OUT   

done;

echo

