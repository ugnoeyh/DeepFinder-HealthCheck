# DeepFinder-HealthCheck
딥파인더 텔레그램 모니터링

---

## 📢소개
시큐온클라우드에서 판매하는 DeepFinder WAF 상품의 텔레그램 모니터링 코드입니다.
외부에서 실시간으로 모니터링 지원이 되지 않아 API를 지원하고 있어서 만들었습니다.
 
<br>

## 📱 지원 가능 메신저
Telegram

---

## 📌 주요 기능
에이전트연결 상태, 필터정책 동기화 모니터링


## 명령어
/mute [ip] 
해당 아이피 알림 무시

/excute [ip]
무시한 아이피 알림 허용

/list
mute 한 IP 목록 나열

---

## 📮사용법
### 1. 모듈 설치
pip install -r requirements.txt
설치 모듈 : telebot==0.0.5, requests==2.28.2, urllib3==1.26.15

#### 2. 실행
python3 DeepFinder-Telegram.py

백그라운드 실행시
nohup python3 DeepFinder-Telegram.py &

## TO-DO List
추후 지원 메신저 : Slack
코드 보안 및 기능 추가

## 참고
[API 문서](http://52.78.52.101/ko/install/4.API.html#getagentinfo)