from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder

class Voiceassistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('voiceassistant').require('Assistant').build())
    def handle_voiceassistant(self, message):
        self.speak_dialog('voiceassistant')


def create_skill():
    return Voiceassistant()

