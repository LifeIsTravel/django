# LifeIsTravel

## 프로젝트 소개
http://lifeistravel.shop

## 실행
### requirements.txt 속 패키지 설치
```bash
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```
### 프로젝트 실행
```bash
gunicorn --bind 0.0.0.0:8000 configuration.wsgi:application
```
### 설치된 패키지 목록 requirements.txt 생성
```bash
gunicorn --bind 0.0.0.0:8000 configuration.wsgi:application

## 아키텍처
![image](https://github.com/user-attachments/assets/735dbc89-5bd4-4321-a215-ced48878a8da)

