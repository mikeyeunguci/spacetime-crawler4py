import sys
import re

#This method runs in O(n) for every word it finds using the .split() where n is the number of words
#as well as O(l) where l is the length of the word for isascii checking, to convert into lowercase, to use regex twice, and to iterate through the word twice(for underscore and before appending)
#This method should run in about linear time to the size of the file(s) with O(n) + O(l), n being the number of words and l being the length of words
#returns list of tokens
def tokenize(name): 
    Tokens = []        
    
    with open(name) as File:
        for line in File:
            for word in line.split():                                   #For ever word in a line from File make lowercase
                if word.isascii():                                      #Check for non-English characters in the word and doesnt proceed if it does, makes lower if all English
                    word = word.lower()
                    if "_" in word:                                     #Regular expression are used to remove/filter unwanted characters
                        word = re.sub(r'_', " ", word)                  #These regex checks of edges of words for non-word characters such as spaces(\b) and                      
                    word = re.findall(r'\b[A-Za-z0-9]+\b', word)        #removes anything not A-z and 0-9 (A-Za-z0-9) that are next to each other(+) as well as uses '_' to remove underscores and replace them with spaces
                    for w in word:                                      #Appends to List and return
                        Tokens.append(w)                             
        File.close
    return Tokens


#This method run in O(n) + O(nlogn) time where n is the size of the array(Tokens/Words). This is becuase the sorting algorithms is .sort() and sorted() take O(nlogn) time
#It takes O(n) to iterate through the array of words and O(nlogn) twice to sort the dictionary by alphabet and then by value(frequency)
#Since the sorting algorithms take the most time, the overall runtime of this method is O(nlogn) a log-linear time complexity
# returns dictionary of tokens and frequencies
def computeWordFrequencies(Tokens): 
    sortedDict = {}

    for token in Tokens:                                                    #For every token if its not in dictionary, add to dictionary, else increment its count
        if token not in sortedDict:
            sortedDict[token] = 1
        else:
            sortedDict[token] = sortedDict.get(token) + 1

    keys = list(sortedDict.keys())                                          #Take keys and sort by alphabet
    keys.sort()

    sortedDict = {key: sortedDict[key] for key in keys}                     #use sorted keys to then sort by value of key and return
    sortedDict = dict(sorted(sortedDict.items(), key=lambda x : x[1], reverse=True))
    return sortedDict

#This method takes O(n) time becuase it has through go through all of the dictionary of n size(words)
#prints out whats in the Dictionary
def printTokenFreq(Dict):
    for key in Dict:
        print(key, "-", Dict[key])

def main():
    try:
        if sys.argv[1].endswith('.txt'):
            try:
                printTokenFreq(computeWordFrequencies(tokenize(sys.argv[1])))
            except:
                print("File not found, Closing Script")
                quit()
        else:
            print("Invalid File, Closing Script")
            quit()
    except IndexError:
        print("Missing File Input, Closing Script")
        quit()

if __name__ == "__main__":
    main()