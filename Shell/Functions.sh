#!/bin/bash


Function()
{

    echo
    echo ">>> Function"
    echo ">>> \$# = $#"

    var="lol"               # variable set globally
    local localvar="foo"    # variable set locally
    Input $@                # pass arguments

}



Input()
{

    echo
    echo ">>> Input"
    echo "\$var=$var"
    echo "\$localvar=$localvar"
    echo ">>> \$# = $#"
    if [ $# -gt 0 ]
    then
        echo ">>> \$1 = $1"
    fi
    echo

}



Test()
{

    local var=$1
    #local var=2
    #local var
    if [ -n "$var" ] # test wether variable is set
    then
        echo ">>> variable var is set"
    else
        echo ">>> variable var is NOT set"
    fi

}