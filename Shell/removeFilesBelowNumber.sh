#!/bin/bash

FILES="*.e* *.o*"

for f in $FILES; do
  n=`echo $f | sed -r 's/.*e([0-9]*)/\1/g'`
  if [[ $n < 3813100 ]]; then
    echo $f
  fi
done