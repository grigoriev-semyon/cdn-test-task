# Сервис городов 

Сервис для хранения информации о городах и работы с ней

## Запуск
0. Установите python3.11

1. Перейдите в папку проекта

2. Выполните команды:
    ```console
    foo@bar:~$ make configure
    foo@bar:~$ make db
    foo@bar:~$ make env
    foo@bar:~$ make migrate
    foo@bar:~$ make run
    ```

## ENV-file description
- `DB_DSN=postgresql://postgres@localhost:5432/postgres` – Данные для подключения к БД
