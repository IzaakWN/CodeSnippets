#!/bin/bash
# http://www.cyberciti.biz/faq/bash-for-loop/


ForLoops()
{

    echo ">>> I can count, wacth me:"


    echo
    echo ">>> for i in 1 2 3"
    for i in 1 2 3
    do
       echo ">>> $i"
    done


    echo
    echo ">>> for i in {4..6}"
    for i in {4..6}
    do
        echo ">>> $i"
    done


    n=10
    echo
    echo ">>> n=$n"
    echo ">>> for ((7=1;i<=n;i++))"
    for ((i=7;i<=n;i++))
    do
        echo ">>> $i"
    done


    # seq involves the execution of an external command which
    # usually slows things down. This may not matter but it
    # becomes important if you're writing a script to handle
    # lots of data
    n=14
    echo
    echo ">>> n=$n"
    echo ">>> for i in \$(seq 11 \$n)"
    for i in $(seq 11 $n)
    do
        echo ">>> $i"
    done


    echo
    echo ">>> Yes, I can even count with steps of two!"


#    # for Bash v4.0+
#    echo "Bash version ${BASH_VERSION}..."
#    # {START..END..INCREMENT}
#    echo
#    echo ">>> for i in {0..10..2}"
#    for i in {0..10..2}
#    do
#        echo ">>> $i"
#    done


    echo
    echo ">>> for i in {0..5}"
    echo ">>> echo \$(( 2 * i ))"
    for i in {0..5}
    do
        echo $(( 2 * i ))
    done


}
