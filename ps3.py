# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import numpy as np

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 10

SCRABBLE_LETTER_VALUES = {
    '*':0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word=word.lower()
    #calculate the first component (sum of points for letters in the word)
    first_comp=0
    for letter in word:
        first_comp=first_comp+SCRABBLE_LETTER_VALUES[letter]
         
    #calculate the second component:
    if (7*len(word)-3*(n-len(word))) > 1:
        second_comp=7*len(word)-3*(n-len(word))
    else:
        second_comp=1
    
    word_score=first_comp*second_comp
    
    return word_score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        #add value 1 to key
        hand[x] = hand.get(x, 0) + 1
    hand['*']=hand.get('*',0)+1
    # for i in range(num_vowels):
    #     x = random.choice(VOWELS)
    #     #add value 1 to key
    #     hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand
# print(deal_hand(6))
#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 
    
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.
    
    Has no side effects: does not modify hand.
    
    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
#if all the characters in the word are in the hand -> no penalty -> modify hand -> new_hand
#create a dictionary out of the word and compare it

    word_dict=get_frequency_dict(word.lower())
    new_hand=hand.copy()
# print(new_hand.keys())
    for key1 in word_dict.keys():
        for key2 in new_hand.keys():
        #if the keys are similar, delete them from either dict
            if key1==key2 and word_dict[key1]<new_hand[key2]:
                new_hand[key2]=new_hand[key2]-word_dict[key1]
                word_dict[key1]=0
            
            elif key1==key2 and word_dict[key1]>new_hand[key2]:
                word_dict[key1]=word_dict[key1]-new_hand[key2]
                new_hand[key2]=0
                
            elif key1==key2 and word_dict[key1]==new_hand[key2]:
                word_dict[key1]=0
                new_hand[key2]=0
        
    # print(new_hand)
#if the word dictionary is empty, then the hand can form the word, else penalized -> modify the original hand   
# count_in=0s
# count_out=0
# print(new_hand)
# print(word_dict)

#create an array to verify if the word dict is empty
    veri_array=[]
    for keys in word_dict.keys():
        veri_array.append(word_dict[keys])
        
    veri_array=np.array(veri_array)
    is_all_zero=np.all(veri_array==0)
# print(veri_array)
    if is_all_zero:
        # print('Word is made')
        flag=True
        
    else:
        # print('Word is not made')
        flag=False
    #change the original hand input if word isnt made
    if flag==False:
        # print(new_hand)
        new_hand=hand
        word_dict=get_frequency_dict(word.lower())
        word_dict_copy=word_dict.copy()
        for key1 in word_dict.keys():
            for key2 in new_hand.keys():
            #if the keys are similar, delete them from either dict
                if key1==key2 and word_dict[key1]<new_hand[key2]:
                    new_hand[key2]=new_hand[key2]-word_dict[key1]
                    word_dict[key1]=0
                
                elif key1==key2 and word_dict[key1]>new_hand[key2]:
                    word_dict[key1]=word_dict[key1]-new_hand[key2]
                    new_hand[key2]=0
                    
                elif key1==key2 and word_dict[key1]==new_hand[key2]:
                    word_dict[key1]=0
                    new_hand[key2]=0
        # print(new_hand)
        #return the original dict if the word dict doesnt change (no letters from the hand could make the word)
        if word_dict_copy == word_dict.copy():
            return {}
        #return{}
        #else return the modified original hand
        else:
            return (new_hand)
    #if the word can be made, return the modified copy without modifying the original hand   
    else:
        return (new_hand)
# (update,flag)=word_made(hand,word)
# return update
# for key1 in word_dict.keys():
#     #completes if the word dict is empty -> return the remainings
#     if word_dict[key1]==0:
#         count_in=count_in+1
#         if count_in==len(word_dict):
#             print('The word can be made')
#             return new_hand
#     else:
#         count_out=count_out+1
#         if count_in+count_out==len(word_dict):
#             hand=new_hand
#             print('The word isnt made')
#             return hand
#         else: print(count_out+count_in)


# hand = {'r': 1, 'a': 3, 'p': 2, 't': 1, 'u':2}
# word="honey"
# a=display_hand(hand)
# x=update_hand(hand,"haney")
# print(x)
# print(hansd)
# print(hand)
# x=display_hand(hand)
# y=display_hand(new_hand)
# #


# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    #if the hand after function update is different from the original -> the word wanst made
    hand_copy=hand.copy()
    word_copy=word.lower()
    # print(hand_orig)
    x=update_hand(hand,word.lower())
    # print(x)
    # print(hand_copy)
    #If the copy hand is like the original and the return hand 
    #word can be made if the original hand doesnt change
    #However, if none character in the hand can is in the word, the original hand doesn't change as well
    if hand_copy == hand and x!={}:
        flag1=True
    
    else:
        flag1=False
        
    # print(flag1)
    
    #only True if the word is in the list
    count=0
    # print(word_copy)
    for letter in ('a','e','i','o','u'):
        # print(letter)
        word_copy=word.replace('*',letter)
        # print(word_copy)
        count=count+1
        # print(count)
        if word_copy in word_list or word.lower() in word_list:
            flag2=True
            # print(word.lower())
            break
        elif word_copy not in word_list and count==5:
            flag2=False
    # print(flag2)
    # if word.lower() in word_list:
    #     flag2=True
    # else:
    #     flag2=False
    # # print(flag2)
    
    
    return (flag1 and flag2)
    
    #test for wildcards:
# hand={'n': 1, 'h': 1, '*': 1, 'y': 1, 'd': 1, 'w': 1, 'e': 2}
# word='h*ney'
# m=is_valid_word(word,hand,load_words())

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length=0
    for value in hand.values():
        # print(value)
        length=length+value
    return length  # TO DO... Remove this line when you implement this function

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    n=calculate_handlen(hand)
    # print(n)
    # Keep track of the total score
    # score=get_word_score(word, n)
    total_score=0
    # As long as there are still letters left in the hand:
    while n>0:
        # Display the hand
        print('Current hand: ')
        disp=display_hand(hand)
        # Ask user for input
        word=str(input('Enter word, or "!!" to indicate that you are finished. If you enter a non-existent word, you got penalized: '))
        # If the input is two exclamation points:
        if word=='!!':
            # End the game (break out of the loop)
            break
        else:   
        # Otherwise (the input is not two exclamation points):
            validity=is_valid_word(word, hand, word_list)
            # If the word is valid:
            if validity == True:
                # Tell the user how many points the word earned,
                # and the updated total score
                score=get_word_score(word,n)
                total_score=total_score+score
                print(word+' earned '+str(score)+' points. Total: '+str(total_score)+' points')
                hand=update_hand(hand,word)
                n=calculate_handlen(hand)
            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
            else:
                print('That is not a valid word. You got penalized.')
            # update the user's hand by removing the letters of their inputted word
                hand=update_hand(hand,word)
                n=calculate_handlen(hand)

    # Game is over (user entered '!!' or ran out of letters),
    if word=='!!':
        print('Total score: '+str(total_score))
    else:
        print('Ran out of letters. Total score: '+str(total_score))
    # so tell user the total score
    # Return the total score as result of function
    return total_score
# hand={'a':1,'c':1,'i':1,'f':1,'t':1,'x':1,'*':1}
# game=play_hand(hand, load_words())

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand. 

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

#replace all copies of that letter with another one not in the set.

    hand_copy=hand.copy()
    alphabet='abcdefghijklmnopqrstuvwxyz'
    #create an array with character we can use:
    available_char=alphabet
    # print(available_char)
    for char in hand_copy.keys():
        # print(char)
        available_char=available_char.replace(char,'')
    #choose a random char and sub it in the hand_copy:
    pick=random.choice(available_char)
    # print(available_char)
    hand_copy[pick]=hand_copy.pop(letter)
    return hand_copy
              
# hand={'a':1,'c':1,'i':1,'f':1,'t':1,'x':1,'*':1}
# game=substitute_hand(hand, 'f')
# print(game)

def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings

    """
    play_time=int(input('Enter times you want to play: '))
    total_score=0
    for time in range(play_time):
        print('Turn #'+str(time+1))
        hand=deal_hand(HAND_SIZE)
        print('Current hand: ')
        disp=display_hand(hand)
        ok=0
        while ok==0:
            sub=str(input('Would you like to substitute a letter?: '))
            if sub=='yes' or sub=='no':
                ok=1
        if sub=='yes':
            letter=str(input('What is the letter? '))
            #If the letter is not in the hand, do nothing and ask for reinput
            while letter not in hand.keys():
                letter=str(input('Choose a letter that is in current hand: '))
            #substitute function
            hand=substitute_hand(hand,letter)
            total_score=total_score+play_hand(hand, word_list)
        else:
            total_score=total_score+play_hand(hand, word_list)
        print('----------------------')
    print('Final score: '+str(total_score))
    return total_score 
                
    
    #  ask=''
    # if ask!='yes' or ask!='no':
    # #Ask if user want to sub a letter? 
    #     ask=str(input('Would you like to substitute a letter? ')).lower()
    #     #If yes, which?
    #     if ask=='yes':
    #         letter=str(input('What is the letter? '))
    #         #If the letter is not in the hand, do nothing and ask for reinput
    #         #
    #         if letter not in hand.keys():
    #             letter=str(print('Choose a letter that is in current hand: '))
        
    #         #Otherwise, replace all copies of that letter with another one not in the set.
    #         else:
    #             hand_copy=hand.copy()
    #             alphabet='abcdefghijklmnopqrstuvwxyz'
    #             #create an array with character we can use:
    #             available_char=alphabet
    #             # print(available_char)
    #             for char in hand_copy.keys():
    #                 # print(char)
    #                 available_char=available_char.replace(char,'')
    #             #choose a random char and sub it in the hand_copy:
    #             pick=random.choice(available_char)
    #             # print(available_char)
    #             hand_copy[pick]=hand_copy.pop(letter)
    #             return hand_copy
                
                
    #     #otherwise, proceed to playgame, returning the same hand as input
    #     elif ask=='no':
    #         return hand
    #     else:
    #         print('Answer again, only yes or no: ')
    # print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
