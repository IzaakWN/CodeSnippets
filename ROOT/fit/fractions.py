# Author: Izaak Neutelings (September 2017)
# 
# calculate fraction for RooFit model of several summed up pdfs

fracs0 = [0.50,0.30,0.10,0.06,0.04,0.01,0.05]

print
for n in range(2,6):
    print ">>> n = %s"%n
    formulas = ""
    fracs = fracs0[:n-1]
    print ">>>      %s"%fracs
    for i in range(1,n+1):
        fraci = 1
        if i is 1:
            fraci    = fracs[0]
            formulas += "f%d"%i
        else:
            fraci = (1-fracs[i-2])
            formulas += "(1-f%d)"%(i-1)
        fraci0 = max(1,i-1)
        print ">>>   %d: %s"%(i,fracs[fraci0:len(fracs)])
        for j, frac in enumerate(fracs[fraci0:len(fracs)],fraci0):
            fraci    *= frac
            formulas += "*f%d"%(j+1)
        formulas += " (%.1f%%),  "%(100*fraci)
    print ">>>   %s\n>>>"%(formulas)
print