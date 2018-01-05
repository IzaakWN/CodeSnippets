#!/bin/bash

#rm test.txt
#grep source CMS_PhaseII_Substructure_PIX4022_200PU.tcl >> test.txt
CARD="CMS_PhaseII_Substructure_PIX4022_200PU.tcl"
PATTERN="source"
FILES=`grep "$PATTERN" $CARD | sed "s~$PATTERN~~g" | uniq`

echo $FILES

for f in $FILES; do
  echo ">>> replace with content from $f"
  sed -i "s~$PATTERN $f~$(sed -e 's/[\&/]/\\&/g' -e 's/$/\\n/' $f | tr -d '\n')~g" "$CARD"
done