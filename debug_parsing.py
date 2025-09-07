#!/usr/bin/env python3
"""
Отладка парсинга ответа модели
"""

import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Добавляем путь к src
sys.path.append(str(Path(__file__).parent / "src"))

# Принудительно загружаем .env
load_dotenv(override=True)

from src.agents.vkr_topic_agent import VKRTopicAgent
from src.models import EducationLevel


async def debug_parsing():
    """Отладка парсинга"""
    print("🔍 ОТЛАДКА ПАРСИНГА ОТВЕТА МОДЕЛИ")
    print("=" * 50)
    
    agent = VKRTopicAgent()
    
    # Создаем простой промпт для генерации тем
    field = "Информатика"
    level = EducationLevel.BACHELOR
    count = 1
    
    prompt = f"""Сгенерируй {count} тему для выпускной квалификационной работы по направлению "{field}" для уровня "{level.value}".

Требования:
- Тема должна быть актуальной и интересной
- Подходящей для уровня {level.value}
- Связанной с направлением {field}

Формат ответа (JSON):
{{
  "topics": [
    {{
      "title": "Название темы",
      "description": "Краткое описание темы",
      "keywords": ["ключевое", "слово1", "слово2"],
      "difficulty": "Легкая/Средняя/Сложная"
    }}
  ]
}}

Ответ:"""
    
    print("Промпт:")
    print(prompt)
    print("\n" + "="*50)
    
    try:
        print("Отправляем запрос к модели...")
        response = await agent.llm.ainvoke(prompt)
        
        print(f"✅ Получен ответ от модели:")
        print(f"Длина ответа: {len(response.content)} символов")
        print(f"Ответ:\n{response.content}")
        
        # Пробуем парсить ответ
        print("\n" + "="*50)
        print("Попытка парсинга...")
        
        # Ищем JSON в ответе
        content = response.content
        
        # Ищем блок JSON
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            print(f"Найден JSON: {json_str}")
            
            import json
            try:
                data = json.loads(json_str)
                print(f"✅ JSON успешно распарсен!")
                print(f"Количество тем: {len(data.get('topics', []))}")
                
                for i, topic in enumerate(data.get('topics', []), 1):
                    print(f"\nТема {i}:")
                    print(f"  Заголовок: {topic.get('title', 'Нет')}")
                    print(f"  Описание: {topic.get('description', 'Нет')}")
                    print(f"  Ключевые слова: {topic.get('keywords', [])}")
                    print(f"  Сложность: {topic.get('difficulty', 'Нет')}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Ошибка парсинга JSON: {e}")
        else:
            print("❌ JSON не найден в ответе")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_parsing())
