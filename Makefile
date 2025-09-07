# Makefile для сервиса генерации тем ВКР

.PHONY: help install test test-quick test-unit test-api test-perf test-integration test-manual clean run dev

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Показать справку
	@echo "$(GREEN)Сервис генерации тем ВКР$(NC)"
	@echo "========================"
	@echo ""
	@echo "$(YELLOW)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "$(YELLOW)Установка зависимостей...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Зависимости установлены$(NC)"

install-dev: ## Установить зависимости для разработки
	@echo "$(YELLOW)Установка зависимостей для разработки...$(NC)"
	pip install -r requirements.txt
	pip install pytest pytest-cov pytest-asyncio httpx
	@echo "$(GREEN)✅ Зависимости для разработки установлены$(NC)"

test: ## Запустить все тесты
	@echo "$(YELLOW)Запуск всех тестов...$(NC)"
	python tests/run_tests.py

test-quick: ## Быстрое тестирование
	@echo "$(YELLOW)Быстрое тестирование...$(NC)"
	python test_quick.py

test-unit: ## Unit тесты
	@echo "$(YELLOW)Запуск unit тестов...$(NC)"
	python -m pytest tests/test_models.py tests/test_agents.py tests/test_database.py -v

test-api: ## Тесты API
	@echo "$(YELLOW)Запуск тестов API...$(NC)"
	python -m pytest tests/test_api.py -v

test-perf: ## Тесты производительности
	@echo "$(YELLOW)Запуск тестов производительности...$(NC)"
	python -m pytest tests/test_performance.py -v -s

test-integration: ## Интеграционные тесты
	@echo "$(YELLOW)Запуск интеграционных тестов...$(NC)"
	python -m pytest tests/test_integration.py -v

test-manual: ## Ручное тестирование API
	@echo "$(YELLOW)Ручное тестирование API...$(NC)"
	python tests/manual_test.py

test-coverage: ## Тесты с покрытием кода
	@echo "$(YELLOW)Запуск тестов с покрытием кода...$(NC)"
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)Отчет о покрытии: htmlcov/index.html$(NC)"

test-watch: ## Тесты в режиме наблюдения
	@echo "$(YELLOW)Запуск тестов в режиме наблюдения...$(NC)"
	python -m pytest tests/ -f -v

run: ## Запустить сервер
	@echo "$(YELLOW)Запуск сервера...$(NC)"
	python main.py

dev: ## Запустить сервер в режиме разработки
	@echo "$(YELLOW)Запуск сервера в режиме разработки...$(NC)"
	python -m uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

lint: ## Проверка кода линтером
	@echo "$(YELLOW)Проверка кода...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src tests --max-line-length=100 --ignore=E203,W503; \
	else \
		echo "$(RED)flake8 не установлен. Установите: pip install flake8$(NC)"; \
	fi

format: ## Форматирование кода
	@echo "$(YELLOW)Форматирование кода...$(NC)"
	@if command -v black >/dev/null 2>&1; then \
		black src tests --line-length=100; \
	else \
		echo "$(RED)black не установлен. Установите: pip install black$(NC)"; \
	fi

clean: ## Очистка временных файлов
	@echo "$(YELLOW)Очистка временных файлов...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -f .coverage
	rm -f coverage.xml
	rm -f test.db
	@echo "$(GREEN)✅ Очистка завершена$(NC)"

setup: install-dev ## Настройка проекта для разработки
	@echo "$(YELLOW)Настройка проекта...$(NC)"
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "$(GREEN)✅ Создан файл .env$(NC)"; \
	fi
	@echo "$(GREEN)✅ Проект настроен для разработки$(NC)"
	@echo "$(YELLOW)Не забудьте настроить API ключи в .env файле$(NC)"

check: test-quick lint ## Быстрая проверка проекта
	@echo "$(GREEN)✅ Быстрая проверка завершена$(NC)"

ci: install-dev test-coverage lint ## Проверка для CI/CD
	@echo "$(GREEN)✅ Проверка CI/CD завершена$(NC)"

docker-build: ## Сборка Docker образа
	@echo "$(YELLOW)Сборка Docker образа...$(NC)"
	docker build -t vkr-topic-generator .

docker-run: ## Запуск в Docker
	@echo "$(YELLOW)Запуск в Docker...$(NC)"
	docker run -p 8000:8000 --env-file .env vkr-topic-generator

docs: ## Генерация документации
	@echo "$(YELLOW)Генерация документации...$(NC)"
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs build; \
		echo "$(GREEN)Документация: site/index.html$(NC)"; \
	else \
		echo "$(RED)mkdocs не установлен. Установите: pip install mkdocs$(NC)"; \
	fi

docs-serve: ## Запуск локального сервера документации
	@echo "$(YELLOW)Запуск сервера документации...$(NC)"
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs serve; \
	else \
		echo "$(RED)mkdocs не установлен. Установите: pip install mkdocs$(NC)"; \
	fi

# Специальные команды для тестирования
test-models: ## Тесты только моделей
	python -m pytest tests/test_models.py -v

test-agents: ## Тесты только агентов
	python -m pytest tests/test_agents.py -v

test-db: ## Тесты только базы данных
	python -m pytest tests/test_database.py -v

# Команды для отладки
debug-test: ## Запуск тестов с отладкой
	python -m pytest tests/ -v -s --pdb

test-failed: ## Запуск только неудачных тестов
	python -m pytest tests/ --lf -v

test-slow: ## Запуск медленных тестов
	python -m pytest tests/test_performance.py -v -s -m "slow"

# Команды для мониторинга
monitor: ## Мониторинг сервера
	@echo "$(YELLOW)Мониторинг сервера...$(NC)"
	@echo "Откройте в браузере:"
	@echo "  - API: http://localhost:8000/docs"
	@echo "  - Health: http://localhost:8000/health"
	@echo "  - Stats: http://localhost:8000/stats"
	@echo ""
	@echo "Нажмите Ctrl+C для остановки"
	@while true; do \
		curl -s http://localhost:8000/health > /dev/null && echo "$(GREEN)✅ Сервер работает$(NC)" || echo "$(RED)❌ Сервер недоступен$(NC)"; \
		sleep 5; \
	done
