#! /bin/bash
# Author: Izaak Neutelings (February 2023)
# Description: Clean build file when type-setting LaTeX.

EXTS="log aux synctex.gz" # LaTeX
EXTS+=" log mp t[1-9] [1-9] fls fdb_latexmk" # MetaPost, feynmp

for ext in $EXTS; do
  echo ">>> Look for files with extension $ext..."
  IFS=$'\n' # split on newline
  for f in `ls -1 */*.$ext */*/*.$ext 2>/dev/null`; do
    #echo "Found $f"
    [[ ! -e "$f" ]] && continue
    echo ">>>   Removing $f..."
    rm "$f"
  done
done