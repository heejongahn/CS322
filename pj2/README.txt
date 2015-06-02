CS322 본프로젝트 2
20130380 안희종

-------------------------------------------------------------------------

<프로그래밍 환경>
Windows 8.1 64bit
IDE : JetBrain PyCharm 3.4.1

-------------------------------------------------------------------------

<사용 언어>
Python 2.7.6 Version

-------------------------------------------------------------------------

<실행 방법>

파이썬 2.7.6 버전으로
automata2.py 를 run하면 실행됩니다.

-------------------------------------------------------------------------

<입/출력 방법>

regex를 입력받습니다. 이 때 Symbol은 알파벳 대소문자로 제한합니다.

입력 예시 : (a+b)*

이 때 AST->e-NFA로 바뀔 때, e-NFA -> DFA로 바뀔 때, DFA -> mDFA로 바뀔 때 각각 (states, vocabulary, stateTransitionFunction, initialState, finalStates) 를 터미널상에 출력합니다.

-------------------------------------------------------------------------

<코드에 대한 간단한 설명>

automata2.py파일은

lex & yacc 을 위한 정의 부분
-------
클래스 정의
-------
Helper Function 정의
-------
Regex parsing
-------
AST Construction
-------
AST -> eNFA
-------
e-NFA -> DFA
-------
DFA -> mDFA
-------
DFA_Simulator
-------
실행 및 출력


형태로 구성되어 있습니다.



1. lex & yacc 을 위한 정의 부분입니다.
PLY Documentation 및 Example에 있는 코드를 대부분 참조하여 작성했습니다.
*(asterisk), +(union), &(ampersand), () (parenthesis)들을 operator로, 알파벳 대소문자를 symbol로 간주하였습니다.


2. 클래스들을 정의한 부분입니다.
편의를 위해 Abstract Syntax Tree, eNFA, DFA를 정의하였습니다.
모두 클래스 변수만 있고, 클래스 메소드는 정의하지 않았습니다.


3. Helper Function들을 정의한 구간입니다.

(A) eClosureOfState(state, stateTransitionFunction):
stateTransitionFunction이 주어진 상태에서 argument로 들어온 state의 eClosure(set 자료구조 이용) 을 반환합니다.
eNFA_to_DFA에서 호출되며, BFS를 이용하여 구현했습니다.

(B) nextState(stateTransitionFunction, currentState, input):
stateTransitionFunction이 주어진 상태에서 currentState에 input이 들어왔을 때 다음 state를 반환합니다.
DFA_to_mDFA 내부에서 Table Filling Algorithm 에 사용되는 함수로, 편의를 위해 따로 작성하였습니다.

(C) eNFAStateRenaming(RE_eNFA, n):
두 e-NFA를 합치는 과정에서 state name이 겹칠 경우 발생하는 문제를 예방하기 위해 RE_eNFA의 모든 state name을 n만큼 증가시키는 함수입니다.
states, stateTransitionFunction 에서의 모든 state를 n만큼 증가시킵니다.

(D) unionOfTwoList(list1, list2):
두 리스트의 합집합에 해당하는 리스트를 리턴하는 간단한 함수입니다.
두 e-NFA를 합치는 과정에서 새로운 e-NFA의 vocabulary를 계산하기 위해 사용하였습니다.

(E) eNFA_UNION(left_eNFA, right_eNFA):
AST에서 '+' (union) node를 만났을 경우 호출됩니다.
left child에 해당하는 RE와 right child에 해당하는 RE의 Union에 해당하는 RE를 나타내는 e-NFA를 리턴하는 함수입니다.

(F) eNFA_CONCATENATION(left_eNFA, right_eNFA):
AST에서 '&' (ampersand) node를 만났을 경우 호출됩니다.
left child에 해당하는 RE와 right child에 해당하는 RE의 Concatenation에 해당하는 RE를 나타내는 e-NFA를 리턴하는 함수입니다.

(G) eNFA_ASTERISK(RE_eNFA):
AST에서 '*' (asterisk) node를 만났을 경우 호출됩니다.
left child에 해당하는 RE의 Asterisk(star)에 해당하는 RE를 나타내는 e-NFA를 리턴하는 함수입니다.

(H) Symbol_to_eNFA(symbol):
AST에서 Symbol에 해당하는 leaf node를 만났을 경우 호출됩니다.
해당 Symbol만을 accepting하는 e-NFA를 생성 및 리턴합니다.


4. Regex parsing 부분입니다.
Standard input을 이용, regex를 입력 받은 뒤 위에서 작성한 lex, yacc을 이용해 yacc.parse() 함수를 호출해 parsed에 저장합니다.


5. AST Construction 부분입니다.
인자로 주어진 Parsed를 이용해 Abstract Syntax Tree를 recursive하게 생성한 뒤 반환합니다.


6. AST -> eNFA 부분입니다.
주어진 AST로부터 recursive하게 eNFA를 생성합니다.
eNFA_UNION, eNFA_CONCATENATION, eNFA_ASTERISK, Symbol_to_eNFA 네 helper function들을 이용합니다. 

7. eNFA_to_DFA(states, vocabulary, stateTransitionFunction, initialState, finalStates):
eNFA를 DFA로 변환하는 함수입니다.
교과서나 TP에 나와있는 전형적인 방식을 따라 작성하였습니다.
내부에서 eClosureOfState(state, stateTransitionFunction) 를 수차례 호출합니다.

8. DFA_to_mDFA(states, vocabulary, stateTransitionFunction, initialState, finalStates):
DFA를 mDFA로 변환하는 함수입니다.
Table Filling Algorithm 을 사용하여 각각의 state끼리가 distinguishable한지를 일단 판별합니다.
그 후, indistinguishable한 state간에 모두 e-Move를 만들어 준 뒤, 그렇게 생긴 e-NFA를 다시 eNFA_to_DFA 함수의 인자로서 사용합니다.
해당 함수의 실행으로부터 리턴된 DFA가 처음 주어진 e-NFA의 minimal DFA가 됩니다.


9. DFA_Simulator (states, vocabulary, stateTransitionFunction, initialState, finalStates)
보조프로젝트 1-1 에서 사용했던 DFA 시뮬레이터 입니다.
기본적으로는 실행되지 않는 상태입니다. 
코드의 마지막 줄 (227 line)의 주석표시를 제거하면 이 함수를 이용해 m-DFA로의 변환을 마친 뒤 어떤 문자열이 해당 DFA에서 받아들여지는지를 체크할 수 있습니다.


10. 위에서 정의한 함수들의 실행 및 입/출력 방식에서 설명한 출력이 이루어지는 구간입니다.