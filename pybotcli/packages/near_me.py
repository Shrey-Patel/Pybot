from utilities.GeneralUtilities import wordIndex
import CmdInterpreter
import mapps


def main(data):
    word_list = data.split()
    try:
        things = " ".join(word_list[0:wordIndex(data, "|")])
    except ValueError:
        cmd = CmdInterpreter.CmdInterpreter("", "")
        cmd.help_near()
        return

    if " me" in data:
        city = 0
    else:
        word_list = data.split()
        city = " ".join(word_list[wordIndex(data, "|") + 1:])
        print(city)
    mapps.search_near(things, city)
