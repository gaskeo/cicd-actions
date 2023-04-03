# CI/CD калькулятор

Простой пример реализации API калькулятора, который собирается
в [DockerHub](https://hub.docker.com) и разворачивается на сервере.

## Этапы CI/CD

1. [Проверка](.github/workflows/ci.yml#L11) исходного кода с помощью [SAST Bandit](https://bandit.readthedocs.io/en/latest/)
2. [Сборка](.github/workflows/ci.yml#L58) контейнера
3. [Отправка собранного контейнера](.github/workflows/ci.yml#L58) в [DockerHub](https://hub.docker.com)
4. Логин [в WireGuard](.github/workflows/cd.yml#L17)
5. [Отправка запроса](https://github.com/gaskeo/cd-handler) на развертывание нового образа [на специальную ручку на сервере](.github/workflows/cd.yml#L34) по виртуальной сети
6. [Развертывание](.github/workflows/cd.yml#L35) нового образа на сервере

## Секретные переменные

| Название переменной    | Значение                                                               |          Пример          | 
|:-----------------------|:-----------------------------------------------------------------------|:------------------------:|
| `DOCKERHUB_USERNAME`   | Имя на DockerHub                                                       |        `username`        |
| `DOCKERHUB_TOKEN`      | [Токен с DockerHub](https://docs.docker.com/docker-hub/access-tokens/) | `dckr_fds_faslkdfjas...` |
| `DOCKERHUB_REPOSITORY` | Название репозитория                                                   |       `repository`       |
| `WG_PRIVATE_KEY`       | Приватный ключ WireGuard клиента                                       |    `fsdaasfasvckjnx`     |
| `WG_ADDERSS`           | Адрес WireGuard клиента в виртуальной сети                             |      `10.0.0.12/24`      |
| `WG_PUBLIC_KEY`        | Публичный ключ WireGuard сервера                                       |     `fasdsajwlrjwfs`     |
| `WG_ENDPOINT`          | Адрес и порт WireGuard сервера                                         |   `11.23.31.43:51141`    |
| `WG_ALLOWED_IPS`       | Подмаска адресов, с которыми клиент связан через сервер WireGuard      |      `10.0.0.0/24`       |
| `CD_HOST`              | Адрес CD-сервера внутри виртуальной сети WireGuard                     | `http://10.0.0.13:8080`  |
| `CD_SECRET`            | Токен, необходимый для прохождения аутентификации на CD-сервере        |    `fsadjsadfgsafas`     | 

## CI

Весь CI запускается в одном [github action](.github/workflows/ci.yml), он состоит из двух работ и 9 этапов.

### Работа 1. Этап 1. Копирование кода

[Исходный код копируется](.github/workflows/ci.yml#L12) в экшен посредством `actions/checkout@v3`.

### Работа 1. Этап 2. Подготовка python

[Устанавливается](.github/workflows/ci.yml#L14) [Python](https://www.python.org/) 3.9.

### Работа 1. Этап 3. Bandit

[Устанавливаются](.github/workflows/ci.yml#L18) зависимости, [Bandit](https://bandit.readthedocs.io/en/latest/) готовит отчет.

### Работа 1. Этап 4. Артефакты 

Результат работы [Bandit](https://bandit.readthedocs.io/en/latest/) [сохраняется](.github/workflows/ci.yml#L35) в артефакты экшена.

### Работа 1. Этап 5. Проверка

Результат работы Bandit проверяется на наличие high-level уязвимостей. 

### Работа 2. Этап 1. Копирование кода

[Исходный код копируется](.github/workflows/docker-image.yml#L12) в экшен посредством `actions/checkout@v3`.

### Работа 2. Этап 2. Вход в DockerHub

[Авторизация](.github/workflows/docker-image.yml#L15) происходит по токену с помощью `docker/login-action@v2`.

### Работа 2. Этап 3. Копирование для сборки образа

[На данном этапе](.github/workflows/docker-image.yml#L21) создается окружение для сборки образа.

### Работа 2. Этап 4. Сборка и отправка образа

Образ [собирается внутри экшена и отправляется](.github/workflows/docker-image.yml#L24) в DockerHub.

## CD

Процесс CD запускается с помощью одного экшена в 3 этапа.

### Этап 1. Копирование кода

[Исходный код копируется](.github/workflows/cd.yml#L13) в экшен
посредством `actions/checkout@v3`.

### Этап 2. Подключение к WireGuard

[На данном этапе](.github/workflows/cd.yml#L16) происходит установка клиента
WireGuard и его настройка на работу с сервером.

### Этап 3. Отправка данных на север

Из экшена [формируется запрос](.github/workflows/cd.yml#L33) на специальную
ручку на сервере, запрос выполняется внутри виртуальной сети WireGuard. Тело
данного запроса состоит из формы, в которой передаются:

- Токен — необходим для подтверждения запроса
- `entry.sh` — Файл, который будет запускать процесс развертывания
- `myFiles` — остальные файлы, которые необходимы для развертывания

## API калькулятора

Калькулятор слушает `8000` порт.

### Swagger

Swagger находится на ручке [/docs]()

### expression

Ручка [/expression]() проводит вычисления для двух чисел. Используется `GET`
запрос с параметрами:

| Параметр    |                    Тип                    |
|:------------|:-----------------------------------------:|
| `n1`        |                    int                    |
| `n2`        |                    int                    |
| `operation` | <code>a &#124; s &#124; m &#124; d</code> |

Ответ возвращается в формате `JSON`:

```json
{
  "answer": 5,
  "expression": "2 + 3"
}
```

#### Пример

```shell
curl --location --request GET \
  'http://localhost:8000/expression?n1=2&n2=3&operation=a
```