#! /bin/bash
# Author: Izaak Neutelings (August 2021)
# ./Opts2.sh -a foo
# ./Opts2.sh -a foo -b bar
# ./Opts2.sh -a foo -b bar fname1 fname2

#function printargs {
#  echo "\$ARGS=$OPTIND"
#  echo "\$OPTA=$OPTA"
#  echo "\$OPTB=$OPTB"
#  echo "\$@=$@"
#  echo "\$#=$#"
#  echo "\$OPTIND=$OPTIND"
#}

echo "BEFORE"
echo "  \$@=$@"
echo "  \$#=$#"
echo "  \$OPTIND=$OPTIND"
echo "  \$ARGS=$ARGS"
echo "  \$OPTA=$OPTA"
echo "  \$OPTB=$OPTB"

ARGS="NONE"
OPTA="NONE"
OPTB="NONE"
VERB=0
while getopts 'a:b:v' option; do
  echo "GETOPTS: option=$option, OPTARG=$OPTARG"
  echo "  \$@=$@"
  echo "  \$#=$#"
  echo "  \$OPTIND=$OPTIND"
  echo "  \$ARGS=$ARGS"
  echo "  \$OPTA=$OPTA"
  echo "  \$OPTB=$OPTB"
  case "${option}" in
    a) OPTA=${OPTARG};;
    b) OPTB=${OPTARG};;
    v) VERB=1;;
  esac
done

echo "AFTER getopts"
echo "  \$@=$@"
echo "  \$#=$#"
echo "  \$OPTIND=$OPTIND"
echo "  \$ARGS=$ARGS"
echo "  \$OPTA=$OPTA"
echo "  \$OPTB=$OPTB"

shift $((OPTIND-1))
ARGS="$@"

echo "AFTER shift"
echo "  \$@=$@"
echo "  \$#=$#"
echo "  \$OPTIND=$OPTIND"
echo "  \$ARGS=$ARGS"
echo "  \$OPTA=$OPTA"
echo "  \$OPTB=$OPTB"