import re
print

weight = "weight"
cuts_list = [
              "vetos==0 && iso_cuts==1 && njets>1",
              "vetos==0 &&  iso_cuts == 1  && njets>1",
              "vetos==0&&iso_1<0.15&&iso_2<0.20&&njets>1",
              "vetos==0 && iso_1<0.15 && iso_2<0.20 && njets>1",
              "vetos==0 && iso_1<0.15 && njets>1 && iso_2<0.20",
              "iso_1<0.15 && vetos==0 && njets>1 && iso_2<0.20",
              "iso_1<0.15&&vetos==0&&njets>1&&iso_2<0.20",
             ]

for cuts in cuts_list:
    
    cuts0 = cuts
    
    # CUTS: relaxed
    match_iso_1 = re.findall(r"iso_1\ *[<>]\ *\d+\.\d+\ *(?:&&\ *)?",cuts)
    match_iso_2 = re.findall(r"iso_2\ *[<>]\ *\d+\.\d+\ *(?:&&\ *)?",cuts)
    print ">>> match_iso_1=%s"%match_iso_1
    print ">>> match_iso_2=%s"%match_iso_2
    iso_relaxed = "iso_1<0.5 && iso_2<0.5 && (iso_1>0.20||iso_2<0.15)"
    if "iso_cuts==1" in cuts.replace(' ',''):
        cuts = re.sub(r"iso_cuts\ *==\ *1",iso_relaxed,cuts)
    elif len(match_iso_1) and len(match_iso_2):
        if len(match_iso_1)>1: print warning("QCD: More than one iso_1 match! cuts=%s"%cuts)
        if len(match_iso_2)>1: print warning("QCD: More than one iso_2 match! cuts=%s"%cuts)
        cuts = cuts.replace(match_iso_1[0],'')
        cuts = cuts.replace(match_iso_2[0],'')
        cuts = "%s && %s" % (iso_relaxed,cuts)
    elif cuts:
        cuts = "%s && %s" % (iso_relaxed,cuts)
    cuts    = cuts.rstrip(' ').rstrip('&').rstrip(' ')
    weight  = "%s*getQCDWeight(pt_2, pt_1, dR_ll)" % weight
    print ">>> %s\n>>>   -> %s" % (cuts0,cuts)
    print
    
print