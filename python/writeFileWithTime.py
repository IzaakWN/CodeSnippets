import time
starttime = time.clock()

def accountTime():
    minutes, seconds = divmod(time.clock()-starttime,60)
    hours, minutes   = divmod(minutes,60)
    with open("submitSFrame.log","a") as file:
        file.write("\n\n")
        file.write("Test\n")
        file.write("done: %s" % (time.strftime("%a %d/%m/%Y %H:%M:%S\n",time.gmtime())) )
        file.write("took: %s hours, %s minutes and %.1f seconds" % (hours,minutes,seconds))
    print "\nDone after %s hours, %s minutes and %.1f seconds.\n" % (hours,minutes,seconds)
    
accountTime()