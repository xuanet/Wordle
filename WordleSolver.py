"""
Created on 6/7/2022

@author: xuanet
"""

from Wordle import WordleGame

class WordleSolver(WordleGame):

    def __init__(self, file):
        self.word = self.chooseWord(file)
        self.freq = self.createFreqDict(self.word)
        # self.debug = self.debugMode()
        self.debug = False

        self.myCurrGuess = None
        self.myCurrGYB = None
        self.score = 0

    def recommendWord(self):
        print("There are " + str(len(self.list)) + " candidate words")
        print("I suggest " + self.list[0])

    def recommendWordSimulator(self):
        if len(self.list) == 0:
            print(self.score)
            raise IndexError("empty list")
        return self.list[0]

    def modifySeachList(self):
        newList = []
        blackLetters = set([])
        greenLetters = set([])
        greenLetterIndices = set([])
        yellowLetters = set([])
        yellowLetterIndices = set([])

        for i in range(5):
            if self.myCurrGYB[i] == "B":
                blackLetters.add(self.myCurrGuess[i])
            elif self.myCurrGYB[i] == "G":
                greenLetters.add(self.myCurrGuess[i])
                greenLetterIndices.add(i)
            elif self.myCurrGYB[i] == "Y":
                yellowLetters.add(self.myCurrGuess[i])
                yellowLetterIndices.add(i)

        blackExclusive = blackLetters - yellowLetters - greenLetters

        for w in self.list:

            toInclude = True
            for index in yellowLetterIndices:
                if self.myCurrGuess[index] not in w:
                    toInclude = False
                    break

            if not toInclude:
                continue

            for i in range(5):
                if i in greenLetterIndices and w[i] != self.myCurrGuess[i]:
                    toInclude = False
                    break
                if i in yellowLetterIndices and w[i] == self.myCurrGuess[i]:
                    toInclude = False
                    break
                if w[i] in blackExclusive:
                    toInclude = False
                    break

            if toInclude:
                newList.append(w)

        if self.myCurrGuess in newList:
            newList.remove(self.myCurrGuess)

        self.list = newList


    def runGame(self):
        """Runs the Wordle game"""

        whitespace = "                                         " \


        allGuesses = []
        allGYB = []
        countGuesses = 0
        attemptsLeft = 10

        while attemptsLeft > 0:
            if self.debug:
                print("\n" + self.word + "\n")

            print("Type a 5-letter word")
            currGuess = input()
            self.myCurrGuess = currGuess
            while len(currGuess) != 5:
                print("Guess must have 5 letters")
                currGuess = input()
                self.myCurrGuess = currGuess

            allGuesses.append(list(currGuess))
            currGYB = self.processGuess(currGuess, self.word, self.freq)
            self.myCurrGYB = currGYB
            allGYB.append(currGYB)

            for i in range(len(allGuesses)):
                myGuess = " ".join(allGuesses[i])
                myGYB = " ".join(allGYB[i])

                print(whitespace + myGuess + "         " + myGYB)

            if currGuess == self.word:
                countGuesses += 1
                self.score += 1
                print("You won!")
                print("Guesses used " + str(countGuesses))
                return True

            print("here")

            self.modifySeachList()
            self.recommendWord()

            print("now here")

            attemptsLeft -= 1
            countGuesses += 1
            self.score += 1
            print("Totol guesses " + str(countGuesses))

        print("You lost\nThe correct word was " + self.word)
        return False


    def runGameSimulation(self):
        """Runs the Wordle game simulator"""

        allGuesses = []
        allGYB = []
        countGuesses = 0

        while True:
            if self.score == 0:
                currGuess = "crane"

            else:
                currGuess = self.recommendWordSimulator()

            self.myCurrGuess = currGuess

            allGuesses.append(list(currGuess))
            currGYB = self.processGuess(currGuess, self.word, self.freq)
            self.myCurrGYB = currGYB
            allGYB.append(currGYB)

            # for i in range(len(allGuesses)):
            #     myGuess = " ".join(allGuesses[i])
            #     myGYB = " ".join(allGYB[i])
            #
            #     print(whitespace + myGuess + "         " + myGYB)

            if currGuess == self.word:
                countGuesses += 1
                self.score += 1
                return True

            self.modifySeachList()
            countGuesses += 1
            self.score += 1

if __name__ == '__main__':
    pass

# print("here")

# playAgain = True
# wins = 0
# losses = 0

# print("now here")

# while playAgain == True:
#     won = WordleSolver("fiveletterwords.txt").runGame()
#     if won == True:
#         wins += 1
#     else:
#         losses += 1
#     f = input("Play again? y/n")
#     if f == 'n':
#         playAgain = False

#     print("Your final score is " + str(wins) + " wins and " + str(losses) + " losses.")

d = {}
for i in range(1, 15):
    d[i] = 0

for i in range(1000):
    game = WordleSolver("wordle-answers-alphabetical.txt")
    game.runGameSimulation()
    d[game.score] += 1

print(d)

expectedScore = 0
for i in range(1, 15):
    expectedScore += d[i]*i

print("\nAverage score: " + str(expectedScore/1000))
