#!/usr/bin/env python3
"""
Прямой тест API OpenRouter
"""

import requests
import json
import os
from dotenv import load_dotenv

def test_direct_api():
    """Прямой тест API"""
    print("🔍 ПРЯМОЙ ТЕСТ API OPENROUTER")
    print("=" * 50)
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ API ключ не найден")
        return
    
    print(f"✅ API ключ: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Пробуем разные модели
    models_to_test = [
        "deepseek/deepseek-chat-v3.1:free",
        "meta-llama/llama-3.3-8b-instruct:free", 
        "openai/gpt-oss-20b:free",
        "mistralai/mistral-7b-instruct:free",
        "google/gemma-3n-e2b-it:free"
    ]
    
    for model in models_to_test:
        print(f"\n🧪 Тестируем модель: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Hi! Reply with just 'OK'"}
            ],
            "max_tokens": 5
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"   Статус: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"   ✅ УСПЕХ! Ответ: {content}")
                return True
            else:
                print(f"   ❌ Ошибка: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
    
    print("\n❌ Все модели не работают")
    return False

def check_account_info():
    """Проверка информации об аккаунте"""
    print("\n👤 ПРОВЕРКА АККАУНТА")
    print("=" * 30)
    
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Пробуем получить информацию об аккаунте
        response = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers)
        print(f"Статус проверки ключа: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Ключ валиден")
            print(f"Ответ: {response.text}")
        else:
            print(f"❌ Ключ невалиден: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_account_info()
    success = test_direct_api()
    
    if not success:
        print("\n💡 ВОЗМОЖНЫЕ ПРИЧИНЫ:")
        print("1. API ключ неактивен или истек")
        print("2. У аккаунта нет кредитов")
        print("3. Ключ имеет ограниченные права")
        print("4. Модели недоступны для вашего региона")
        print("\n🔧 РЕШЕНИЯ:")
        print("1. Зайдите на https://openrouter.ai/ и проверьте статус аккаунта")
        print("2. Создайте новый API ключ")
        print("3. Добавьте кредиты на аккаунт")
        print("4. Попробуйте другую модель")
