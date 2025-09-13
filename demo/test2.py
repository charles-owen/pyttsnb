import objc
from Foundation import NSObject
from AVFoundation import AVSpeechSynthesizer, AVSpeechUtterance
from CoreFoundation import CFRunLoopRunInMode, kCFRunLoopDefaultMode

# Define a delegate class to handle speech events
class SpeechDelegate(NSObject):
    def speechSynthesizer_didFinishSpeechUtterance_(self, synthesizer, utterance):
        print("✅ Speech finished: ", utterance.speechString)

# Initialize the speech synthesizer and delegate
synth = AVSpeechSynthesizer.alloc().init()
delegate = SpeechDelegate.alloc().init()
synth.setDelegate_(delegate)

# Create an utterance
utterance = AVSpeechUtterance.alloc().initWithString_("Hello! This is a test using CFRunLoop.")
utterance.setRate_(0.5)

# Start speaking
synth.speakUtterance_(utterance)

# Keep the run loop alive until speech finishes
while True:
    CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.1, False)
    if not synth.isSpeaking():
        break
