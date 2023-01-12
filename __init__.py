from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
import csv
import cv2
import time
from .testOpencv import take_photo
from multiprocessing import Process, Queue



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
    @intent_handler('view.goods.intent')
    def handler_view_goods(self, message):	
    	self.speak('Taking a photo now. Please wait a second for me to get the result')
    	self.img_multi = ''
    	self.img_hand = ''
    	img_queue = Queue()
    	take_photo_process = Process(target = take_photo, args=(img_queue,))
    	take_photo_process.daemon = True
    	take_photo_process.start()
    	take_photo_process.join()
    	self.img_mult = img_queue.get()
    	self.speak('I find some goods here, you can ask me whatever goods you want.', expect_response=True)
    	



def create_skill():
    return Voiceassistant()

