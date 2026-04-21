# RAGStudyBot

FastAPI бэкенд для чат-бота по алгоритмам и структурам данных.
Работает через OpenAI-совместимый API (OpenAI, OpenRouter, Ollama, Gemini, Mistral).

На текущем этапе (pre-RAG) бот отвечает из собственных знаний LLM.
База материалов и векторный поиск будут добавлены позже.

---

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — менеджер зависимостей
- [just](https://just.systems/) — таск-раннер (опционально)
- API ключ от OpenRouter или любого OpenAI-совместимого провайдера

---

## Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/AlexmMercer/rag-algorithm-bot.git
cd rag-algorithm-bot
```

### 2. Установи зависимости

```bash
uv sync
```

Команда создаст виртуальное окружение `.venv/` и установит всё из `pyproject.toml`.

### 3. Создай `.env` файл

Скопируй шаблон и пропиши свой ключ:

```bash
cp .env.example .env
```

Открой `.env` и замени значение `LLM_API_KEY` на свой ключ.

Получить ключ на [OpenRouter](https://openrouter.ai/keys) — самый быстрый способ
(есть бесплатные модели, один ключ даёт доступ к GPT, Claude, DeepSeek и другим).

Пример `.env`:

```env
LLM_HOST=https://openrouter.ai/api/v1
LLM_MODEL=deepseek/deepseek-r1
LLM_API_KEY=sk-or-v1-...
PROMPT_PATH=prompts/system.md
```

---

## Запуск

### Через just (рекомендуется)

```bash
just server
```

### Напрямую через uv

```bash
uv run uvicorn app.main:app --reload
```

Сервер запустится на `http://localhost:8000`.

---

## Проверка работы

После запуска открой в браузере:

- `http://localhost:8000/` — редирект на Swagger UI
- `http://localhost:8000/docs` — интерактивная документация API
- `http://localhost:8000/health` — проверка что сервер жив

### Отправить тестовый вопрос

Через Swagger UI (самый простой способ):

1. Открой `http://localhost:8000/docs`
2. Раскрой `POST /question`
3. Нажми `Try it out`
4. В теле запроса напиши:
   ```json
   {"text": "Объясни как работает binary search"}
   ```
5. Нажми `Execute`

Через curl:

```bash
curl -X POST http://localhost:8000/question \
  -H "Content-Type: application/json" \
  -d '{"text": "Объясни как работает binary search"}'
```

---

## API эндпоинты

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/` | Редирект на `/docs` |
| `GET` | `/health` | Статус сервера + текущая модель |
| `POST` | `/question` | Задать вопрос боту |

Формат запроса к `POST /question`:

```json
{"text": "Твой вопрос здесь"}
```

Ограничения на поле `text`:
- минимум 1 символ
- максимум 2000 символов

Формат ответа:

```json
{"text": "Ответ бота"}
```

---

## Команды проекта

Все команды доступны через `just`:

| Команда | Описание |
|---|---|
| `just server` | Запуск dev-сервера с автоперезагрузкой |
| `just test` | Запуск тестов |
| `just lint` | Проверка кода (ruff) |
| `just fmt` | Форматирование кода (ruff) |
| `just fix` | Авто-исправление + форматирование |
| `just hooks` | Установка pre-commit хуков |

---

## Структура проекта

```
app/
├── main.py              # точка входа FastAPI
├── settings.py          # конфигурация через pydantic-settings
├── dependencies.py      # провайдеры зависимостей для Depends()
├── prompt_loader.py     # загрузка промпта из файла
├── routes/
│   └── chat.py          # роутер с эндпоинтами
├── schemas/
│   └── chat.py          # Pydantic модели запроса и ответа
└── clients/
    └── llm.py           # LLMClient с retry логикой

prompts/
└── system.md            # system prompt для LLM

tests/
└── test_question.py     # тесты API
```

---

## Смена LLM провайдера

Просто поменяй значения в `.env` — код менять не нужно.

**OpenAI:**
```env
LLM_HOST=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=sk-...
```

**OpenRouter:**
```env
LLM_HOST=https://openrouter.ai/api/v1
LLM_MODEL=deepseek/deepseek-r1
LLM_API_KEY=sk-or-...
```

**Ollama (локально):**
```env
LLM_HOST=http://localhost:11434/v1
LLM_MODEL=llama3
LLM_API_KEY=ollama
```

---

## Редактирование промпта

Системный промпт живёт в [prompts/system.md](prompts/system.md) — обычный markdown.
Редактируй его без перезапуска сервера только в dev-режиме (из-за `lru_cache`
нужен рестарт).

Можно указать другой файл через `PROMPT_PATH` в `.env`.
