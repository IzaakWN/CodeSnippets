#! /bin/bash
# Author: Izaak Neutelings (July 2021)
# Description: Convert all PDFs to PNG (if none pre-exists)

function peval { echo -e ">>> $@"; eval "$@"; }

ANIMATE=0
PNG_RESO="400" #  PNG DPI resolution
GIF_RESO="1000" # GIF DPI resolution
DELAY="200" # GIF delay

for pdf in *.pdf; do
  if [[ $ANIMATE -gt 0 && `identify -format "%n" $pdf` -gt 1 ]]; then # animate
    gif="${pdf/%.pdf/.gif}"
    [[ -e $gif ]] && continue
    OPTS="-verbose -delay $DELAY -loop 0 -density $GIF_RESO -despeckle -dispose previous"
    #peval "convert -verbose -delay $DELAY -loop 0 -density $GIF_RESO -dispose previous $pdf -coalesce -layers optimize $gif" # convert to animated GIF
    peval "convert $OPTS $pdf -resize $GIF_RESO -coalesce -layers optimize $gif"
  else
    png="${pdf/%.pdf/.png}"
    [[ -e $png ]] && continue
    #echo ">>> $pdf -> $png"
    peval "convert -density $RESO -trim ${pdf}[0] $png" # convert to PNG
  fi
done

for pdf in *.pdf; do
  tex="${pdf/%.pdf/.tex}"
  [[ ! -e $tex ]] && echo ">>> Warning! $pdf does not have a tex file $tex..."
  if [[ $ANIMATE -gt 0 && `identify -format "%n" $pdf` -gt 1 ]]; then # animate
    gif="${pdf/%.pdf/.gif}"
    [[ ! -e $gif ]] && echo ">>> Warning! Conversion to GIF failed for $pdf..."
  else
    png="${pdf/%.pdf/.png}"
    [[ ! -e $png ]] && echo ">>> Warning! Conversion to PNG failed for $pdf..."
  fi
done

for tex in *.tex; do
  png="${tex/%.tex/.png}"
  [[ -e $png ]] && continue
  echo ">>> Warning! $tex does not have a png!"
done
