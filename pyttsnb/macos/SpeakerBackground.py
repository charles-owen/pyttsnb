


import AVFoundation
import threading
import queue
from CoreFoundation import ( CFRunLoopRun, CFRunLoopStop, CFRunLoopGetMain,CFRunLoopGetCurrent,
    kCFRunLoopDefaultMode, CFRunLoopPerformBlock, CFRunLoopWakeUp)

"""
This class is for the code runs
in the separate background process

Do not use this class directly
"""
class SpeakerBackground():
    # The single instance of this class
    instance = None


    def __init__(self, q):
        """
        Constructor
        :param q: The foreground to background queue
        """
        self._queue = q

        # Retrieve the British English voice.
        # and create the speech synthesizer
        self._voice = AVFoundation.AVSpeechSynthesisVoice.voiceWithLanguage_("en-GB")
        self._synth = AVFoundation.AVSpeechSynthesizer.alloc().init()

        # A worker thread that will listen for
        # messages from the foreground process and
        # communicate them to the speech synthesizer
        self._thread = threading.Thread(target=self._thread_process)

        # This queue facilitates communications between the workers thread and the main thread
        self._queue2 = queue.Queue()

    def run(self):
        """
        Run the background system
        :return:
        """
        self._thread.start()
        CFRunLoopRun()

    def say(self, text, interrupt=False):
        """
        Say something!
        :param text: what to say?
        :param interrupt: if true, Amy, active speech is immediately terminated
        :return:
        """
        if interrupt:
            self._synth.stopSpeakingAtBoundary_(AVFoundation.AVSpeechBoundaryImmediate)

        utterance = AVFoundation.AVSpeechUtterance.speechUtteranceWithString_(text)

        # Configure the utterance.
        utterance.setRate_(0.57)
        utterance.setPitchMultiplier_(0.8)
        utterance.setPostUtteranceDelay_(0)
        utterance.setVolume_(1)
        # Assign the voice to the utterance.
        utterance.setVoice_(self._voice)
        self._synth.speakUtterance_(utterance)

    def _thread_process(self):
        """
        This is the entry point for the
        worker thread that listens. For
        messages from the foreground process
        and communicates them to the main
        thread of the background process.
        :return: None
        """
        while True:
            msg = self._queue.get()
            if msg is None:
                msg = {"cmd": "stop"}

            self._queue2.put(msg)

            CFRunLoopPerformBlock(CFRunLoopGetMain(), kCFRunLoopDefaultMode, lambda: self._main_thread_target())
            CFRunLoopWakeUp(CFRunLoopGetMain())

            if msg["cmd"] == "stop":
                break


    def _main_thread_target(self):
        """
        The worker thread since messages to
        the main thread through this function
        that performs the message action.
        :return: None
        """
        while True:
            try:
                msg = self._queue2.get_nowait()

                if msg["cmd"] == "say":
                    self.say(msg["text"], interrupt=msg["int"])
                elif msg["cmd"] == "voice":
                    self.voice(msg["voice"])
                elif msg["cmd"] == "stop":
                    CFRunLoopStop(CFRunLoopGetMain())
            except queue.Empty:
                return

    def voice(self, voice):
        voics = AVFoundation.AVSpeechSynthesisVoice.speechVoices()
        for v in voics:
            name = str(v.name)
            if voice in name:
                self._voice = v
                print("Set voice to " + name)
                break


    @staticmethod
    def entry(queue):
        """
        The entry point for the process.
        Creates a Singleton of the
        speaker background class and
        runs it.
        :param queue:
        :return:Exit code
        """
        if SpeakerBackground.instance is None:
            SpeakerBackground.instance = SpeakerBackground(queue)
            SpeakerBackground.instance.run()
        else:
            raise NotImplementedError(" more than one speaker object is not currently supported.")

        return 0
