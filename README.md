# Прокси-сервер IPv6 обратного подключения
Этот проект представляет собой простой прокси-сервер с использованием протокола SOCKS5 для обратного подключения через IPv6. Прокси-сервер создает и ротирует случайные IPv6 адреса из заданной подсети для обеспечения анонимности и разнообразия.

## Установка и запуск
1. Клонируйте репозиторий:
```bash
git clone https://github.com/z3r0xxx/IPv6-Proxy-Server.git
```
2. Перейдите в каталог проекта:
```
cd IPv6-Proxy-Server
```
3. Запустите скрипт proxy_server.py:
```
python3 proxy_server.py
```

## Параметры конфигурации
Прокси-сервер может быть настроен с помощью следующих параметров:

- `subnet`: Подсеть IPv6, из которой будут генерироваться адреса.
- `prefix_length`: Длина префикса подсети IPv6.
- `num_proxies`: Общее количество прокси, которое будет создано.
- `rotation_interval`: Интервал ротации IPv6 адресов в секундах.
- `username`: Логин для аутентификации на прокси-сервере (опционально).
- `password`: Пароль для аутентификации на прокси-сервере (опционально).
- `allowed_hosts`: Список разрешенных хостов, к которым можно подключаться через прокси (опционально).
- `blocked_hosts`: Список запрещенных хостов (опционально).

## Пример использования
```
from proxy_server import ProxyServer

# Создание экземпляра прокси-сервера
proxy_server = ProxyServer(subnet="fe80::", prefix_length=48, num_proxies=10, rotation_interval=300)

# Запуск SOCKS5 сервера
proxy_server.start_socks5_server()
```

## Подключение клиента
Запрос должен быть направлен на порт 1080<br>
После установления соединения клиент должен отправить запрос на авторизацию (в случае если установлен лог/пасс)

Пример запроса с лог/пасс
```
GET / HTTP/1.1
Host: yourhost.ru
Proxy-Authorization: Basic base64encodedusernameandpassword
```
Пример запроса без лог/пасса
```
GET / HTTP/1.1
Host: yourhost.ru
```

После успешной аутентификации прокси-сервер будет отправлять клиенту IP-адрес прокси, через который будет осуществляться подключение к удалённому серверу
Пример ответа прокси сервера
```
HTTP/1.1 200 OK
Proxy-IP: [IPv6 address]
```

## Лицензия
Этот проект распространяется под лицензией MIT.
