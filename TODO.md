# Задачи по переделке проекта

---

## 1. app/settings.py

**Что сделать:**
- Удалить поле `llm_system_prompt`
- Добавить поле `prompt_path: str` — путь к файлу с промптом

**Результат:**
```python
prompt_path: str = Field(
    default="prompts/system.txt",
    description="Path to system prompt file",
)
```

**Для закрепления:** изучи `pathlib.Path` — понадобится в следующем шаге.
Попробуй в Python консоли:
```python
from pathlib import Path
text = Path("prompts/system.txt").read_text(encoding="utf-8")
print(text)
```

---

## 2. app/dependencies.py — создать с нуля

**Что сделать:**
- Функция `get_settings()` с декоратором `@lru_cache` — возвращает `Settings()`
- Функция `get_llm_client()` — читает файл промпта через `Path`, создаёт и возвращает `LLMClient`

**Что изучить:**
- `@lru_cache` — https://docs.python.org/3/library/functools.html#functools.lru_cache
- `Depends()` в FastAPI — https://fastapi.tiangolo.com/tutorial/dependencies/

**Задача для закрепления:** напиши простой пример — функция `get_db()` которая
возвращает словарь, и хендлер который получает его через `Depends(get_db)`.
Убедись что понимаешь когда `get_db` вызывается.

---

## 3. app/routes/chat.py — создать с нуля

**Что сделать:**
- Создать `APIRouter`
- Перенести эндпоинты `GET /` и `POST /question` из `main.py`
- Хендлер `POST /question` получает `LLMClient` через `Depends(get_llm_client)`
- Вызывает `llm.ask(body.text)` вместо `ask_llm(body.text)`

**Что изучить:**
- Bigger Applications — https://fastapi.tiangolo.com/tutorial/bigger-applications/

**Задача для закрепления:** добавь второй роутер `app/routes/health.py`
с эндпоинтом `GET /health`. Подключи оба в `main.py`.

---

## 4. app/main.py — обновить

**Что сделать:**
- Убрать импорты `ask_llm`, `settings`, `HTTPException`
- Подключить роутер: `app.include_router(chat_router)`
- Оставить только: создание `app`, `exception_handler`, `include_router`

**Результат — main.py должен быть ~15 строк.**

---

## 5. tests/ — переписать на dependency_overrides

**Что сделать:**
- Создать `tests/conftest.py`
- В нём написать фикстуру которая подменяет `get_llm_client` через
  `app.dependency_overrides` на фейковый класс с методом `.ask()`
- Убрать все `@patch("app.main.ask_llm", ...)` из тестов
- Обновить тесты — теперь они используют фикстуру из conftest

**Что изучить:**
- Testing dependencies — https://fastapi.tiangolo.com/advanced/testing-dependencies/
- pytest fixtures — https://docs.pytest.org/en/stable/how-to/fixtures.html

**Пример фейкового клиента:**
```python
class FakeLLMClient:
    async def ask(self, question: str) -> str:
        return "fake answer"
```

**Задача для закрепления:** добавь фикстуру которая возвращает разные ответы
в зависимости от вопроса — для теста edge-cases.

---

## Порядок выполнения

```
settings.py → dependencies.py → routes/chat.py → main.py → tests/
```

Каждый шаг зависит от предыдущего — иди строго по порядку.

---

## Полезные материалы

| Тема | Ссылка |
|---|---|
| FastAPI туториал (основа) | https://fastapi.tiangolo.com/tutorial/ |
| Depends и DI | https://fastapi.tiangolo.com/tutorial/dependencies/ |
| Bigger Applications (роутеры) | https://fastapi.tiangolo.com/tutorial/bigger-applications/ |
| Testing dependencies | https://fastapi.tiangolo.com/advanced/testing-dependencies/ |
| lru_cache | https://docs.python.org/3/library/functools.html#functools.lru_cache |
| pytest fixtures | https://docs.pytest.org/en/stable/how-to/fixtures.html |
| ArjanCodes (YouTube) | поиск: "ArjanCodes dependency injection python" |

---
---

# Мини-проект: Historical Character Chat API

## Суть

API для чата с историческими персонажами. Пользователь выбирает персонажа
и задаёт вопросы — бот отвечает от первого лица, в роли этого человека.

## Эндпоинты

```
POST /chat/{character}   — отправить сообщение персонажу
GET  /characters         — список доступных персонажей
```

Пример запроса:
```json
POST /chat/napoleon
{"text": "Расскажи о своих главных ошибках"}
```

Пример ответа:
```json
{"character": "napoleon", "text": "Поход на Москву в 1812 году..."}
```

## Требования

**Персонажи:**
- Минимум 3 персонажа на выбор (например: napoleon, caesar, turing)
- Каждый персонаж — отдельный файл промпта `prompts/{character}.txt`
- Если персонаж не найден — возвращать HTTP 404

**Валидация:**
- `text` — обязательное поле, min 1, max 1000 символов
- `character` в URL — только из списка допустимых (используй Enum)

**История диалога:**
- В рамках одного запроса персонаж должен помнить контекст разговора
- Реализуй через передачу `messages` списка в LLM

**Архитектура — обязательные требования:**
- `app/routes/chat.py` — роутер с эндпоинтами
- `app/schemas/chat.py` — Pydantic модели запроса и ответа
- `app/clients/llm.py` — LLM клиент (можно взять из текущего проекта)
- `app/characters.py` — реестр персонажей (Enum + словарь с путями к промптам)
- `app/dependencies.py` — провайдеры через Depends
- `prompts/napoleon.txt` и т.д. — промпты для каждого персонажа

**Тесты:**
- Тест успешного запроса к существующему персонажу
- Тест 404 для несуществующего персонажа
- Тест валидации пустого текста
- Используй `dependency_overrides` — без `@patch`

## Промпты для персонажей

Каждый промпт должен содержать:
- Кто ты (роль, эпоха, контекст)
- Как говоришь (стиль речи, манера)
- Что знаешь и чего не знаешь (персонаж не знает о событиях после своей смерти)
- Ограничения (не выходи из роли)

Пример структуры `prompts/napoleon.txt`:
```
You are Napoleon Bonaparte, Emperor of France (1769-1821).
You speak with authority and confidence. You refer to yourself
in third person occasionally. You are proud of your military
campaigns but reflective about your mistakes...
```

## Что закрепишь

- Path параметры в URL (`{character}`)
- Enum для валидации допустимых значений
- Управление историей сообщений (messages list для LLM)
- Несколько промптов под разные сущности
- Dependency injection через Depends
- Тесты с dependency_overrides
- HTTPException с разными статус-кодами

## Правила

1. Пиши сам — ИИ только для вопросов когда застрял
2. Не подсматривай в текущий RAGStudyBot проект пока не застрял
3. Начни с самого простого — один эндпоинт, один персонаж, без истории
4. Добавляй сложность постепенно

## Порядок работы

```
1. Создай проект (uv init)
2. Напиши схемы (schemas/chat.py)
3. Создай один промпт (prompts/napoleon.txt)
4. Напиши LLM клиент
5. Сделай один рабочий эндпоинт POST /chat/{character}
6. Добавь GET /characters
7. Добавь валидацию через Enum
8. Напиши тесты
```
