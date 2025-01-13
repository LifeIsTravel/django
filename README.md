# ✈️ LifeIsTravel

**여행을 더 편리하게! 항공권 및 호텔 가격 비교부터 지연 예측, 날씨 정보까지 한 번에 제공하는 서비스입니다.**  
🔗 **[웹사이트 바로가기](http://lifeistravel.shop)**  

---

## 🏝️ 프로젝트 소개

### 1️⃣ 메인 페이지
<img src="https://github.com/user-attachments/assets/cdda2aca-ca41-4f55-81e6-75cc8da522f8" width="800"/>

---

### 2️⃣ ✈️ 항공권 가격 비교

<div align="center">
  <img src="https://github.com/user-attachments/assets/4a3c0961-a349-4ae7-8e9f-89a181f1becd" width="45%"/>
  <img src="https://github.com/user-attachments/assets/143f4ec7-d141-4e00-b359-b3b31f22b17c" width="45%"/>
</div>

---

### 3️⃣ 🏨 호텔 가격 비교

<div align="center">
  <img src="https://github.com/user-attachments/assets/13c655d5-3cf0-4175-b18b-8eeda4f5329a" width="45%"/>
  <img src="https://github.com/user-attachments/assets/ac7b932d-d398-4126-be74-32e8bef34ecf" width="45%"/>
</div>

---

### 4️⃣ ✈️ 항공편 + 호텔 조합 추천

<div align="center">
  <img src="https://github.com/user-attachments/assets/8c6b269b-16f5-4768-bad9-f41ba0495c80" width="45%"/>
  <img src="https://github.com/user-attachments/assets/4fa11a2c-3006-4fe8-b353-5b66dbadb9db" width="45%"/>
</div>

---

### 5️⃣ 🛫 항공편 지연 예측 + 🌤️ 날씨 정보

<div align="center">
  <img src="https://github.com/user-attachments/assets/ce231b7e-d200-40fd-8536-abe12158e432" width="45%"/>
  <img src="https://github.com/user-attachments/assets/275d3cb1-408d-44c2-9332-1a2930e3ee3b" width="45%"/>
</div>

---

## ⚙️ 실행 방법

### 1️⃣ 패키지 설치
```bash
$ source env/bin/activate
(env)$ pip install -r requirements.
```
### 2️⃣ 프로젝트 실행
```bash
gunicorn --bind 0.0.0.0:8000 configuration.wsgi:application
```
### 3️⃣ 설치된 패키지 목록 저장
```bash
pip freeze > requirements.txt
```

## 🏗️ 아키텍처
<img src="https://github.com/user-attachments/assets/735dbc89-5bd4-4321-a215-ced48878a8da" width="800"/>
