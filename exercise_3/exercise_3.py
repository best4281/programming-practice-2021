import exercise_3_lib as elib

def exercise_3(inputs): # DO NOT CHANGE THIS LINE

    output = elib.second_ordered(inputs)
    print(output)

    return output       # DO NOT CHANGE THIS LINE

while True:
    try:
        print("press Ctrl+C to stop the program")
        sentence = input("Please insert the sentence:")
        exercise_3(sentence)
    except KeyboardInterrupt:
        elib.keep_history()
        break
print("\nProgram exited.")
