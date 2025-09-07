#!/usr/bin/env python3
"""
Тест нового API ключа
"""

import requests
import os
from dotenv import load_dotenv

def test_new_key():
    """Тест нового ключа"""
    print("🔑 ТЕСТ НОВОГО API КЛЮЧА")
    print("=" * 40)
    
    # Принудительно загружаем .env
    load_dotenv(override=True)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"Загруженный ключ: {api_key[:20]}...")
    
    if not api_key:
        print("❌ Ключ не найден")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Простой тест
    data = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [{"role": "user", "content": "Hi! Reply 'OK'"}],
        "max_tokens": 5
    }
    
    try:
        print("🧪 Тестируем API...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ УСПЕХ! Ответ: {content}")
            return True
        else:
            print(f"❌ Ошибка: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

if __name__ == "__main__":
    success = test_new_key()
    
    if success:
        print("\n🎉 API ключ работает!")
        print("Можете запускать сервис:")
        print("  conda run python run_openrouter.py")
    else:
        print("\n❌ API ключ не работает")
        print("Проверьте правильность ключа на https://openrouter.ai/")
