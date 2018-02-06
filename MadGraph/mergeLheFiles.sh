#! /bin/bash

DIRS=`ls -d LowMassDiTau_M-*_MB-*_*`
G="\e[37m"
S="\e[0m"

for dir in $DIRS; do

  printf "\n>>> ${G}${dir}${S}\n"  
  OUT="$dir/$dir.lhe"
  ls $dir/*lhe > list.txt
  ./mergeLheFiles list.txt $OUT   

done;

echo

