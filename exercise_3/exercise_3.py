import exercise_3_lib as elib

def exercise_3(inputs): # DO NOT CHANGE THIS LINE

    output = elib.second_ordered(inputs)
    print(output)

    return output       # DO NOT CHANGE THIS LINE

print("press Ctrl+C to stop the program")
while True:
    try:
        sentence = input("Please insert the sentence:")
        exercise_3(sentence)
    except KeyboardInterrupt:
        elib.keep_history()
        break
print("\nProgram exited.")
