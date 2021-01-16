# keylogger

대상 컴퓨터의 입력 받은 키를 서버를 통해 전달받는 프로그램

창이 전환될때 마다 바뀌는 윈도우 제목에 따라 입력된 키를 전달한다

## Setting
```
pip install -r requirements.txt 
```

## 파일화
```
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```

> ※  환경변수 설정 필수 `C:\Users\"유저명"\AppData\Local\Programs\Python\"파이썬버전"\Scripts`

## 상대방 컴퓨터에서 실행되지 않는 경우
* 해결법1 : pyqt5와 pyinstaller간의 문제로 python 버전을 3.5로 낮춰서 다시 세팅해보기
* 해결법2 : 환경변수로 pyqt5의 해당 dll의 위치를 전역으로 설정해주기

## 실행
```
python main.py
```