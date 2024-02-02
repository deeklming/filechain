# Filechain
프로그램 실행 전 또는 프로그램 업데이트 및 배포시 자동 무결성 검증 알고리즘

## Explain
프로그램을 배포 서버에서 클라이언트까지 중간에 수정 없이 제대로 배포 되었는지 간단한 알고리즘으로 확인하는 방법이다.   
이것은 보안 프로그램 추가없이 변경되지 말아야 할 파일들의 무결성을 검증하는 기능을 담고있다.   
네트워크 사용할 때에 Filechain(파일체인)은 Blockchain(블록체인)을 기반으로 하고 저비용 고사양을 목표로 한다.   
가능한 많은 플랫폼인 데스크톱, 모바일, IoT, 임베디드 환경 등에서 사용가능 하도록 목표로 한다.

## Technology Development Background
1. CBC (Cipher-block Chaining) - integrity
2. BLAKE2 (Hash Algorithm) - fast
3. JSON (JavaScript Object Notation) - setting

## Blueprint
### without network
<div><img width="460" src="https://user-images.githubusercontent.com/71743128/171807672-694e3c9f-d756-4eb2-a07c-c75655a7eecb.png"></img></div></br>

네트워크 없이 클라이언트에서 매번 프로그램 실행 전에 무결성을 검사하고 실행한다.

### with network
<div><img width="500" src="https://user-images.githubusercontent.com/71743128/170218506-62a171c4-8238-4152-91a2-193506ee4455.png"></img></div></br>

```
    total: 5
    success: 3 or more
    failure: 2 or less
```
네트워크는 메시형으로 구성하고 서버는 실시간 실행중인 모든 클라이언트 프로그램 정보를 지역단위로 필요로 한다.   
클라이언트는 프로그램 실행 시작시 서버 상관없이 현재 실행중인 모든 프로그램들 중 일치하는 파일체인 값의 수량이 50%만 넘으면 해당 프로그램을 실행 시킬 수 있다.

## Concept
### Filechain Hash Structure
<div><img width="230" src="https://user-images.githubusercontent.com/71743128/170274746-e630bac2-18dd-49d0-834f-6e4f657bf1a6.png"></img></div></br>

Now Hash는 현재 실행 프로그램의 파일 군집 해시값이고 Last Hash는 이전 파일 군집 해시값 또는 초기값이다.   
Now Hash와 Last Hash를 합쳐서 Filechain Hash라고 하고 이것이 하나의 단위가 된다.

### Create Info Hash
<div><img width="600" src="https://user-images.githubusercontent.com/71743128/170274951-b73213c6-66e5-49ca-95ff-2e3bc0bee992.png"></img></div></br>

Info Hash는 한 파일이나 디렉토리의 정보를 해싱한 것이다.   
Info Hash를 생성 할 때 프로그램 실행 도중 변경하지 않는 모든 디렉토리와 파일들을 불러와서 파일은 파일 이름, 파일 크기, 파일 수정 시간을 문자열로 합치고 디렉토리는 이름만을 가지고 각각 64Byte로 해시화 한다.

### Create Final Hash
<div><img width="360" src="https://user-images.githubusercontent.com/71743128/170275111-4b53aa4a-722f-447e-8d44-558cd4d23848.png"></img></div></br>

Final Hash는 Info Hash를 가지고 만든 최종 해시값이다.   
Final Hash는 CBC 형식처럼 서버측에서 지정한 Initialization Hash 또는 Info Hash 또는 Now Hash를 가지고 해시를 XOR한다. 그리고 XOR 과정을 각 디렉토리와 파일마다 반복하여 Final Hash를 만든다.   
Final Hash와 Now Hash의 차이점은 Final Hash는 메모리상에 저장된 해시값이고 Now Hash는 디스크에 저장된 해시값이다.   

### Filechain Hash flow
<div><img width="700" src="https://user-images.githubusercontent.com/71743128/170275327-ae17f61d-e59c-450a-9dc5-126aae9f1d66.png"></img></div></br>

프로그램 첫 배포시에는 Initialization Hash를 프로그램 업데이트와 증명시에는 Now Hash를 가지고 Final Hash를 만든다.   
Initialization Hash는 서버측에서 직접 만들거나 랜덤값으로 지정하면 되고 Now Hash와 Last Hash에 중복해서 생성한다.   
서버측에서 프로그램 버전 업데이트시에 Filechain Hash도 업데이트 하는데 Now Hash를 Last Hash로 덮어쓴 다음 Now Hash와 New Info Hash들로 XOR해서 Final Hash를 만들고 Now Hash에 덮어쓴다.   
클라이언트측에서 프로그램 실행전 증명시에 Now Hash와 Now Info Hash들로 XOR해서 Final Hash를 만들고 Last Hash와 비교하고 같으면 무결성이 증명되어 프로그램을 실행하고 다르면 파일 군집에 무엇인가 변경 되었다는 뜻으로 프로그램을 종료한다.

## Function
- help
- make initialization hash
- added and ignored
- create filechain
- filechain update
- filechain verify

#### Now
* 현재 단일폴더 절대경로만 사용가능
* 변경 예정

#### Developer
* Deeklming