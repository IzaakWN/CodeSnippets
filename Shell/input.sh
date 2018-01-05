#!/bin/bash
# http://www.thegeekstuff.com/2010/07/bash-case-statement

echo -n "Do you agree with this? [yes or no]: "
read yno
case $yno in

    [yY] | [yY][Ee][Ss] )
        echo "Agreed"
        ;;

    [nN] | [n|N][O|o] )
        echo "Not agreed, you can't proceed the installation";
        exit 1
        ;;
    *) echo "Invalid input"
        ;;
esac