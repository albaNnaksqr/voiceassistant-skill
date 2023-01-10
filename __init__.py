from mycroft import MycroftSkill, intent_file_handler


class Voiceassistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('voiceassistant.intent')
    def handle_voiceassistant(self, message):
        self.speak_dialog('voiceassistant')


def create_skill():
    return Voiceassistant()

