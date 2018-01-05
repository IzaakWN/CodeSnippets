#
# option
# http://stackoverflow.com/questions/14447406/bash-shell-script-check-for-a-flag-and-grab-its-value
# http://wiki.bash-hackers.org/howto/getopts_tutorial
# http://stackoverflow.com/questions/16654607/using-getopts-inside-a-bash-function
# http://stackoverflow.com/questions/10454501/why-getopts-within-a-function-fails-to-work
# http://wiki.bash-hackers.org/scripting/posparams


Opt()
{
    local OPTIND opt a     # declaration OPTIND necessary in function
    while getopts ":a" opt # left colon => silent error reporting mode
    do
        case "${opt}" in
            a)  echo ">>> -a was triggered";;
            \?) echo ">>> invalid option";;
        esac
    done
}



Opts()
{
    local OPTIND opt a
    echo ">>> \$*=$*"
    echo ">>> \$@=$@"
    while getopts ":ab" opt
    do
        case "${opt}" in
            a)  echo ">>> -a was triggered";;
            b)  echo ">>> -b was triggered";;
            \?) echo ">>> invalid option";;
        esac
    done
}



OptArg()
{
    local OPTIND opt a
    while getopts ":a:" opt
    do
        case $opt in
            a)  echo ">>> -a was triggered, parameter: $OPTARG" >&2;;
            \?) echo ">>> invalid option: -$OPTARG" >&2;;
            :)  echo ">>> option -$OPTARG requires an argument" >&2;;
        esac
    done
}



OptsArg()
{
    local OPTIND opt a
    while getopts ":a:b" opt
    do
        case $opt in
            a)  echo ">>> -a was triggered, parameter: $OPTARG" >&2;;
            b)  echo ">>> -b was triggered" >&2;;
            :)  echo ">>> option -$OPTARG requires an argument" >&2;;
            \?) echo ">>> invalid option: -$OPTARG" >&2;;
        esac
    done
}



OptsReorder()
{
    echo ">>> before:  \$*=$*"
    echo ">>>          \$@=$@"

    echo ">>> \$1 = $1"

    new=""

    for (( i=$#; i>0; i-- ))
    do

        echo
        echo ">>> \$i = $i"
        eval x="\$$i"
        echo ">>> eval x=\"\\$\$i\" -> eval x=\"\$$i\""
        echo ">>> \$x = $x"

        if [ $i -eq 1 ]
        then
            eval new=$new"\$$i"
        else
            eval new=$new"\$$i"
            new=$new" "
        fi
    done

    echo ">>> $new"
    echo ">>> after:  \$*=$*"
    echo ">>>         \$@=$@"

}


