# Yatube

Блог, позволяющий пользователям обменивать публикациями, подписываться друг на друга и комментировать публикации. 

## Getting Started

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/awrora2/API_for_Yatube.git
cd yatube_api
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
cd yatube
python3 manage.py runserver
```
### Prerequisites

```
Django==2.2.16
mixer==7.1.2
Pillow==8.3.1
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
requests==2.26.0
six==1.16.0
sorl-thumbnail==12.7.0
Faker==12.0.1
```




