# Mini-CRM (FastAPI)

Короткое мини‑CRM для распределения лидов (обращений) между операторами по источникам с учётом весов и лимитов.

## Быстрый старт

Локально (несколько вариантов запуска):

```bash
# 1) Если активировали виртуальное окружение (venv):
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2) Или запустить явно через venv в репозитории:
./env/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3) (альтернатива) Запуск через Docker (см. ниже)
```

**One-command start (recommended for reviewer)**

Если у вас установлен Docker — самый быстрый способ запустить проект (клонировать репозиторий и выполнить пару команд):

```bash
git clone <REPO_URL>
cd fastapi_testovoe_zadanie
docker build -t minicrm .
docker run -p 8000:8000 --rm minicrm
```

После этого API будет доступно по `http://localhost:8000` и документация по `http://localhost:8000/docs`.


Примеры запросов (порт 8000):

- Создать оператора:

```bash
curl -X POST "http://localhost:8000/api/v1/operators/" -H "Content-Type: application/json" \
  -d '{"name":"ivan","is_active":true,"max_load":10}'
```

- Создать источник (бот):

```bash
curl -X POST "http://localhost:8000/api/v1/sources/" -H "Content-Type: application/json" \
  -d '{"name":"telegram_bot_A"}'
```

- Привязать оператора к источнику с весом:

```bash
curl -X POST "http://localhost:8000/api/v1/operator-sources/" -H "Content-Type: application/json" \
  -d '{"operator_id":1,"source_id":1,"weight":20}'
```

- Зарегистрировать обращение (contact):

```bash
curl -X POST "http://localhost:8000/api/v1/contacts/" -H "Content-Type: application/json" \
  -d '{"external_id":"user@example.com","source_id":1}'
```

Ответ содержит информацию об обращении и назначенном операторе (поле `operator_id` может быть `null`).

## Модель данных (кратко)

- `Operator`: id, name, `is_active` (может ли принимать обращения), `max_load` (максимальное число обращений на оператора).
- `Source`: канал/бот, откуда пришло обращение.
- `Lead`: конечный клиент, определяется `external_id` (входной идентификатор). `external_id` нормализуется (strip + lower), поэтому одинаковые значения считаются одним лидом.
- `OperatorSource`: связывает оператора и источник с числовым `weight` — чем больше вес, тем большую долю трафика оператор должен получать для данного источника.
- `Contact`: конкретное обращение (lead_id, source_id, operator_id, created_at).

Нагрузка оператора определяется как текущее количество записей в таблице `contacts`, у которых `operator_id` равен id оператора.

## Алгоритм распределения

1. На вход при создании контакта подаётся `external_id` (или данные для поиска лида) и `source_id`.
2. Система ищет существующего `Lead` по `external_id`. Если не найден — создаёт новый `Lead`.
3. Берётся конфигурация `OperatorSource` для данного `source_id` — список операторов и их весов.
4. Операторы фильтруются по:
   - `is_active == True`;
   - `current_load < max_load` (где `current_load` — количество контактов, назначенных оператору).
5. Если доступных операторов нет, контакт создаётся без оператора (`operator_id = null`) и возвращается клиенту.
6. Если доступны — выбирается оператор случайно с вероятностью пропорциональной весу (weight / sum(weights)).

Замечание: при высокой параллельности возможны состояния гонки (короткие превышения лимита), для этого можно добавить более строгие DB‑блокировки или механизмы очередей.

## Что делать, если нужно изменить поведение

- Пересчитать веса и логику выбора — `app/crud.py::assign_operator`.
- Поменять определение нагрузки (например, считать только активные/открытые обращения) — в модели/CRUD.

## Docker

Создан `Dockerfile`, который собирает образ и запускает Uvicorn.

Сборка и запуск (в корне репозитория):

```bash
docker build -t minicrm .
# Запуск без сохранения БД (временный контейнер):
docker run -p 8000:8000 --rm minicrm

# Рекомендуемый запуск с сохранением SQLite-файла на хосте:
docker run -p 8000:8000 -v $(pwd)/minicrm_app.db:/app/minicrm_app.db --rm minicrm

# Или запустить из локального кода (dev, если вы не хотите билдить образ):
docker run -p 8000:8000 -v $(pwd):/app -v $(pwd)/minicrm_app.db:/app/minicrm_app.db --rm minicrm uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Если хотите автоперезагрузку при изменении кода, добавьте флаг `--reload` к команде запуска (как показано в примере dev).


## API роуты (основные)

- `POST /api/v1/operators/` — создать оператора
- `GET  /api/v1/operators/` — список операторов
- `PUT  /api/v1/operators/{id}` — обновить оператора
- `POST /api/v1/sources/` — создать источник
- `GET  /api/v1/sources/` — список источников
- `POST /api/v1/operator-sources/` — назначить оператору вес для источника
- `POST /api/v1/contacts/` — создать обращение (основной endpoint распределения)
- `GET  /api/v1/contacts/` — список обращений
- `GET  /api/v1/leads/` — список лидов
