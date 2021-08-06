#! /bin/bash
# Author: Izaak Neutelings (July 2021)
# Description: Convert all PDFs to PNG (if none pre-exists)

function peval { echo -e ">>> $@"; eval "$@"; }

ANIMATE=0
PAGE=0
PNG_RESO="400" #  PNG DPI resolution
GIF_RESO="1000" # GIF DPI resolution
DELAY="200" # GIF delay
VERBOSE=0
while getopts 'ad:i:r:v' option; do
  case "${option}" in
    a) ANIMATE=1;;
    d) DELAY=${OPTARG};;
    i) PAGE=${OPTARG};;
    r) RESO=${OPTARG};;
    v) VERBOSE=1;;
  esac
done
shift $((OPTIND-1))
[ "$@" ] && PDFS=$@ || PDFS="*.pdf"

if [[ $VERBOSE -gt 0 ]]; then
  echo ">>> PDFS=$PDFS"
  echo ">>> RESO=$RESO"
  echo ">>> DELAY=$DELAY"
  echo ">>> ANIMATE=$ANIMATE"
fi
for pdf in $PDFS; do
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
    peval "convert -density $PNG_RESO -trim ${pdf}[$PAGE] $png" # convert to PNG
  fi
done

for pdf in $PDFS; do
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
