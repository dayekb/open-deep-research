#!/usr/bin/env python3
"""
Скрипт для обновления API ключа OpenRouter
"""

import os
from dotenv import load_dotenv, set_key

def update_api_key():
    """Обновление API ключа"""
    print("🔑 ОБНОВЛЕНИЕ API КЛЮЧА OPENROUTER")
    print("=" * 50)
    
    # Загружаем текущий .env
    load_dotenv()
    current_key = os.getenv("OPENROUTER_API_KEY")
    
    if current_key:
        print(f"Текущий ключ: {current_key[:20]}...")
    else:
        print("Текущий ключ: НЕ НАЙДЕН")
    
    print("\nВведите новый API ключ OpenRouter:")
    print("(или нажмите Enter для пропуска)")
    
    new_key = input("Новый ключ: ").strip()
    
    if not new_key:
        print("❌ Ключ не введен")
        return False
    
    if not new_key.startswith("sk-or-v1-"):
        print("⚠️  Ключ не похож на OpenRouter API ключ")
        print("   Обычно ключи начинаются с 'sk-or-v1-'")
        confirm = input("Продолжить? (y/N): ").strip().lower()
        if confirm != 'y':
            return False
    
    try:
        # Обновляем .env файл
        set_key('.env', 'OPENROUTER_API_KEY', new_key)
        print(f"✅ Ключ обновлен: {new_key[:20]}...")
        
        # Тестируем новый ключ
        print("\n🧪 Тестирование нового ключа...")
        test_new_key(new_key)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления: {e}")
        return False

def test_new_key(api_key):
    """Тестирование нового ключа"""
    import requests
    
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
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ Ключ работает! Ответ: {content}")
            return True
        else:
            print(f"❌ Ключ не работает: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = update_api_key()
    
    if success:
        print("\n🎉 API ключ успешно обновлен!")
        print("Теперь можете запустить сервис:")
        print("  conda run python run_openrouter.py")
    else:
        print("\n❌ Обновление не удалось")
        print("Проверьте правильность ключа и попробуйте снова")
