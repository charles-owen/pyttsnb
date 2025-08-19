
"""
Management of all speech functionality
"""

"""
Non-blocking speech synthesis 
"""
class Speaker :
    def __init__(self):
        from .macos import MacSpeaker
        self._speaker = MacSpeaker()

    def start(self):
        self._speaker.start()

    def shutdown(self):
        self._speaker.shutdown()


    def say(self, text, interrupt=False):
        self._speaker.say(text, interrupt=interrupt)

    def voice(self, voice):
        self._speaker.voice(voice)
