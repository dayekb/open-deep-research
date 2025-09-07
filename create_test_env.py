#!/usr/bin/env python3
"""
Создание тестового .env файла
"""

def create_test_env():
    """Создание тестового .env файла"""
    print("🔧 СОЗДАНИЕ ТЕСТОВОГО .ENV ФАЙЛА")
    print("=" * 40)
    
    # Содержимое .env файла
    env_content = """# API ключи для языковых моделей
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENROUTER_API_KEY=ЗАМЕНИТЕ_НА_ВАШ_КЛЮЧ

# Поисковые API
TAVILY_API_KEY=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

# LangSmith для мониторинга
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=vkr-topic-generator

# Настройки базы данных
DATABASE_URL=sqlite:///./vkr_topics.db

# Настройки сервера
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Настройки генерации тем
DEFAULT_MODEL=openrouter:deepseek/deepseek-chat-v3.1:free
DEFAULT_SEARCH_API=tavily
MAX_TOPICS_PER_REQUEST=10
DEFAULT_TOPICS_COUNT=5
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Тестовый .env файл создан!")
        print("\n📝 ИНСТРУКЦИИ:")
        print("1. Откройте файл .env в редакторе")
        print("2. Замените 'ЗАМЕНИТЕ_НА_ВАШ_КЛЮЧ' на ваш настоящий API ключ")
        print("3. Сохраните файл")
        print("4. Запустите: conda run python test_direct_api.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    create_test_env()
