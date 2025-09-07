#!/bin/bash
# Скрипт для настройки Git репозитория

echo "🔧 Настройка Git репозитория для проекта генерации тем ВКР"
echo "============================================================"

# Инициализация Git репозитория
echo "📁 Инициализация Git репозитория..."
git init

# Настройка конфигурации Git
echo "⚙️ Настройка конфигурации Git..."
git config user.name "VKR Topic Generator"
git config user.email "vkr-generator@example.com"
git config core.autocrlf true
git config core.safecrlf true
git config pull.rebase false

# Настройка шаблона сообщений коммитов
echo "📝 Настройка шаблона сообщений коммитов..."
git config commit.template .gitmessage

# Добавление файлов в индекс
echo "📦 Добавление файлов в индекс..."
git add .

# Первый коммит
echo "💾 Создание первого коммита..."
git commit -m "feat: initial commit - VKR topic generation service

- Add FastAPI server for topic generation
- Add LangChain integration with OpenRouter
- Add contextual generation with student preferences
- Add department context support
- Add database models and repository
- Add comprehensive testing suite
- Add documentation and examples
- Add Makefile for development commands"

echo "✅ Git репозиторий настроен успешно!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Добавьте remote origin: git remote add origin <repository-url>"
echo "2. Отправьте код: git push -u origin main"
echo "3. Настройте CI/CD для автоматического тестирования"
echo "4. Создайте Issues и Projects для планирования задач"
echo ""
echo "🎉 Проект готов к работе!"
