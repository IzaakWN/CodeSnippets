import os, sys
import time
from math import log
# http://stackoverflow.com/questions/3249524/print-in-one-line-dynamically
# http://stackoverflow.com/questions/3160699/python-progress-bar





class LoadingBar(object):
    """Class to make a simple, custom loading bar."""
    # from math import log, import sys

    def __init__(self, *args, **kwargs):
        '''Constructor for LoadingBar object.'''
        self.steps = 10
        if len(args)>0 and isinstance(args[0],int) and args[0]>0: self.steps = args[0]
        self.tally   = 0
        self.position = 0
        self.steps   = max(kwargs.get('steps',self.steps),1)
        self.width   = max(kwargs.get('width',self.steps),1)
        self.counter = kwargs.get('counter',False)
        self.counterformat = "%%%ii" % (log(self.steps,10)+1)
        self.remove  = kwargs.get('remove',False)
        self.symbol  = kwargs.get('symbol',"=")
        self.prepend = kwargs.get('prepend',">>> ")
        self.append  = kwargs.get('append',"")
        self.message_ = kwargs.get('message',"")
        self.done    = False
        if self.counter: self.counter = " %s/%i" % (self.counterformat%self.tally,self.steps)
        else:            self.counter = ""
        sys.stdout.write("%s[%s]" % (self.prepend," "*self.width))
        sys.stdout.flush()
        sys.stdout.write("\b"*(self.width+1)) # return to start of line, after '['
        if self.counter: self.updateCounter()
        if self.message_: self.message(self.message_)

    def count(self,*args,**kwargs):
        """Count one step."""
        if self.done: return
        i = 1.0
        message = ""
        if len(args)>0 and isinstance(args[0],int) and args[0]>0:
            i = args[0]
            args.remove(i)
        if len(args)>0 and isinstance(args[0],str):
            message = args[0]
        i = max(min(i,self.steps-self.tally),0)
        newposition = int(round(float(self.tally+i)*self.width/self.steps))
        step = newposition-self.position
        self.position = newposition
        sys.stdout.write(self.symbol*step)
        sys.stdout.flush()
        self.tally += i
        if self.counter: self.updateCounter()
        if message: self.message(message)
        if self.tally >= self.steps:
            if self.append: self.message(self.append,moveback=self.remove)
            if self.remove:
                sys.stdout.write("\b"*(self.width+1+len(self.prepend)))
                sys.stdout.write(' '*(len(self.prepend)+self.width+len(self.counter)+len(self.message_)+4))
                sys.stdout.write("\b"*(len(self.prepend)+self.width+len(self.counter)+len(self.message_)+4))
            elif not self.append: self.message("\n")
            self.done = True

    def updateCounter(self,**kwargs):
        """Update the counter."""
        self.counter = " %s/%i" % (self.counterformat%self.tally,self.steps)
        sys.stdout.write("%s]%s" % (' '*(self.width-self.position), self.counter))
        sys.stdout.flush()
        sys.stdout.write("\b"*(self.width+1-self.position+len(self.counter)))

    def message(self,newmessage,moveback=True):
        """Append the counter with some progress message."""
        end_ = ""
        if "\n" in newmessage:
            end_ = newmessage[newmessage.index("\n"):]
            newmessage = newmessage[:newmessage.index("\n")]
        self.message_ = newmessage.ljust(len(self.message_))+end_
        sys.stdout.write("%s]%s %s" % (' '*(self.width-self.position), self.counter, self.message_))
        sys.stdout.flush()
        if moveback: sys.stdout.write("\b"*(self.width+2-self.position+len(self.counter)+len(self.message_)))




def main():
    """Main function."""
    print ">>> "
    step = 0.1
    messages = ["lol", "lolbroek", "papey", "pop", "foobar", "barderman", "OMG", "lollol<<<", "domdomdom"]

    bar = LoadingBar(5)
    for i in range(0,8):
        time.sleep(step)
        bar.count()
    print ">>> Done with first loading bar."

    bar = LoadingBar(5,prepend=">>> Loading bar: ")
    for i in range(0,7):
        time.sleep(step)
        bar.count()

    bar = LoadingBar(20,width=17)
    for i in range(0,21):
        time.sleep(step)
        bar.count()

    bar = LoadingBar(steps=20,width=10,append=" Done!\n")
    for i in range(0,21):
        time.sleep(step)
        bar.count()

    bar = LoadingBar(17,width=23)
    for i in range(0,20):
        time.sleep(step)
        bar.count()

    bar = LoadingBar(10,width=30,remove=True)
    for i in range(0,10):
        time.sleep(step)
        bar.count()
    print ">>> Removed bar!"

    bar = LoadingBar(20,width=17,counter=True,append=" Done!\n")
    for i in range(0,21):
        time.sleep(step*3)
        bar.count()

    bar = LoadingBar(5,width=17,counter=True)
    for i in range(0,5):
        time.sleep(1)
        bar.count(messages[i])

    bar = LoadingBar(5,width=17,counter=True,remove=True)
    for i in range(0,5):
        time.sleep(step*3)
        bar.count(messages[i])
    print ">>> Removed bar again..."

    bar = LoadingBar(8,width=10,counter=True,append="Done.\n")
    for i in range(0,9):
        time.sleep(step*3)
        bar.count(messages[i])

    bar = LoadingBar(5,width=10,counter=True,append="Done.",remove=True)
    for i in range(0,5):
        time.sleep(step*3)
        bar.count(messages[i])
    print ">>> Removed bar again..."

    bar = LoadingBar(5,width=10,counter=True,append="Done.\n")
    for i in range(0,5):
        bar.message(messages[i])
        time.sleep(step*3)
        bar.count()




if __name__ == '__main__':
    
    print " "
    main()
    print ">>>\n>>> done\n"


