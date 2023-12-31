# Стек
- Python 3.11 - язык для разработки бекенда
- FastAPI - фреймворк для API
- EdgeDB - база данных
- dramatiq - фоновые задачи (вычисления с моделью)
- redis - брокер сообщений для dramatiq
- minio - S3-like объектное хранилище (хранение загружаемых Excel)

# Структура проекта
- app/main.py - регистрация роутеров, настройка CORS
- app/settings.py - настройки проекта, задаваемые переменными окружения
- app/minio.py - инициализация клиента minio
- app/database.py - инициализация клиента edgedb
- app/dependencies.py - функция авторизации, вынесенная в зависимости (используется для применения авторизации на весь роутер)
- app/background.py - фоновые задачи
- app/routers - хендлеры запросов
- app/queries - запросы к БД
- app/models - описание моделей, которые возвращает или принимает API

# Архитектура
```
frontend <---> backend <---> edgedb
                 |            ^
                 |            |
                 |            |
                 v            v
               redis <---> dramatiq_worker <---> model
```

Фронтенд через предоставленный API обращается к бекенду для получения информации об объектах и их состоянии.

При загрузке excel файла, бекенд создает новую запись о файле в edgedb, отправляет данный файл в minio и создает новую задачу в redis.

Первый свободный worker забирает задачу из redis, выполняет необходимые вычисления, и записывает результат в edgedb.

Workerы можно располагать на других серверах в любом необходимом количестве.

# Деплой
1. Создать .env из .env.example
2. Поднять хранилище объектов - docker compose up -d minio
3. Перейти по http://127.0.0.1:9001/access-keys/new-account, user:password
4. Создать ключ доступа, скопировать два полученных ключа в .env в `S3_ACCESS_KEY` и `S3_SECRET_KEY`
5. Перейти по http://127.0.0.1:9001/buckets/add-bucket, создать хранилище с любым названием
6. Указать название в `S3_BUCKET`
7. Поднимаем базы данных - docker compose up redis edgedb. Первый запуск edgedb может занять время
8. Поднимаем бекенд и воркеров - docker compose up app worker

API доступно по - http://127.0.0.1/
Методы API описаны в - http://127.0.0.1/docs

# Результаты исследования

В папке `ML` содержатся все необходимые файлы по обработке и обучению моделей.

Файл `start.ipynb` содержит пердобрабтку данных.

Файл `predict_test.ipynb` содержит готовый пайпалйн обучения и предсказания модели для тестовых данный.

Файл `model.ipynb` содержит обучение моделей и подбор гиперпараметров.