프로그래밍한 환경 : 랩탑, Pycharm 3.4.1을 이용해서 프로그래밍


사용한 언어 : Python 2.7.6



자세한 실행 방법 : 파일을 실행하면 
(states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState) = Demo_Mealy()
라인이 실행되어 Demo_Mealy 를 call한다.

이 때 Demo_Mealy 는 차례로 states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState 를 stdin을 이용해 입력받는다.
initialState를 제외한 다른 인풋에서 각 원소는 @("@")로 구분하여 입력한다. (@를 사용한 이유는 앞으로 작성할 파이썬 코드에서 사용할 일이 없는 간단한 단어라고 생각했기 때문)

stateTransitionFunction의 경우 (현 상태, 입력문자) -> 다음 상태 를 한 쌍이라고 생각하고 순서대로 마찬가지로 @로 구분하여 입력한다.
예를 들어, ('q0', 'a') -> 'q1'이라면 q0@a@q1 와 같은 식으로 입력한다. 

outputFunction의 경우 (현 상태, 입력문자) -> 출력 문자 를 한 쌍이라고 생각하고 순서대로 마찬가지로 @로 구분하여 입력한다.
예를 들어, ('q0', 'a') -> 'print 1'이라면 q0@a@print 1 와 같은 식으로 입력한다. 

입력된 문자를 Demo_Mealy가 파싱한 뒤 그 리턴값을 전역변수의 튜플인 (states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState)에 저장하고
그것들을 원소로 Mealy_Simulator를 call한다.




입/출력 방식 : Mealy Machine의 여섯 원소는 Mealy_Simulator 함수의 argument로 받고, 테스트하고자 하는 스트링은 해당 함수를 call하면 standard input으로 입력받는다.
Mealy_Simulator 함수는 call된 즉시 output.txt를 생성한다. 
이 함수는 한 transition이 일어날 때마다 해당 transition을 통해 나온 output character를 output.txt에 쓴다.
정상적으로 인풋 스트링을 다 받아들인 후에는 최종적으로 output.txt를 라인 별로 읽어오며 exec을 이용해 해당 함수를 실행시킨다.






코드에 관한 간단한 설명 :
argument로 주어진 states, vocabulary, outputCharacters, stateTransitionFunction, outputFunction, initialState는 각각
string의 list, character의 list, character의 list, (string, character) 꼴의 tuple -> string으로 hash되는 dictionary, (string, character) 꼴의 tuple -> string으로 hash되는 dictionary, string 의 자료구조를 갖는다. (A의 B는 A를 원소들로 갖는 B를 의미)

input string의 길이만큼의 반복문을 돌려 input string의 첫 글자부터 마지막 글자까지에 대해 각각 current state와 input symbol에 해당하는 state transition function이 있는지 체크하고
만약 있을 경우 다음 글자로 넘어가며, 해당 transition의 output string을 output.txt에 작성한다.
해당 글자가 vocabulary에 들어있지 않거나 state transition function이 정의되어 있지 않는 경우, 즉 dead state에 해당하는 경우는 에러 메시지를 출력하고 리턴한다.
이상 없이 모든 글자를 다 체크한 후 최종적으로 output.txt에 해당하는 코드를 라인별로 실행한 뒤 리턴한다.