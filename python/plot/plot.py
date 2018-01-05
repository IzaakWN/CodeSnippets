# https://matplotlib.org/users/pyplot_tutorial.html

import matplotlib.pyplot as plot

fig = plot.figure() # to save
plot.plot([1,2,3,4])
plot.ylabel('some numbers')
plot.show()
fig.savefig("plot.png")
