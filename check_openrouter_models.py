#!/usr/bin/env python3
"""
Проверка доступных моделей OpenRouter
"""

import requests
import json
import os

def check_available_models():
    """Проверка доступных моделей"""
    print("🔍 Проверка доступных моделей OpenRouter...")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers)
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Найдено {len(models.get('data', []))} моделей")
            
            # Фильтруем бесплатные модели
            free_models = []
            llama_models = []
            
            for model in models.get('data', []):
                model_id = model.get('id', '')
                name = model.get('name', '')
                pricing = model.get('pricing', {})
                
                # Проверяем бесплатные модели
                if pricing.get('prompt') == '0' and pricing.get('completion') == '0':
                    free_models.append({
                        'id': model_id,
                        'name': name,
                        'context_length': model.get('context_length', 0)
                    })
                
                # Ищем модели Llama
                if 'llama' in model_id.lower() or 'llama' in name.lower():
                    llama_models.append({
                        'id': model_id,
                        'name': name,
                        'context_length': model.get('context_length', 0),
                        'pricing': pricing
                    })
            
            print(f"\n🆓 Бесплатные модели ({len(free_models)}):")
            for model in free_models[:10]:  # Показываем первые 10
                print(f"   • {model['id']}")
                print(f"     Название: {model['name']}")
                print(f"     Контекст: {model['context_length']} токенов")
                print()
            
            print(f"\n🦙 Модели Llama ({len(llama_models)}):")
            for model in llama_models[:10]:  # Показываем первые 10
                print(f"   • {model['id']}")
                print(f"     Название: {model['name']}")
                print(f"     Контекст: {model['context_length']} токенов")
                print(f"     Цена: {model['pricing']}")
                print()
            
            # Рекомендуем лучшие бесплатные модели
            print("\n💡 Рекомендуемые бесплатные модели:")
            recommended = [
                "meta-llama/llama-3.2-3b-instruct:free",
                "meta-llama/llama-3.2-1b-instruct:free", 
                "microsoft/phi-3-mini-128k-instruct:free",
                "google/gemma-2-2b-it:free",
                "mistralai/mistral-7b-instruct:free"
            ]
            
            for rec in recommended:
                if any(rec in model['id'] for model in free_models):
                    print(f"   ✅ {rec}")
                else:
                    print(f"   ❌ {rec} (не найдена)")
            
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_model(model_id):
    """Тестирование конкретной модели"""
    print(f"\n🧪 Тестирование модели: {model_id}")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": "Привет! Это тест. Ответь коротко."}
        ],
        "max_tokens": 50
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
            print(f"✅ Модель работает!")
            print(f"   Ответ: {content}")
            return True
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция"""
    print("🔍 ПРОВЕРКА МОДЕЛЕЙ OPENROUTER")
    print("=" * 50)
    
    # Проверяем доступные модели
    check_available_models()
    
    # Тестируем рекомендуемую модель
    test_model_id = "meta-llama/llama-3.2-3b-instruct:free"
    print(f"\n🧪 Тестирование рекомендуемой модели...")
    if test_model(test_model_id):
        print(f"\n✅ Модель {test_model_id} работает!")
        print("Можете использовать её в настройках.")
    else:
        print(f"\n❌ Модель {test_model_id} не работает.")
        print("Попробуйте другую модель из списка выше.")

if __name__ == "__main__":
    main()
