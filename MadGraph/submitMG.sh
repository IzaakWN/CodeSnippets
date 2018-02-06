#! /bin/bash

printf "###############################################\n"
printf "##   Run MadGraph for sample %-16s##\n" "$1"
printf "###############################################\n"



SAMPLE="$1"
BASESAMPLE="$SAMPLE"
N="$2"
SEOUTFILES="*.gz"

DBG=2
JOBLOGFILES="myout.txt myerr.txt"
BASEDIR="/shome/ineuteli/production/MG5_aMC_v2_5_4"
XROOTD="root://t3dcachedb.psi.ch:1094"
GFAL="gsiftp://t3se01.psi.ch"
SE_HOME="/pnfs/psi.ch/cms/trivcat/store/user/$USER"
JOBDIR="submitMG"

# optional parameters (always after non-optional ones!)
OPTIND=3 # look for optional arguments after first two non-optional ones
MASS=-1
BMASS=-1
NEVENTS=-1
PT_L_MIN=-1
NO_DR_LL_MIN=1
OPT_CORE=""
echo ">>> arguments are $@"
while getopts M:B:N:j:c:l: option; do
case "${option}" in
  M) MASS=${OPTARG};;
  B) BMASS=${OPTARG};;
  N) NEVENTS=${OPTARG};;
  l) PT_L_MIN=${OPTARG};;
  j) OPT_CORE="--multicore --nb_core=${OPTARG}";;
  c) OPT_CORE="--multicore --nb_core=${OPTARG}";;
esac
done

[ $MASS     -gt 0 ] && SAMPLE="${SAMPLE}_M-${MASS}"
[ $BMASS    -gt 0 ] && SAMPLE="${SAMPLE}_MB-${BMASS}"
[ $PT_L_MIN -gt 0 ] && SAMPLE="${SAMPLE}_FilterLep${PT_L_MIN}"
SAMPLE_N="${SAMPLE}_${N}"

cat <<EOF

###########################################
##            JOB PARAMETERS:            ##
###########################################
  \$BASESAMPLE=$BASESAMPLE
  \$SAMPLE=$SAMPLE
  \$SAMPLE_N=$SAMPLE_N
  \$N=$N
  \$SEOUTFILES=$SEOUTFILES
  \$MASS=$MASS
  \$PT_L_MIN=$PT_L_MIN
  \$NEVENTS=$NEVENTS
  \$OPT_CORE=$OPT_CORE
EOF

WORKDIR=/scratch/$USER/$JOBDIR/$SAMPLE_N
WORKMGDIR=$WORKDIR/$BASESAMPLE     # MG directory generate with proc_card
OUTDIR=$WORKMGDIR/Events/$SAMPLE_N # where SEOUTFILES are generated
RESULTDIR=$BASEDIR/$JOBDIR
REPORTDIR=$BASEDIR/$JOBDIR
SERESULTDIR=$SE_HOME/samples/"${SAMPLE}_madgraph"

CARDS="run madspin pythia"
CARDDIR="$BASEDIR/myCards"
WORKCARDDIR="$WORKMGDIR/Cards"
[[ $SAMPLE == LowMass* ]] && CARDS="run param" && CARDDIR="$CARDDIR/LowMassCards"



##### MONITORING/DEBUG INFORMATION #######################################################

mkdir -p /shome/ineuteli/production/MG5_aMC_v2_5_4/submitMG/
#$ -e /shome/ineuteli/production/MG5_aMC_v2_5_4/submitMG/
#$ -o /shome/ineuteli/production/MG5_aMC_v2_5_4/submitMG/

DATE_START=`date +%s`
echo "Job started at " `date`
cat <<EOF

###########################################
##       QUEUEING SYSTEM SETTINGS:       ##
###########################################
  \$HOME=$HOME
  \$USER=$USER
  \$JOB_ID=$JOB_ID
  \$JOB_NAME=$JOB_NAME
  \$HOSTNAME=$HOSTNAME
  \$TASK_ID=$TASK_ID
  \$QUEUE=$QUEUE
EOF



##### SET ENVIRONMENT ####################################################################

if test -e "$WORKDIR"; then
   echo "ERROR: WORKDIR ($WORKDIR) already exists!" >&2
   echo "ls $TOPWORKDIR"
   echo `ls $TOPWORKDIR` >&22
   echo "ls $WORKDIR"
   echo `ls $WORKDIR` >&2
   #exit 1
fi
mkdir -p $WORKDIR
if [ ! -d $WORKDIR ]; then
   echo "ERROR: Failed to create workdir ($WORKDIR)! Aborting..." >&2
   exit 1
fi
gfal-mkdir -p $GFAL/$SERESULTDIR # always before cmsenv!
if [ ! -d $SERESULTDIR ]; then
   echo "ERROR: Failed to create resultdir on the SE ($SERESULTDIR)! Aborting..." >&2
   exit 1
fi

cat <<EOF

###########################################
##             JOB SETTINGS:             ##
###########################################
  \$BASEDIR=$BASEDIR
  \$WORKDIR=$WORKDIR
  \$WORKMGDIR=$WORKMGDIR
  \$WORKCARDDIR=$WORKCARDDIR
  \$RESULTDIR=$RESULTDIR
  \$REPORTDIR=$REPORTDIR
  \$SERESULTDIR=$SERESULTDIR
EOF



##### MAIN FUNCTIONALITY CODE ############################################################

echo " "
echo "###########################################"
echo "##       SETUP FUNCTIONALITY CODE        ##"
echo "###########################################"

cd $WORKDIR
source $VO_CMS_SW_DIR/cmsset_default.sh >&2

# MAKE process dir
CMD_PROC="$BASEDIR/bin/mg5_aMC $CARDDIR/${BASESAMPLE}_proc_card.dat >> myout.txt 2>> myerr.txt"
echo "$CMD_PROC"
eval "$CMD_PROC"

# COPY cards
for CARD in $CARDS; do
  echo "cp $CARDDIR/${BASESAMPLE}_${CARD}_card.dat $WORKCARDDIR/${CARD}_card.dat"
  cp $CARDDIR/${BASESAMPLE}_${CARD}_card.dat $WORKCARDDIR/${CARD}_card.dat
done

# REPLACE mass
PARAM_CARD="$WORKCARDDIR/param_card.dat"
RUN_CARD="$WORKCARDDIR/run_card.dat"
if [ $NEVENTS -gt 0 ]; then
  OLDLINE=`grep -m1 -e "nevents" $RUN_CARD` # 50000 = nevents ! Number of unweighted events requested
  OLDNEVENTS=`echo $OLDLINE | grep -Po "[0-9]+" | grep -m1 ""`
  NEWNEVENTS=$NEVENTS
  NEWLINE=`echo "$OLDLINE # REPLACED" | sed "s/$OLDNEVENTS/$NEWNEVENTS/"`
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$RUN_CARD" "$OLDLINE" "$NEWLINE"
  sed -i "s/$OLDLINE/$NEWLINE/" $RUN_CARD
fi
if [ $MASS -gt 0 ] && [[ $SAMPLE == LowMass* ]]; then
  # MASS 7000021 (X)
  OLDLINE=`grep -Em1 "^\ *7000021.*[0-9]+\.[0-9]+e[+-][0-9]+" $PARAM_CARD` # 7000021 2.800000e+01 # mvn
  OLDMASS=`echo $OLDLINE | grep -Po "[0-9]+.[0-9]+e[+-][0-9]+" | grep -m1 ""`
  NEWMASS=`printf "%e" $MASS` # format in scientific notation
  NEWLINE=`echo "$OLDLINE # REPLACED" | sed "s/$OLDMASS/$NEWMASS/"`
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$PARAM_CARD" "$OLDLINE" "$NEWLINE"
  sed -i "s/$OLDLINE/$NEWLINE/" $PARAM_CARD
fi
if [ $BMASS -gt 0 ] && [[ $SAMPLE == LowMass* ]]; then
  # MASS 6000007 (X)
  OLDLINE=`grep -Em1 "^\ *6000007.*[0-9]+\.[0-9]+e[+-][0-9]+" $PARAM_CARD` # 7000021 2.800000e+01 # mvn
  OLDMASS=`echo $OLDLINE | grep -Po "[0-9]+.[0-9]+e[+-][0-9]+" | grep -m1 ""`
  NEWMASS=`printf "%e" $BMASS` # format in scientific notation
  NEWLINE=`echo "$OLDLINE # REPLACED" | sed "s/$OLDMASS/$NEWMASS/"`
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$PARAM_CARD" "$OLDLINE" "$NEWLINE"
  sed -i "s/$OLDLINE/$NEWLINE/" $PARAM_CARD
fi
if [ $MASS -gt 0 -o $BMASS -gt 0 ] && [[ $SAMPLE == LowMass* ]]; then
  # DECAY WIDTH 7000021 (X) & 6000007 (B')
  OLDLINE1=`grep -Em1 ".*DECAY.*7000021.*[0-9]+\.[0-9]+e[+-][0-9]+" $PARAM_CARD` # DECAY  7000021   2.528913e+00
  OLDLINE2=`grep -Em1 ".*DECAY.*6000007.*[0-9]+\.[0-9]+e[+-][0-9]+" $PARAM_CARD` # DECAY  6000007   7.309080e+00
  OLDWIDTH1=`echo $OLDLINE1 | grep -Po "[0-9]+.[0-9]+e[+-][0-9]+" | grep -m1 ""`
  OLDWIDTH2=`echo $OLDLINE2 | grep -Po "[0-9]+.[0-9]+e[+-][0-9]+" | grep -m1 ""`
  NEWLINE1=`echo "$OLDLINE1 # REPLACED" | sed "s/$OLDWIDTH1/auto/"`
  NEWLINE2=`echo "$OLDLINE2 # REPLACED" | sed "s/$OLDWIDTH2/auto/"`
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$PARAM_CARD" "$OLDLINE1" "$NEWLINE1"
  sed -i "s/$OLDLINE1/$NEWLINE1/" $PARAM_CARD
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$PARAM_CARD" "$OLDLINE2" "$NEWLINE2"
  sed -i "s/$OLDLINE2/$NEWLINE2/" $PARAM_CARD
fi
if [ $PT_L_MIN -gt 0 ]; then
  OLDLINE1=`grep -m1 -e "ptl1min" $RUN_CARD` # 0.0   = ptl1min ! minimum pt for the leading lepton in pt
  OLDLINE2=`grep -m1 -e "ptl2min" $RUN_CARD` # 0.0   = ptl2min ! minimum pt for the leading lepton in pt
  OLDPT1=`echo $OLDLINE1 | grep -Po "[0-9]+.[0-9]+" | grep -m1 ""`
  OLDPT2=`echo $OLDLINE2 | grep -Po "[0-9]+.[0-9]+" | grep -m1 ""`
  NEWPT=`printf "%.1f" $PT_L_MIN` # format as float with one decimal
  NEWLINE1=`echo "$OLDLINE1 - REPLACED" | sed "s/$OLDPT1/$NEWPT/"`
  NEWLINE2=`echo "$OLDLINE2 - REPLACED" | sed "s/$OLDPT2/$NEWPT/"`
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$RUN_CARD" "$OLDLINE1" "$NEWLINE1"
  sed -i "s/$OLDLINE1/$NEWLINE1/" $RUN_CARD
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$RUN_CARD" "$OLDLINE2" "$NEWLINE2"
  sed -i "s/$OLDLINE2/$NEWLINE2/" $RUN_CARD
fi
if [ $NO_DR_LL_MIN -gt 0 ]; then
  OLDLINE=`grep -m1 -e "drll " $RUN_CARD` # 0.4 = drll    ! min distance between leptons
  OLDDR=`echo $OLDLINE | grep -Po "[0-9]+.[0-9]+" | grep -m1 ""`
  NEWDR="0.0" # format as float with one decimal
  NEWLINE=`echo "$OLDLINE - REPLACED" | sed "s/$OLDDR/$NEWDR/"`
  printf "\n>>> replacing in %s:\n  \"%s\"\n  \"%s\"\n\n" "$RUN_CARD" "$OLDLINE" "$NEWLINE"
  sed -i "s/$OLDLINE/$NEWLINE/" $RUN_CARD
fi

echo "ls"
ls



echo " "
echo "###########################################"
echo "##         MY FUNCTIONALITY CODE         ##"
echo "###########################################"

# GENERATE events
CMD_GENERATE="$WORKMGDIR/bin/generate_events -f $SAMPLE_N $OPT_CORE >> myout.txt 2>> myerr.txt"
echo "$CMD_GENERATE"
eval "$CMD_GENERATE"

# RENAME output
cd $OUTDIR
echo "\
rename _events "" *.gz"
rename _events "" *.gz
echo "\
rename $SAMPLE $SAMPLE_N *.gz"
rename $SAMPLE $SAMPLE_N *.gz
echo "\
rename unweighted ${SAMPLE_N}_madgraph_unweighted *.gz"
rename unweighted ${SAMPLE_N}_madgraph_unweighted *.gz

# CHECK whether output is properly compressed
for f in `ls *.gz`; do
  if file $f | grep -q -v "compres"; then
      echo ">>> Warning! $f not correctly compressed, fixing:"
      f2=`echo $f | sed 's/.lhe.gz/.lhe/g'`
      echo "mv $f $f2"
      mv $f $f2
      echo "gzip $f2"
      gzip $f2
  fi
done



##### RETRIEVAL OF OUTPUT FILES AND CLEANING UP ##########################################

cd $WORKDIR
if [ 0"$DBG" -gt 0 ]; then
    echo " " 
    echo "########################################################"
    echo "##   OUTPUT WILL BE MOVED TO \$RESULTDIR and \$OUTDIR   ##"
    echo "########################################################"
    echo "  \$RESULTDIR=$RESULTDIR"
    echo "  \$REPORTDIR=$REPORTDIR"
    echo "  \$PWD: " `pwd`
    find -maxdepth 2 -ls #ls -Rl
    ls $OUTDIR
fi

cd $WORKDIR
if test x"$JOBLOGFILES" != x; then
    mkdir -p $REPORTDIR
    if test ! -e "$REPORTDIR"; then
        echo "ERROR: Failed to create $REPORTDIR ...Aborting..." >&2
        exit 1
    fi
    for n in $JOBLOGFILES; do
        NEWJOBLOGFILE="$REPORTDIR/${SAMPLE_N}_$n"
        echo ">>> copying $n to $NEWJOBLOGFILE"
        if test ! -e $WORKDIR/$n; then
            echo "WARNING: Cannot find output file $WORKDIR/$n. Ignoring it" >&2
        else
            cp -a $WORKDIR/$n $NEWJOBLOGFILE
            if test $? -ne 0; then
                echo "ERROR: Failed to copy $WORKDIR/$n to $NEWJOBLOGFILE" >&2
            fi
    fi
    done
fi

cd $OUTDIR
if test x"$SEOUTFILES" != x; then
    if [ 0"$DBG" -gt 2 ]; then
        debug="-v"
    fi
    if [[ ! -d $SERESULTDIR ]]; then
        echo ">>> $SERESULTDIR does not exist!"
        #echo "uberftp t3se01.psi.ch 'mkdir $SERESULTDIR'"
        #uberftp t3se01.psi.ch 'mkdir $SERESULTDIR'
    fi
    for n in `ls $SEOUTFILES`; do
        echo ">>> copying $OUTDIR/$n to $SERESULTDIR/$n"
        echo "xrdcp -d $DBG $debug --force $OUTDIR/$n $XROOTD/$SERESULTDIR/$n >&2"
        xrdcp -d $DBG $debug --force $OUTDIR/$n $XROOTD/$SERESULTDIR/$n >&2
        if test $? -ne 0; then
            echo "ERROR: Failed to copy $OUTDIR/$n to $SERESULTDIR/$n" >&2
        fi
    done
fi

printf "\nRemoving $WORKDIR (on ${HOSTNAME})\n"
rm -rf $WORKDIR



##########################################################################################

DATE_END=`date +%s`
RUNTIME=$((DATE_END-DATE_START))
printf "\n#####################################################"
printf "\n    Job finished at %s" "$(date)"
printf "\n    Wallclock running time: %02d:%02d:%02d" "$(( $RUNTIME / 3600 ))" "$(( $RUNTIME % 3600 /60 ))" "$(( $RUNTIME % 60 ))"
printf "\n#####################################################\n\n"

exit 0
