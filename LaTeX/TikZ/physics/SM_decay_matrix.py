#! /usr/bin/env python
# Author: Izaak Neutelings (May 2022)
# Description: Compute decay channels of HH, HW, HZ

d = {
  'Z': [('bb',0.156),('cc',0.116),('qq',0.428),('tt',0.034),('mm',0.034),('ee',0.034),('inv',0.200)],
  'W': [('qq',0.674),('tt',0.114),('mm',0.106),('ee',0.107),],
  #'H': [('bb',0.5807),('WW',0.2154),('ZZ',0.02643),('gg',0.08179),('tt',0.06256),('cc',0.02883),('aa',0.00227),('other',0.00202)],
  'H': [('bb',0.5807),('WW',0.2154),('ZZ',0.02643),('gg',0.08179),('tt',0.06256),('cc',0.02883),('aa',0.00227),('Za',0.001541),('mm',0.000217)],
  #'H': [('bb',0.5807),('WW',0.2154),('ZZ',0.02643),('tt',0.06256),('cc',0.02883),('gg',0.08179)],
}
#d['Z'].append(('other',1-sum(x for a,x in d['Z'])))
#d['W'].append(('other',1-sum(x for a,x in d['W'])))
d['H'].append(('other',1-sum(x for a,x in d['H'])))

from itertools import combinations, product
#[((100 if a==b else 200)*x*y,a,b) for (a,x), (b,y) in zip(H,H)+list(combinations(H,2))]
m = lambda a,b: (200.0 if U==V and a!=b else 100.)
for U, V in ['HH','HZ','HW','ZZ','WW']:
  dU = d[U][::-1] # reverse
  print("\n%4s decays"%(U+V))
  print ' '*14 + ''.join("%10s"%a for a, x in dU)
  for b, y in d[V]:
    #print "%6.3g"%(100*y) + "%8s"%b + ''.join("%10.5f"%(m(a,b)*x*y) for a, x in dU)
    print "%6.3g"%(100*y) + "%8s"%b + ''.join("%10.2e"%(m(a,b)*x*y/100.) for a, x in dU)
  print ' '*14 + ''.join("%10s"%a for a, x in dU)
  print ' '*14 + ''.join("%10.4g"%(100*x) for a, x in dU)
  ###if U==V:
  ###  for (a,x), (b,y) in zip(d[U],d[V]):
  ###    print("%8.3f%%: %s-%s"%(100*x*y,a,b))
  ###  for (a,x), (b,y) in combinations(d[U],2):
  ###    print("%8.3f%%: %s-%s"%(200*x*y,a,b)) # double (symmetric)
  ###else:
  ###  for (a,x), (b,y) in product(d[U],d[V]):
  ###    print("%8.3f%%: %s-%s"%(100*x*y,a,b))
  
