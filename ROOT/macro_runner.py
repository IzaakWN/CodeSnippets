# simple script to run C macro with ROOT

import ROOT
ROOT.gROOT.LoadMacro("macro.c")

ROOT.foo() # prints blabla

test = ROOT.gROOT.GetGlobal("lumi")
print test # prints blabla
print ROOT.lumi

#test.__assign__("new_value")
ROOT.lumi = "new_value"

print ROOT.lumi # prints new_value
ROOT.foo() # prints new_value
