from ..Speaker import Speaker
"""
Management of all speech functionality
for a Mac system
"""
import multiprocessing
from .SpeakerBackground import SpeakerBackground

"""
Non-blocking speech synthesis 
for Mac systems
"""
class SpeakerMacos(Speaker) :
    def __init__(self):
        # The queue that transmits
        # messages to the background process
        super().__init__()
        self._queue = multiprocessing.Queue()

        self._process = None


    def start(self):
        # the background process
        self._process = multiprocessing.Process(target=SpeakerBackground.entry, args=(self._queue,))
        self._process.start()

    def shutdown(self):
        self._queue.put({"cmd": "stop"})
        self._queue.close()
        self._process.join()


    def say(self, text, interrupt=False):
        # print("Speaker says: " + text)
        msg = {
            "cmd": "say",
            "text": text,
            "int": interrupt
        }

        self._queue.put(msg)

    def voice(self, voice):
        print("Speaker voice: " + voice)
        msg ={"cmd": "voice",
            "voice": voice}

        self._queue.put(msg)

