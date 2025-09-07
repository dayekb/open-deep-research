#!/usr/bin/env python3
"""
Простой тест API ключа OpenRouter
"""

import requests
import os
from dotenv import load_dotenv

def test_api_key():
    """Тестирование API ключа"""
    print("🔑 ТЕСТИРОВАНИЕ API КЛЮЧА OPENROUTER")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в .env файле")
        return False
    
    print(f"✅ API ключ найден: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Тест 1: Получение списка моделей
    print("\n📋 Тест 1: Получение списка моделей...")
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Список моделей получен: {len(models.get('data', []))} моделей")
        else:
            print(f"❌ Ошибка получения моделей: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Тест 2: Простой запрос к модели
    print("\n💬 Тест 2: Простой запрос к модели...")
    
    # Пробуем разные модели
    test_models = [
        "deepseek/deepseek-chat-v3.1:free",
        "meta-llama/llama-3.3-8b-instruct:free",
        "openai/gpt-oss-20b:free",
        "mistralai/mistral-7b-instruct:free"
    ]
    
    for model in test_models:
        print(f"\n   Тестируем модель: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Привет! Ответь коротко: 'Тест прошел успешно'"}
            ],
            "max_tokens": 20
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"   ✅ Модель {model} работает!")
                print(f"   📝 Ответ: {content}")
                return True
            else:
                print(f"   ❌ Ошибка {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    print("\n❌ Ни одна модель не работает")
    return False

def test_with_curl():
    """Тест с помощью curl команды"""
    print("\n🌐 Тест с помощью curl...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ API ключ не найден")
        return
    
    curl_command = f'''curl -X POST "https://openrouter.ai/api/v1/chat/completions" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{"model": "deepseek/deepseek-chat-v3.1:free", "messages": [{{"role": "user", "content": "Привет!"}}], "max_tokens": 10}}' '''
    
    print("Выполните эту команду в терминале:")
    print(curl_command)

if __name__ == "__main__":
    success = test_api_key()
    
    if not success:
        print("\n🔧 РЕКОМЕНДАЦИИ:")
        print("1. Проверьте правильность API ключа на https://openrouter.ai/")
        print("2. Убедитесь, что у вас есть кредиты на аккаунте")
        print("3. Попробуйте создать новый API ключ")
        print("4. Проверьте, что ключ имеет права на использование моделей")
        
        test_with_curl()
    else:
        print("\n🎉 API ключ работает! Можете использовать сервис.")
