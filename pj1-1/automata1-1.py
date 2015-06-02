__author__ = 'Nobell_User'
# -*- coding: utf-8 -*-

def DFA_Simulator (states, vocabulary, stateTransitionFunction, initialState, finalStates):
    # We're gonna receive state transition function as dictionary : {(current state, input): next state, ...}
    print "Enter the string that you want to check"
    inputString = raw_input()
    inputLength = len(inputString)
    # When function is called, we accept the string to test using standard input of python.

    currentState = initialState
    for i in range (inputLength):
    # We're gonna check the legitimacy of the string, character by character.
        if inputString[i] not in vocabulary:
            print "아니요"
            return
        # If current character is not an element of vocabulary, DFA should not accept the string.

        isDeadState = True
        # Assume that current state is a dead state
        if ((currentState, inputString[i]) in stateTransitionFunction):
            currentState = stateTransitionFunction[(currentState, inputString[i])]
            isDeadState = False
        # If there's (currentState, inputString[i]) defined in state transition function, then the state is not a dead state.
        # Also, set current state as next state. (We assume that the step move is made in this point.)

        if isDeadState:
            print "아니요"
            return
        # If isDeadState is still true : there are two possibilities
        # 1. current state is a dead state
        # 2. current state is not a dead state, but there's no state transition function for current state that accepts current character (inputString[i])
        # Either way, DFA should not accept the string.

    if (currentState in finalStates):
        print "예"
        return
    # After the simulator go through the whole string, if current state is in final states, DFA should accept the string.

    print "아니요"
    return
    # Elsewhere (if current state is not in final states), DFA should not accept the string.

def Demo_DFA():
    # This is just a demo of dfa simulator. In this demo, all inputs are using stdin, but in real project, we might use different methods.
    print "Input states of the DFA, separated by space( )"
    raw_states=raw_input();
    states=raw_states.split(" ")

    print "Input vocabulary of the DFA, separated by space( )"
    raw_vocabulary=raw_input();
    vocabulary=raw_vocabulary.split(" ")

    print "Input state transition function of the DFA as follow in order: currentState input nextState separated by space( )"
    raw_stateTransitionFunction=raw_input();
    list_stateTransitionFunction=raw_stateTransitionFunction.split(" ")
    stateTransitionFunction={}
    for i in range((len(list_stateTransitionFunction)+1)/3):
        key = (list_stateTransitionFunction[3*i], list_stateTransitionFunction[3*i+1])
        value = list_stateTransitionFunction[3*i+2]
        stateTransitionFunction[key] = value

    print "Input initial state of the DFA"
    initialState = raw_input();

    print "Input final states of the DFA, separated by space( )"
    raw_finalStates=raw_input();
    finalStates=raw_finalStates.split(" ")

    return (states, vocabulary, stateTransitionFunction, initialState, finalStates)

(states, vocabulary, stateTransitionFunction, initialState, finalStates) = Demo_DFA()
DFA_Simulator(states, vocabulary, stateTransitionFunction, initialState, finalStates)