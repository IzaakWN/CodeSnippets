#! /bin/bash
# Author: Izaak Neutelings (January 2018)

echo
BASEDIR="/Users/IWN/Downloads"
DIR1="$BASEDIR/Summer16_23Sep2016V3_MC"
DIR2="$BASEDIR/Summer16_23Sep2016V4_MC"
PRINT=1

for f1 in `ls $DIR1`; do
  f2=`echo $f1 | sed 's,V3,V4,'`
  p1="$DIR1/$f1"
  p2="$DIR2/$f2"
  ND=`diff $p1 $p2 | wc -l | xargs printf`
  printf "%4s diff(s) >>> %s vs.\n" "$ND" "$f1"
  printf "                 %s\n" "$f2"
  if [ $ND -gt 0 -a $PRINT -gt 0 ]; then
    diff $p1 $p2
    printf "\n\n"
  fi
done

echo
