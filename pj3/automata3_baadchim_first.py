__author__ = 'Nobell_User'
# -*- coding: utf-8 -*-

#########################  KOREAM_Mealy_Simulator에 사용할 변수들  ##########################################

states = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67']
vocabulary = ['#', '$', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '_']
vocamap= {'#':'ㅜ', '$':'ㅈ', '0':'ㅇ', '1':'ㄱ', '2':'ㅣ', '3':'ㅏ', '4':'ㄷ', '5':'ㄴ', '6':'ㅓ', '7':'ㅁ', '8':'ㅂ', '9':'ㅗ'}
finalStates = ['0', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '22', '23', '26', '28', '31', '32', '33', '35', '36', '38', '39', '42', '45', '46', '47', '50', '52', '53', '54', '58', '59', '60', '62', '63', '64', '65', '66', '67']


CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ' , 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ','ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
BASE = 44032
CHOSUNG = 588
JUNGSUNG = 28

stateTransitionFunction = {}
state_file  = open("stateTransitionFunction_baadchim.txt", "r")
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
output_file  = open("outputFunction_baadchim.txt", "r")
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
    currentString+=vocamap[inputChar]
    return currentString

def JaEumtoMoEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    jaeum = currentString[length-3:]

    chosungIndex = CHOSUNG_LIST.index(jaeum)
    jungsungIndex = JUNGSUNG_LIST.index(vocamap[inputChar])

    nextWord = unichr(BASE+CHOSUNG*chosungIndex+JUNGSUNG*jungsungIndex).encode('utf-8')
    rest += nextWord
    return rest

def replaceJaEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    jaeum = currentString[length-3:]

    currentJaEumIndex = CHOSUNG_LIST.index(jaeum)
    inputJaEumIndex = CHOSUNG_LIST.index(vocamap[inputChar])

    if inputJaEumIndex == 0:
        if currentJaEumIndex == 0:
            newJaEum = 'ㅋ'
        elif currentJaEumIndex == 15:
            newJaEum = 'ㄲ'
        else:
            newJaEum = 'ㄱ'
    elif inputJaEumIndex == 2:
        if currentJaEumIndex == 2:
            newJaEum = 'ㄹ'
        else:
            newJaEum = 'ㄴ'
    elif inputJaEumIndex == 3:
        if currentJaEumIndex == 3:
            newJaEum = 'ㅌ'
        elif currentJaEumIndex == 25:
            newJaEum = 'ㄸ'
        else:
            newJaEum = 'ㄷ'
    elif inputJaEumIndex == 6:
        if currentJaEumIndex == 6:
            newJaEum = 'ㅅ'
        elif currentJaEumIndex == 9:
            newJaEum = 'ㅆ'
        else:
            newJaEum = 'ㅁ'
    elif inputJaEumIndex == 7:
        if currentJaEumIndex == 7:
            newJaEum = 'ㅍ'
        elif currentJaEumIndex == 26:
            newJaEum = 'ㅃ'
        else:
            newJaEum = 'ㅂ'
    elif inputJaEumIndex == 11:
        if currentJaEumIndex == 11:
            newJaEum = 'ㅎ'
        else:
            newJaEum = 'ㅇ'
    else:
        if currentJaEumIndex == 12:
            newJaEum = 'ㅊ'
        elif currentJaEumIndex == 14:
            newJaEum = 'ㅉ'
        else:
            newJaEum = 'ㅈ'

    rest += newJaEum
    return rest

def replaceMoEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]

    currentWord = currentString[length-3:]
    currentOrd = ord(currentWord.decode('utf-8'))
    currentJaEumIndex = (currentOrd - BASE) / CHOSUNG
    currentMoEumIndex = ((currentOrd - BASE) % CHOSUNG) / JUNGSUNG
    inputMoEumIndex = JUNGSUNG_LIST.index(vocamap[inputChar])

    if inputMoEumIndex == 20:

        # ㅏ -> ㅐ
        if currentMoEumIndex == 0:
            nextMoEumIndex = 1

        # ㅑ -> ㅒ
        elif currentMoEumIndex == 2:
            nextMoEumIndex = 3

        # ㅓ -> ㅔ
        elif currentMoEumIndex == 4:
            nextMoEumIndex = 5

        # ㅕ -> ㅖ
        elif currentMoEumIndex == 6:
            nextMoEumIndex = 7

        # ㅗ -> ㅚ
        elif currentMoEumIndex == 8:
            nextMoEumIndex = 11

        # ㅜ -> ㅟ
        elif currentMoEumIndex == 13:
            nextMoEumIndex = 16

        # ㅘ -> ㅙ
        elif currentMoEumIndex == 9:
            nextMoEumIndex = 10

        # ㅝ -> ㅞ
        elif currentMoEumIndex == 14:
            nextMoEumIndex = 15

        # ㅣ -> ㅡ
        elif currentMoEumIndex == 20:
            nextMoEumIndex = 18

        # ㅡ -> ㅢ
        elif currentMoEumIndex == 18:
            nextMoEumIndex = 19

        # ㅢ -> ㅣ
        else:
            nextMoEumIndex = 20


    elif inputMoEumIndex == 0:

        # ㅏ -> ㅑ
        if currentMoEumIndex == 0:
            nextMoEumIndex = 2

        # ㅑ -> ㅏ
        elif currentMoEumIndex == 2:
            nextMoEumIndex = 0

        # ㅗ -> ㅘ
        else:
            nextMoEumIndex = 9

    elif inputMoEumIndex == 4:

        # ㅓ -> ㅕ
        if currentMoEumIndex == 4:
            nextMoEumIndex = 6

        # ㅕ -> ㅓ
        elif currentMoEumIndex == 6:
            nextMoEumIndex = 4

        # ㅜ -> ㅝ
        else:
            nextMoEumIndex = 14

    elif inputMoEumIndex == 8:

        # ㅗ -> ㅛ
        if currentMoEumIndex == 8:
            nextMoEumIndex = 12

        # ㅛ -> ㅗ
        elif currentMoEumIndex == 12:
            nextMoEumIndex = 8

    elif inputMoEumIndex == 13:

        # ㅜ -> ㅠ
        if currentMoEumIndex == 13:
            nextMoEumIndex = 17

        # ㅠ -> ㅜ
        elif currentMoEumIndex == 17:
            nextMoEumIndex = 13


    nextWord = unichr(BASE+CHOSUNG*currentJaEumIndex+JUNGSUNG*nextMoEumIndex).encode('utf-8')
    rest += nextWord
    return rest

def replaceBaadChim(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]
    currentOrd = ord(currentWord.decode('utf-8'))
    currentJaEumIndex = (currentOrd - BASE) / CHOSUNG
    currentMoEumIndex = ((currentOrd - BASE) % CHOSUNG) / JUNGSUNG
    currentBaadChimIndex = (currentOrd - BASE) % JUNGSUNG
    inputBaadChimIndex = JONGSUNG_LIST.index(vocamap[inputChar])

    if inputBaadChimIndex == 1:
        if currentBaadChimIndex == 1:
            nextBaadChimIndex = 24
        elif currentBaadChimIndex == 24:
            nextBaadChimIndex = 2
        else:
            nextBaadChimIndex = 1

    elif inputBaadChimIndex == 4:
        if currentBaadChimIndex == 4:
            nextBaadChimIndex = 8
        else:
            nextBaadChimIndex = 4

    elif inputBaadChimIndex == 7:
        nextBaadChimIndex = 25

    elif inputBaadChimIndex == 16:
        if currentBaadChimIndex == 16:
            nextBaadChimIndex = 19
        elif currentBaadChimIndex == 19:
            nextBaadChimIndex = 20
        elif currentBaadChimIndex == 20:
            nextBaadChimIndex = 16
        else:
            nextBaadChimIndex = 12


    elif inputBaadChimIndex == 17:
        if currentBaadChimIndex == 17:
            nextBaadChimIndex = 26
        else:
            nextBaadChimIndex = 14

    elif inputBaadChimIndex == 21:
        if currentBaadChimIndex == 21:
            nextBaadChimIndex = 27
        else:
            nextBaadChimIndex = 21

    elif inputBaadChimIndex == 22:
        nextBaadChimIndex = 23

    nextWord = unichr(BASE+CHOSUNG*currentJaEumIndex+JUNGSUNG*currentMoEumIndex+nextBaadChimIndex).encode('utf-8')
    rest += nextWord
    return rest

def BaadChimtoJaEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]
    currentOrd = ord(currentWord.decode('utf-8'))
    currentJaEumIndex = (currentOrd - BASE) / CHOSUNG
    currentMoEumIndex = ((currentOrd - BASE) % CHOSUNG) / JUNGSUNG
    currentBaadChimIndex = (currentOrd - BASE) % JUNGSUNG
    inputJaEumIndex = CHOSUNG_LIST.index(vocamap[inputChar])


    if inputJaEumIndex == 0:
        nextBaadChimIndex = 8
        newJaEum = 'ㅋ'
    elif inputJaEumIndex == 3:
        nextBaadChimIndex = 8
        newJaEum = 'ㄸ'
    elif inputJaEumIndex == 6:
        newJaEum = 'ㅆ'
        if currentBaadChimIndex == 3:
            nextBaadChimIndex = 1
        elif currentBaadChimIndex == 12:
            nextBaadChimIndex = 8
        else:
            nextBaadChimIndex = 17
    elif inputJaEumIndex == 7:
        newJaEum = 'ㅃ'
        if currentBaadChimIndex == 14:
            nextBaadChimIndex = 8
        else:
            nextBaadChimIndex = 0
    elif inputJaEumIndex == 11:
        newJaEum = 'ㅇ'
        if currentBaadChimIndex == 6:
            nextBaadChimIndex = 4
        else:
            nextBaadChimIndex = 8
    else:
        if currentBaadChimIndex == 5:
            nextBaadChimIndex = 4
            newJaEum = 'ㅊ'
        else:
            nextBaadChimIndex = 0
            newJaEum = 'ㅉ'

    nextWord = unichr(BASE+CHOSUNG*currentJaEumIndex+JUNGSUNG*currentMoEumIndex+nextBaadChimIndex).encode('utf-8')
    rest += nextWord
    rest += newJaEum
    return rest

def JaEumtoBaadChim(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-6]
    lastWord = currentString[length-6 : length-3]
    jaeum = currentString[length-3:]

    lastOrd = ord(lastWord.decode('utf-8'))
    lastJaEumIndex = (lastOrd - BASE) / CHOSUNG
    lastMoEumIndex = ((lastOrd - BASE) % CHOSUNG) / JUNGSUNG
    lastBaadChimIndex = ((lastOrd - BASE) % JUNGSUNG)

    currentJaEumIndex = CHOSUNG_LIST.index(jaeum)
    inputJaEumIndex = CHOSUNG_LIST.index(vocamap[inputChar])

    if lastBaadChimIndex == 0:
        if inputJaEumIndex == 3:
            nextBaadChimIndex = 7
        elif inputJaEumIndex == 7:
            nextBaadChimIndex = 17
        else:
            nextBaadChimIndex = 22

    elif lastBaadChimIndex == 17:
        nextBaadChimIndex = 18

    elif lastBaadChimIndex == 1:
        nextBaadChimIndex = 3

    elif lastBaadChimIndex == 4:
        if currentJaEumIndex == 11:
            nextBaadChimIndex = 6
        else:
            nextBaadChimIndex = 5

    else:
        if currentJaEumIndex == 1:
            nextBaadChimIndex = 9
        elif currentJaEumIndex == 3:
            nextBaadChimIndex = 13
        elif currentJaEumIndex == 10:
            nextBaadChimIndex = 10
        elif currentJaEumIndex == 8:
            nextBaadChimIndex = 11
        else:
            nextBaadChimIndex = 15


    nextWord = unichr(BASE+CHOSUNG*lastJaEumIndex+JUNGSUNG*lastMoEumIndex+nextBaadChimIndex).encode('utf-8')
    rest += nextWord
    return rest

def MoEumtoBaadChim(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]

    currentOrd = ord(currentWord.decode('utf-8'))
    jongsungIndex = JONGSUNG_LIST.index(vocamap[inputChar])

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
    inputBaadChimIndex = JONGSUNG_LIST.index(vocamap[inputChar])


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
        if inputBaadChimIndex == 1:
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

def BaadChimtoMoEum(currentString, inputChar):
    length = len(currentString)

    rest = currentString[:length-3]
    currentWord = currentString[length-3:]

    currentOrd = ord(currentWord.decode('utf-8'))
    currentBaadChimIndex = (currentOrd - BASE) % JUNGSUNG
    if JONGSUNG_LIST[currentBaadChimIndex] in CHOSUNG_LIST:
        currentOrd -= currentBaadChimIndex
        currentWord = unichr(currentOrd).encode('utf-8')
        rest += currentWord

        newString = rest + JONGSUNG_LIST[currentBaadChimIndex]
        newString = JaEumtoMoEum(newString, inputChar)
        return newString

    else:
        if currentBaadChimIndex == 3:
            currentOrd -= currentBaadChimIndex
            currentOrd += 1
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[19]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 5:
            currentOrd -= currentBaadChimIndex
            currentOrd += 4
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[22]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 6:
            currentOrd -= currentBaadChimIndex
            currentOrd += 4
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[27]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 9:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[1]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 10:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[16]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 11:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[17]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 12:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[19]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 13:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[25]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 14:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[26]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 15:
            currentOrd -= currentBaadChimIndex
            currentOrd += 8
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[27]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

        elif currentBaadChimIndex == 18:
            currentOrd -= currentBaadChimIndex
            currentOrd += 17
            currentWord = unichr(currentOrd).encode('utf-8')
            rest += currentWord

            newString = rest + JONGSUNG_LIST[19]
            newString = JaEumtoMoEum(newString, inputChar)
            return newString

def Space(currentString, inputChar):
    return currentString

def BackSpace(currentString, inputChar):
    length = len(currentString)
    if length == 0:
        return currentString
    return currentString[:length-3]

#############################################################################################################

################################### 한글 모아쓰기 오토마타 ##################################################

def KOREAN_Mealy_Simulator (states, vocabulary, stateTransitionFunction, outputFunction, initialState, finalStates):
    # We're gonna receive state transition function as dictionary : {(current state, input): next state, ...}
    print "핸드폰 자판을 입력하세요."
    inputString = raw_input()
    if inputString=='':
        inputString='8#62551119325544_44#200'
    inputLength = len(inputString)
    currentState = initialState
    currentString = ''

    for i in range (inputLength):
        inputChar = inputString[i]
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

        if isDeadState or currentState=='1':
            print "Error occurred : This input is not accepted by given grammar."
            return
        # If isDeadState is still true : there are two possibilities
        # 1. current state is a dead state
        # 2. current state is not a dead state, but there's no state transition function for current state that accepts current character (inputString[i])
        # Either way, Mealy machine should not accept the string.

    if currentState not in finalStates:
        print "Error occurred : This input is not accepted by given grammar."
        return

    return

#############################################################################################################

KOREAN_Mealy_Simulator (states, vocabulary, stateTransitionFunction, outputFunction, '0', finalStates)