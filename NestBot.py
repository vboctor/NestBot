#! /usr/bin/python

import ConfigParser
import os
import sys
import time
import urllib2

from nestpy.nest import Nest
from tweepy import (API, OAuthHandler)

class NestBot:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, watermarkFilePath):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = API(auth)
        self.watermarkFilePath = watermarkFilePath

        # 'example: 278910647155179520'
        self.last_message_id = self.ReadAllText(watermarkFilePath)

    def ReadAllText(self, filePath):
        if os.path.exists(filePath):
            f = open(filePath, 'r')
            text = f.read().strip()
            f.close()

            if (len(text) == 0):
                text = None
        else:
            text = None

        return text;

    def WriteAllText(self, filePath, text):
        f = open(filePath, 'w')
        f.write(text)
        f.close()

    def shouldExecute(self, sender):
        return sender == 'vboctor'

    def printMessage(self, id, message, sender, sentAt):
        print id, message, sender, sentAt

    def executeMessage(self, id, message, sender, sentAt):
        if (not self.shouldExecute(sender)):
            print 'Skipping "' + message + '" from "' + sender + '"'
        elif (message == 'status'):
            print 'getting status... not implemented.'
            self.api.send_direct_message(user = sender, text = 'Here is your status!!!')
        elif (message == 'away'):
            print 'setting away... not implemented.'
            self.api.send_direct_message(user = sender, text = 'Your nest is now set to away.')

    def updateWatermark(self, messageId):
        self.last_message_id = str(messageId)
        self.WriteAllText(self.watermarkFilePath, self.last_message_id)

    def run(self):
        while (True):
            print 'checking queue...'
            messages = self.api.direct_messages(since_id = self.last_message_id)
            if (len(messages) == 0):
                print '  no work, sleep for a while.'
                time.sleep(20)
            else:
                # reverse the list of messages to process them in chronological order
                # this is import to make the last command win and for watermarking to work
                messages = reversed(messages)

                for message in messages:        
                    self.printMessage(message.id, message.text, message.sender.screen_name, message.created_at)
                    self.executeMessage(message.id, message.text, message.sender.screen_name, message.created_at)
                    self.updateWatermark(message.id)

def main():    
    config = ConfigParser.ConfigParser()
    config.read('settings.config')

    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')

    access_token = config.get('twitter', 'access_token')
    access_token_secret = config.get('twitter', 'access_token_secret')

    watermarkFilePath = 'watermark.txt'

    bot = NestBot(consumer_key, consumer_secret, access_token, access_token_secret, watermarkFilePath)
    bot.run()

    sys.exit(0);

if __name__=="__main__":
   main()
