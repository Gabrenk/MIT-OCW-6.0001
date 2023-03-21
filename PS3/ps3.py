# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Breno
# Time spent    : around 7hours

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
    'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10,'r': 1, 's': 1, 't': 1, 'u': 1,
    'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,'*': 0
}


WORDLIST_FILENAME = "words.txt"

def load_words():
      
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def get_word_score(word, n):
    
    first_component = 0
    word_length = len(word)
    for letter in word.lower():
        first_component += SCRABBLE_LETTER_VALUES.get(letter, 0)
        
    second_component = max(7*word_length - 3*(n - word_length), 1)#!used max
        
    word_score = first_component*second_component
    
    
    return word_score


def display_hand(hand):
    print("Current hand:", end=" ")
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line


def deal_hand(n):
    
    hand={}
    hand["*"] = 1
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand


def update_hand(hand, word):
    new_hand = hand.copy()
    
    for letter in word.lower():
        if new_hand.get(letter, 0) > 0:
            new_hand[letter] -= 1

    return new_hand


def is_valid_word(word, hand, word_list):
    new_hand = hand.copy()
    word_low = word.lower()
    #wildcard check
    if "*" in word_low:
        wildcard_matches = 0
        for vowel in VOWELS:
            word_with_wildcard = word_low.replace("*", vowel)
            if word_with_wildcard in word_list:
                wildcard_matches += 1
        
        if wildcard_matches == 0:
            return False
        
        else:
            for letter in word_low:
                if letter in new_hand.keys():#composed of letters from current hand
                    new_hand[letter] -= 1
                else:
                    return False
                
            for key in new_hand.keys():
                if new_hand[key] < 0:
                    return False
            
            return True
    
    # is in word list check
    else:
        if word_low in word_list:
            for letter in word_low:
                if letter in new_hand.keys():#composed of letters from current hand
                    new_hand[letter] -= 1
                else:
                    return False
                    
            for key in new_hand.keys():
                if new_hand[key] < 0:
                    return False
            
            return True
        
        else:
            return False
 

def calculate_handlen(hand):
    # saw on the internet: return sum(list(hand.values()))
    hand_length = 0
    for key in hand:
        hand_length += hand[key]
        
    return hand_length


def play_hand(hand, word_list):
    current_score = 0
    hand_length = calculate_handlen(hand)
    playing_hand = hand.copy()
    # game is only played while you have cards in your hand
    while hand_length > 0:
        display_hand(playing_hand)#show the hand to the player
        word = input("Enter word, or \"!!\" to indicate that you are finished: ")
	#Allow the player to quit the hand early
        if word == "!!":
            print("\n")
            break
        else:
            print("\n")
            if is_valid_word(word, playing_hand, word_list):
                word_score = get_word_score(word, calculate_handlen(playing_hand))
                current_score += word_score #remove the letter of a valid word and five the player it's points
                print(f"{word} earned {word_score} points. Total: {current_score}")
            else:
                print("That is not a valid word. Please choose another word")
            playing_hand = update_hand(hand, word)# remove the letters from an unvalid word
        hand_length = calculate_handlen(playing_hand)
            
    print("You ran out of letters")
    print(f"Total score for this round: {current_score}")
    
    return current_score


def substitute_hand(hand, letter):    
    new_hand = hand.copy()
    #check if the hand has the letter hte player wants to change
    if letter.lower not in list(new_hand.keys()):
        return hand
    
    else:
        alphabet = VOWELS + CONSONANTS# "*" is in alphabet but will never be given to the player, as the letter alredy exist in the player's hand
        while True:#while loop that will search for a correct letter to replace
            new_letter = random.choice(alphabet)
            if new_letter not in list(new_hand.keys()):
                new_hand[new_letter] = new_hand[letter]
                del(new_hand[letter])
                print(f"Your new letter is: '{new_letter}'")
                break
    
    return new_hand
       
    
def play_game(word_list):
    #gets the player input on how many hands he wants to play    
    total_score = 0
    hands_to_play = int(input("How many hands do you want to play? "))
    
    print("\n")
    while hands_to_play > 0:#while loop that will play until all the hands are played
        current_hand = deal_hand(HAND_SIZE)
        display_hand(current_hand)
	#allow the player to make a sub
        if input("Would you like to substitute a letter?(yes / no)").lower() == "yes":
            print("\n")
            letter_to_replace = input("Which letter would you like to replace: ")
            current_hand = substitute_hand(current_hand, letter_to_replace)
        first_round_score = play_hand(current_hand, word_list)
        current_score = first_round_score
        print("----------")
	#allow the player to replay the hand
        if input("Would you like to replay the hand?").lower() == "yes":
            second_round_score = play_hand(current_hand, word_list)
	#passes on only the highest value
            current_score = max(first_round_score, second_round_score)
        total_score += current_score
        hands_to_play -= 1
    print("----------")
    print("Total score over all hands: ", total_score)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
