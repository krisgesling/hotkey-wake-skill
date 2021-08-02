import time

from pynput import keyboard

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
        if self.listener:
            self.listener.stop()
        key_combo = self.settings.get('key_combo')
        # get methods default arg may not work if set to empty string.
        if not key_combo:
            self.log.info(
                'No key combination provided. Please set this in your Skill '
                'settings. Falling back to default "<ctrl>+<alt>+r".')
            key_combo = '<ctrl>+<alt>+r'
            return False
        self.listener = self.create_listener(key_combo)
        if self.listener:
            self.listener.start()

    def create_listener(self, key_combo):
        # Single key press example
        if '+' in key_combo:
            listener = self.create_multi_key_listener(key_combo)
        else:
            listener = self.create_single_key_listener(key_combo)
        return listener

    def create_single_key_listener(self, key_combo):
        def on_press(key):
            if key == keyboard.KeyCode.from_char(key_combo):
                self.bus.emit(Message('mycroft.mic.listen'))

        listener = keyboard.Listener(on_press=on_press)
        return listener

    def create_multi_key_listener(self, key_combo):
        # Using global hotkeys
        def on_activate():
            self.bus.emit(Message('mycroft.mic.listen'))

        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(key_combo),
            on_activate)

        listener = keyboard.Listener(on_press=for_canonical(hotkey.press),
                                     on_release=for_canonical(hotkey.release))
        return listener

    def shutdown(self):
        if self.listener:
            self.listener.stop()


def create_skill():
    return HotKeyWake()
