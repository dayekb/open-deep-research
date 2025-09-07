#!/usr/bin/env python3
"""
Пример контекстной генерации тем ВКР
"""

import requests
import json

def generate_personalized_topics():
    """Генерация персонализированных тем"""
    print("🎯 ПРИМЕР КОНТЕКСТНОЙ ГЕНЕРАЦИИ ТЕМ ВКР")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Пример 1: Студент-разработчик
    print("\n👨‍💻 Студент-разработчик (веб-технологии)")
    print("-" * 50)
    
    web_developer_request = {
        "field": "Информатика",
        "level": "Бакалавриат",
        "count": 2,
        "student_preferences": {
            "interests": ["веб-разработка", "пользовательский интерфейс"],
            "skills": ["JavaScript", "React", "Node.js", "MongoDB"],
            "career_goals": ["Full-stack Developer", "UI/UX Designer"],
            "preferred_technologies": ["React", "Vue.js", "Express", "MongoDB"],
            "work_style": "практический",
            "complexity_preference": "средняя"
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-topics",
            json=web_developer_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сгенерировано {len(data['topics'])} тем")
            
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n{i}. {topic['title']}")
                print(f"   Описание: {topic['description']}")
                print(f"   Технологии: {', '.join(topic['keywords'])}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
    
    # Пример 2: Студент-аналитик данных
    print("\n📊 Студент-аналитик данных")
    print("-" * 50)
    
    data_analyst_request = {
        "field": "Информатика",
        "level": "Магистратура",
        "count": 2,
        "student_preferences": {
            "interests": ["анализ данных", "машинное обучение", "статистика"],
            "skills": ["Python", "R", "SQL", "Pandas", "Scikit-learn"],
            "career_goals": ["Data Scientist", "Business Analyst"],
            "preferred_technologies": ["Python", "Jupyter", "TensorFlow", "PostgreSQL"],
            "work_style": "аналитический",
            "complexity_preference": "высокая"
        },
        "department_context": {
            "existing_topics": [
                "Анализ эффективности маркетинговых кампаний",
                "Прогнозирование продаж на основе исторических данных"
            ],
            "research_directions": ["Большие данные", "Искусственный интеллект"],
            "available_resources": ["GPU кластер", "База данных 1TB", "Статистическое ПО"]
        },
        "avoid_duplicates": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-topics",
            json=data_analyst_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сгенерировано {len(data['topics'])} тем")
            
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n{i}. {topic['title']}")
                print(f"   Описание: {topic['description']}")
                print(f"   Методология: {topic.get('methodology', 'Не указана')}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Исключение: {e}")
    
    # Пример 3: Студент-кибербезопасник
    print("\n🔒 Студент-кибербезопасник")
    print("-" * 50)
    
    cybersecurity_request = {
        "field": "Информатика",
        "level": "Бакалавриат",
        "count": 1,
        "student_preferences": {
            "interests": ["кибербезопасность", "этичный хакинг", "криптография"],
            "skills": ["Python", "C++", "Linux", "Wireshark", "Metasploit"],
            "career_goals": ["Penetration Tester", "Security Analyst"],
            "preferred_technologies": ["Kali Linux", "Burp Suite", "Nmap", "OWASP"],
            "work_style": "практический",
            "complexity_preference": "высокая"
        },
        "department_context": {
            "existing_topics": [
                "Анализ уязвимостей веб-приложений",
                "Разработка системы обнаружения вторжений"
            ],
            "research_directions": ["Кибербезопасность", "Криптография"],
            "available_resources": ["Лаборатория безопасности", "Тестовая среда", "Специализированное ПО"]
        },
        "avoid_duplicates": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-topics",
            json=cybersecurity_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сгенерировано {len(data['topics'])} тем")
            
            for i, topic in enumerate(data['topics'], 1):
                print(f"\n{i}. {topic['title']}")
                print(f"   Описание: {topic['description']}")
                print(f"   Сложность: {topic.get('difficulty_level', 'Не указана')}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"❌ Исключение: {e}")


if __name__ == "__main__":
    generate_personalized_topics()
