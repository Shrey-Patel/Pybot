from utilities.GeneralUtilities import IS_MACOS


if IS_MACOS:
    from os import system
else:
    import pyttsx

'''
    ABOUT: This class is the Voice of Pybot.
           The methods included in this class
           generate audio output of Pybot while
           interacting with the user.
    DOCUMENTATION on pyttsx:
           https://pyttsx.readthedocs.io/en/latest/
'''


class Voice:
    def __init__(self):
        """
        This constructor creates a pyttsx object.
        """
        if not IS_MACOS:
            self.create()
            self.engine = None

    def create(self):
        """
        This method creates a pyttsx object.
        :return: Nothing to return.
        """
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 120)

    def destroy(self):
        """
        This method destroys a pyttsx object in order
        to create a new one in the next interaction.
        :return: Nothing to return.
        """
        del self.engine

    def speak(self, first_run):
        """
        This method must be invoked whenever Pybot is ready to
        get a command by its user.
        :param first_run: notifies Pybot if this is the
                          if this is the first interaction with
                          the user. If so it says "Hi" to him.
        :return: Nothing to return.
        """
        if first_run:
            self.text_to_speech('Hi, what can I do for you?')
        else:
            self.text_to_speech('What can i do for you?')

    def text_to_speech(self, speech):
        """
        This method converts a text to speech.
        :param speech: The text we want Pybot to generate as audio
        :return: Nothing to return.
        """
        if IS_MACOS:
            system('say {}'.format(speech))
        else:
            self.create()
            self.engine.say(speech)
            self.engine.runAndWait()
            self.destroy()


'''
    The following block of code is a test for this class.
    In order to execute it run this script from the terminal
    as: ~$ python Voice.py
'''

if __name__ == '__main__':
    pybot = Voice()
    pybot.speak(True)
    text = ['Say hello to my little friend', 'What time is it',
            'Welcome to Pybot', 'I am trolling you']
    for _ in text:
        pybot.text_to_speech(_)
