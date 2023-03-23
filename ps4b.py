# Problem Set 4B
# Name: Breno
# Collaborators:
# Time Spent: 7 hours

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        #Firstly, adequate the shift parameter
        #Here I took a different aproach and allowed negative shifts as well
        if -26 > shift or shift > 26:
            shift = shift % 26
        #and to speed up,  another checks if the shift is equal to 0. 
        #If it is, the program will simply reprint the starting message
        
        #create a list with all lowercase and uppercase letters
        alphabet_lower = string.ascii_lowercase
        alphabet_upper = string.ascii_uppercase        
        shifts = {}
        #each letter in each alphabet has a unicode character
        #ex: "a" = 97 and "A" = 65
        
        for alphabet in (alphabet_lower, alphabet_upper):
            first_letter_i = ord(alphabet[0])
            last_letter_i = ord(alphabet[-1])
            
            for letter in alphabet:
                num = ord(letter)
                #To that unicode character will add the shift. If the character 
                #surprasses the max number lowercase and uppercase,
                # will bring them back to the interspace 
                #Then, translate it from unicode to a letter
                if  num + shift > last_letter_i:
                     shifts[letter] = chr(num + shift - 26)                  
                elif num + shift < first_letter_i:
                    shifts[letter] = chr(num + shift + 26)
                else:
                    shifts[letter] = chr(num + shift)
                    
                       
        return shifts
                

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        #if shift = 0 return the same message, this way, there is less
        #calculation to be done.
        if shift == 0:
            return self.message_text
        # create a place to store the shift text then build the shift dic
        shifted_text = ""
        shift_dictionary = self.build_shift_dict(shift)
        
        #allow the characters that aren't letters to stay the same and
        #replace all letters.
        for character in self.message_text:
            if character in shift_dictionary:
                shifted_text += shift_dictionary[character]
            else:
                shifted_text += character
        return shifted_text
            

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
            #self.message_text = text
            #self.valid_words = load_words(WORDLIST_FILENAME)    
        
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')
        

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
               
        ciphered_messages ={}
        #for every message, try all possible shifts
        #Try all the 52 possible combinations:{-26<=shift>0<shift>=0}
        for shift_value in range (-26, 26):
            shifted_message = self.apply_shift(shift_value)
            valid_words = []
            #since spaces were not translated, usem them as ways to
            #cut that string into a group of characters of a list
            for characters in shifted_message.split():
                #by using is_word, all ponctuation will be ignored
                valid_words.append(is_word(self.valid_words, characters))
                
                
                #for every group of letters in the list that passes is_valid_word
                #increases the amount of counted words in that list 
                #store the results in a dictionary
                ciphered_messages[sum(valid_words)] = (shift_value, shifted_message)
                    
                
        return ciphered_messages.get(max(ciphered_messages))
        

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('--------------------')
    
    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    print('--------------------')
    #TODO: WRITE YOUR TEST CASES HERE
    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', -2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('--------------------')
    

    #TODO: best shift value and unencrypted story
    story = get_story_string()
    print("Encrypted Story:")
    print(story)
    cipher = CiphertextMessage(story)
    print("Decrypted Story:")
    print(cipher.decrypt_message())
    
    
