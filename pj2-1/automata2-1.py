__author__ = 'Nobell_User'
# -*- coding: utf-8 -*-

def eClosureOfState(state, stateTransitionFunction):
    eClosure=set()
    eClosure.add(state)

    queue=[state]
    while len(queue)!=0 :
        currentState=queue.pop()
        for e in stateTransitionFunction:
            if e[0] == (currentState, 'eps') and e[1] not in eClosure:
                eClosure.add(e[1])
                queue.append(e[1])
    return eClosure

def nextState(stateTransitionFunction, currentState, input):
    for e in stateTransitionFunction:
        if e[0]==(currentState, input):
            return e[1]


def eNFA_to_DFA(states, vocabulary, stateTransitionFunction, initialState, finalStates):
    eClosures=[]
    # a list of eClosures

    init = eClosureOfState(initialState, stateTransitionFunction)
    eClosures.append(init)
    queue = [init]
    # initial state of DFA : e-closure of initial state of NFA

    newStateTransitionFunction = []

    while len(queue)!=0 :
        currentClosure = queue.pop()
        # Check the transition from the unconsidered state (subset)


        for input in vocabulary:
            newTemp = set()
            newClosure = set()
            for state in currentClosure:
                for e in stateTransitionFunction:
                    if e[0] == (state, input):
                        newTemp.add(e[1])
                # newTemp is a set which contains every state that can be reached from currentClosure by input
            for e in newTemp:
                newClosure = newClosure.union(eClosureOfState(e, stateTransitionFunction))
            # newClosure is union of e-closures in newTemp

            if newClosure not in eClosures:
                eClosures.append(newClosure)
                queue.append(newClosure)
            # if newClosure is newly discovered, add it to the queue and eClosures

            f = eClosures.index(currentClosure)
            t = eClosures.index(newClosure)

            if [(f, input), t] not in newStateTransitionFunction:
                newStateTransitionFunction.append([(f, input), t])

    newStates = range(0, len(eClosures))
    newInitialState = 0
    newFinalStates = []

    for newState in newStates:
        for final in finalStates:
            if final in eClosures[newState]:
                newFinalStates.append(newState)
                break

    return (newStates, vocabulary, newStateTransitionFunction, newInitialState, newFinalStates)


def DFA_to_mDFA(states, vocabulary, stateTransitionFunction, initialState, finalStates):
    table={}
    length = len(states)
    for i in range(0, length-1):
        for j in range(i+1, length):
            if i in finalStates and j not in finalStates:
                table[(i,j)] = 'd'
            elif j in finalStates and i not in finalStates:
                table[(i,j)] = 'd'
            else:
                table[(i,j)] = 'null'

    # Table Filling Algorithm Step 1 : Final States and Non-final States are distinguishable

    while True:
        setChange = False
        for i in range(0, length-1):
            for j in range(i+1, length):
                if table[(i,j)] == 'null':
                    for input in vocabulary:
                        if nextState(stateTransitionFunction, i, input) != nextState(stateTransitionFunction, j, input):
                            table[(i,j)] = 'd'
                            setChange = True
        if not setChange:
            break

    # Table Filling Algorithm Step 2 : Iteration


    for i in range(0, length-1):
        for j in range(i+1, length):
            if table[(i,j)]=='null':
                stateTransitionFunction.append([(i, 'eps'), j])
                stateTransitionFunction.append([(j, 'eps'), i])
    # Add e-move between all pairs of indistinguishable states


    return eNFA_to_DFA(states, vocabulary, stateTransitionFunction, initialState, finalStates)


def Demo_eNFA():
    # This is just a demo of e-NFA simulator. In this demo, all inputs are using stdin, but in real project, we might use different methods.

    print "Input states of the eNFA, separated by space( )"
    raw_states=raw_input();
    states=raw_states.split(" ")

    print "Input vocabulary of the eNFA, separated by space( )"
    raw_vocabulary=raw_input();
    vocabulary=raw_vocabulary.split(" ")

    print "Input state transition function of the eNFA as follow in order: currentState input nextState separated by space( )"
    print "If you're done with this, type 'end'"
    stateTransitionFunction=[]
    while (1):
        raw_stateTransitionFunction=raw_input();
        if raw_stateTransitionFunction == 'end':
            break

        list_stateTransitionFunction=raw_stateTransitionFunction.split(" ")
        for i in range((len(list_stateTransitionFunction)+1)/3):
            key = (list_stateTransitionFunction[3*i], list_stateTransitionFunction[3*i+1])
            value = list_stateTransitionFunction[3*i+2]
            stateTransitionFunction.append([key, value])

    print "Input initial state of the DFA"
    initialState = raw_input();

    print "Input final states of the DFA, separated by space( )"
    raw_finalStates=raw_input();
    finalStates=raw_finalStates.split(" ")

    return (states, vocabulary, stateTransitionFunction, initialState, finalStates)

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

(states, vocabulary, stateTransitionFunction, initialState, finalStates) = Demo_eNFA()

(states, vocabulary, stateTransitionFunction, initialState, finalStates) = eNFA_to_DFA(states, vocabulary, stateTransitionFunction, initialState, finalStates)
print '##########################################DFA################################################'
print "States :",
print states
print "Vocabulary :",
print vocabulary
print "State Transition Functions :"
for e in stateTransitionFunction:
    print e[0],
    print "=>",
    print e[1]
print "Initial State :",
print initialState
print "Final State :",
print finalStates

print " "
print " "


print '##########################################mDFA################################################'
(states, vocabulary, stateTransitionFunction, initialState, finalStates) = DFA_to_mDFA(states, vocabulary, stateTransitionFunction, initialState, finalStates)
print "States : ",
print states
print "Vocabulary : ",
print vocabulary
print "State Transition Functions :"
for e in stateTransitionFunction:
    print e[0],
    print "=>",
    print e[1]
print "Initial State : ",
print initialState
print "Final State : ",
print finalStates

# DFA_Simulator (states, vocabulary, stateTransitionFunction, initialState, finalStates)