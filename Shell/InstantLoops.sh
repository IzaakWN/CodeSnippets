#!/bin/bash
#
# Date: 17 April 2016
# Author: Izaak Neutelings
#
#
# Description:
#   This file allow you to save loop AB-timestamps to play different video and/or
#   audio files in VLC. Once set, you can call any defined loop from the command line
#   in Terminal (Mac OSX or Linux).
#
#
# How to use this file:
#
#
# 1) For every file you want to loop over, you'll need to add two seperate functions
#    in this file:
#       - "user function": main function that can be used as a command in Terminal
#       - "loop function": function that saves the AB timestamps of every numbered loops
#
#
# 2) In the user function, edit the following:
#       - the name you can use in the Terminal command line, e.g. "jimi2"
#       - FILE: give the correct path to the file that VLC will open
#       - LIST: (optional) write all available loops, in case you forget
#       - LOOPFUNCTION: name of the loop function, e.g. "Jimi2Loops"
#
#    After that, it should look something like:
#    (Note: keep the quotation marks, and don't add spaces between the equals signs!)
#
#    jimi2()
#    {
#       local FUNCTIONNAME=$FUNCNAME
#       local FILE="/Users/Izaak/Movies/Guitar/Jimi's Influence/Lesson 2/JimisInfluence-Lesson2-Demonstration-HD.mov"
#       local LIST=">>> available loops: 1-19"
#       local LOOPFUNCTION=Jimi2Loops
#       InstantLoops $@
#    }
#
#
# 3) In the loop function, edit:
#       - the name corresponding to LOOPFUNCTION in user function, e.g. "Jimi2Loops"
#       - for every loop: the number and the timestamps A and B in seconds, e.g.:
#             2)  A=10; B=15.4;;
#         (note you can include letters to number the loops: e.g. L5 or C1L5)
#
#    For example:
#
#    Jimi2Loops()
#    {
#        L="$1"
#        case $L in
#            1)  A=7;     B=16.4;;
#            2)  A=16.4;  B=26;;
#            3)  A=26;    B=36;;
#            4)  A=36;    B=43.6;;
#            5)  A=43.6;  B=61.6;;
#            6)  A=61.6;  B=68;;
#            7)  A=68;    B=71.5;;
#            8)  A=71.5;  B=76.4;;
#            9)  A=76.0;  B=81;;
#            10) A=81;    B=90;;
#        esac
#        echo "$A $B $L"
#    }
#
#
# 4) Now open a fresh Terminal window, and execute these two line seperately:
#    but make sure the paths to the VLC app and InstantLoops.sh are correct:
#
#    alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'
#    . /Users/Izaak/Documents/InstantLoops.sh
#
#    Now you're ready! Type the name of your user function followed by the number
#    of one, all seperated by spaces, e.g. "jimi2 4" or "jimi2 4 6". A VLC
#    window should open.
#
#
# 5) To stop, just quit VLC (command + Q).
#
# 
# 6) As finishing touch, you can add the first two command lines in step 4) to a
#    file that will run automatically every time you open a new Terminal window.
#
#    a) Check wether the files ~/.bashrc and ~/.bash_profile exist in your home
#       directory. "ls -a ~/" in Terminal will give a list of all files (including
#       hidden files whose name start with a dot).
#
#    b) If one does not exit, you can create them with a new txt file in TextEdit
#       (use shift+command+T) and save it in your home directory with just the name.
#       ".bash_profile" or ".bashrc".
#
#    c) Open the files with "open -a TextEdit ~/.bashrc" in Terminal.
#
#    d) Now make sure ~/.bashrc_profile contains something like:
#           "if [ -f ~/.bashrc ]; then . ~/.bashrc; fi"
#        or "[[ -r ~/.bashrc ]] && . ~/.bashrc"
#       Otherwise add "[[ -r ~/.bashrc ]] && . ~/.bashrc"
#
#    e) Copy-paste the following two lines in your ~/.bashrc file,
#       but again make sure the paths to the VLC app and InstantLoops.sh are correct:
#
#           alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'
#           . /Users/Izaak/Documents/InstantLoops.sh
#
#    d) Now you're done!
#
#



ChorusLick()
{
    # this functions splits input into chorus and lick, e.g.:
    # C1L3  -> 1 3
    # c1l3  -> 1 3
    # C21L3 -> 21 3
    # 4L3   -> 4 3

    local CHORUS LICK

    # split input in delimiter "L" or "l" (bash-only)
    IFS="lL" read CHORUS LICK <<< "$1"

    # get rid of "c" of "C" in CHORUS
    CHORUS=`cut -d c -f 2 <<< cut -d C -f 2 <<< $CHORUS`

    echo "$CHORUS $LICK"
}



Jimi1Loops()
{
    local C L
    read C L < <(ChorusLick $1) # split input into chorus and lick
    case $C in
        1)  case $L in
                1) A=7;    B=22;;
                2) A=22;   B=25.5;;
                3) A=25.5; B=31;;
                4) A=31;   B=37;;
                5) A=37;   B=44;;
                6) A=44;   B=47.5;;
                7) A=47.5; B=52;;
                8) A=52;   B=59;;
            esac;;
        2)  case $L in
                1) A=59;    B=76;;
                2) A=76;    B=81;;
                3) A=81;    B=86;;
                4) A=86;    B=95;;
                5) A=96;    B=101;;
                6) A=101;   B=108;;
                7) A=107;   B=117.4;;
                8) A=117.4; B=120.2;;
                9) A=120.2; B=122.4;;
            esac;;
        3)  case $L in
                1) A=122.4; B=128.5;;
                2) A=128.5; B=133.8;;
                3) A=133.8; B=145.0;;
                4) A=144.7; B=151.7;;
                5) A=151.6; B=157.0;;
                6) A=157.0; B=162.8;;
            esac;;
    esac
    L="C$C""L$L"
    echo "$A $B $L"
}



Jimi2Loops()
{
    L="$1"
    case $L in
        1)  A=7;     B=16.4;;
        2)  A=16.4;  B=26;;
        3)  A=26;    B=36;;
        4)  A=36;    B=43.6;;
        5)  A=43.6;  B=61.6;;
        6)  A=61.6;  B=68;;
        7)  A=68;    B=71.5;;
        8)  A=71.5;  B=76.4;;
        9)  A=76.0;  B=81;;
        10) A=81;    B=90;;
        11) A=90;    B=98;;
        12) A=98;    B=107;;
        13) A=107;   B=114;;
        14) A=114;   B=122.5;;
        15) A=122.5; B=131;;
        16) A=131;   B=141;;
        17) A=141;   B=150;;
        18) A=150;   B=167;;
        19) A=167;   B=177;;
        20) A=177;   B=184;;
        21) A=184;   B=193;;
        22) A=193;   B=199;;
        23) A=199;   B=209;;
        24) A=209;   B=218;;
        25) A=218;   B=226;;
        26) A=226;   B=237;;
        27) A=237;   B=245;;
        28) A=245;   B=251;;
        29) A=251;   B=272;;
    esac
    echo "$A $B $L"
}



BirgitLoops()
{
    L="$1"
    case $L in
        1)  A=0;     B=6;;      # Opening / turn-around
        2)  A=6;     B=11;;
        3)  A=11;    B=16.8;;
        4)  A=16.8;  B=22.2;;   # IV
        5)  A=22.2;  B=26.2;;   # V
        6)  A=26.2;  B=29;;
        7)  A=29;    B=31.8;;   # Turn-around
        8)  A=31.8;  B=37;;     # Chorus 2
        9)  A=37;    B=45.6;;
        10) A=45.6;  B=51.5;;
        11) A=51.5;  B=55;;
        12) A=55;    B=61;;
        13) A=61;    B=65;;     # Turn-around
    esac
    echo "$A $B $L"
}



jimi1()
{
    local FUNCTIONNAME=$FUNCNAME

    local FILE="/Users/IWN/Movies/Gitaar/Jimi Hendrix/Jimi's Influence/"
    FILE=$FILE$"Lesson 1/JimisInfluence-Lesson1-Demonstration-HD.mov"

    local LOOPFUNCTION=Jimi1Loops

    local LIST=">>> available licks:\n"
    LIST=$LIST$">>> \t chorus 1, licks 1-8\n"
    LIST=$LIST$">>> \t chorus 2, licks 1-9\n"
    LIST=$LIST$">>> \t chorus 3, licks 1-6"

    InstantLoops $@
}



jimi2()
{
    local FUNCTIONNAME=$FUNCNAME

    local FILE="/Users/IWN/Movies/Gitaar/Jimi Hendrix/Jimi's Influence/"
    FILE=$FILE$"Lesson 2/JimisInfluence-Lesson2-Demonstration-HD.mov"

    local LOOPFUNCTION=Jimi2Loops

    local LIST=">>> available licks: 1-19"

    InstantLoops $@
}



birgit()
{
    local FUNCTIONNAME=$FUNCNAME

    local FILE="/Users/IWN/Movies/Gitaar/Birgit Pijpops - Rock Me Mama Blues.mp4"

    local LOOPFUNCTION=BirgitLoops

    local LIST=">>> available licks: 1-13"

    InstantLoops $@
}



InstantLoops()
{
    usage()
    {
        echo
        echo " Usage: $FUNCTIONNAME [-a] [-c] [-l] [loop1 [loop2]] "
        echo " Function to play instant loops of a video or song file in VLC. "
        echo " Options: "
        echo "   [lick1] : loop over this loop,"
        echo "             if a second loop is given: loop over from loop1 to loop2 "
        echo "        -a : list all available loops "
        echo "        -c : print vlc command of loop "
        echo "        -h : print usages "
        echo "        -l : print the AB timestamps without opening the file "
        echo
    }

    if [ $# -eq 0 ]
    then
        vlc "$FILE"           # just open without loops
    else
        local A B
        local OPEN=true       # open file with vlc
        local LINE=false
        local LOOP=false
        local OPTIND opt a
        while getopts ":hacl" opt
        do
            case "${opt}" in
                h)  usage
                    unset -f usage;;
                a)  echo -e $LIST   # list all available licks
                    OPEN=false;;
                c)  LINE=true       # print vlc command of loop
                    OPEN=false;;
                l)  LOOP=true       # print the AB timestamps without opening the file
                    OPEN=false;;
                \?) echo ">>> invalid option";;
            esac
        done
        shift $((OPTIND-1))

        if [ $# -eq 0 ] && [ "$LOOP" = true ]
        then
            echo ">>> no input for -l"
        elif [ $# -eq 1 ]
        then
            local L
            read A B L < <($LOOPFUNCTION $1)
            PROMPT=">>> loop $L: A B = $A $B"
        elif [ $# -eq 2 ]
        then
            local x L1 L2
            read A x L1 < <($LOOPFUNCTION $1)
            read x B L2 < <($LOOPFUNCTION $2)
            PROMPT=">>> loop $L1-$L2: A B = $A $B"
        fi

        if [ -n "$A" ] && [ -n "$B" ] # test wether variable is set
        then
            echo $PROMPT
            if [ "$OPEN" = true ]
            then
                vlc "$FILE" --start-time "$A" --stop-time "$B" --repeat
            fi
            if [ "$LINE" = true  ]
            then
                echo "vlc \"$FILE\" --start-time $A --stop-time $B --repeat"
            fi
        else                          # variable is not set (correctly)
            if [ "$OPEN" = true ]
            then
                echo ">>> unexisting input,"
                echo $LIST
            fi
            if [ "$LINE" = true  ]
            then
                echo "vlc \"$FILE\" --start-time \"\$A\" --stop-time \"\$B\" --repeat"
            fi
        fi
    fi
}


