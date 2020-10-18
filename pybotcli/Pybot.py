# -*- coding: utf-8 -*-

from colorama import Fore
from utilities.GeneralUtilities import print_say
from CmdInterpreter import CmdInterpreter

PROMPT_CHAR = '~>'

class Pybot(CmdInterpreter, object):
   
    first_reaction_text = ""
    first_reaction_text += Fore.BLUE + \
        'Pybot\' sound is by default disabled.' + Fore.RESET
    first_reaction_text += "\n"
    first_reaction_text += Fore.BLUE + 'In order to let Pybot talk out loud type: '
    first_reaction_text += Fore.RESET + Fore.RED + 'enable sound' + Fore.RESET
    first_reaction_text += "\n"
    first_reaction_text += Fore.BLUE + \
        "Type 'help' for a list of available actions." + Fore.RESET
    first_reaction_text += "\n"
    prompt = (
        Fore.RED +
        "{} Hi, what can I do for you?\n".format(PROMPT_CHAR) + Fore.RESET
    )

    def __init__(self, first_reaction_text=first_reaction_text,
                 prompt=prompt, first_reaction=True, enable_voice=False):
        CmdInterpreter.__init__(self, first_reaction_text, prompt,
                                first_reaction, enable_voice)

    def default(self, data):
        """Pybot let's you know if an error has occurred."""
        print_say("I could not identify your command...", self, Fore.RED)

    def precmd(self, line):
        """Hook that executes before every command."""
        words = line.split()

        # append calculate keyword to front of leading char digit (or '-') in line
        if len(words) > 0 and (words[0].isdigit() or line[0] == "-"):
            line = "calculate " + line
            words = line.split()

        if len(words) == 0:
            line = "None"
        elif len(words) == 1:
            # if the action is a dict action, the command should contain more than one word
            # such as 'disable sound' or 'please, could you check the weather in Madrid'
            dict_actions = [action.keys()[0]
                            for action in self.actions if isinstance(action, dict)]
            if words[0] in dict_actions:
                self.default(words)
        elif (len(words) > 2) or (words[0] not in self.actions):
            line = self.parse_input(line)
        return line

    def postcmd(self, stop, line):
        """Hook that executes after every command."""
        if self.first_reaction:
            self.prompt = (
                Fore.RED +
                "{} What can i do for you?\n".format(PROMPT_CHAR) + Fore.RESET
            )
            self.first_reaction = False
        if self.enable_voice:
            self.speech.text_to_speech("What can i do for you?\n")

    def speak(self):
        if self.enable_voice:
            self.speech.speak(self.first_reaction)

    def parse_input(self, data):
        """This method gets the data and assigns it to an action"""
        data = data.lower()
        # say command is better if data has punctuation marks
        if "say" not in data:
            data = data.replace("?", "")
            data = data.replace("!", "")
            data = data.replace(".", "")
            data = data.replace(",", "")

        # Check if Pybot has a fixed response to this data
        if data in self.fixed_responses:
            output = self.fixed_responses[data]  # change return to output =
        else:
            # if it doesn't have a fixed response, look if the data corresponds to an action
            output = self._find_action(data)
        return output

    def _find_action(self, data):
        """Checks if input is a defined action.
        :return: returns the action"""
        output = "None"
        action_found = False
        words = data.split()
        words_remaining = data.split()  # this will help us to stop the iteration

        # check word by word if exists an action with the same name
        for word in words:
            words_remaining.remove(word)
            for action in self.actions:
                # action can be a string or a dict
                if type(action) is dict and word in action.keys():
                    # command name exists, assign it to the output
                    action_found = True
                    output = self._generate_output_if_dict(
                        action, word, words_remaining)
                    break
                # For the 'near' keyword, the words before 'near' are also needed
                elif word == "near":
                    initial_words = words[:words.index('near')]
                    output = word + " " +\
                        " ".join(initial_words + ["|"] + words_remaining)
                elif word == action:  # command name exists
                    action_found = True
                    output = word + " " + " ".join(words_remaining)
                    break
            if action_found:
                break
        return output

    def _generate_output_if_dict(self, action, word, words_remaining):
        """Generates the correct output if action is a dict"""
        output = word
        # command is a dictionary, let's check if remaining words are one of it's completions
        if len(words_remaining) != 0:
            command_arguments = list(words_remaining)  # make a copy
            for argument in words_remaining:
                command_arguments.remove(argument)
                for value in action[word]:
                    if argument == value:
                        output += " " + argument
                        output += " " + " ".join(command_arguments)
            # make Pybot complain if none of the words_remaining are part
            # of the word values (as in 'enable cat' or 'check whatever you want')
        if output == word:
            self.default(output)
        return output

    def executor(self):
        """
        Terminates when the user send the "exit", "quit"
        or "goodbye command"
        :return: Nothing to return.
        """
        self.speak()
        self.cmdloop(self.first_reaction_text)
