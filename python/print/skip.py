# Author: Izaak Neutelings (December 2017)

print


def skip1():
    nJobs       = 400
    runningJobs = range(1,nJobs+1)
    nJobs       = len(runningJobs)
    skip        = 5 if nJobs<400 else 10
    print ">>> nJobs = %s"%nJobs
    while runningJobs:
      for j in runningJobs:
        runningJobs.remove(j)
        nRunningJobs = len(runningJobs)
        if (nRunningJobs%skip)==0 or not(nJobs*0.25<nRunningJobs<nJobs*0.75):
          print "waiting for %d job(s) in the queue" %(len(runningJobs))

    #print runningJobs
    

def skip2():
    nJobs       = 900
    runningJobs = range(1,nJobs+1)
    nJobs       = len(runningJobs)
    skip        = 5 if nJobs<400 else 10
    skip2       = 5 if nJobs>400 else 1
    print ">>> nJobs = %s"%nJobs
    while runningJobs:
      for j in runningJobs:
        runningJobs.remove(j)
        nRunningJobs = len(runningJobs)
        if ((nRunningJobs%skip )==0 or not(nJobs*0.25<nRunningJobs<nJobs*0.75)) and\
           ((nRunningJobs%skip2)==0 or not(nJobs*0.07<nRunningJobs<nJobs*0.93)):
          print "waiting for %d job(s) in the queue" %(len(runningJobs))

    #print runningJobs
    


#skip1()
skip2()
print