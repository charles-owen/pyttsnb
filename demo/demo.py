import pyttsnb

# the entry module for any script must
# include this test for main
if __name__ == "__main__":
    print("Hello")
    speaker = pyttsnb.create()
    speaker.start()
    speaker.say("Welcome to pi t t s n b")

    while True:
        print("1-Say something")
        print("0-Exit")
        print("Option? ")
        option = input()
        if option == "1":
            speaker.say("Something")
        elif option == "0":
            break

    speaker.shutdown()
