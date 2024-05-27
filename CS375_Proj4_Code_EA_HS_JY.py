# CS375_Proj4_Code_EA_HS_JY.py
# CS375 Project 4: Edit Distance and Dynamic Programming
# Authors: Emmanuel Essumang, Hannah Soria, Jaime Yockey
# Date: 5/13/24


# Instructions on running:
# command: python CS375_Proj4_Code_EA_HS_JY.py


import os
import re
import sys
import time

class Dictionary:
    ''' dicitonary to be used for the spell checker'''
    def __init__(self):
        '''constructor
        
        parameters:
        files_reRead .  array, list of files to be read in order to build the dict
        '''
        self.dictionary = []

    def find_words(self, text):
        '''line of text to words
        '''
        pattern = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
        return pattern.findall(text.lower())

    # make the list of words in SCOWLS file + CS375 specific files
    def make_domain_dict(self):
        files = ["en_US-large.txt","dict_data/proj1.txt", "dict_data/proj2.txt", "dict_data/proj3.txt", "dict_data/ps0.txt", "dict_data/ps1.txt", "dict_data/ps2.txt"]
        word_list = []
        for file in files:
            fname = open(file)
            for line in fname:
                line = self.find_words(line)
                for word in line:
                    if word not in word_list:
                        word_list.append(word)
        word_list.sort()
        print(len(word_list))
        return word_list
    
    # make the list of the words in SCOWL file
    def make_scowl_dict(self):
        files = ["en_US-large.txt"]
        word_list = []
        for file in files:
            fname = open(file)
            for line in fname:
                line = self.find_words(line)
                for word in line:
                    if word not in word_list:
                        word_list.append(word)
        word_list.sort()
        return word_list
    
    # make the string of the text in "Proj4.txt"
    def make_string(self):
        mispelled = ""
        fname = open("Proj4.txt")
        for line in fname:
            line = self.find_words(line)
            for word in line:
                if word not in  mispelled:
                    word = word + " "
                    mispelled += word
        return mispelled
    
    # recursive implementation of edit distance
    def editDistance_recursive(self, S, T):
        '''return the distance lowest distance
        S singular word
        T singular word
        '''

        # base case: either s or t is 0 so return their lengths
        if len(S) == 0:
            return(len(T))
        elif len(T) == 0:
            return(len(S))

        else:
            # if their length is not 0 and the last character in the word is the same
            if S[-1] == T[-1]:
                # recursively call the next last element of each word
                return self.editDistance_recursive(S[:-1],T[:-1])
            # if their length is not zero and the last characters are not equal
            if S[-1] != T[-1]:
                # call min + 1 on the following recursive calls: both second to last elements, second to last S and last T, and last S and second to last T
                return( 1 + min(self.editDistance_recursive(S[:- 1],T[:- 1]), 
                                self.editDistance_recursive(S[:- 1],T), 
                                self.editDistance_recursive(S,T[:- 1])))


    # dynamic implementation of editDistance
    def editDistance_dynamic(self, S, T):
        #Get the length of both strings
        s, t = len(S), len(T)
        
        #Initialize a matrix to hold the minimum edit distances for all substring pairs
        #The matrix dimensions are (s+1) x (t+1) because we include the empty substring cases
        result = [[0] * (t + 1) for _ in range(s + 1)]
        
        #Base cases: transforming empty S to substrings of T (insert operations)
        for i in range(s + 1):
            result[i][0] = i

        #Base cases: transforming empty T from substrings of S (delete operations)
        for j in range(t + 1):
            result[0][j] = j
        
        #Fill the matrix with the costs of converting substrings of S to substrings of T
        for i in range(1, s + 1):
            for j in range(1, t + 1):
                #If the current characters in S and T are the same, no new cost is added
                if S[i - 1] == T[j - 1]:
                    result[i][j] = result[i - 1][j - 1]
                else:
                    #Calculate the cost of each operation and take the minimum
                    result[i][j] = 1 + min(result[i][j - 1],    # Insertion
                                        result[i - 1][j],    # Deletion
                                        result[i - 1][j - 1]) # Substitution
        
        #we use backtracking to find the transformation steps
        i, j = s, t
        steps = []
        while i > 0 and j > 0:
            if S[i - 1] == T[j - 1]:
                i -= 1
                j -= 1
            else:
                if result[i][j] == result[i - 1][j] + 1:
                    steps.append(f"Delete '{S[i-1]}' from position {i-1}")
                    i -= 1
                elif result[i][j] == result[i][j - 1] + 1:
                    steps.append(f"Insert '{T[j-1]}' at position {i}")
                    j -= 1
                else:
                    steps.append(f"Replace '{S[i-1]}' with '{T[j-1]}' at position {i-1}")
                    i -= 1
                    j -= 1
        
        #to handle the remaining insertions or deletions
        while i > 0:
            steps.append(f"Delete '{S[i-1]}' from position {i-1}")
            i -= 1
        while j > 0:
            steps.append(f"Insert '{T[j-1]}' at position {i}")
            j -= 1

        steps.reverse()

        #return both the edit distance and the transformation steps so we can see the steps and whats happening 
        return result[s][t], steps

    # finds mispelled words in the string T and returns the five closest suggestions
    def spell_Checker(self,T,D):
        mispelled = 0
        misspelled_words = []
        T = T.split() # split the text on while spaces
        possibles = {} # create a dictionary for possible corrections to the target word
        for word in T:  # for each word in the iput string
            if word not in D:  # if that word is not in the dictionary
                mispelled += 1
                misspelled_words.append(word)
                dist = {} # new dictionary
                for item in D:  # for each word in dictionary D
                    dist[item] = self.editDistance_dynamic(word, item) # add to the dictionary the word and the distance
                matches = sorted(dist, key=dist.get) # sort the dictionary by distances 
                possibles[word] = matches[:5] # updates possibles dictionary with the mispelled word as key and first 5 in matches dict as value
                curr = possibles
                print(curr,"\n")
                curr.clear()
        print("the number of mispelled words: ", mispelled)
        print("the mispelled words: ", misspelled_words)
        return possibles
    

    # make the string of the text in "dict_data/parent_article.txt"
    def make_string_slang(self):
        mispelled = ""
        fname = open("dict_data/parent_article.txt")
        for line in fname:
            line = self.find_words(line)
            for word in line:
                if word not in  mispelled:
                    word = word + " "
                    mispelled += word
        return mispelled
    
    # make the list of words in SCOWLS file + slang.txt file
    def make_domain_dict_slang(self):
        files = ["en_US-large.txt","dict_data/slang.txt"]
        word_list = []
        for file in files:
            fname = open(file)
            for line in fname:
                words = self.find_words(line)
                for word in words:
                    if word not in word_list:
                        word_list.append(word)
        return word_list
    

    
def main():

    # EDIT DISTANCE TESTING
    print("--------------------------------------------------------------------------")
    print("edit distance testing")

    # test edit distance recursive
    tester_dict = Dictionary()
    S = "world"
    T = "worll"
    print("testing recursive editDistance on 1 edit:")
    time.sleep(5)
    time_re = time.time()
    tester_dict.editDistance_recursive(S,T)
    time_re2 = time.time()
    print(tester_dict.editDistance_recursive(S,T))
    total_re = time_re2-time_re
    print("time to run: ", total_re, "\n")

    S = "hellohellohellohellohellohello"
    T = "worll"
    print("testing recursive editDistance on 27 edits: ")
    time.sleep(5)
    time_re3 = time.time()
    tester_dict.editDistance_recursive(S,T)
    time_re4 = time.time()
    print(tester_dict.editDistance_recursive(S,T))
    total_re2 = time_re4-time_re3
    print("time to run: ", total_re2, "\n")

    # test edit distance dynamic
    tester_dict = Dictionary()
    S = "world"
    T = "worll"
    print("testing dynamic editDistance on 1 edit:")
    time.sleep(5)
    time_dy = time.time()
    tester_dict.editDistance_dynamic(S,T)
    time_dy2 = time.time()
    print(tester_dict.editDistance_dynamic(S,T))
    total_dy = time_dy2-time_dy
    print("time to run: ", total_dy, "\n")

    S = "hellohellohellohellohellohello"
    T = "worll"
    print("testing dynamic editDistance on 27 edits: ")
    time.sleep(5)
    time_dy3 = time.time()
    tester_dict.editDistance_dynamic(S,T)
    time_dy4 = time.time()
    print(tester_dict.editDistance_dynamic(S,T))
    total_dy2 = time_dy4-time_dy3
    print("time to run: ", total_dy2, "\n")
    
    
    # SPELL CHECKER TESTING
    print("--------------------------------------------------------------------------")
    print("spell checker testing")

    # create dictionary obj
    test_dict = Dictionary()

    # create scowls dictionary
    print("creating SCOWL dictionary and Proj4 string")
    new_dict = test_dict.make_scowl_dict()
    new_spell = test_dict.make_string()

    # get the time for scowls
    time3 = time.time()
    test_dict.spell_Checker(new_spell, new_dict)
    time4 = time.time()

    # create domain specific dictionary
    print("creating domain specific dictionary and Proj4 string")
    dictionary = test_dict.make_domain_dict()
    mispelled = test_dict.make_string()

    # get the time for domain specific
    time1 = time.time()
    test_dict.spell_Checker(mispelled, dictionary)
    time2 = time.time()

    # get the total times
    total = time2-time1
    total2 = time4-time3

    # print the domain specific
    print("the total for domain specific",total)
    print("the total for scowl",total2)

    # ANOTHER SPECIIC DOMAIN TESTING
    print("--------------------------------------------------------------------------")
    print("another specific domain:")
    
    # create dictionary obj
    test_dict2 = Dictionary()

    # create scowls dictionary
    print("creating SCOWL dictionary and parent article")
    new_dict_slang = test_dict2.make_scowl_dict()
    new_spell_slang = test_dict2.make_string_slang()
    test_dict2.spell_Checker(new_spell_slang, new_dict_slang)

    print("creating domain specific dictionary")
    new_dict_slang2 = test_dict2.make_domain_dict_slang()
    test_dict2.spell_Checker(new_spell_slang, new_dict_slang2)


if __name__ == "__main__":
    main()