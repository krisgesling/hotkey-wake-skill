import time

import keyboard

from mycroft import MycroftSkill
from mycroft.messagebus.message import Message


class HotKeyWake(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.listener = None

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()

    def on_settings_changed(self):
        self.stop_keyboard_listener()
        key_combo = self.settings.get('key_combo')
        # get methods default arg may not work if set to empty string.
        if not key_combo:
            self.log.info(
                'No key combination provided. Please set this in your Skill '
                'settings. Falling back to default "ctrl+alt+r".')
            key_combo = 'ctrl+alt+r'
        listener = keyboard.add_hotkey(key_combo, self.handle_hotkey_press)

    def handle_hotkey_press(self):
        """Actions to perform when the hotkey combo is detected."""
        self.log.debug("Wake hotkey detected.")
        self.bus.emit(Message('mycroft.mic.listen'))

    def stop_keyboard_listener(self):
        """Stop the keyboard listener. Remove all hotkeys"""
        if self.listener:
            keyboard.remove_hotkey(self.listener)
            self.listener = None

    def shutdown(self):
        self.stop_keyboard_listener()

def create_skill():
    return HotKeyWake()
