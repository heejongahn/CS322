__author__ = 'Nobell_User'
# -*- coding: utf-8 -*-

def Mealy_Simulator (states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState):
    # We're gonna receive state transition function as dictionary : {(current state, input): next state, ...}
    print "Enter the string that you want to check"
    inputString = raw_input()
    inputLength = len(inputString)
    f = file("output.txt", "w")
    # When function is called, we accept the string to test using standard input of python.

    currentState = initialState

    for i in range (inputLength):
    # We're gonna check the legitimacy of the string, character by character.
        if inputString[i] not in vocabulary:
            print "Error occurred : This input is not accepted by given grammar."
            return
        # If current character is not an element of vocabulary, Mealy Machine should not accept the string.

        isDeadState = True
        # Assume that current state is a dead state
        if ((currentState, inputString[i]) in stateTransitionFunction):
            currentOutput = outputFunction[(currentState, inputString[i])] + "\n"
            currentState = stateTransitionFunction[(currentState, inputString[i])]
            f.write(currentOutput)
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

    f.close()
    f = open("output.txt", "r")
    lines = f.readlines()
    for line in lines:
        exec line

    return


def Demo_Mealy():
    # This is just a demo of mealy machine simulator. In this demo, all inputs are using stdin, but in real project, we might use different methods.
    print "Input states of the DFA, separated by @('@')"
    raw_states=raw_input();
    states=raw_states.split("@")

    print "Input vocabulary of the DFA, separated by @('@')"
    raw_vocabulary=raw_input();
    vocabulary=raw_vocabulary.split("@")

    print "Input output characters of the DFA, separated by @('@')"
    raw_outputCharacters=raw_input();
    outputCharacters=raw_outputCharacters.split("@")

    print "Input state transition function of the DFA as follow in order: currentState input nextState separated by @ ('@')"
    raw_stateTransitionFunction=raw_input();
    list_stateTransitionFunction=raw_stateTransitionFunction.split("@")
    stateTransitionFunction={}
    for i in range((len(list_stateTransitionFunction)+1)/3):
        key = (list_stateTransitionFunction[3*i], list_stateTransitionFunction[3*i+1])
        value = list_stateTransitionFunction[3*i+2]
        stateTransitionFunction[key] = value

    print "Input output function of the DFA as follow in order: currentState, input, output separated by @ ('@')"
    raw_outputFunction=raw_input();
    list_outputFunction=raw_outputFunction.split("@")
    outputFunction={}
    for i in range((len(list_outputFunction)+1)/3):
        key = (list_outputFunction[3*i], list_outputFunction[3*i+1])
        value = list_outputFunction[3*i+2]
        outputFunction[key] = value

    print "Input initial state of the DFA"
    initialState = raw_input();



    return (states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState)

(states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState) = Demo_Mealy()
Mealy_Simulator(states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState)