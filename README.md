# Warehouse

## Описание
Проект предназначен для управления складскими запасами и включает REST API для обработки данных о продуктах, партиях и отгрузках. Система реализована с использованием FastAPI, PostgreSQL, Redis и Docker для удобного развёртывания и масштабирования.

## Стек технологий
- **FastAPI**: для разработки REST API
- **PostgreSQL**: база данных для хранения информации о продуктах и партиях
- **Redis**: кэширование данных для ускорения доступа
- **Docker**: контейнеризация для упрощения развёртывания

## Установка и запуск

Содержание`.env` файла:
   ```env
   APP_TITLE=WH
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@warehouse_db:5432/warehouse
   SECRET=склад
   API_ROOT_PATH=/
   ```

   Склонируйте репозиторий:
   ```git clone git@github.com:Ostashev/warehouse.git```

   Перейдите в дирректорию:
   ```cd warehouse```

   Запустите контейнеры:
   ```docker-compose up --build```

   После успешного запуска, сервер API будет доступен по адресу:
   ```http://localhost:8089```
