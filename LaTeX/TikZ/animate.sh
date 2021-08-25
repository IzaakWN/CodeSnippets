#! /bin/bash
# Author: Izaak Neutelings (July 2021)
# Description: Animate pages in PDFs to GIF
#set -e -o pipefail # exit script on error

function peval { echo -e ">>> $@"; eval "$@"; }

RESO="1200" # GIF DPI resolution
DELAY="200" # GIF delay
FIRST=0 # first index
WHITE=0 # deactivate alpha, white background
MAXNPAGES=-1
OPEN=0
VERBOSE=0
while getopts 'd:i:n:or:vw' option; do
  case "${option}" in
    w) WHITE=1;;
    d) DELAY=${OPTARG};;
    i) FIRST=${OPTARG};;
    n) MAXNPAGES=${OPTARG};;
    o) OPEN=1;;
    r) RESO=${OPTARG};;
    v) VERBOSE=1;;
  esac
done
shift $((OPTIND-1))
PDFS=$@
OPTS1="-delay $DELAY -loop 0 -density $RESO -despeckle -dispose previous"
OPTS2="-resize $RESO -coalesce -layers optimize" # -gravity center
[[ $VERBOSE -gt 0 ]] && OPTS1="-verbose $OPTS1"
[[ $WHITE -gt 0 ]] && OPTS2="-background white -alpha remove -alpha off $OPTS2"

if [[ $VERBOSE -gt 0 ]]; then
  echo ">>> PDFS=$PDFS"
  echo ">>> RESO=$RESO"
  echo ">>> DELAY=$DELAY"
  echo ">>> OPTS1=$OPTS1"
  echo ">>> OPTS2=$OPTS2"
fi
GIFS=""
for pdf in $PDFS; do
  echo ">>> "
  [[ ! $pdf = *".pdf" ]] && echo ">>> Warning! Invalid input: $pdf! Ignoring..." && continue
  NPAGES=$MAXNPAGES
  if [[ $NPAGES -lt 1 ]]; then # get npages from file
    NPAGES="$(identify $pdf | wc -l | xargs)" #`identify -format "%n" $pdf` # number of pages
    [[ ! "$NPAGES" ]] && echo ">>> Warning! Could not get PDF pages! Ignoring..." && continue
    [[ $NPAGES -lt 2 ]] && echo ">>> Warning! Not enough pages ($NPAGES) in $pdf! Ignoring..." && continue
  fi
  GIF="${pdf/%.pdf/.gif}"
  if [[ $FIRST -lt 0 || $FIRST -gt 1 ]]; then
    [[ $FIRST -gt $NPAGES ]] && echo ">>> Warning! Not enough pages in $pdf to start at index $FIRST! Ignoring..." && continue
    [[ $FIRST -lt 0 ]] && FIRST=$((NPAGES+1+FIRST))
    PDF=$pdf # "naked pdf name"
    pdf=""
    INDICES="$(seq $((FIRST-1)) $((NPAGES-1)) | xargs)"
    [[ $FIRST -gt 1 ]] && INDICES+=" $(seq 0 $((FIRST-2)) | xargs)"
    [[ $VERBOSE -gt 0 ]] && echo ">>> FIRST=$FIRST, NPAGES=$NPAGES, INDICES='$INDICES'"
    for i in $INDICES; do
      pdf+="$PDF[$i] "
    done
    pdf="$(echo $pdf | xargs)"
  fi
  [[ $VERBOSE -gt 0 ]] && echo ">>> pdf='$pdf'"
  peval "convert $OPTS1 $pdf $OPTS2 $GIF"
  GIFS+="$GIF "
done
echo ">>> "
if [[ "$GIFS" ]]; then
  echo ">>> Created $GIFS"
  peval "ls -hlt $GIFS"
  [[ $OPEN -gt 0 ]] && peval "open $GIFS"
else
  echo ">>> Could not create GIFs..."
fi
