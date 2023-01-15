from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
import csv
import cv2
import time
from .testOpencv import take_photo
from multiprocessing import Process, Queue
from .getObjLabel import getObjectsThenLabel



class Voiceassistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.img_multi = ''
        self.img_hand = ''
        self.objList = []
        self.info = {}

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

    	img_queue = Queue()
    	take_photo_process = Process(target = take_photo, args=(img_queue,))
    	take_photo_process.daemon = True
    	take_photo_process.start()
    	take_photo_process.join()
    	self.img_multi = img_queue.get()
    	self.info = getObjectsThenLabel(self.img_multi)
    	n = self.info['objectNum']
    	for i in range(n):
    	    self.objList.append(self.info['objectList'][i]['name'][0].lower())
    	    objStr = generate_str(self.objList)
    	if n < 5:
    	    self.speak_dialog('item.category', {'category' : objStr})
    	else:
    	    self.speak('I find some goods here, you can ask me whatever goods you want.', expect_response=True)
    	    
    @intent_handler('is.there.any.intent')
    def handler_is_there_any(self, message):
    	category_label = message.data.get('category')
    	if category_label in self.objList:
    	    for i in range(len(self.objList)):
    	    	if self.objList[i] == category_label.lower():
    	    	    self.speak_dialog('yes.is.there.item', {'category':self.objList[i], 'location': self.info['objectList'][i]['loc']})
    	else:
            self.speak_dialog('no.is.there.item', {'category': category_label})            	    
    	
def generate_str(possible_list):
    '''
    Generate string for Mycroft to speak it

    Args: 
        possible_list: array list with len = 3, each element is a string
    Returns:
        a string, e.g. possible_list = ['a', 'b', 'c'], res = 'a, b, and c'
    '''
    res = ''
    n = len(possible_list)
    if n < 5 and n > 1:
        for i in range(n-1):
            res += possible_list[i] + ' '
        res += 'and ' + possible_list[n-1]
    elif len(possible_list) == 1:
        res = possible_list[0]

    return res


def create_skill():
    return Voiceassistant()

