# Cloud
Файловое хранилище с загрузкой файлов в один клик.  
Урок 3 курса Асинхронный Python от Devman.

## Запуск
```bash
$ pip install -r requirements.txt
$ python server.py
```

## Конфигурация
Через аргументы командой строки
```bash
usage: server.py [-h] [-nl] [-d DELAY] [-p PATH]

options:
  -nl, --nolog              Выключение логов
  -d DELAY, --delay DELAY   Задержка ответа (с)
  -p PATH, --path PATH      Путь до каталога с файлами
```

## Docker

```bash
$ docker run -i -p 8080:8080 mayosen/dvmn_cloud
```

С аргументами командой строки
```bash
$ docker run -i -p 8080:8080 mayosen/dvmn_cloud -nl -d 1
```
