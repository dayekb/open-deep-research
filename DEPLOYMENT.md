# Руководство по развертыванию сервиса генерации тем ВКР

## Быстрый старт

### 1. Установка зависимостей

```bash
# Клонирование репозитория
git clone <your-repo-url>
cd vkr-topic-generator

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка окружения

```bash
# Копирование файла конфигурации
cp env.example .env

# Редактирование настроек
nano .env
```

Обязательно настройте следующие переменные в `.env`:

```env
# API ключи (обязательно)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# LangSmith (опционально, для мониторинга)
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
```

### 3. Запуск сервиса

```bash
# Запуск сервера
python main.py
```

Сервис будет доступен по адресу: http://localhost:8000

## Конфигурация

### Модели ИИ

Сервис поддерживает различные языковые модели:

- **OpenAI**: `openai:gpt-4.1`, `openai:gpt-4.1-mini`, `openai:gpt-5`
- **Anthropic**: `anthropic:claude-sonnet-4`, `anthropic:claude-haiku`
- **Ollama**: `ollama:llama3`, `ollama:mistral` (для локального использования)

Настройка в `.env`:
```env
DEFAULT_MODEL=openai:gpt-4.1
```

### Поисковые API

- **Tavily** (по умолчанию): Требует API ключ
- **Google**: Настройка через переменные окружения
- **Bing**: Настройка через переменные окружения

### База данных

По умолчанию используется SQLite. Для продакшена рекомендуется PostgreSQL:

```env
# SQLite (разработка)
DATABASE_URL=sqlite:///./vkr_topics.db

# PostgreSQL (продакшен)
DATABASE_URL=postgresql://user:password@localhost/vkr_topics
```

## Развертывание в продакшене

### Docker

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

Создайте `docker-compose.yml`:

```yaml
version: '3.8'

services:
  vkr-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/vkr_topics
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=vkr_topics
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Запуск:
```bash
docker-compose up -d
```

### Облачные платформы

#### Heroku

1. Создайте `Procfile`:
```
web: python main.py
```

2. Настройте переменные окружения в панели Heroku

3. Разверните:
```bash
git push heroku main
```

#### Railway

1. Подключите GitHub репозиторий
2. Настройте переменные окружения
3. Railway автоматически развернет сервис

#### Google Cloud Run

1. Создайте `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/vkr-service', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/vkr-service']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'vkr-service', '--image', 'gcr.io/$PROJECT_ID/vkr-service', '--platform', 'managed', '--region', 'us-central1']
```

2. Разверните:
```bash
gcloud builds submit
```

## Мониторинг и логирование

### LangSmith

Для мониторинга работы с языковыми моделями:

```env
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=vkr-topic-generator
```

### Логирование

Сервис использует Loguru для логирования. Настройка в коде:

```python
from loguru import logger

# Логи будут выводиться в консоль и файл
logger.add("logs/vkr_service.log", rotation="1 day", retention="30 days")
```

## Масштабирование

### Горизонтальное масштабирование

1. Используйте балансировщик нагрузки (nginx, HAProxy)
2. Настройте общую базу данных (PostgreSQL)
3. Используйте Redis для кеширования

### Вертикальное масштабирование

1. Увеличьте количество воркеров uvicorn:
```bash
uvicorn src.api.server:app --workers 4
```

2. Настройте лимиты памяти и CPU в Docker/Kubernetes

## Безопасность

### API ключи

- Никогда не коммитьте `.env` файлы
- Используйте секреты в облачных платформах
- Регулярно ротируйте API ключи

### CORS

Настройте CORS для продакшена:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Rate Limiting

Добавьте ограничения на количество запросов:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/generate-topics")
@limiter.limit("10/minute")
async def generate_topics(request: Request, ...):
    ...
```

## Резервное копирование

### База данных

```bash
# PostgreSQL
pg_dump vkr_topics > backup.sql

# Восстановление
psql vkr_topics < backup.sql
```

### Автоматическое резервное копирование

Создайте cron задачу:

```bash
# Ежедневное резервное копирование в 2:00
0 2 * * * pg_dump vkr_topics | gzip > /backups/vkr_topics_$(date +\%Y\%m\%d).sql.gz
```

## Обновление

1. Остановите сервис
2. Создайте резервную копию базы данных
3. Обновите код
4. Запустите миграции (если есть)
5. Перезапустите сервис

```bash
# Остановка
docker-compose down

# Обновление кода
git pull origin main

# Запуск
docker-compose up -d
```
