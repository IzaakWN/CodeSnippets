from random import choice

possibles = "abcdefghijklmnopqrstuvwxyz" + \
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + \
            "01234567890" + \
            ".,:;!?'\"\\/ "



def withSelection(goal="Hello World!"):
    print "\n\n # withSelection\n"

    string = "*"*len(goal)

    print "\ngoal = " + goal
    print "t=0: " + string

    t = 0
    while not string == goal:
        t += 1
        for i in range(len(string)):
            if not string[i] == goal[i]:
                string = string[:i] + choice(possibles) + string[i+1:]

        print "t=%s: "%t + string



def withSelectionN(**kwargs):
    print "\n\n # withSelectionStats\n"
    
    goal = kwargs.get("goal", "Hello World!")
    N = kwargs.get("N", 100)

    T = []
    
    print "goal = " + goal + "\n"

    for i in range(N):
        t = 0
        string = "*"*len(goal)
        while not string == goal:
            t += 1
            for i in range(len(string)):
                if not string[i] == goal[i]:
                    string = string[:i] + choice(possibles) + string[i+1:]
        T.append(t)

    print "Mean time to get goal with selection and N=%i: t=%s" % (N,(sum(T)/N))



def main():
    
    withSelection()
    withSelectionN(N=100)
    withSelectionN(N=1000)

    print "\nFin.\n"


if __name__ == '__main__':
    main()