from mycroft import MycroftSkill, intent_file_handler


class HotkeyWake(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('wake.hotkey.intent')
    def handle_wake_hotkey(self, message):
        self.speak_dialog('wake.hotkey')


def create_skill():
    return HotkeyWake()

