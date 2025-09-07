# Руководство по тестированию сервиса генерации тем ВКР

## Обзор тестирования

Сервис включает комплексную систему тестирования, покрывающую все компоненты от unit-тестов до интеграционных тестов и тестов производительности.

## Структура тестов

```
tests/
├── conftest.py              # Конфигурация pytest
├── test_models.py           # Тесты моделей данных
├── test_agents.py           # Тесты агентов генерации
├── test_database.py         # Тесты базы данных
├── test_api.py              # Тесты API эндпоинтов
├── test_integration.py      # Интеграционные тесты
├── test_performance.py      # Тесты производительности
├── run_tests.py             # Скрипт запуска всех тестов
└── manual_test.py           # Ручное тестирование API
```

## Типы тестов

### 1. Unit тесты

Тестируют отдельные компоненты в изоляции:

- **test_models.py** - Валидация моделей данных
- **test_agents.py** - Логика агентов генерации
- **test_database.py** - Операции с базой данных

### 2. Интеграционные тесты

Тестируют взаимодействие между компонентами:

- **test_api.py** - API эндпоинты
- **test_integration.py** - Полные потоки данных

### 3. Тесты производительности

Проверяют скорость и масштабируемость:

- **test_performance.py** - Время выполнения, память, нагрузка

## Запуск тестов

### Автоматический запуск всех тестов

```bash
# Запуск всех тестов
python tests/run_tests.py

# Или напрямую через pytest
python -m pytest tests/ -v
```

### Запуск отдельных групп тестов

```bash
# Только unit тесты
python -m pytest tests/test_models.py tests/test_agents.py tests/test_database.py -v

# Только API тесты
python -m pytest tests/test_api.py -v

# Только тесты производительности
python -m pytest tests/test_performance.py -v -s

# Только интеграционные тесты
python -m pytest tests/test_integration.py -v
```

### Запуск с покрытием кода

```bash
# Установка pytest-cov
pip install pytest-cov

# Запуск с покрытием
python -m pytest tests/ --cov=src --cov-report=html

# Просмотр отчета
open htmlcov/index.html
```

## Ручное тестирование

### Запуск сервера для тестирования

```bash
# Запуск сервера
python main.py

# В другом терминале - запуск тестов
python tests/manual_test.py
```

### Интерактивное тестирование API

```bash
# Базовое тестирование
python tests/manual_test.py

# С параметрами
python tests/manual_test.py --url http://localhost:8000 --field "Экономика" --count 5

# Тестирование удаленного сервера
python tests/manual_test.py --url https://your-api.com
```

### Тестирование через curl

```bash
# Проверка здоровья
curl http://localhost:8000/health

# Генерация тем
curl -X POST "http://localhost:8000/generate-topics" \
  -H "Content-Type: application/json" \
  -d '{"field": "Информатика", "count": 3, "level": "Бакалавриат"}'

# Поиск тем
curl "http://localhost:8000/topics?query=машинное%20обучение&limit=5"

# Статистика
curl http://localhost:8000/stats
```

## Настройка тестового окружения

### 1. Установка зависимостей для тестирования

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### 2. Настройка переменных окружения

```bash
# Создание тестового .env файла
cp env.example .env.test

# Редактирование настроек для тестов
nano .env.test
```

Тестовые настройки:
```env
# Тестовая база данных
DATABASE_URL=sqlite:///:memory:

# Тестовые API ключи (можно использовать моки)
OPENAI_API_KEY=test_key
ANTHROPIC_API_KEY=test_key
TAVILY_API_KEY=test_key

# Отключение трассировки для тестов
LANGCHAIN_TRACING_V2=false
```

### 3. Запуск тестов с тестовой конфигурацией

```bash
# Установка переменной окружения
export TESTING=true

# Запуск тестов
python -m pytest tests/ -v
```

## Примеры тестов

### Тест генерации тем

```python
def test_generate_topics():
    """Тест генерации тем"""
    agent = VKRTopicAgent()
    
    topics = await agent.generate_topics_simple(
        field="Информатика",
        count=3,
        level=EducationLevel.BACHELOR
    )
    
    assert len(topics) == 3
    assert all(topic.field == "Информатика" for topic in topics)
    assert all(topic.level == EducationLevel.BACHELOR for topic in topics)
```

### Тест API эндпоинта

```python
def test_generate_topics_api(test_client):
    """Тест API генерации тем"""
    request_data = {
        "field": "Информатика",
        "count": 2,
        "level": "Бакалавриат"
    }
    
    response = test_client.post("/generate-topics", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert len(data["topics"]) == 2
```

### Тест производительности

```python
def test_generation_speed():
    """Тест скорости генерации"""
    start_time = time.time()
    
    topics = await agent.generate_topics_simple(
        field="Информатика",
        count=5
    )
    
    end_time = time.time()
    generation_time = end_time - start_time
    
    assert generation_time < 10.0  # Менее 10 секунд
    assert len(topics) == 5
```

## Отладка тестов

### Включение подробного вывода

```bash
# Подробный вывод
python -m pytest tests/ -v -s

# Очень подробный вывод
python -m pytest tests/ -vv -s

# Остановка на первой ошибке
python -m pytest tests/ -x
```

### Запуск конкретного теста

```bash
# Запуск конкретного теста
python -m pytest tests/test_models.py::TestVKRTopic::test_valid_topic_creation -v

# Запуск тестов по паттерну
python -m pytest tests/ -k "test_generate" -v
```

### Отладка с pdb

```python
import pdb; pdb.set_trace()  # Вставить в тест для отладки
```

```bash
# Запуск с отладчиком
python -m pytest tests/ --pdb
```

## Непрерывная интеграция

### GitHub Actions

Создайте `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

### Pre-commit хуки

```bash
# Установка pre-commit
pip install pre-commit

# Создание .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: python -m pytest tests/ -v
        language: system
        pass_filenames: false
        always_run: true
EOF

# Установка хуков
pre-commit install
```

## Мониторинг тестов

### Отчеты о покрытии

```bash
# Генерация HTML отчета
python -m pytest tests/ --cov=src --cov-report=html

# Генерация XML отчета
python -m pytest tests/ --cov=src --cov-report=xml

# Просмотр покрытия в консоли
python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Метрики производительности

```bash
# Запуск тестов производительности с профилированием
python -m pytest tests/test_performance.py -v -s --durations=10
```

## Лучшие практики

### 1. Структура тестов

- Один тест = одна проверка
- Понятные имена тестов
- Использование фикстур для подготовки данных
- Очистка после тестов

### 2. Моки и заглушки

- Мокайте внешние зависимости
- Используйте реальные данные для интеграционных тестов
- Проверяйте взаимодействие с моками

### 3. Тестовые данные

- Используйте фабрики для создания тестовых данных
- Избегайте хардкода в тестах
- Создавайте реалистичные тестовые сценарии

### 4. Асинхронные тесты

- Используйте `pytest.mark.asyncio`
- Правильно обрабатывайте исключения
- Тестируйте таймауты и отмены

## Устранение неполадок

### Частые проблемы

1. **Ошибки импорта**
   ```bash
   # Убедитесь, что PYTHONPATH настроен
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Ошибки базы данных**
   ```bash
   # Очистите тестовую базу
   rm -f test.db
   ```

3. **Ошибки API ключей**
   ```bash
   # Используйте тестовые ключи или моки
   export OPENAI_API_KEY=test_key
   ```

4. **Таймауты тестов**
   ```bash
   # Увеличьте таймаут
   python -m pytest tests/ --timeout=300
   ```

### Логирование

```python
# Включение логирования в тестах
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Заключение

Комплексная система тестирования обеспечивает:

- ✅ **Качество кода** - Unit тесты проверяют корректность компонентов
- ✅ **Интеграцию** - Интеграционные тесты проверяют взаимодействие
- ✅ **Производительность** - Тесты производительности выявляют узкие места
- ✅ **Надежность** - Автоматизированное тестирование предотвращает регрессии

Регулярное выполнение тестов гарантирует стабильную работу сервиса генерации тем ВКР.
