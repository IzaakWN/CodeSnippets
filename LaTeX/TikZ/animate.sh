#! /bin/bash
# Author: Izaak Neutelings (July 2021)
# Description: Animate pages in PDFs to GIF

function peval { echo -e ">>> $@"; eval "$@"; }

RESO="1000" # GIF DPI resolution
DELAY="200" # GIF delay
FIRST=-1 # first index
VERBOSE=0
while getopts 'd:i:r:v' option; do
  case "${option}" in
    d) DELAY=${OPTARG};;
    i) FIRST=${OPTARG};;
    r) RESO=${OPTARG};;
    v) VERBOSE=1;;
  esac
done
shift $((OPTIND-1))
PDFS=$@

if [[ $VERBOSE -gt 0 ]]; then
  echo ">>> PDFS=$PDFS"
  echo ">>> RESO=$RESO"
  echo ">>> DELAY=$DELAY"
fi
for pdf in $PDFS; do
  [[ ! $pdf = *".pdf" ]] && echo ">>> Warning! Invalid input: $pdf! Ignoring..." && continue
  NPAGES="$(identify $pdf | wc -l | xargs)" #`identify -format "%n" $pdf` # number of pages
  [[ $NPAGES -lt 2 ]] && echo ">>> Warning! Not enough pages in $pdf! Ignoring..." && continue
  GIF="${pdf/%.pdf/.gif}"
  if [[ $FIRST -gt 0 ]]; then
    [[ $FIRST -gt $NPAGES ]] && echo ">>> Warning! Not enough pages in $pdf to start at index $FIRST! Ignoring..." && continue
    PDF=$pdf # "naked pdf name"
    pdf=""
    INDICES=`seq $((FIRST-1)) $NPAGES | xargs`
    [[ $FIRST -gt 1 ]] && INDICES+=" $(seq 0 $((FIRST-2)) | xargs)"
    [[ $VERBOSE -gt 0 ]] && echo ">>> FIRST=$FIRST, NPAGES=$NPAGES, INDICES=$INDICES"
    for i in $INDICES; do
      pdf+="$PDF[$i] "
    done
    [[ $VERBOSE -gt 0 ]] && echo ">>> pdf='$pdf'"
  fi
  OPTS="-verbose -delay $DELAY -loop 0 -density $RESO -despeckle -dispose previous"
  peval "convert $OPTS $pdf -resize $RESO -coalesce -layers optimize $GIF"
done
