# http://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
# http://stackoverflow.com/questions/4915361/whats-the-difference-between-raw-input-and-input-in-python3-x


def proceed(prompt=">>> proceed?",proceed_message=">>> proceding...",stop_message=">>> stop"):
    proceed = False
    while True:
        answer = raw_input(prompt+" (y or n) ").lower()
        if answer in [ 'y', 'ye', 'yes', 'yeah', 'yep', 'jep' ]:
            print proceed_message
            proceed = True
            break
        elif answer in [ 'n', 'no', 'na', 'nah', 'nee', 'neen', 'nop' ]:
            print stop_message
            proceed = False
            break
        else:
            print ">>> incorrect input"
            continue
        return proceed


while True:
    data = raw_input("Pick an answer from A to D: ")
    if data.lower() not in ('a', 'b', 'c', 'd'):
        print("Not an appropriate choice.")
    else:
        print("Got it!")
        break
