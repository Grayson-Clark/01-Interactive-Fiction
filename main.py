#!/usr/bin/env python3
import sys,os,json,time
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"

#  Returns a map of the specified json file.  #
def load(l):
    #  joins the current path of this py file with the file specified by "l".  #
    path = os.path.join(sys.path[0], l)

    #  Opens the file at path.  #
    f = open(path)

    #  Reads in the filedata based on the filehandle gotten above.  #
    data = f.read()

    #  Use json libary to parse filedata gotten above.  #
    j = json.loads(data)

    return j


#  Searches a map for a specified "pid" and returns the "passage" at that pid (pid -> Passage ID).  #
def find_passage(game_desc, pid):

    #  Iterate through the values at key "passages".  #
    for p in game_desc["passages"]:

        #  if the pid at the current passage is the pid passed to this func, return that passage.  #
        if p["pid"] == pid:
            return p

    #  If pid not found, return empty map.  #
    return {}


#  clear terminal/bash.  #
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------------------------------------

def render(current):
    #  Get text and find index that splits the actual message body and the options.  #
    print("\n")
    full_text = current["text"]
    option_split_idx = full_text.find("\n\n[[")

    #  Get and print message body.  #
    text = full_text[ : option_split_idx]
    print(text + "\n")

    #  To keep track of current iteration/option idx.  #
    optionnum = 1

    #  Iterate through options split over each newline.  #
    for option in full_text[option_split_idx : ].split("\n"):

        #  If the line has a "->", then it's a valid option we want to print out.  #
        if "->" in option:

            #  Parse and print the current option.  #
            option = option[option.find("[[")+2 : option.find("->")]
            print(str(optionnum) + ".) " + option)

            optionnum += 1
    

def update(current, game_desc, choice):
    new_current = current
    links = current["links"]

    #  Sanity check on user's choice.  #
    if int(choice) > len(links) or int(choice) == 0:
        print("Make sure your choice is a num that corresponds to one of the option(s)")
        time.sleep(2)
        return new_current

    # Iterate through our links and if the current "iteration" is the same as the choice that the user made, then set our return value to that passage.  #
    linknum = 1
    for link in links:
        if linknum == int(choice):
            new_current = find_passage(game_desc, link["pid"])
        linknum += 1

    return new_current

def get_input(current):
    #  Get keyboard input.  #
    inp = input("\n---- Enter the corresponding number for your choice ----\n")

    #  Sanity check for user input containing only digits.  #
    if not inp.isdigit():
        print("Make sure your choice is a valid number!")
        time.sleep(2)
        return get_input(current)
    return inp

# ------------------------------------------------------

def main():
    #  Clear console on "boot", makes things prettier.  #
    clear_console()

    #  Init values for first node of the game.  #
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    #  Game loop.  #
    while choice != "quit" and current != {}:

            render(current)

            #  If current passage object doesn't have any link objects, break out of loop and end the game.  #
            if not "links" in current:
                break

            choice = get_input(current)

            current = update(current, game_desc, choice)

            clear_console()

    print("Thanks for playing!")
    time.sleep(3)




if __name__ == "__main__":
    main()