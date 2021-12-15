#! /bin/bash
# Author: Izaak Neutelings (July 2021)
# Description: Convert all PDFs to PNG (if none pre-exists)
# Example: ./convert.sh -vwfA -r 800 -o pngs mechanics_stress.pdf
set -e -o pipefail # exit script upon first error

function peval { echo -e ">>> $@"; eval "$@"; }

PAGE=0 # PAGE TO CONVERT
MAXNPAGES=-1 # NUMBER OF PAGES
ANIMATE=0 # animate PDF pages
CONVERT_ALL=0 # convert each page
PNG_RESO="800" #  PNG DPI resolution
GIF_RESO="1000" # GIF DPI resolution
DELAY="200" # GIF delay
WIDTH=0 # maximum width
OUTPUT=""
OPTS=""
WHITE=0
FORCE=0
VERBOSE=0
while getopts 'Aad:fi:n:o:r:vW:w' option; do
  case "${option}" in
    A) CONVERT_ALL=1;; # convert each page
    a) ANIMATE=1;; # animate PDF pages
    d) DELAY=${OPTARG};;
    f) FORCE=1;;
    i) PAGE=${OPTARG};;
    n) MAXNPAGES=${OPTARG};;
    o) OUTPUT=${OPTARG};;
    r) PNG_RESO=${OPTARG}; GIF_RESO=${OPTARG};;
    v) VERBOSE=1;;
    w) WHITE=1;; # remove transparancy
    W) WIDTH=${OPTARG};;
  esac
done
shift $((OPTIND-1))
[[ "$@" ]] && PDFS="$@" || PDFS="*.pdf"

if [[ $VERBOSE -gt 0 ]]; then
  echo ">>>" `for i in {1..40}; do printf '-'; done`
  echo ">>> PDFS=$PDFS"
  echo ">>> OUTPUT=$OUTPUT"
  echo ">>> PAGE=$PAGE"
  echo ">>> MAXNPAGES=$MAXNPAGES"
  echo ">>> PNG_RESO=$PNG_RESO"
  echo ">>> GIF_RESO=$GIF_RESO"
  echo ">>> WIDTH=$WIDTH"
  echo ">>> DELAY=$DELAY"
  echo ">>> ANIMATE=$ANIMATE"
  echo ">>> CONVERT_ALL=$CONVERT_ALL"
  echo ">>> FORCE=$FORCE"
  echo ">>> WHITE=$WHITE"
  echo ">>> VERBOSE=$VERBOSE"
  echo ">>>" `for i in {1..40}; do printf '-'; done`
fi
[[ $OUTPUT != "" && ! -d $OUTPUT ]] && peval "mkdir $OUTPUT" # create output directory

for pdf in $PDFS; do
  NPAGES=$MAXNPAGES
  if [[ $NPAGES -lt 1 ]]; then # get npages from file
    #INFO=`identify $pdf 2>&1`
    #[[ $INFO = *"error"* ]] && echo ">>> ERROR: Could not derive a number from identify: $INFO" && continue
    NPAGES="$(identify $pdf | wc -l | xargs)" #`identify -format "%n" $pdf` # number of pages
    #intregexp='^[0-9]+$'
    #[[ ! $NPAGES =~ $intregexp ]] && echo "ERROR: NPAGES not a number: NPAGES=$NPAGES" && continue
  fi
  [[ $VERBOSE -gt 0 ]] && echo ">>> $pdf, npages=$NPAGES"
  if [[ $ANIMATE -gt 0 && $NPAGES -gt 1 ]]; then # animate PDF pages
    gif="${pdf/%.pdf/.gif}"
    [[ -e $gif ]] && continue
    OPTS="-verbose -delay $DELAY -loop 0 -density $GIF_RESO -despeckle -dispose previous"
    #peval "convert -verbose -delay $DELAY -loop 0 -density $GIF_RESO -dispose previous $pdf -coalesce -layers optimize $gif" # convert to animated GIF
    peval "convert $OPTS $pdf -resize $GIF_RESO -coalesce -layers optimize $gif"
  elif [[ $CONVERT_ALL -gt 0 ]]; then # convert all pages to PNG #&& $NPAGES -gt 1
    for i in `seq 1 $NPAGES`; do # loop over all pages
      tag=`printf "%03d" $i`
      png="${pdf/%.pdf/-$tag.png}" # png name
      [[ $OUTPUT != "" ]] && png="$OUTPUT/$png"
      page="$((i-1))"
      [[ $FORCE -lt 1 && -e $png ]] && continue
      OPTS="-density $PNG_RESO"
      [[ $WIDTH -gt 0 ]] && OPTS+=" -resize $WIDTH"
      [[ $WHITE -gt 0 ]] && OPTS+=" -background white -alpha remove -alpha off"
      #echo ">>>   $pdf[$page] -> $png"
      peval "convert $OPTS -trim ${pdf}[$page] $png" # convert to PNG
    done
  else
    png="${pdf/%.pdf/.png}" # png name
    [[ $FORCE -lt 1 && -e $png ]] && continue
    #echo ">>>   $pdf[$PAGE] -> $png"
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
