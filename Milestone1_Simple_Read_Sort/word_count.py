import string
import argparse


# Function to look for a word in a line of text that has been split into words with
# all punctuation removed
def countSingleWord(source, word):
    # make lower case so we don't have mismatch on case
    source = source.lower()
    word = word.lower()

    # split line into a list of words
    sourceList = source.split()

    # loop through the list and remove any punctuation from the words
    cleanList = []
    for w in sourceList:
        w = w.strip(string.punctuation)
        cleanList.append(w)

    # Call the countWordOccurrences function
    count = countWordOccurrences(cleanList, word)
    return count


# Recursive function to count the occurences of a single string in a list.
def countWordOccurrences(myList, value):
    # base case
    if myList == []:
        return 0
    # check if element is another list
    elif isinstance(myList[0], list):
        # call function with current element and add the rest of the list
        return countWordOccurrences(myList[0], value) + countWordOccurrences(myList[1:], value)
    else:
        # check if element is the value that was passed in
        if myList[0] == value:
            # call function with rest of list and add 1 (since we found an occurrence)
            return 1 + countWordOccurrences(myList[1:], value)
        else:
            # call function with rest of list
            return countWordOccurrences(myList[1:], value)


# Function to count the occurrences of a phrase in a string
def countPhrase(line, phrase):
    # Make lower case to avoid case mismatch
    line = line.lower()
    phrase = phrase.lower()

    # Look in line for the phrase, if found continue looking through the rest of the line until not found
    count = 0
    while True:

        # Find position in line where phrase was found
        position = line.find(phrase)
        if position != -1:
            count = count + 1
            line = line[position + 1:]  # remove up to where the phrase was found so we don't find it again
        else:
            break

    return count


# User the argument parser to get the word that was passed in
parser = argparse.ArgumentParser()
parser.add_argument("word")
args = parser.parse_args()
targetWord = args.word

# check if word is a single word or phrase
tmpList = targetWord.split()
if len(tmpList) > 1:
    singleWord = False
else:
    singleWord = True

# Input file
sourceFile = "tweets.txt"

# Read file content into a list
file = open(sourceFile, "r", encoding="UTF-8")
fileContent = file.readlines()

# Initialize word count
wordCount = 0

# Loop through all lines in the file
for line in fileContent:

    # Call appropriate function based on a single word or phrase
    if singleWord == True:
        # count the number of times the word appears in the current line
        tmpCount = countSingleWord(line, targetWord)
    else:
        # count the number of time the phrase appears in the current line
        tmpCount = countPhrase(line, targetWord)

    # Increment the wordCount
    wordCount = wordCount + tmpCount

print("The word: " + targetWord + " appeared " + str(wordCount) + " times in the source file: " + sourceFile)



