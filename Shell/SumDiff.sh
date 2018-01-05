
SumDiffReturn1()
{
    sum=$(( $1 + $2 ))
    dif=$(( $1 - $2 ))
    echo "$sum $dif"
}



SumDiffReturn2()
{
    sum=$(( $1 + $2 ))
    dif=$(( $1 - $2 ))
    return "$sum $dif"
}



SumDiff()
{
    read sum dif < <(SumDiffReturn1 $1 $2)
    echo "1) sum=$sum, dif=$dif"

    read sum dif < <(SumDiffReturn2 $1 $2)
    echo "2) sum=$sum, dif=$dif"

    ret=`SumDiffReturn2 $1 $2`
    read sum dif < <($ret)
    echo "3) sum=$sum, dif=$dif"

}
