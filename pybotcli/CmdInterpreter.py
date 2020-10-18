from os import system
from cmd import Cmd
import signal
from platform import system as sys
from platform import architecture, release, dist
from time import ctime
from colorama import Fore
from requests import ConnectionError

from utilities import voice
from utilities.GeneralUtilities import (
    IS_MACOS, MACOS, print_say, unsupported
)

from packages import mapps,forecast, movie, wiki, evaluator
from packages import chat, directions_to, near_me, weather_pinpoint,  weatherIn, timeIn
from packages.memory.memory import Memory
from packages.reminder import reminder_handler, reminder_quit
from packages.systemOptions import turn_off_screen
from packages.news import News
from packages.clear import clear_scr
from packages.fb import fb_login
from packages.twitter import twitter_login, twitter_tweet, twitter_end

MEMORY = Memory()

CONNECTION_ERROR_MSG = "You are not connected to Internet"


class CmdInterpreter(Cmd):

    def __init__(self, first_reaction_text, prompt, first_reaction=True, enable_voice=False):
        """
        This constructor contains a dictionary with Pybot's Actions (what Pybot can do).
        """
        Cmd.__init__(self)
        self.first_reaction = first_reaction
        self.first_reaction_text = first_reaction_text
        self.prompt = prompt
        self.enable_voice = enable_voice
        signal.signal(signal.SIGINT, self.interrupt_handler)

        self.actions = ("ask",
                        "calculate",
                        {"check": ("ram", "weather", "time", "forecast")},
                        "clear",
                        "clock",
                        {"decrease": ("volume",)},
                        "directions",
                        "exit",
                        "fb",
                        "goodbye",
                        "how_are_you",
                        {"increase": ("volume",)},
                        {"movie": ("cast", "director", "plot", "producer", "rating", "year",)},
                        "near",
                        "news",
                        {"open": ("camera",)},
                        "os",
                        "locate",
                        "q",
                        "quit",
                        "say",
                        {"screen": ("off",)},
                        {"twitter": ("login", "tweet")},
                        {"update": ("location", "system")},
                        "weather",
                        {"wiki": ("search", "summary", "content")}
                        )

        self.fixed_responses = {"what time is it": "clock",
                                "where am I": "locate",
                                "how are you": "how_are_you"
                                }

        self.speech = voice.Voice()

    def close(self):
        """Closing Pybot."""
        reminder_quit()
        print_say("Goodbye, see you later!", self, Fore.RED)
        exit()

    def completedefault(self, text, line, begidx, endidx):
        """Default completion"""
        return [i for i in self.actions if i.startswith(text)]

    def error(self):
        """Pybot will let you know if an error has occurred."""
        print_say("I could not identify your command...", self, Fore.RED)

    def get_completions(self, command, text):
        """Returns a list with the completions of a command."""
        dict_target = (item for item in self.actions
                       if type(item) == dict and command in item).next()  # next() will return the first match
        completions_list = dict_target[command]
        return [i for i in completions_list if i.startswith(text)]

    def interrupt_handler(self, signal, frame):
        """Closes Pybot on SIGINT signal. (Ctrl-C)"""
        self.close()

    def do_ask(self, s):
        """Start chating with Pybot"""
        chat.main(self)

    def help_ask(self):
        """Prints help about ask command."""
        print_say("Start chating with Pybot", self)

    def do_calculate(self, s):
        """Pybot will get your calculations done!"""
        tempt = s.replace(" ", "")
        if len(tempt) > 1:
            evaluator.calc(tempt, self)
        else:
            print_say("Error: Not in correct format", self, Fore.RED)

    def help_calculate(self):
        """Print help about calculate command."""
        print_say("Pybot will get your calculations done!", self)
        print_say("-- Example:", self)
        print_say("\tcalculate 3 + 5", self)

   

    def do_check(self, s):
        """Checks your system's RAM stats."""
        # if s == "ram":
        if "ram" in s:
            system("free -lm")
        # if s == "time"
        elif "time" in s:
            timeIn.main(self, s)
        elif "forecast" in s:
            forecast.main(self, s)
        # if s == "weather"
        elif "weather" in s:
            try:
                weatherIn.main(self, s)
            except ConnectionError:
                print(CONNECTION_ERROR_MSG)

    def help_check(self):
        """Prints check command help."""
        print_say("ram: checks your system's RAM stats.", self)
        print_say("time: checks the current time in any part of the globe.", self)
        print_say(
            "weather in *: checks the current weather in any part of the globe.", self)
        print_say(
            "forecast: checks the weather forecast for the next 7 days.", self)
        print_say("-- Examples:", self)
        print_say("\tcheck ram", self)
        print_say("\tcheck time in Manchester (UK)", self)
        print_say("\tcheck weather in Canada", self)
        print_say("\tcheck forecast", self)
        print_say("\tcheck forecast in Madrid", self)
        # add here more prints

    def complete_check(self, text, line, begidx, endidx):
        """Completions for check command"""
        return self.get_completions("check", text)

    

    def do_clear(self, s=None):
        """Clear terminal screen. """
        clear_scr()

    def help_clear(self):
        """Help:Clear terminal screen"""
        print_say("Clears terminal", self)

    def do_clock(self, s):
        """Gives information about time."""
        print_say(ctime(), self, Fore.BLUE)

    def help_clock(self):
        """Prints help about clock command."""
        print_say("Gives information about time.", self)

   

    def do_decrease(self, s):
        """Decreases you speakers' sound."""
        if s == "volume":
            if IS_MACOS:
                system(
                    'osascript -e "set volume output volume '
                    '(output volume of (get volume settings) - 10) --100%"'
                )
            else:
                system("pactl -- set-sink-volume 0 -10%")

    def help_decrease(self):
        """Print help about decrease command."""
        print_say("volume: Decreases you speaker's sound.", self)

    def complete_decrease(self, text, line, begidx, endidx):
        """Completions for decrease command"""
        return self.get_completions("decrease", text)

    def do_directions(self, data):
        """Get directions about a destination you are interested to."""
        try:
            directions_to.main(data)
        except ValueError:
            print("Please enter destination")
        except ConnectionError:
            print(CONNECTION_ERROR_MSG)

    def help_directions(self):
        """Prints help about directions command"""
        print_say("Get directions about a destination you are interested to.", self)
        print_say("-- Example:", self)
        print_say("\tdirections to the Eiffel Tower", self)

    def do_disable(self, s):
        """Deny Pybot to use his voice."""
        if "sound" in s:
            self.enable_voice = False

    def help_disable(self):
        """Displays help about disable command"""
        print_say("sound: Deny Pybot his voice.", self)

    def complete_disable(self, text, line, begidx, endidx):
        """Completions for check command"""
        return self.get_completions("disable", text)

    def do_display(self, s):
        """Displays photos."""
        if "pics" in s:
            s = s.replace("pics", "").strip()
            picshow.showpics(s)

    def help_display(self):
        """Prints help about display command"""
        print_say("Displays photos of the topic you choose.", self)
        print_say("-- Example:", self)
        print_say("\tdisplay pics of castles", self)

    def complete_display(self, text, line, begidx, endidx):
        """Completions for display command"""
        return self.get_completions("display", text)

    def do_enable(self, s):
        """Let Pybot use his voice."""
        if "sound" in s:
            self.enable_voice = True

    def help_enable(self):
        """Displays help about enable command"""
        print_say("sound: Let Pybot use his voice.", self)

    def complete_enable(self, text, line, begidx, endidx):
        """Completions for enable command"""
        return self.get_completions("enable", text)

    def do_exit(self, s=None):
        """Closing Pybot."""
        self.close()

    def help_exit(self):
        """Closing Pybot."""
        print_say("Close Pybot", self)

    def do_fb(self, s=None):
        """Pybot will login into your facebook account either by prompting id-password or by using previously saved"""
        try:
            fb_login(self)
        except ConnectionError:
            print(CONNECTION_ERROR_MSG)

    def help_fb(self):
        """Help for fb"""
        print_say("type fb and follow instructions", self)

    def do_goodbye(self, s=None):
        """Closing Pybot."""
        self.close()

    def help_goodbye(self):
        """Closing Pybot."""
        print_say("Close Pybot", self)

    def do_how_are_you(self, s):
        """Pybot will inform you about his status."""
        print_say("I am fine, How about you?", self, Fore.BLUE)

    def help_how_are_you(self):
        """Print info about how_are_you command"""
        print_say("Pybot will inform you about his status.", self)

    def do_increase(self, s):
        """Increases you speakers' sound."""
        if s == "volume":
            if IS_MACOS:
                system(
                    'osascript -e "set volume output volume '
                    '(output volume of (get volume settings) + 10) --100%"'
                )
            else:
                system("pactl -- set-sink-volume 0 +3%")

    def help_increase(self):
        """Print help about increase command."""
        print_say("volume: Increases your speaker's sound.", self)

    def complete_increase(self, text, line, begidx, endidx):
        """Completions for increase command"""
        return self.get_completions("increase", text)

    def do_movie(self, s):
        """Pybot will get movie details for you"""
        k = s.split(' ', 1)
        if k[0] == "cast":
            data = movie.cast(k[1])
            for d in data:
                print_say(d['name'], self)
        elif k[0] == "director":
            data = movie.director(k[1])
            for d in data:
                print_say(d['name'], self)
        elif k[0] == "plot":
            data = movie.plot(k[1])
            print_say(data, self)
        elif k[0] == "producer":
            data = movie.producer(k[1])
            for d in data:
                print_say(d['name'], self)
        elif k[0] == "rating":
            data = movie.rating(k[1])
            print_say(str(data), self)
        elif k[0] == "year":
            data = movie.year(k[1])
            print_say(str(data), self)

    def help_movie(self):
        """Print help about movie command."""
        print_say("Pybot - movie command", self)
        print_say("List of commands:", self)
        print_say("movie cast", self)
        print_say("movie director", self)
        print_say("movie plot", self)
        print_say("movie producer", self)
        print_say("movie rating", self)
        print_say("movie year", self)

   

    def do_near(self, data):
        """Pybot can find what is near you!"""
        near_me.main(data)

    def help_near(self):
        """Print help about near command."""
        print_say("Pybot can find what is near you!", self)
        print_say("-- Examples:", self)
        print_say("\trestaurants near me", self)
        print_say("\tmuseums near the eiffel tower", self)

    def do_news(self, s):
        """Time to get an update about the local news."""
        if s == "quick":
            try:
                n = News()
                n.quick_news()
            except:
                print_say("I couldn't find news", self, Fore.RED)
        else:
            try:
                n = News()
                n.news()
            except:
                print_say("I couldn't find news", self, Fore.RED)

    def help_news(self):
        """Print help about news command."""
        print_say("Time to get an update about the local news.", self)
        print_say(
            "Type \"news\" to choose your source or \"news quick\" for some headlines.", self)

    def do_open(self, s):
        """Pybot will open the camera for you."""
        if "camera" in s:
            if IS_MACOS:
                system('open /Applications/Photo\ Booth.app')
            else:
                print_say("Opening cheese.......", self, Fore.RED)
                system("cheese")

    def help_open(self):
        """Print help about open command."""
        print_say("camera: Pybot will open the camera for you.", self)

    def complete_open(self, text, line, begidx, endidx):
        """Completions for open command"""
        return self.get_completions("open", text)

    def do_os(self, s):
        """Displays information about your operating system."""
        print_say('[!] Operating System Information', self, Fore.BLUE)
        print_say('[*] ' + sys(), self, Fore.GREEN)
        print_say('[*] ' + release(), self, Fore.GREEN)
        print_say('[*] ' + dist()[0], self, Fore.GREEN)
        for _ in architecture():
            print_say('[*] ' + _, self, Fore.GREEN)

    def help_os(self):
        """Displays information about your operating system."""
        print_say("Displays information about your operating system.", self)

    def do_locate(self, s):
        """Pybot will pinpoint your location."""
        try:
            mapps.locate_me()
        except ConnectionError:
            print(CONNECTION_ERROR_MSG)

    def help_locate(self):
        """Print help about pinpoint command."""
        print_say("Pybot will pinpoint your location.", self)

    def do_q(self, s=None):
        """Closing Pybot"""
        self.close()

    def help_q(self):
        """Closing Pybot"""
        print_say("Closing Pybot!!", self)

    def do_quit(self, s=None):
        """Closing Pybot."""
        self.close()

    def help_quit(self):
        """Closing Pybot."""
        print_say("Close Pybot", self)

    def do_say(self, s):
        """Reads what is typed."""
        voice_state = self.enable_voice
        self.enable_voice = True
        self.speech.text_to_speech(s)
        self.enable_voice = voice_state

    def help_say(self):
        """Prints help text from say command."""
        print_say("Reads what is typed.")

    def do_screen(self, s):
        """Turns off the screen instantly"""
        if "off" in s:
            turn_off_screen()

    def help_screen(self):
        """Print help about screen command."""
        print_say("Turns off the screen instantly", self)
        print_say("-- Example:", self)
        print_say("screen off", self)

    def complete_screen(self, text, line, begidx, endidx):
        """Completions for screen command"""
        return self.get_completions("screen", text)

    def do_twitter(self, s):
        """Pybot will login into your facebook account either by prompting id-password or by using previously saved"""
        if "login" in s:
            try:
                driver = twitter_login(self)
                twitter_end(self, driver)
            except ConnectionError:
                print(CONNECTION_ERROR_MSG)
        elif "tweet" in s:
            try:
                driver = twitter_tweet(self)
                twitter_end(self, driver)
            except ConnectionError:
                print(CONNECTION_ERROR_MSG)

    def help_twitter(self):
        """help for twitter"""
        print_say("enter twitter and follow the instructions", self)


    def do_update(self, s):
        """Updates location or system."""
        if "location" in s:
            location = MEMORY.get_data('city')
            loc_str = str(location)
            print_say("Your current location is set to " + loc_str, self)
            print_say("What is your new location?", self)
            try:
                i = raw_input()
            except:
                i = input()
            MEMORY.update_data('city', i)
            MEMORY.save()
        elif "system" in s:
            update_system()

    def help_update(self):
        """Prints help about update command"""
        print_say("location: Updates location.", self)
        print_say("system: Updates system.", self)

    def complete_update(self, text, line, begidx, endidx):
        """Completions for update command"""
        return self.get_completions("update", text)

    def do_weather(self, s):
        """Get information about today's weather."""
        try:
            weather_pinpoint.main(MEMORY, self, s)
        except ConnectionError:
            print(CONNECTION_ERROR_MSG)

    def help_weather(self):
        """Prints help about weather command."""
        print_say(
            "Get information about today's weather in your current location.", self)

    def do_wiki(self, s):
        """Pybot will get wiki details for you"""
        k = s.split(' ', 1)
        data = None
        if k[0] == "search":
            data = wiki.search(" ".join(k[1:]))
        elif k[0] == "summary":
            data = wiki.summary(" ".join(k[1:]))
        elif k[0] == "content":
            data = wiki.content(" ".join(k[1:]))

        if isinstance(data, list):
            print "\nDid you mean one of these pages?\n"
            for d in range(len(data)):
                print(str(d + 1) + ": " + data[d])
        else:
            print("\n" + data)

    def help_wiki(self):
        """Help for wiki"""
        print_say("Pybot has now wiki feature", self)
        print_say("enter wiki search for searching related topics", self)
        print_say("enter wiki summary for getting summary of the topic", self)
        print_say("wiki content for full page article of topic", self)

    
