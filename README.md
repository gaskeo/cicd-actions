# CI/CD калькулятор

Простой пример реализации API калькулятора, который собирается
в [DockerHub](https://hub.docker.com) и разворачивается на сервере.

## Этапы CI/CD

1. [Сборка](.github/workflows/docker-image.yml) контейнера
2. [Отправка собранного контейнера](.github/workflows/docker-image.yml)
   в [DockerHub](https://hub.docker.com)
3. Логин [в WireGuard](.github/workflows/docker-image.yml)
4. [Отправка запроса](https://github.com/gaskeo/cd-handler) на развертывание нового
   образа [на специальную ручку на сервере](.github/workflows/cd.yml#L34) по
   виртуальной сети
5. Развертывание нового образа на сервере

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
| `CD_SECRET`            | Токен, необходимый для прохождения аутентификации на CD-сервере        |   `fsadjsadfgsafas`      | 

## CI 
Весь CI запускается в одном [github action](https://github.com/gaskeo/cicd-actions/blob/main/.github/workflows/docker-image.yml), 
он состоит из 4 этапов.

### Этап 1. Копирование кода

[Исходный код копируется](.github/workflows/docker-image.yml#L12) в экшен посредством `actions/checkout@v3`.

### Этап 2. Вход в DockerHub

[Авторизация](.github/workflows/docker-image.yml#L15) происходит по токену с помощью `docker/login-action@v2`.

### Этап 3. Копирование для сборки образа

[На данном этапе](.github/workflows/docker-image.yml#L21) создается окружение для сборки образа.

### Этап 4. Сборка и отправка образа 

Образ [собирается внутри экшена и отправляется](.github/workflows/docker-image.yml#L24) на DockerHub.

## CD

Процесс CD также запускается с помощью одного экшена в 3 этапа.

### Этап 1. Копирование кода

[Исходный код копируется](.github/workflows/cd.yml#L13) в экшен посредством `actions/checkout@v3`.

### Этап 2. Подключение к WireGuard 

[На данном этапе](.github/workflows/cd.yml#L16) происходит установка клиента WireGuard и его настройка на работу с сервером.

### Этап 3. Отправка данных на север

Из экшена [формируется запрос](.github/workflows/cd.yml#L33) на специальную ручку на сервере, запрос выполняется внутри виртуальной сети WireGuard. Тело данного запроса состоит из формы, в которой передаются:

- Токен — необходим для подтверждения запроса
- `entry.sh` — Файл, который будет запускать процесс развертывания
- `myFiles` — остальные файлы, которые необходимы для развертывания


