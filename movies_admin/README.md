## Коротко о том, что происходит
Поднимается БД postgres и в контейнер закидывается db_schema.sql из schema_design, который автоматически применяется и готовит базу данных к работе.
Из текущей директории собирается docker контейнер на основе содержимого src (django проект).
В контейнер подкидываются файлы из sqlite_to_postgres, для переноса данных из базы sql.

## Шаблон .env
```
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
POSTGRES_PASSWORD=
```

## Как запустить
```
'docker-compose up -d --build'
'docker-compose exec backend make run'
и ввести пароль для пользователя admin
```

## Что делает make run
```
создаёт статические файлы из django проекта
создаёт миграции
применяет миграции
загружает данные из sql в postgres
создаёт пользователя admin для админки django
```