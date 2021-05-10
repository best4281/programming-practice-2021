import pickle

try:
    with open("history.p", 'rb') as f:
        previous_input = "Last input from previous session: " + pickle.load(f)
except:
    previous_input = "There was no previous input, or the history file was deleted."
#Task 2
word_count = 0
sentence_count = 0

used = False
vowels = ['a','e','i','o','u']

def second_or_first(word):
    try:
        return word[1]
    except:
        return word[0]

#def less_than_five(word_list):
#    return [word for word in word_list if len(word) < 5]

#Task 3.3
def less_than_five_without_vowels(word_list):
    qualified = []
    for word in word_list:
        no_vowel = word
        for alphabet in word.lower():
            if alphabet in vowels:
                no_vowel = no_vowel.replace(alphabet, '')
        #print(no_vowel, word)
        if len(no_vowel) < 5:
            qualified.append(word)
    return qualified

#Task 1
def second_ordered(sentence):
    if sentence == 'previous':
        global previous_input
        return previous_input
    else:
        global used
        used = True
        previous_input = sentence
        words = ' '.join(sentence.split()).split()
        global word_count
        global sentence_count
        word_count += len(words)
        sentence_count += 1
        words.sort(key = lambda x: second_or_first(x))
        #Task 3.2
        short_word = [w for w in words if len(w) < 5]
        short_word_without_vowels = less_than_five_without_vowels(words)
        ### RETURN VALUE FOR TASK 1, 3.1, 3.2, and 2 ###
        return words, short_word, short_word_without_vowels, word_count, sentence_count
        ###

def keep_history():
    global used
    if not used:
        return
    global previous_input
    with open("history.p", 'wb') as f:
        pickle.dump(previous_input,f)
    return

if __name__ == "__main__":
    print("press Ctrl+C to stop the program")
    while True:
        try:
            sentence = input("Please insert the sentence:")
            output = second_ordered(sentence)
            print(output)
        except KeyboardInterrupt:
            keep_history()
            break
    print("\nProgram exited.")