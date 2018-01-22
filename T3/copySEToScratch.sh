#! /bin/bash

XROOTD="root://t3dcachedb.psi.ch:1094"
PNFS="/pnfs/psi.ch/cms/trivcat/store/user/$USER/samples"
SCRATCH="/scratch/ineuteli"
FROM_PNFS="$PNFS"
FROM_XRD="$XROOTD/$FROM_PNFS"
TO_SCRATCH="$SCRATCH/samples"
MAXI=10

GREY="\e[37m"
BOLD="\e[1m"
GREYB="${GREY}${BOLD}"
REDB="\e[31m\e[1m"
ERROR="${REDB}ERROR!"
S="\e[0m"

DIRS="LowMassDiTau_M-70_FilterLep18_madgraph"
DIRS0="LowMassDiTau_M-70_FilterLep18_madgraph"
# IGNORE=""
# SELECT=""

# # FILTER out dirs matching search term in IGNORE
# for pattern in $IGNORE; do
#   DIRS0=`ls $DIRS0 | grep -v $pattern`
# done
# 
# # SELECT dirs matching search term in SELECT
# for pattern in $SELECT; do
#   DIRS0=`ls $DIRS0 | grep $pattern`
# done
# DIRS=$DIRS0

# COPY directories
i=0
cd $FROM_PNFS
N=`echo $DIRS | wc -w`
CHECK_FROM=">>> FROM dirs:"
CHECK_TO=">>> TO dirs:"
for dir in `echo $DIRS`; do
  i=$((i+1))
  [ $MAXI -gt 0 -a $i -gt $MAXI ] && break
  
  FROM_NO_XRD=$FROM_PNFS/$dir
  FROM=$FROM_XRD/$dir
  TO=$TO_SCRATCH/$dir
  MK_COMMAND="mkdir -p $TO"
  CP_COMMAND="xrdcp -fr $FROM $TO/"
  GZ_COMMAND="cd $TO && gunzip -f --verbose *.gz && cd -"
  
  echo
  echo -e ">>> ${i}/${N}: ${GREY}${dir}${S} ($(ls $dir | wc -l) files)"
  echo -e ">>> ${GREYB}$MK_COMMAND${S}"
  eval "$MK_COMMAND"
  [ ! -d $FROM_NO_XRD ] && printf ">>> ${ERROR} FROM directory does not exists:${S}\n>>>   ${REDB}$FROM_NO_XRD${S}\n" && exit 1
  [ ! -d $TO ]          && printf ">>> ${ERROR} TO directory does not exists${S}:  \n>>>   ${REDB}$TO${S}\n"          && exit 1
  echo -e ">>> ${GREYB}$CP_COMMAND${S}"
  eval "$CP_COMMAND"
  
  echo
  echo -e ">>> ${GREYB}$GZ_COMMAND${S}"
  eval "$GZ_COMMAND"
  
  echo
  #NEVENTS_FROM=`grep -ch "<event>" $FROM_NO_XRD/*.lhe | paste -sd+ | bc`
  NEVENTS_TO=`grep -ch "<event>" $TO/*.lhe | paste -sd+ | bc`
  CHECK_FROM+=`printf "\n>>>   %2s /%2s: %3s files in ${GREY}$FROM_NO_XRD${S}" $i $N $(ls $FROM_NO_XRD | wc -l)`
  CHECK_TO+=`printf "\n>>>   %2s /%2s: %3s files ($NEVENTS_TO events) in ${GREY}$TO${S}" $i $N $(ls $TO | wc -l)`
done

printf ">>> comparing directories:"
printf "\n>>>\n$CHECK_FROM"
printf "\n>>>\n$CHECK_TO"
printf "\n\n"

exit 0