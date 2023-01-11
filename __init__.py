from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
import csv
#import sys
#from csv_test import csv_extract

class Voiceassistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('voiceassistant').require('Assistant').build())
    def handle_voiceassistant(self, message):
        self.speak_dialog('voiceassistant')
        
    @intent_handler('Have.I.Bought.intent')
    def handler_Have_I_Bought(self, message):
    	category_label = message.data.get('category')
    	
    	item_bought = []
    	with open('/home/ai-user/mycroft-core/skills/voiceassistant-skill/items.csv', newline = '') as file:
    	   reader = csv.reader(file)
    	   for item in reader:
    	   	item_bought.append(item[0])
    	if category_label in item_bought:
    	    know_more = self.ask_yesno('Know.more.about')
    	    if know_more == 'yes':
    	    	self.speak('The item is ...') 
    	    elif know_more == 'no': 
    	        self.speak('Wish you have a good day')
    	else:
    	    self.speak('No, you did not buy this stuff')


def create_skill():
    return Voiceassistant()

