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

from datetime import datetime, timedelta
from matplotlib import pyplot as plot
from matplotlib import dates as mdates

oneDay     = timedelta(days=1)
daystart   = datetime.strptime('00:00','%H:%M')
dayend     = datetime.strptime('00:00','%H:%M') + oneDay
time_min   = datetime.strptime('06:00','%H:%M')
time_max   = datetime.strptime('04:00','%H:%M') + oneDay
#date_min   = datetime.strptime('27/08/2017','%d/%m/%Y')
#date_max   = datetime.strptime('07/09/2017','%d/%m/%Y')



def punchPeriod(list1,list2):
    return [list1[0],list1[1],list2[1]]
    


def shift(list):
    date = [d+oneDay for d in list[0]]
    time = [t-oneDay for t in list[1]]
    return [date,time]
    



def main():

    events     = [ 'Work', 'Lunch', 'Sleep' ]
    linecolors = { 'Sleep':"darkblue",   'Work':"darkgreen",   'Lunch':"darkorange" }
    fillcolors = { 'Sleep':"dodgerblue", 'Work':"forestgreen", 'Lunch':"gold" }

    punchIn     = { }
    punchOut    = { }
    for event in events:
        punchIn[event]     = [  ]
        punchOut[event]    = [  ]
        #punchPeriod[event] = [ [[], [], [],] ]

    with open("PunchCard2017.txt") as file:
        for line in file:
            fields = line.split('\t')
            if fields[0] in events:
                event = fields[0]
                dt    = fields[5].split(':')
                hours = fields[5].split(':')[0]
                if not hours or int(hours) > 23:
                    print "Warning! Ignoring: dt=%s"%dt
                    continue
                print ">>> %s: %s; %s; %s" % (fields[0],fields[2],fields[3],fields[4])
                #dates.append(datetime.strptime(fields[2],'%d/%m/%Y'))
                #times.append(datetime.strptime(fields[3],'%H:%M'))
                date1 = datetime.strptime(fields[2],'%d/%m/%Y')
                date2 = datetime.strptime(fields[2],'%d/%m/%Y')
                time1 = datetime.strptime(fields[3],'%H:%M')
                time2 = datetime.strptime(fields[4],'%H:%M')
                if time1 > time2:
                    time2 += oneDay
                    #date2 += oneday
                if time1 < time_min: # assuming time2 > time_min
                    time1 += oneDay
                    time2 += oneDay
                    date1 -= oneDay
                    date2 -= oneDay
                
                if len(punchIn[event]) is not len(punchIn[event]):
                    print ">>> Warning! len(punchIn[event]) = %s is not len(punchIn[event]) = %s" %\
                                       (len(punchIn[event]),len(punchIn[event]))
                    exit(1)
                # make new list
                #   if no list exists
                #   if a day is skipped
                if len(punchIn[event]) is 0 or punchIn[event][-1][0][-1]+oneDay < date1:
                    print ">>> skip one day: %s" % (date1)
                    punchIn[event].append([[], []])
                    punchOut[event].append([[], []])
                
                punchIn[event][-1][0].append(date1)
                punchIn[event][-1][1].append(time1)
                punchOut[event][-1][0].append(date2)
                punchOut[event][-1][1].append(time2)
            


    (fig, axis) = plot.subplots()

    # format the ticks
    years      = mdates.YearLocator()
    months     = mdates.MonthLocator()
    days       = mdates.DayLocator()
    hours      = mdates.HourLocator()
    axis.xaxis.set_major_locator(months)
    axis.xaxis.set_minor_locator(days)
    axis.yaxis.set_major_locator(hours)
    dateFormat = mdates.DateFormatter('%d/%m/%y')
    timeFormat = mdates.DateFormatter('%H:%M')
    axis.xaxis.set_major_formatter(dateFormat)
    axis.yaxis.set_major_formatter(timeFormat)
    #axis.set_xlim(date_min,date_max)
    axis.set_ylim(time_min,time_max)
    #axis.autoscale_view()

#     for event in events:
#         axis.plot(*punchIn[event], color=linecolors[event])
#         axis.plot(*punchOut[event],color=linecolors[event])
#         plot.fill_between(*punchPeriod(punchIn[event],punchOut[event]), facecolor=fillcolors[event])
#         
#         punchIn_shifted  = shift(punchIn[event])
#         punchOut_shifted = shift(punchOut[event])
#         axis.plot(*punchIn_shifted, color=linecolors[event])
#         axis.plot(*punchOut_shifted,color=linecolors[event])
#         plot.fill_between(*punchPeriod(punchIn_shifted,punchOut_shifted), facecolor=fillcolors[event])

    for event in events:
        for punchInList, punchOutList in zip(punchIn[event],punchOut[event]):
            axis.plot(*punchInList, color=linecolors[event])
            axis.plot(*punchOutList,color=linecolors[event])
            plot.fill_between(*punchPeriod(punchInList,punchOutList), facecolor=fillcolors[event])
        
            punchIn_shifted  = shift(punchInList)
            punchOut_shifted = shift(punchOutList)
            axis.plot(*punchIn_shifted, color=linecolors[event])
            axis.plot(*punchOut_shifted,color=linecolors[event])
            plot.fill_between(*punchPeriod(punchIn_shifted,punchOut_shifted), facecolor=fillcolors[event])

        
    #plot.show()
    fig.savefig("plotPunchCard.png")
    


if __name__ == '__main__':
    main()
    print ">>>\n>>> Done.\n"
    

