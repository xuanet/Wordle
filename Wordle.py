"""Created by xuanet"""
"""June 5, 2022"""

import random
import copy

def chooseWord(filename):
    """Chooses a random 5-letter word from the file"""

    f = open(filename)
    wordList = []
    for word in f:
        wordList.append(word.strip())
    return random.choice(wordList)


def createFreqDict(word):
    """Creates a dictionary relating letter indices with its corresponding
    letter"""

    d = {}
    for i in range(len(word)):
        char = word[i]
        if char not in d:
            d[char] = 0
        d[char] = d[char] + 1
    return d


def processGuess(guess, actual, frequencies):
    """Returns the Green-Yellow-Black analysis of user's guess"""

    GYB = []
    letterFreq = copy.deepcopy(frequencies)
    for i in range(5):
        guessLetter = guess[i]
        if guessLetter not in letterFreq:
            GYB.append("B")
            continue
        if guessLetter == actual[i]:
            GYB.append("G")
            letterFreq[guessLetter] = letterFreq[guessLetter] - 1
            continue
        for j in range(5):
            if i != j and guessLetter == actual[j] and letterFreq.get(
                    guessLetter) > 0 and guess[j] != actual[j]:
                GYB.append("Y")
                letterFreq[guessLetter] = letterFreq[guessLetter] - 1
                break

            elif letterFreq.get(guessLetter) == 0 or j == 4:
                GYB.append("B")
                break

    if len(GYB) != len(guess):
        print(GYB)
        #print("error")
        raise ValueError("GYB length is mismatched with guess length")
    return GYB


def debugMode():
    """Asks user whether to play in debug mode"""

    debug = input("Debug mode? y/n")
    if debug == "y":
        return True
    return False


def runGame():
    """Runs the Wordle game"""

    whitespace = "                                                     "
    # debug = debugMode()
    debug = False
    secretWord = chooseWord("wordle-answers-alphabetical.txt")

    freq = createFreqDict(secretWord)
    allGuesses = []
    allGYB = []
    countGuesses = 0
    attemptsLeft = 10

    while attemptsLeft > 0:
        if debug:
            print("\n" + secretWord + "\n")

        print("Type a 5-letter word")
        currGuess = input()
        while len(currGuess) != 5:
            print("Guess must have 5 letters")
            currGuess = input()

        allGuesses.append(list(currGuess))
        currGYB = processGuess(currGuess, secretWord, freq)
        allGYB.append(currGYB)

        for i in range(len(allGuesses)):
            myGuess = " ".join(allGuesses[i])
            myGYB = " ".join(allGYB[i])

            print(whitespace + myGuess + "         " + myGYB)

        if currGuess == secretWord:
            countGuesses += 1
            print("You won!")
            print("Guesses used " + str(countGuesses))
            return True

        attemptsLeft -= 1
        countGuesses += 1
        print("Total guesses " + str(countGuesses))

    print("You lost\nThe correct word was " + secretWord)


if __name__ == '__main__':
    pass

playAgain = True
wins = 0
losses = 0

while playAgain == True:
    won = runGame()
    if won == True:
        wins += 1
    else:
        losses += 1
    f = input("Play again? y/n")
    if f == 'n':
        playAgain = False

    print("Your final score is " + str(wins) + " wins and " + str(losses) + " losses.")
