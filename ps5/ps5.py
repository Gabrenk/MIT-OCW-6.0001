# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

class NewsStory(object):
    
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
   
   #get
    def get_guid(self):
       return self.guid
   
    def get_title(self):
       return self.title
   
    def get_description(self):
       return self.description
   
    def get_link(self):
       return self.link
   
    def get_pubdate(self):
       return self.pubdate
   
   #set
    def set_guid(self, guid):
       self.guid = guid

    def set_title(self, title):
       self.title = title

    def set_description(self, description):
       self.description = description

    def set_link(self, link):
       self.link = link

    def set_pubdate(self, pubdate):
       self.pubdate = self


#======================
# Triggers
#======================

class Trigger(object):
     def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    
    def get_phrase(self):
        return self.phrase
    
    def  is_phrase_in(self, text):
        
        ponctuation = string.punctuation
        #strip the phrase of every ponctuation they have
        unpunctuated_text = "".join(ch if ch not in ponctuation 
                                       else " " for ch in text.lower())
        unpunctuated_phrase = "".join(ch if ch not in ponctuation
                                       else " " for ch in self.phrase.lower())
        #remove extra spaces
        cleaned_text = " ".join(unpunctuated_text.split()) + " " 
        cleaned_phrase = " ".join(unpunctuated_phrase.split()) + " "
        
        # check if the phrase is in the text
        if cleaned_phrase in cleaned_text:
            return True
        else:
            return False
        
        
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

class TimeTrigger(Trigger):
    def __init__(self, pubtime):
        # formating in "%d %b %Y %H:%M:%S"
        date_time = datetime.strptime(pubtime ,"%d %b %Y %H:%M:%S")
        #converting to EST
        converted_time = date_time.replace(tzinfo=pytz.timezone("EST"))
        self.date_time = converted_time

# Problem 6
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return  story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.date_time 

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.date_time
        
        



# COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    def __init__(self, uninverted_trigger):
        self.uninverted_trigger = uninverted_trigger
        
    def evaluate(self, story):
        return not self.uninverted_trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2
        
    def evaluate(self, story):
        return self.trigger_1.evaluate(story) and self.trigger_2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.trigger_1 = trigger_1
        self.trigger_2 = trigger_2
        
    def evaluate(self, story):
        return self.trigger_1.evaluate(story) or self.trigger_2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
               
    
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    #split the remaining lines by it's (,)
    # hte first word is the name or ADD
    # second element is a key word for the type of trigger
    #remaining elements are the arguments
    # if first word is ADD, then will add them to the trigger_list
    
    trigger_list = []
    
    trigger_types ={"TITLE" : TitleTrigger,
                    "DESCRIPTION" : DescriptionTrigger,
                    "AFTER": AfterTrigger,
                    "BEFORE" : BeforeTrigger, 
                    "NOT" : NotTrigger, 
                    "AND" : AndTrigger,
                    "OR" : OrTrigger}
    #helper function
    for line in lines:
        line_elements = line.split(",")
        if line_elements[0] != "ADD":
            if line_elements[1] == "OR" or "AND":
                pass
            else:
                pass
        else:
            pass
    return trigger_list
    
    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

#https://stackoverflow.com/questions/10999021/how-to-convert-gmt-time-to-est-time-using-python
