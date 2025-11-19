# DB_section

## Docker

### Как поднять контейнер с БД
Из корневой директории проекта выполнить команду:
```bash
docker compose -f docker-compose.yml up -d
```

### После этого выполнить миграции Alembic
```bash
alembic revision --autogenerate -m "Initial commit"
alembic upgrade head
```