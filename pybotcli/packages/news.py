# !!! This uses the https://newsapi.org/ api. TO comply with the TOU
# !!! we must link back to this site whenever we display results.

import urllib
import json
import webbrowser
from memory.memory import Memory

class News:
    def __init__(self, source="google-news", api_key="7488ba8ff8dc43459d36f06e7141c9e5"):
        self.apiKey = api_key
        self.source = source
        self.url = "https://newsapi.org/v1/articles?source=google-news&sortBy=top" \
                   "&apiKey=7488ba8ff8dc43459d36f06e7141c9e5"
        self.m = Memory()
    '''
        This is the defualt news function. It checks to see if the
        user has a preference and and goes through all choices.
    '''

    def news(self):
        self.news_options()
        self.get_news()

    '''
        This is the quickest way to get news it also has the
        least amount of options for the user.
    '''

    def quick_news(self):
        self.request_news()

    '''
        Gets and returns JSON data of news
    '''

    def get_news_json(self):
        response = urllib.urlopen(self.url)
        return json.loads(response.read())

    '''
        This sets the users options and loads them from Memory
        if they exist
    '''

    def news_options(self):
        # check to see if user already has default news source
        if self.m.get_data('news-source'):
            print("your default news source is " +
                  self.m.get_data('news-source'))
            print("Would you like news from this source? (yes/no): ")
            try:
                x = raw_input()
            except:
                x = input()
            if x == 'y' or x == 'yes':
                self.source = self.m.get_data('news-source')
            # if not set get users preference
            else:
                self.get_opt()
        else:
            self.get_opt()

    def get_opt(self):
        # Other sources available here: https://newsapi.org/sources
        print("Select Source (1-5):")
        print("1: BBC")
        print("2: BUZZFEED")
        print("3: Google")
        print("4: Reddit")
        print("5: TechCrunch")

        try:
            i = int(raw_input())
        except:
            i = int(input())

        if i == 1:
            self.source = "bbc-news"
        elif i == 2:
            self.source = "buzzfeed"
        elif i == 3:
            self.source = "google-news"
        elif i == 4:
            self.source = "reddit-r-all"
        elif i == 5:
            self.source = "techcrunch"

        print("would you like to set this as your default? (yes/no): ")
        try:
            x = raw_input()
        except:
            x = input()
        if x == 'y' or x == 'yes':
            self.m.update_data('news-source', self.source)  # save to memory
            self.m.save()

    '''
        This sets the url and sends it to request_news()
    '''

    def get_news(self):
        u = "https://newsapi.org/v1/articles?source=" + \
            self.source + "&sortby=top&apiKey=" + self.apiKey
        self.request_news(u)

    def request_news(self, url=None):
        # check to see if a url was passed
        if url is None:
            url = self.url
        response = urllib.urlopen(url)
        # Load json
        data = json.loads(response.read())
        article_list = {}
        index = 1
        # print articles with their index
        print("Top News Articles from " + self.source)
        for article in data['articles']:
            # print (Fore.GREEN + str(index) + ": " + article['title'] + Fore.RESET)
            print(str(index) + ": " + article['title'])
            article_list[index] = article
            index += 1

        # Attribution link for News API to comply with TOU
        print("Powered by News API. Type NewsAPI to learn more")
        print("Type index to expand news\n")

        # Check to see if index or NewsAPI was enterd
        try:
            idx = raw_input()
        except:
            idx = input()
        if idx.lower() == "newsapi":
            webbrowser.open('https://newsapi.org/')
            return

        # check if we have a valid index
        try:
            int(idx)
            if int(idx) > index:
                print("Not a valid index")
                return
        except:
            print("Not a valid index")
            return

        # if index valid print article description
        print(article_list[int(idx)]['description'])

        print("Do you want to read more? (yes/no): ")
        try:
            i = raw_input()
        except:
            i = input()
        # if user wants to read more open browser to article url
        if i.lower() == "yes" or i.lower() == 'y':
            webbrowser.open(article_list[int(idx)]['url'])
            return
        else:
            return
