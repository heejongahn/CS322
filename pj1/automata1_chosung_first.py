__author__ = 'Nobell_User'
# -*- coding: utf-8 -*-


#########################  KOREAM_Mealy_Simulator에 사용할 변수들  ######################################################

states = ["S", "V", "O", "U", "A", "I", "K", "N", "R", "L", 'X']
vocabulary = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ", "ㄲ", "ㄸ", "ㅃ", "ㅆ", "ㅉ", "ㅏ", "ㅑ", "ㅓ", "ㅕ", "ㅗ", "ㅛ", "ㅜ", "ㅠ", "ㅡ", "ㅣ", "ㅔ", "ㅖ", "ㅐ", "ㅒ", "---" ]
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ' , 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ','ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
BASE = 44032
CHOSUNG = 588
JUNGSUNG = 28

stateTransitionFunction = {}
state_file  = open("stateTransitionFunction_chosung.txt", "r")
line = state_file.readline()
while line :
    line = line.strip("\n")
    line_list = line.split(" ")
    line_list[1] = line_list[1].split("@")
    for e in line_list[1]:
        key = (line_list[0], e)
        value = line_list[2]
        stateTransitionFunction[key] = value
    line = state_file.readline()


outputFunction = {}
output_file  = open("outputFunction_chosung.txt", "r")
line = output_file.readline()
while line :
    line = line.strip("\n")
    line_list = line.split(" ")
    line_list[1] = line_list[1].split("@")
    for e in line_list[1]:
        key = (line_list[0], e)
        value = line_list[2]
        outputFunction[key] = value
    line = output_file.readline()

#############################################################################################################


###################################### outputFunction들의 정의 ##############################################

def newChar(currentString, inputChar):
    currentString+=inputChar
    return currentString

def JaEumtoMoEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    jaeum = currentString[length-3:]

    chosungIndex = CHOSUNG_LIST.index(jaeum)
    jungsungIndex = JUNGSUNG_LIST.index(inputChar)

    nextWord = unichr(BASE+CHOSUNG*chosungIndex+JUNGSUNG*jungsungIndex).encode('utf-8')
    rest += nextWord
    return rest

def MoEumtoBaadChim(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]

    currentOrd = ord(currentWord.decode('utf-8'))
    jongsungIndex = JONGSUNG_LIST.index(inputChar)

    nextWord = unichr(currentOrd + jongsungIndex).encode('utf-8')
    rest += nextWord
    return rest

def MoEumtoMoEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]
    currentOrd = ord(currentWord.decode('utf-8'))
    currentMoEumIndex = ((currentOrd - BASE) % CHOSUNG) / JUNGSUNG
    inputMoEumIndex = JUNGSUNG_LIST.index(inputChar)

    if currentMoEumIndex == 8 :
        if inputMoEumIndex == 0 :
            newMoEumIndex = 9
        elif inputMoEumIndex == 1 :
            newMoEumIndex = 10
        elif inputMoEumIndex == 20 :
            newMoEumIndex = 11
    elif currentMoEumIndex == 13 :
        if inputMoEumIndex == 4 :
            newMoEumIndex = 14
        elif inputMoEumIndex == 5 :
            newMoEumIndex = 15
        elif inputMoEumIndex == 20 :
            newMoEumIndex = 16
    elif currentMoEumIndex == 18:
        newMoEumIndex = 19

    nextWord = unichr(currentOrd - currentMoEumIndex * JUNGSUNG + newMoEumIndex * JUNGSUNG).encode('utf-8')
    rest += nextWord
    return rest

def BaadChimtoBaadChim(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]
    currentOrd = ord(currentWord.decode('utf-8'))
    currentBaadChimIndex = (currentOrd - BASE) % JUNGSUNG
    inputBaadChimIndex = JONGSUNG_LIST.index(inputChar)

    if currentBaadChimIndex == 1 :
        nextBaadChimIndex = 3
    elif currentBaadChimIndex == 17 :
        nextBaadChimIndex = 18
    elif currentBaadChimIndex == 4 :
        if inputBaadChimIndex == 22 :
            nextBaadChimIndex = 5
        else:
            nextBaadChimIndex = 6
    elif currentBaadChimIndex == 8 :
        if inputBaadChimIndex == 7 :
            nextBaadChimIndex = 9
        if inputBaadChimIndex == 16 :
            nextBaadChimIndex = 10
        if inputBaadChimIndex == 17:
            nextBaadChimIndex = 11
        if inputBaadChimIndex == 19 :
            nextBaadChimIndex = 12
        if inputBaadChimIndex == 25 :
            nextBaadChimIndex = 13
        if inputBaadChimIndex == 26 :
            nextBaadChimIndex = 14
        if inputBaadChimIndex == 27 :
            nextBaadChimIndex = 15

    nextWord = unichr(currentOrd - currentBaadChimIndex + nextBaadChimIndex).encode('utf-8')
    rest += nextWord
    return rest

def BaadChimtoDoubleBaadChim(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]

    newString = MoEumtoBaadChim(rest, currentWord)
    return newChar(newString, inputChar)

def JaEumtoJaEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]

    newString = MoEumtoBaadChim(rest, currentWord)
    return newChar(newString, inputChar)

def DoubleJaEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]
    rest = BaadChimtoBaadChim(rest, currentWord)
    return newChar(rest, inputChar)

def BackSpace(currentString, inputChar):
    length = len(currentString)
    if length == 0:
        return currentString
    return currentString[:length-3]


def CheckFinal(currentString) :
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]

    if ord(currentWord.decode('utf-8')) <= BASE:
        return MoEumtoBaadChim(rest, currentWord)
    else:
        return currentString

#############################################################################################################

################################### 한글 모아쓰기 오토마타 ###################################################

def KOREAN_Mealy_Simulator (states, vocabulary, stateTransitionFunction, outputFunction, initialState):
    # We're gonna receive state transition function as dictionary : {(current state, input): next state, ...}
    print "한글 스트링을 입력하세요."
    inputString = raw_input()
    if inputString=='':
        inputString='ㅁㅜㄹㄲㅡㄹㅎㄴㅡㄴㄷㅏ'
    inputLength = len(inputString)
    currentState = initialState
    currentString = ''

    for i in range (inputLength/3):
        inputChar = inputString[3*i:3*i+3]
    # We're gonna check the legitimacy of the string, character by character.
        if inputChar not in vocabulary:
            print "Error occurred : This input is not accepted by given grammar!!!"
            return
        # If current character is not an element of vocabulary, Mealy Machine should not accept the string.

        isDeadState = True
        # Assume that current state is a dead state
        if ((currentState, inputChar) in stateTransitionFunction):
            currentOutput = outputFunction[(currentState, inputChar)]
            currentState = stateTransitionFunction[(currentState, inputChar)]
            currentString = eval(currentOutput + '("' + currentString + '",' + '"' + inputChar + '")')
            print currentString
            isDeadState = False
        # If there's (currentState, inputString[i]) defined in state transition function, then the state is not a dead state.
        # Also, set current state as next state. (We assume that the step move is made in this point.)

        if isDeadState:
            print "Error occurred : This input is not accepted by given grammar."
            return
        # If isDeadState is still true : there are two possibilities
        # 1. current state is a dead state
        # 2. current state is not a dead state, but there's no state transition function for current state that accepts current character (inputString[i])
        # Either way, Mealy machine should not accept the string.

    currentString = CheckFinal(currentString)
    print currentString
    return

#############################################################################################################

KOREAN_Mealy_Simulator (states, vocabulary, stateTransitionFunction, outputFunction, 'S')