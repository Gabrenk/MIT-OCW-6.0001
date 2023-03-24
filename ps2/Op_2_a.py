import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    
#------------------------------------------------------------------
    
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

def get_guessed_word(secret_word, letters_guessed):
    secret_word_print = ""
    for char in secret_word:
        if char not in letters_guessed:
            secret_word_print += " _ "
        else:
            secret_word_print += char
            
    return secret_word_print

def is_word_guessed(secret_word, letters_guessed):
    secret_word_split = [*secret_word]
    for letter in letters_guessed:
        while letter in secret_word_split:
            secret_word_split.remove(letter)
    
    if len(secret_word_split ) == 0:
        return True
    else:
        return False

def get_available_letters(letters_guessed):
    
    
    avaible_letters = [*string.ascii_lowercase]
    for letter in letters_guessed:
        if letter in avaible_letters:
            avaible_letters.remove(letter)
    avaible_letters = " ".join(avaible_letters)

    return avaible_letters            

def hangman():
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    
    print(f"""
Welcome to the game of hangman!
I am thinking of a word that is {len(secret_word)} letters long""")
    

    while True:
        print(f"""You have {guesses_remaining} guesses left
Avaible letters: {get_available_letters(letters_guessed)}""")
        
        letter_guessed = input("Please, enter a letter: ").lower()
        
        if letter_guessed.isalpha():
            if letter_guessed not in letters_guessed:
                letters_guessed.append(letter_guessed)
                guessed_word = get_guessed_word(secret_word, letters_guessed)
                
                if letter_guessed in secret_word:
                    print(f"Good guess: {guessed_word}")
                elif letter_guessed in "aeiou":
                    guesses_remaining -= 2
                    print(f"That letter is not in my word:  {guessed_word}")
                else:
                    guesses_remaining -= 1
                    print(f"That letter is not in my word:  {guessed_word}")        
            else:
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(f"""You've alredy guessed that letter. You still have {warnings_remaining} warnings remaining
{guessed_word}""")
                else:
                    guesses_remaining -= 1
                    print(f"""You've alredy guessed that letter.
Since you don't have any more warnings left you'll lose one guess
{guessed_word}""")
        elif warnings_remaining >0:
            warnings_remaining -= 1
            print(f"""Thats not a valid letter! You still have {warnings_remaining} warnings
{guessed_word}""")
        else:
            guesses_remaining -= 1
            print(f"""That's not a valid letter! You've ran out of warnings and lost a guess!
{guessed_word}""")
        
        print("-------------")
        
        #Winning condition
        if is_word_guessed(secret_word, letters_guessed):
            
            total_points = guesses_remaining * len(letters_guessed)
            print("Congratulations! You Won!")
            print(f"Your total points for this game are {total_points}")
        
        
        if guesses_remaining <= 0:
            print(f"""Game Over!
You ran out of guesses. The word was: {secret_word}""")
            break
    
    
#------------------------------------------------------------------
def match_with_gaps(my_word, other_word, letters_guessed):
    #return false if the two words are not of the same lenght or don't match
    my_word_no_space = my_word.replace(" ", "")
    
    if len(my_word_no_space) != len(other_word):
        return False
    
    for n in range(len(my_word_no_space)):
        my_current_letter = my_word_no_space[n]
        other_current_letter = other_word[n]
        
        if my_current_letter.isalpha():
            if my_current_letter != other_current_letter:
                return False
        else:
            if my_current_letter == "_" and other_current_letter in letters_guessed:
                return False
    return True

def show_possible_matches(wordlist, my_word, letters_guessed):
    matched_words = []
    for word in wordlist:
        if match_with_gaps(my_word, word, letters_guessed):
            matched_words.append(word)
    matched_words = " ".join(matched_words)
    
    if len(matched_words) > 0:
        print("Possible matches:\n", matched_words)
    else:
        print("No matches found")

def hangman_with_hints ():
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    
    print(f"""
Welcome to the game of hangman!
I am thinking of a word that is {len(secret_word)} letters long""")
    

    while True:
        print(f"""You have {guesses_remaining} guesses left
Avaible letters: {get_available_letters(letters_guessed)}""")
        
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        letter_guessed = input("Please, enter a letter: ").lower()
        
        if letter_guessed.isalpha():
            if letter_guessed not in letters_guessed:
                letters_guessed.append(letter_guessed)
                guessed_word = get_guessed_word(secret_word, letters_guessed)
                
                if letter_guessed in secret_word:
                    print(f"Good guess: {guessed_word}")
                elif letter_guessed in "aeiou":
                    guesses_remaining -= 2
                    print(f"That letter is not in my word:  {guessed_word}")
                else:
                    guesses_remaining -= 1
                    print(f"That letter is not in my word:  {guessed_word}")        
            else:
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(f"""You've alredy guessed that letter. You still have {warnings_remaining} warnings remaining
{guessed_word}""")
                else:
                    guesses_remaining -= 1
                    print(f"""You've alredy guessed that letter.
Since you don't have any more warnings left you'll lose one guess
{guessed_word}""")
        
        elif letter_guessed == "*":
            show_possible_matches(wordlist, guessed_word, letters_guessed)
        
        elif warnings_remaining >0:
            warnings_remaining -= 1
            print(f"""Thats not a valid letter! You still have {warnings_remaining} warnings
{guessed_word}""")
        
        else:
            guesses_remaining -= 1
            print(f"""That's not a valid letter! You've ran out of warnings and lost a guess!
{guessed_word}""")
        
        print("-------------")
        
        #Winning condition
        if is_word_guessed(secret_word, letters_guessed):
            
            total_points = guesses_remaining * len(letters_guessed)
            print("Congratulations! You Won!")
            print(f"Your total points for this game are {total_points}")
        
        
        if guesses_remaining <= 0:
            print(f"""Game Over!
You ran out of guesses. The word was: {secret_word}""")
            break







hangman_with_hints()