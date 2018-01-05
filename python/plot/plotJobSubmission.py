#! /usr/bin/env python
#
# Author: Izaak Neutelings (September 2017)
#
# https://matplotlib.org/users/pyplot_tutorial.html
# https://matplotlib.org/1.5.1/examples/color/named_colors.html
# https://docs.python.org/3/library/datetime.html
# https://matplotlib.org/api/dates_api.html
# https://matplotlib.org/examples/pylab_examples/date_demo1.html
# http://matplotlib.org/examples/api/date_demo.html
# https://matplotlib.org/users/colors.html

from datetime import datetime, timedelta
from matplotlib import pyplot as plot
from matplotlib import dates as mdates
import re

#oneDay     = timedelta(days=1)
time_min   = datetime.strptime('00:00','%H:%M')
time_max   = datetime.strptime('12:00','%H:%M') #+ oneDay

Nmax = -1
samples_all = [ "TT", "DY", "WJ", "ST", "WW", "WZ", "VV", "ZZ", "LowMass", "signal", "HTT", "VBF", "SUSY", "SingleMuon", "SingleElectron" ]
samples = [ "TT", "DY", "WJ", "ST", "SingleMuon", "SingleElectron" ]
samples_dict = { }
colors = [ "darkblue", "darkgreen", "darkred", "darkorange", "silver",
           "aqua",    "olive",     "fuchsia", "sienna",      ]
for sample in samples:
    if sample not in samples_all:
        print ">>> Warning! \"%s\" not in list of possible samples! Ignoring..."%(sample)
        continue
    samples_dict[sample] = ( [], [] )


def main():
    
    with open("submitSFrame.log") as file:
      sample = ""
      nJobs  = 0
      time   = 0
      for i,line in enumerate(file):
          if i>Nmax and Nmax>0: break
          #print "%s\n%s\n%s"%('-'*20,line,'-'*20)
          
          # 1) FIND SAMPLE
          for sample0 in samples_all:
              if sample0 in line and line[:len(sample0)] == sample0:
                  #print ">>> Found sample: %s"%(sample0)
                  sample = sample0
          
          # 2) FIND NUMBER OF JOBS
          if "number of jobs" in line:
              if not sample: print ">>> Warning: floating \"number of jobs\"!"
              nJobs = re.findall("number of jobs:.* (\d+)",line)
              if len(nJobs)!=1: print ">>> Warning! %s: len(nJobs)!=3: nJobs=%s"%(sample,nJobs)
              nJobs = float(nJobs[0])
          
          # 3) FIND DURATION
          if "took" in line:
              if not sample or not nJobs:
                  print ">>> Warning: floating \"took\"! Ignoring!"
                  continue
              parts = re.findall("took:.* (\d+(?:\.\d+)?) h.* (\d+(?:\.\d+)?) min.* (\d+(?:\.\d+)?) sec.*",line)
              if len(parts)!=1: print ">>> Warning! %s: len(parts)!=2: parts=%s"%(sample,parts)
              if len(parts[0])!=3:
                  print ">>> Warning! %s: len(parts[0])!=3: parts[0]=%s"%(sample,parts[0])
                  continue
              if sample not in samples:
                  sample = ""; nJobs = 0; time = 0 # RESET
                  continue
              hours,minutes,seconds = parts[0]
              hours,minutes,seconds = float(hours),float(minutes),float(seconds)
              time = "%02d:%02d:%02d"%(hours,minutes,seconds)
              time_obj = datetime.strptime(time,'%H:%M:%S')
              samples_dict[sample][0].append(nJobs)
              samples_dict[sample][1].append(time_obj)
    
    
    (fig, axis) = plot.subplots()

    # format the ticks
    hours      = mdates.HourLocator()
    minutes    = mdates.MinuteLocator()
    axis.yaxis.set_major_locator(hours)
    axis.yaxis.set_minor_locator(minutes)
    timeFormat = mdates.DateFormatter('%H:%M')
    axis.yaxis.set_major_formatter(timeFormat)
    axis.set_xlim(0,2500)
    axis.set_ylim(time_min,time_max)
    #axis.autoscale_view()
    
    for i, (sample, info) in enumerate(samples_dict.items()):
        #print ">>> %s: %s"%(sample,info)
        axis.scatter(info[0],info[1],marker='o',color=colors[i%len(colors)],label=sample)
    
    plot.legend(shadow=True, fancybox=True)
    
#         
#     # set some legend properties.  All the code below is optional.  The
#     # defaults are usually sensible but if you need more control, this
#     # shows you how
#     leg = plt.gca().get_legend()
#     ltext  = leg.get_texts()  # all the text.Text instance in the legend
#     llines = leg.get_lines()  # all the lines.Line2D instance in the legend
#     frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend
# 
#     # see text.Text, lines.Line2D, and patches.Rectangle for more info on
#     # the settable properties of lines, text, and rectangles
#     frame.set_facecolor('0.80')      # set the frame face color to light gray
#     plt.setp(ltext, fontsize='small')    # the legend text fontsize
#     plt.setp(llines, linewidth=1.5)      # the legend linewidth

#     text = iter(titles)
#     plotly_fig = tools.mpl_to_plotly( plt.gcf() )
#     print fig
#     print plotly
#     for data in plotly_fig['data']:
#         title = text.next()
#         data.update({'name': title, 'text':title})
# 
#     plotly_fig['layout']['showlegend'] = True
    
    #plot.show()
    fig.savefig("plotJobSubmission.png")
    


if __name__ == '__main__':
    main()
    print ">>>\n>>> Done.\n"
    

