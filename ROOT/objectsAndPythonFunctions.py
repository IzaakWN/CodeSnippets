from ROOT import TH1D, THStack

def overwrite(hist):
    print type(hist)
    hist = THStack("stack","stack")
    print type(hist)

hist = TH1D("hist","hist",100,0,100)
overwrite(hist)
print type(hist)