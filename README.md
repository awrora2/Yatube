# Yatube

Блог, позволяющий пользователям обменивать публикациями, подписываться друг на друга и комментировать публикации. 

## Getting Started

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/awrora2/hw05_final.git
cd hw05_final
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
_12source env/bin/activate_
_python3 -m pip install --upgrade pip_
```
Установить зависимости из файла requirements.txt:
```
_pip install -r requirements.txt_
```
Выполнить миграции:
```
_python3 manage.py migrate_
```
Запустить проект:
```
_cd yatube_
_python3 manage.py runserver_
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




