#! /bin/bash
# Author: Izaak Neutelings (July 2021)
# Description: Animate pages in PDFs to GIF

function peval { echo -e ">>> $@"; eval "$@"; }

PDFS=$@
RESO="1000" # GIF DPI resolution
DELAY="200" # GIF delay

for pdf in $PDFS; do
  [[ ! $pdf = *".pdf" ]] && echo ">>> Warning! Invalid input: $pdf! Ignoring..." && continue
  [[ `identify -format "%n" $pdf` -lt 2 ]] && echo "Warning! Not enough pages in $pdf! Ignoring..." && continue
  gif="${pdf/%.pdf/.gif}"
  OPTS="-verbose -delay $DELAY -loop 0 -density $RESO -despeckle -dispose previous"
  peval "convert $OPTS $pdf -resize $RESO -coalesce -layers optimize $gif"
done
