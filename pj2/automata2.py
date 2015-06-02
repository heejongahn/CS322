__author__ = 'Nobell_User'
# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc

# List of token names.
tokens = (
   'SYMBOL',
   'UNION',
   'DAGGER',
   'ASTERISK',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_SYMBOL = r'[a-zA-Z0-9_#$]'
t_UNION  = r'\|'
t_DAGGER = r'\+'
t_ASTERISK  = r'\*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ignore  = '\t'


# Error handling action
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Parsing tool (Yacc definition)

precedence = (
    ('left','UNION'),
    ('left','DAGGER', 'ASTERISK'),
    )

def p_statement_expr(t) :
    'statement : expression'
    t[0] = t[1]

def p_statement_none(t) :
    'statement : '
    t[0] = None

def p_expression_ampersand(t) :
    'expression : expression expression'
    t[0] = ('&', t[1], t[2])

def p_expression_union(t) :
    'expression : expression UNION expression'
    t[0] = ('|', t[1], t[3])

def p_expression_dagger(t) :
    'expression : expression DAGGER'
    t[0] = ('+', t[1])

def p_expression_asterisk(t) :
    'expression : expression ASTERISK'
    t[0] = ('*', t[1])

def p_expression_group(t) :
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_symbol(t) :
    'expression : SYMBOL'
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


# Definition of Abstract Syntax Tree Class

class AST:
    def __init__(self, value):
        self.rightChild = None
        self.leftChild = None
        self.parent = None
        self.value = value

# Definition of eNFA Class

class eNFA:
    def __init__(self):
        self.states = None
        self.vocabulary = None
        self.stateTransitionFunction = None
        self.initialState = None
        self.finalStates = None

    def getTuples(self):
        return (self.states, self.vocabulary, self.stateTransitionFunction, self.initialState, self.finalStates)

    def setTuples(self, eNFA_states, eNFA_vocabulary, eNFA_stateTransitionFunction, eNFA_initialState, eNFA_finalStates):
        self.states = eNFA_states
        self.vocabulary = eNFA_vocabulary
        self.stateTransitionFunction = eNFA_stateTransitionFunction
        self.initialState = eNFA_initialState
        self.finalStates = eNFA_finalStates

# Definition of DFA Class

class DFA:
    def __init__(self):
        self.states = None
        self.vocabulary = None
        self.stateTransitionFunction = None
        self.initialState = None
        self.finalStates = None

    def getTuples(self):
        return (self.states, self.vocabulary, self.stateTransitionFunction, self.initialState, self.finalStates)

    def setTuples(self, DFA_states, DFA_vocabulary, DFA_stateTransitionFunction, DFA_initialState, DFA_finalStates):
        self.states = DFA_states
        self.vocabulary = DFA_vocabulary
        self.stateTransitionFunction = DFA_stateTransitionFunction
        self.initialState = DFA_initialState
        self.finalStates = DFA_finalStates


# Helper functions

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

def classify(list, new):
    newItem = new
    removeList = []
    for item in list:
        if (newItem & item) != set():
            newItem = (newItem|item)
            removeList.append(item)

    for r in removeList:
        list.remove(r)

    list.append(newItem)

def nextState(stateTransitionFunction, currentState, input):
    for e in stateTransitionFunction:
        if e[0]==(currentState, input):
            return e[1]

def eNFAStateRenaming(RE_eNFA, n):
    (states, vocabulary, stateTransitionFunction, initialState, finalStates) = RE_eNFA.getTuples()

    newStates=[]
    for state in states:
        newStates.append(state+n)

    newStateTransitionFunction = []
    for delta in stateTransitionFunction:
        curr = delta[0][0]
        input = delta[0][1]
        next = delta[1]

        newStateTransitionFunction.append([(curr+n, input), next+n])

    newInitialState = initialState + n
    newFinalStates = []
    for final in finalStates:
        newFinalStates.append(final+n)

    resulteNFA=eNFA()
    resulteNFA.setTuples(newStates, vocabulary, newStateTransitionFunction, newInitialState, newFinalStates)

    return resulteNFA

def unionOfTwoLists(list1, list2):
    temp1 = [var for var in list1]
    temp2 = [var for var in list2 if var not in temp1]

    resultList = temp1 + temp2
    resultList.sort()

    return resultList

def eNFA_UNION(left_eNFA, right_eNFA):
    n = len(left_eNFA.states)
    m = len(right_eNFA.states)

    left_eNFA = eNFAStateRenaming(left_eNFA, 1)
    right_eNFA = eNFAStateRenaming(right_eNFA, 1+n)

    (left_states, left_vocabulary, left_stateTransitionFunction, left_initialState, left_finalStates) = left_eNFA.getTuples()
    (right_states, right_vocabulary, right_stateTransitionFunction, right_initialState, right_finalStates) = right_eNFA.getTuples()

    left_states.extend(right_states)
    newStates = left_states
    newStates.append(0)
    newStates.append(1+n+m)

    newVocabulary = unionOfTwoLists(left_vocabulary, right_vocabulary)

    left_stateTransitionFunction.extend(right_stateTransitionFunction)
    newStateTransitionFunction = left_stateTransitionFunction

    newStateTransitionFunction.append([(0, 'eps'), left_initialState])
    newStateTransitionFunction.append([(0, 'eps'), right_initialState])

    for final in left_finalStates:
        newStateTransitionFunction.append([(final, 'eps'), 1+n+m])

    for final in right_finalStates:
        newStateTransitionFunction.append([(final, 'eps'), 1+n+m])


    newInitialState = 0
    newFinalStates=[1+n+m]

    resulteNFA = eNFA()
    resulteNFA.setTuples(newStates, newVocabulary, newStateTransitionFunction, newInitialState, newFinalStates)

    return resulteNFA

def eNFA_CONCATENATION(left_eNFA, right_eNFA):
    (left_states, left_vocabulary, left_stateTransitionFunction, left_initialState, left_finalStates) = left_eNFA.getTuples()

    n = len(left_eNFA.states)
    right_eNFA = eNFAStateRenaming(right_eNFA, n)

    (right_states, right_vocabulary, right_stateTransitionFunction, right_initialState, right_finalStates) = right_eNFA.getTuples()

    left_states.extend(right_states)
    newStates = left_states
    newVocabulary = unionOfTwoLists(left_vocabulary, right_vocabulary)
    left_stateTransitionFunction.extend(right_stateTransitionFunction)
    newStateTransitionFunction = left_stateTransitionFunction

    for final in left_finalStates:
        newStateTransitionFunction.append([(final, 'eps'), right_initialState])

    newInitialState = left_initialState
    newFinalStates = right_finalStates

    resulteNFA = eNFA()
    resulteNFA.setTuples(newStates, newVocabulary, newStateTransitionFunction, newInitialState, newFinalStates)

    return resulteNFA

def eNFA_ASTERISK(RE_eNFA):
    RE_eNFA = eNFAStateRenaming(RE_eNFA, 1)

    (states, vocabulary, stateTransitionFunction, initialState, finalStates) = RE_eNFA.getTuples()

    n = len(states)

    states.append(0)
    states.append(n+1)

    stateTransitionFunction.append([(0, 'eps'), n+1])
    stateTransitionFunction.append([(0, 'eps'), initialState])

    for final in finalStates:
        stateTransitionFunction.append([(final, 'eps'), initialState])
        stateTransitionFunction.append([(final, 'eps'), n+1])


    resulteNFA = eNFA()
    resulteNFA.setTuples(states, vocabulary, stateTransitionFunction, 0, [n+1])


    return resulteNFA

def eNFA_DAGGER(RE_eNFA):
    RE_eNFA = eNFAStateRenaming(RE_eNFA, 1)

    (states, vocabulary, stateTransitionFunction, initialState, finalStates) = RE_eNFA.getTuples()

    n = len(states)

    states.append(0)
    states.append(n+1)

    stateTransitionFunction.append([(0, 'eps'), initialState])

    for final in finalStates:
        stateTransitionFunction.append([(final, 'eps'), initialState])
        stateTransitionFunction.append([(final, 'eps'), n+1])

    resulteNFA = eNFA()


    resulteNFA.setTuples(states, vocabulary, stateTransitionFunction, 0, [n+1])

    return resulteNFA

def Symbol_to_eNFA(symbol):
    resulteNFA = eNFA()
    resulteNFA.setTuples([0,1], [symbol], [[(0, symbol), 1]], 0, [1])
    return resulteNFA


# Construct tokenizer & parser using Lex & Yacc

lex.lex()
yacc.yacc()


# Step 1 : Receive regular expression as standard input and parse it using Lex & Yacc

s = raw_input('Type in the regular expression > ')   # Use raw_input on Python 2
parsed = yacc.parse(s)


# Step 2 : Construct Absolute Syntax Tree using parsed result from Step 1

def constructAST(parsed):
    if len(parsed) == 1:
        root = AST(parsed)

    else:
        root = AST(parsed[0])

        leftChild = constructAST(parsed[1])
        leftChild.parent = root
        root.leftChild = leftChild
        if len(parsed) == 3 :
            rightChild = constructAST(parsed[2])
            rightChild.parent = root
            root.rightChild = rightChild


    return root


# Step 3: Construct e-NFA from Abstract Syntax Tree

def AST_to_eNFA(tree):
    if tree.value == '|':
        left_eNFA = AST_to_eNFA(tree.leftChild)
        right_eNFA = AST_to_eNFA(tree.rightChild)
        return eNFA_UNION(left_eNFA, right_eNFA)
    elif tree.value == '&':
        left_eNFA = AST_to_eNFA(tree.leftChild)
        right_eNFA = AST_to_eNFA(tree.rightChild)
        return eNFA_CONCATENATION(left_eNFA, right_eNFA)
    elif tree.value == '*':
        child = AST_to_eNFA(tree.leftChild)
        return eNFA_ASTERISK(child)
    elif tree.value == '+':
        child = AST_to_eNFA(tree.leftChild)
        return eNFA_DAGGER(child)
    else :
        return Symbol_to_eNFA(tree.value)


# Step 4 : eNFA to DFA

def eNFA_to_DFA(RE_eNFA):
    eClosures=[]
    # a list of eClosures

    (states, vocabulary, stateTransitionFunction, initialState, finalStates) = RE_eNFA.getTuples()


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

    resultDFA = DFA()

    newStates.sort()
    newStateTransitionFunction.sort()
    newFinalStates.sort()


    resultDFA.setTuples(newStates, vocabulary, newStateTransitionFunction, newInitialState, newFinalStates)

    return resultDFA

# Step 5 : DFA to mDFA

def DFA_to_mDFA(RE_DFA):
    (states, vocabulary, stateTransitionFunction, initialState, finalStates) = RE_DFA.getTuples()


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


    newStates = []

    for i in range(0, length-1):
        for j in range(i+1, length):
            if table[(i,j)] == 'null':
                classify(newStates, {i,j})
            else:
                classify(newStates, {i})
                classify(newStates, {j})


    newStateTransitionFunction = []
    mappingHash = {}

    for newState in newStates:
        ind = newStates.index(newState)
        for e in newState:
            mappingHash[e] = ind


    for delta in stateTransitionFunction:
        newDelta = [(mappingHash[delta[0][0]], delta[0][1]), mappingHash[delta[1]]]
        if newDelta not in newStateTransitionFunction:
            newStateTransitionFunction.append(newDelta)

    newStates = range(len(newStates))

    newFinalStates = []

    for final in finalStates:
        if mappingHash[final] not in newFinalStates:
            newFinalStates.append(mappingHash[final])

    newStateTransitionFunction.sort()
    newFinalStates.sort()

    resultDFA = DFA()
    resultDFA.setTuples(newStates, vocabulary, newStateTransitionFunction, mappingHash[initialState], newFinalStates)

    return resultDFA

def DFA_Simulator (DFA):
    states = DFA.states
    vocabulary = DFA.vocabulary
    stateTransitionFunction = DFA.stateTransitionFunction
    initialState = DFA.initialState
    finalStates = DFA.finalStates


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

RE_AST = constructAST(parsed)

RE_eNFA = AST_to_eNFA(RE_AST)
print '##########################################eNFA################################################'
print "States :",
print RE_eNFA.states
print "Vocabulary :",
print RE_eNFA.vocabulary
print "State Transition Functions :"
for e in RE_eNFA.stateTransitionFunction:
    print e[0],
    print "=>",
    print e[1]
print "Initial State :",
print RE_eNFA.initialState
print "Final State :",
print RE_eNFA.finalStates


RE_DFA = eNFA_to_DFA(RE_eNFA)
print '##########################################DFA################################################'
print "States :",
print RE_DFA.states
print "Vocabulary :",
print RE_DFA.vocabulary
print "State Transition Functions :"
for e in RE_DFA.stateTransitionFunction:
    print e[0],
    print "=>",
    print e[1]
print "Initial State :",
print RE_DFA.initialState
print "Final State :",
print RE_DFA.finalStates

print " "
print " "


print '##########################################mDFA################################################'
RE_mDFA = DFA_to_mDFA(RE_DFA)
print "States : ",
print RE_mDFA.states
print "Vocabulary : ",
print RE_mDFA.vocabulary
print "State Transition Functions :"
for e in RE_mDFA.stateTransitionFunction:
    if e[1] != '1' and e[1] != 1:
        print e[0][0],
        print e[0][1],
        print e[1]



print "Initial State : ",
print RE_mDFA.initialState
print "Final State : ",
print RE_mDFA.finalStates

# DFA_Simulator (states, vocabulary, stateTransitionFunction, initialState, finalStates)
