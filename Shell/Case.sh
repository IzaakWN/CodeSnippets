#!/bin/bash
#
# case statement
# http://www.thegeekstuff.com/2010/07/bash-case-statement/
#
# declare and use boolean variable
# http://stackoverflow.com/questions/2953646/how-to-declare-and-use-boolean-variables-in-shell-script
#
# if else statements
# http://www.tutorialspoint.com/unix/if-else-statement.htm
#
# while true
# http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_09_02.html
#
# while : vs. while true
# http://stackoverflow.com/questions/10797835/while-vs-while-true
#
# case with range of numbers
# http://stackoverflow.com/questions/12614011/using-case-for-range-of-numbers-in-bash
#
#
# http://mywiki.wooledge.org/BashFAQ/054
# http://stackoverflow.com/questions/806906/how-do-i-test-if-a-variable-is-a-number-in-bash
#
# comparison operators
# http://tldp.org/LDP/abs/html/comparison-ops.html


Numbers()
{


    if ! [[ "$1" =~ ^[0-9]+$ ]] # or use case
    then
        echo ">>> input not an integer between 0-10!"
    else
        echo ">>> Okay!"
    fi

}



Guess()
{
    echo -n ">>> Guess my number between 1 and 10: "
    read answer

    case $answer in
        $(($answer<=3))) echo ">>>Very cold...";;
        [4-6]) echo ">>> Cold...";;
        7) echo ">>> Warm...";;
        8) echo ">>> Correct!";;
        9) echo ">>> Warm...!";;
        *) echo ">>> Incorrect!";;
    esac
}



YesOrNo()
{
    echo -n ">>> Do you agree with this? [yes or no]: "
    read answer

    while true
    do
        case $answer in
            [yY] | [yY][eE][sS] )
                echo ">>> You said yes!";
                break;;
            [nN] | [nN][oO] )
                echo ">>> You said no!?";
                break;;
            *)
                echo -n ">>> [Please answer yes or no]: ";
                read answer;;
        esac

    done
}
