# Скрипт для настройки Git репозитория (PowerShell)

Write-Host "🔧 Настройка Git репозитория для проекта генерации тем ВКР" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

# Инициализация Git репозитория
Write-Host "📁 Инициализация Git репозитория..." -ForegroundColor Yellow
git init

# Настройка конфигурации Git
Write-Host "⚙️ Настройка конфигурации Git..." -ForegroundColor Yellow
git config user.name "VKR Topic Generator"
git config user.email "vkr-generator@example.com"
git config core.autocrlf true
git config core.safecrlf true
git config pull.rebase false

# Настройка шаблона сообщений коммитов
Write-Host "📝 Настройка шаблона сообщений коммитов..." -ForegroundColor Yellow
git config commit.template .gitmessage

# Добавление файлов в индекс
Write-Host "📦 Добавление файлов в индекс..." -ForegroundColor Yellow
git add .

# Первый коммит
Write-Host "💾 Создание первого коммита..." -ForegroundColor Yellow
git commit -m "feat: initial commit - VKR topic generation service

- Add FastAPI server for topic generation
- Add LangChain integration with OpenRouter
- Add contextual generation with student preferences
- Add department context support
- Add database models and repository
- Add comprehensive testing suite
- Add documentation and examples
- Add Makefile for development commands"

Write-Host "✅ Git репозиторий настроен успешно!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Следующие шаги:" -ForegroundColor Cyan
Write-Host "1. Добавьте remote origin: git remote add origin <repository-url>" -ForegroundColor White
Write-Host "2. Отправьте код: git push -u origin main" -ForegroundColor White
Write-Host "3. Настройте CI/CD для автоматического тестирования" -ForegroundColor White
Write-Host "4. Создайте Issues и Projects для планирования задач" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Проект готов к работе!" -ForegroundColor Green
