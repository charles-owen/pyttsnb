import objc
from Foundation import NSObject, NSRunLoop, NSDate
from AVFoundation import AVSpeechSynthesizer, AVSpeechUtterance

# Define a delegate class to handle speech events
class SpeechDelegate(NSObject):
    def speechSynthesizer_didFinishSpeechUtterance_(self, synthesizer, utterance1):
        print("Speech Done")
        # print(f"✅ Speech finished: {utterance1.speechString}")
        if utterance == utterance1:
            print("equal")

# Initialize the speech synthesizer and delegate
synth = AVSpeechSynthesizer.alloc().init()
delegate = SpeechDelegate.alloc().init()
synth.setDelegate_(delegate)

# Create an utterance
utterance = AVSpeechUtterance.alloc().initWithString_("Hello! This is a test of AVSpeechSynthesizer from Python.")
utterance.setRate_(0.5)  # Optional: adjust speaking rate
utterance.setVoice_(None)  # Optional: use default voice

# Start speaking
synth.speakUtterance_(utterance)

# Keep the run loop alive until speech finishes
while True:
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))
    if not  synth.isSpeaking():
        break