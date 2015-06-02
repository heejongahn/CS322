CS322 보조프로젝트 2-1
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
automata2-1.py 를 run하면 실행됩니다.

-------------------------------------------------------------------------

<입/출력 방법>

e-Move를 허용하는 NFA를 입력받습니다.

입력은 standard input을 이용하고, spacebar를 separator로 이용합니다.

첫 번째 줄은 state를, 두 번째 줄은 vocabulary를 각각 입력받습니다.

세 번째 줄부터 'end'를 입력 할 때까지 stateTransitionFunction을 입력받습니다.
이 때 지금까지의 프로젝트에서 사용했던 것처럼 currentstate input nextstate 순으로 입력받습니다.
이때 'eps'를 입실론을 나타내는 심볼로 사용합니다. (ex: q0에서 q1으로의 e-move가 있는 경우 q0 eps q1)

그 이후 두 줄에서 각각 initial state, final states를 입력받습니다.

아래는 입력 예시입니다.(from http://web.cecs.pdx.edu/~harry/compilers/slides/LexicalPart3.pdf)

q0 q1 q2 q3 q4 q5 q6 q7 q8 q9 q10
a b
q0 eps q1
q0 eps q7
q1 eps q2
q1 eps q4
q2 a q3
q3 eps q6
q4 b q5
q5 eps q6
q6 eps q1
q6 eps q7
q7 a q8
q8 b q9
q9 b q10
end
q0
q10

이 때 e-NFA -> DFA로 바뀔 때, DFA -> mDFA로 바뀔 때 각각 (states, vocabulary, stateTransitionFunction, initialState, finalStates) 를 터미널상에 출력합니다.

-------------------------------------------------------------------------

<코드에 대한 간단한 설명>

automata2-1.py파일은

인코딩
-------
내부 함수 정의
-------
e-NFA -> DFA
-------
DFA -> mDFA
-------
Demo_eNFA (입력 함수) 정의
-------
DFA_Simulator
-------
실행 및 출력


형태로 구성되어 있습니다.



1. utf-8 인코딩을 사용하였습니다.
제가 사용한 IDE와 제 컴퓨터의 Cygwin 콘솔 모두 기본적으로 한글 입력을 'utf-8'로 받는 것을 확인했습니다.
빌트인 함수 unichr(x) (유니코드 값 x에 해당하는 캐릭터 리턴), ord(chr) (캐릭터 chr의 유니코드값 리턴), encode/decode('utf-8) (유니코드를 utf-8 규칙으로 인코딩/디코딩) 들을 사용했습니다.




2. 내부 함수들을 정의한 구간입니다.

(A) eClosureOfState(state, stateTransitionFunction):
stateTransitionFunction이 주어진 상태에서 argument로 들어온 state의 eClosure(set 자료구조 이용) 을 반환합니다.
eNFA_to_DFA에서 호출되며, BFS를 이용하여 구현했습니다.

(B) nextState(stateTransitionFunction, currentState, input):
stateTransitionFunction이 주어진 상태에서 currentState에 input이 들어왔을 때 다음 state를 반환합니다.
DFA_to_mDFA 내부에서 Table Filling Algorithm 에 사용되는 함수로, 편의를 위해 따로 작성하였습니다.




3. eNFA_to_DFA(states, vocabulary, stateTransitionFunction, initialState, finalStates):
eNFA를 DFA로 변환하는 함수입니다.
교과서나 TP에 나와있는 전형적인 방식을 따라 작성하였습니다.
내부에서 eClosureOfState(state, stateTransitionFunction) 를 수차례 호출합니다.




4. DFA_to_mDFA(states, vocabulary, stateTransitionFunction, initialState, finalStates):
DFA를 mDFA로 변환하는 함수입니다.
Table Filling Algorithm 을 사용하여 각각의 state끼리가 distinguishable한지를 일단 판별합니다.
그 후, indistinguishable한 state간에 모두 e-Move를 만들어 준 뒤, 그렇게 생긴 e-NFA를 다시 eNFA_to_DFA 함수의 인자로서 사용합니다.
해당 함수의 실행으로부터 리턴된 DFA가 처음 주어진 e-NFA의 minimal DFA가 됩니다.




5. Demo_eNFA (입력 함수) 의 정의입니다.
입/출력 방식에서 설명한대로 e-NFA를 입력받습니다.
기본적으로 보조프로젝트 1-1 에서 만든 것을 재사용했지만 stateTransitionFunction이 길어진 관계로 한 줄에 다 받는 대신 end를 입력할 때까지 받도록 변경했습니다.
또한 코드 작성의 편의를 위해 stateTransitionFunction의 자료구조를 dictionary에서 nested list로 변경했습니다.




6. DFA_Simulator (states, vocabulary, stateTransitionFunction, initialState, finalStates)
보조프로젝트 1-1 에서 사용했던 DFA 시뮬레이터 입니다.
기본적으로는 실행되지 않는 상태입니다. 
코드의 마지막 줄 (227 line)의 주석표시를 제거하면 이 함수를 이용해 m-DFA로의 변환을 마친 뒤 어떤 문자열이 해당 DFA에서 받아들여지는지를 체크할 수 있습니다.



7. 위에서 정의한 함수들의 실행 및 입/출력 방식에서 설명한 출력이 이루어지는 구간입니다.