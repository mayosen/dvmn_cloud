# Cloud
Файловое хранилище с загрузкой файлов в один клик.  
Урок 3 курса Асинхронный Python от Devman.

## Запуск
```bash
$ pip install -r requirements.txt
$ python server.py
```

## Конфигурация
С помощью аргументов командой строки можно задать настройки сервера
```bash
usage: server.py [-h] [-nl] [-d DELAY] [-p PATH]

options:
  -nl, --nolog              Выключение логов
  -d DELAY, --delay DELAY   Задержка ответа (с)
  -p PATH, --path PATH      Путь до каталога с файлами
```
