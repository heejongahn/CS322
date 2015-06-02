CS322 본프로젝트 3
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
automata3_baadchim_first.py 를 run하면 받침우선 오토마타를,
automata3_chosung_first.py 를 run하면 초성우선 오토마타를 실행합니다.

이 때, 해당하는 stateTransitionFunction과 outputFunction txt 파일이 반드시 py파일과 같은 폴더에 있어야 정상적으로 작동합니다.


-------------------------------------------------------------------------

<입/출력 방법>

Mealy Machine의 구성 요소 중 output alphabet은 굳이 필요하지도 않고, 우리가 사용하는 output은 원래 밀리머신에서의 개념과 약간 다르므로 생략하였습니다.
한글오토마타 함수인 KOREAN_Mealy_Simulator 는 총 (states, vocabulary, stateTransitionFunction, outputFunction, initialState)로 5개의 argument를 받습니다.
이 때 고정된 값인 states, vocabulary, initialState는 각 py파일의 맨 처음에 정의되어 있습니다. 초성우선과 받침우선 모두 outputFunction을 제외하곤 동일한 인자를 받게 됩니다.

stateTransitionFunction과 outputFunction은 각각 해당하는 txt 파일에 정의되어 있습니다.
마찬가지로 py 파일의 첫 부분에서 파이썬의 빌트인 파일 입출력을 이용해 받아오며 딕셔너리에 저장합니다.
이 때 해당 stateTransitionFunction은 본프로젝트2의 RE -> mDFA를 이용하여 만들어진 결과를 정리하여 사용했습니다.

사용한 정규식은 

(((1+)|(4+)|(5+)|(7+)|(8+)|($+)|(0+))((2+)|(3+)|((3+)2)|(6+)|((6+)2)|(9+)|(9((99)*)3)|(9((99)*)32)|(9((99)*)2)|(#+)|(#((##)*)6)|(#((##)*)62)|(#((##)*)2))((1*)|((4|(44))((444)*))|(5*)|(7*)|((8|(88))((888)*))|(($|($$))(($$$)*))|(0*)|((1((111)*))((77)((777)*)))| ((5((55)*)) (($(($$$)*))|((00)+)))|(((55)+) (((1(111)*)) | (44((444)*)) | ((7|(77))((777)*))| ((8|(88))((888)*))| ((00)+))) | ((8((888)*))((77)((777)*)))))*

입니다.

입력 숫자와 한글과의 관계는 Sky 자판 기준으로

0 | 1 | 2
----------
3 | 4 | 5
----------
6 | 7 | 8
----------
$ | 0 | #

으로 생각했고, '-'가 backspace, '_'가 space의 역할을 하게 됩니다.
자세한 대응관계는 py파일의 처음에 정의된 vocamap 자료구조를 보시면 됩니다.


해당 argument들을 가지고 call된 KOREAN_Mealy_Simulator는 가장 먼저 raw_input() 함수를 이용해 사용자가 체크하고자 하는 한글 스트링을 입력받습니다.
그 후 한글 모아쓰기 오토마타의 기능을 실행하고, 중간에 문제가 생길 시에 에러메세지를 출력하고 즉시 리턴합니다.
만약, 아무 값도 입력하지 않고 엔터를 치면 기본 인풋으로 문자열 '8#62551119325544_44#200' 가 들어갑니다.

초성우선/받침우선 방식의 구현예인 chosung_example.jpg, baadchim_example.jpg를 알집파일에 같이 첨부하였습니다.

-------------------------------------------------------------------------

<코드에 대한 간단한 설명>

두 py파일은 각각

인코딩
-------
KOREAM_Mealy_Simulator에 사용할 변수들
-------
outputFunction들의 정의
-------
한글 모아쓰기 오토마타 정의
-------
한글 모아쓰기 오토마타 호출

형태로 구성되어 있습니다.

1. utf-8 인코딩을 사용하였습니다.
제가 사용한 IDE와 제 컴퓨터의 Cygwin 콘솔 모두 기본적으로 한글 입력을 'utf-8'로 받는 것을 확인했습니다.
빌트인 함수 unichr(x) (유니코드 값 x에 해당하는 캐릭터 리턴), ord(chr) (캐릭터 chr의 유니코드값 리턴), encode/decode('utf-8) (유니코드를 utf-8 규칙으로 인코딩/디코딩) 들을 사용했습니다.

2. 변수들의 선언입니다. <입/출력 방법>에서 언급한 것처럼 states, vocabulary, initialState는 초성우선이 state가 하나 더 많은 점을 제외하곤 동일하고, 컴퓨터 자판 입력을 기준으로 하였습니다.
stateTransitionFunction, outputFunction은 한 row당 스페이스바를 기준으로 3부분으로 나누어진 라인들로 이루어진 텍스트파일을 읽어 와서 딕셔너리에 저장합니다.\
vocamap은 핸드폰 자판과 한글 글자를 매핑해주는 딕셔너리입니다.

3. outputFunction들의 정의입니다.
outputFuntion.txt 파일에는 해당 transition에서 일어나야 할 아웃풋 함수의 이름만이 정의되어 있습니다.
실제로는 그 함수는 KOREAM_Mealy_Simulator 내의 

currentString = eval(currentOutput + '("' + currentString + '",' + '"' + inputChar + '")')

라인에서 eval 을 통해 실행됩니다.
따라서 해당 함수들이 py 파일 어딘가에 정의되어야 하는데, 그에 해당하는 부분입니다.

함수들이 하는 일은 이름에서부터 유추할 수 있습니다.
모든 함수는 해당 작업을 마친 후의 String을 리턴합니다.

* BackSpace는 '-' 로 대체하였으며, 백스페이스 하나가 무조건 한 음절을 통째로 지우도록 구현했습니다. (ex: 'ㄱㅏㄴㅏ-'의 결과값은 '가')
이하 함수별 설명입니다.

받침 우선)
newChar(currentString, inputChar) : currentString의 뒤에 inputChar를 초성으로 갖는 음절을 덧붙입니다.
JaEumtoMoEum(currentString, inputChar) : inputChar을 currentString의 마지막 음절의 중성으로 설정합니다.
MoEumtoMoEum(currentString, inputChar) : inputChar와 currentString의 마지막 음절의 중성을 합친 겹모음을 currentString의 마지막 음절의 중성으로 설정합니다.
MoEumtoBaadChim(currentString, inputChar) : inputChar을 currentString의 마지막 음절의 종성으로 설정합니다.
BaadChimtoBaadChim(currentString, inputChar) : inputChar와 currentString의 마지막 음절의 종성을 합친 겹받침을 currentString의 마지막 음절의 종성으로 설정합니다.
BaadChimtoMoEum(currentString, inputChar) : currentString의 마지막 음절에서 종성을 빼내고, 해당 자음을 초성으로, inputChar를 중성으로 갖는 새로운 음절을 currentString의 뒤에 덧붙입니다.
BackSpace(currentString, inputChar) : currentString의 마지막 음절을 지웁니다.

프로젝트 3에서 추가된 함수들 :

replaceJaEum : 마지막 음절의 자음을 변경합니다.
replaceMoEum : 마지막 음절의 모음을 변경합니다.
replaceBaadChim : 마지막 음절의 받침을 변경합니다.
BaadChimtoJaEum : 마지막 음절의 받침이 종성이 될 수 없는 자음으로 바뀔때 호출됩니다. 예를 들어, '갗'에 '$'이 들어와 '가ㅉ'으로 가야 할 때 호출됩니다.
JaEumtoBaadChim : 위와 반대의 경우에 호출됩니다. 예를 들어, '가ㅉ'에 '$'이 들어와 '갖'으로 가야 할 때 호출됩니다.
Space : 스페이스바입니다. 예를 들어, '갖'에서 '갖ㅈ'로 가고 싶을 때 '$'을 입력하기 전에 '_'를 입력해 이 함수를 호출하면 다음 글자로 넘어갑니다.


초성 우선)
newChar(currentString, inputChar) : 동일.
JaEumtoMoEum(currentString, inputChar) : inputChar을 currentString의 마지막 음절의 중성으로 설정합니다.
MoEumtoMoEum(currentString, inputChar) : inputChar와 currentString의 마지막 음절의 중성을 합친 겹모음을 currentString의 마지막 음절의 중성으로 설정합니다.
MoEumtoBaadChim(currentString, inputChar) : 동일.
BaadChimtoBaadChim(currentString, inputChar) : 동일.
BaadChimtoMoEum(currentString, inputChar) : 동일.
BaadChimtoDoubleBaadChim(currentString, inputChar) : currentString의 마지막 음절을 currentString의 끝에서 두번째 음절의 종성으로 넣습니다. 그 후 inputChar를 그 뒤에 덧붙입니다. 
currentString의 마지막 음절과 inputChar이 겹받침이 될 수 있는 경우에 실행됩니다. (ex: BaadChimtoDoubleBaadChim('가ㄱ', 'ㅅ')='각ㅅ')
DoubleJaEum(currentString, inputChar) : currentString의 마지막 음절과 currentString의 끝에서 두번째 음절의 종성을 합친 자음을 currentString의 끝에서 두번째 음절의 종성으로 넣습니다. 
그 후 inputChar을 그 뒤에 덧붙입니다. (ex: DoubleJaEum('각ㅅ', 'ㅅ')='갃ㅅ')
BackSpace(currentString, inputChar) : 동일.
CheckFianl(currentString) : 스트링을 전부 모아쓰기 한 후 마지막 음절이 초성만 남아 있는 경우 앞 음절의 종성으로 넣어줍니다. (ex: CheckFianl('가ㄱ') = '각')

프로젝트 3에서 추가된 함수들 :

replaceJaEum : 마지막 음절의 자음을 변경합니다.
replaceMoEum : 마지막 음절의 모음을 변경합니다.
replaceBaadChim : 마지막 음절의 받침을 변경합니다.
BaadChimtoJaEum : 마지막 음절의 받침이 종성이 될 수 없는 자음으로 바뀔때 호출됩니다. 예를 들어, '갗'에 '$'이 들어와 '가ㅉ'으로 가야 할 때 호출됩니다.
JaEumtoBaadChim : 위와 반대의 경우에 호출됩니다. 예를 들어, '가ㅉ'에 '$'이 들어와 '갖'으로 가야 할 때 호출됩니다.
Space : 스페이스바입니다. 예를 들어, '갖'에서 '갖ㅈ'로 가고 싶을 때 '$'을 입력하기 전에 '_'를 입력해 이 함수를 호출하면 다음 글자로 넘어갑니다.


위에서 볼 수 있듯이 초성우선의 경우 한글 모아쓰기를 전부 마친 후 마지막 음절이 초성만 남아있는 경우 앞 음절의 종성으로 넣도록 구현했습니다.
예를 들어, 조교님짱짱매ㄴ 으로 끝날 경우 마지막에 CheckFinal 함수를 이용해 조교님짱짱맨 으로 바꿔줍니다.

(만약 조교님, 교수님께서 원하셨던게 그냥 조교님짱짱매ㄴ 으로 끝나는 거라면 한글 모아쓰기 오토마타 함수 내의
currentString = CheckFinal(currentString)
print currentString
두 라인만 지워주면 됩니다.)

4. 한글 모아쓰기 오토마타의 정의입니다.
기본적으로 예비프로젝트 1-2 에서 사용한 밀리머신을 디테일한 부분만 약간 변형해서 사용했습니다.
outputFunction을 코드 내에 직접 정의하고 호출만 함으로서 파일에 쓰고 호출할 필요가 굳이 없어졌습니다. 따라서 파일에 outputFunction들을 적고 호출하는 부분을 바로바로 eval하는 것으로 변경했습니다.
또한 인풋이 들어오지 않고 엔터만 쳤을 경우 기본 인풋 '8#62551119325544_44#200' 가 들어가도록 수정하였습니다.
Legal한 한글이 아닌 경우 에러메세지를 출력하고 리턴합니다.

5. 한글 모아쓰기의 호출입니다. 
앞서 정의한 argument들을 이용해 호출합니다.