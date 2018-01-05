# TODO: make number of columns variable

def printColums(list):
    N = len(list)
    if N%4: list.extend( [" "]*(4-N%4) ); N = len(list)
    for row in zip(list[:N/4],list[N/4:N/2],list[N/2:N*3/4],list[N*3/4:]):
        print ">>> %18s %18s %18s %18s" % row

printColumn(range(27))