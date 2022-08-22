# Yatube

Блог, позволяющий пользователям обменивать публикациями, подписываться друг на друга и комментировать публикации. 

## Getting Started

Клонировать репозиторий и перейти в него в командной строке:
```
_git clone https://github.com/awrora2/hw05_final.git_
_cd hw05_final_
```
Cоздать и активировать виртуальное окружение:
```
_python3 -m venv env_
_source env/bin/activate_
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

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
