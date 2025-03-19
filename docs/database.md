# База данных

## Структура
- PostgreSQL 15
- Пользователь: `homestyle_user`
- База данных: `homestyle`

## Настройка прав
```sql
GRANT ALL ON SCHEMA public TO homestyle_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO homestyle_user;
