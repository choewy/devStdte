# 화재안전팀 의견수렴 프로그램

1. [개요](#1-개요)
2. [주요기능](#2-주요기능)
3. [개발환경](#3-개발환경)
4. [모듈현황](#4-모듈현황)
5. [폴더구조](#5-폴더구조)
6. [실행방법](#6-실행방법)
7. [수정이력](#7-수정이력)

<br>

## 1. 개요

💡 본 프로그램은 다양한 이슈의 의견 수렴을 위한 데이터베이스 기반 프로그램 입니다.

✨ 시간관리 프로그램의 계정을 통해 로그인할 수 있으며, 회원가입 또한 시간관리 프로그램을 통해서만 가능합니다.

✨ 장기 출장자를 고려하여 `firebase`를 사용한 외부 서버로 구축하였기 때문에 더 이상 가상머신(`virtualBox`)의 노예가 되지 않아도 된답니다!🙌

<br>

## 2. 주요기능

✔ 신규 이슈 등록

✔ 답글 등록

✔ 운영 방안 확인 : 모든 사용자가 운영 방안을 확인할 수 있으며, 관리자만 수정 가능합니다.

✨ 신규 이슈 등록자인 경우 이슈 제목, 내용 수정 및 삭제 가능

✨ 관리자인 모든 이슈 수정 및 삭제 가능, 모든 답글 삭제 가능, 운영 방안 수정 가능

<br>

## 3. 개발환경

본 프로그램은 오로지 `Python`으로만 개발하였으며, 관심있으신 분들은 아래 링크를 통해 설치하세요!

🔗 `Python 3.7.9` : [다운로드](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64-webinstall.exe)

💸 `firebase` 는 아래 표의 조건 내에서 무료로 사용 가능한 플랫폼입니다.

| 구분          | 내용                     | 비고                                      |
| ------------- | :----------------------- | :---------------------------------------- |
| 프로젝트 비용 | 무료                     |                                           |
| 저장 용량     | 총 `1GB` 무료 제공       | `2021-07-09` 기준 : `369.3KB` 사용        |
| 트래픽 용량   | 월 무료 `10GB` 무료 제공 | `2021-06 ~ 2021-07` 기준 : `320.3MB` 사용 |

❓ 만약 `firebase`의 모든 서비스가 유료로 전환이 된다면 결재를 하거나, 데이터 백업 후 화재안전팀 서버 PC를 사용하는 방안으로 다시 개발해야 합니다.

<br>

## 4. 모듈현황

⚙ `PyQt5` : `pip3 install pyqt5==5.15.4`

```python
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
```

⚙ `openpyxl` : `pip3 install openpyxl==3.0.7`

```python
import openpyxl
```

⚙ `pandas` : `pip3 install pandas==1.2.3`

```python
import pandas as pd
```

⚙ `firebase_admin` : `pip3 install firebase_admin==5.0.1`

```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
```

⚙ `pyinstaller` : `pip3 install pyinstaller==4.3`

```commandline
pyinstaller -w -i=images/icon.ico app-build-version.py
```

<br> 

## 5. 폴더구조

> 📁 `../images/` : 프로그램에 사용되는 이미지, 아이콘 파일
>
> 📁 `../public/`
>
> > 📁 `../components/`
> >
> > > 📗 `__init__.py` : 패키지 파일
> >
> > > 📗 `authForm.py` : 로그인 화면 파일
> >
> > > 📗 `mainForm.py` : 로그인 후 나타나는 메인 화면 파일
> >
> > 📗 `__init__.py` : 패키지 파일
> >
> > 📗 `window.py` : 프로그램의 메인 윈도우 파일
> >
> > 📗 `central.py` : 메인 윈도우의 메인 위젯 파일
>
> 📁 `../src/`
>
> > 📁 `../dialog/`
> >
> > > 📗 `__init__.py` : 패키지 파일
> >
> > > 📗 `manual.py` : 운영 방안 다이얼로그 파일
> >
> > > 📗 `new.py` : 새 이슈 등록 다이얼로그 파일
> >
> > > 📗 `question.py` : 의사 결정 다이얼로그 파일
> >
> > 📁 `../firebase/`
> >
> > > 📗 `__init__.py` : 패키지 파일
> > >
> > > 📗 `realtimedb.py` : `firebase`의 `Real Time Database` 쿼리 파일
> > >
> > > 🔐 `(.gitignore) scheduler_privacy_key.json` : `firebase` 사용자 인증 파일
> > >
> > > 🔐 `(.gitignore) survey_privacy_key.json` : `firebase` 사용자 인증 파일
> >
> > 📁 `../widget/`
> >
> > > 📗 `__init__.py` : 패키지 파일
> >
> > > 📗 `header.py` : 이슈 상단 헤더 위젯 파일
> > >
> > > 📗 `answer.py` : 이슈에 해당하는 답글 위젯 파일
> > >
> > > 📗 `home.py` : 홈 위젯 파일
> > >
> > > 📗 `list.py` : 이슈 목록 위젯 파일
> > >
> > > 📗 `navBar.py` : 메인 화면 좌측 메뉴 위젯 파일
> > >
> > > 📗 `survey.py` : 이슈 내용 위젯 파일
> > >
> > > 📗 `title.py` : 이슈 목록 제목 위젯 파일
> >
> > 📗 `__init__.py` : 패키지 파일
> >
> > 📘 `style.qss` :  프로그램 스타일시트 파일
>
> 📁 `../temp/`
>
> > 📔 `client.json` : 사용자 아이디 저장 파일
>
> 📔`READ.md` : 프로그램 설명 파일
>
> 📗 `app-build-version.py` : 프로그램 실행 파일
>
> 🔐 `(.gitignore) app-dump-version.py` : 데이터베이스 `dump` 실행 파일

<br>

## 6. 실행방법

✔ 방법 1 : `app.exe` 또는 `stdte Survey` 실행

✔ 방법 2 : 명령 프롬프트 실행

```commandline
cd scheduler
python app-build-survey.py
```

<br>

## 7. 수정이력

✔ `2021-07-12` : 최초 배포