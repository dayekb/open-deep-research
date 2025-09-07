"""
Примеры использования API сервиса генерации тем ВКР
"""

import requests
import json
import time


class VKRTopicClient:
    """Клиент для работы с API сервиса генерации тем"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def generate_topics(self, field: str, count: int = 5, 
                       specialization: str = None, 
                       level: str = "Бакалавриат") -> dict:
        """Генерация тем через API"""
        url = f"{self.base_url}/generate-topics"
        
        data = {
            "field": field,
            "count": count,
            "specialization": specialization,
            "level": level,
            "include_trends": True,
            "include_methodology": True
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def search_topics(self, query: str, limit: int = 10) -> dict:
        """Поиск тем через API"""
        url = f"{self.base_url}/topics"
        
        params = {
            "query": query,
            "limit": limit
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_topic(self, topic_id: int) -> dict:
        """Получение темы по ID"""
        url = f"{self.base_url}/topics/{topic_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> dict:
        """Получение статистики"""
        url = f"{self.base_url}/stats"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_supported_fields(self) -> dict:
        """Получение поддерживаемых областей"""
        url = f"{self.base_url}/fields"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


def print_topics(topics_data: dict):
    """Красивый вывод тем"""
    topics = topics_data.get("topics", [])
    total_count = topics_data.get("total_count", 0)
    generation_time = topics_data.get("generation_time", 0)
    
    print(f"\n📚 Найдено {total_count} тем (время генерации: {generation_time:.2f}с)")
    print("=" * 60)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n{i}. {topic['title']}")
        print(f"   🎓 Уровень: {topic['level']}")
        print(f"   📖 Область: {topic['field']}")
        if topic.get('specialization'):
            print(f"   🔬 Специализация: {topic['specialization']}")
        if topic.get('description'):
            print(f"   📝 Описание: {topic['description']}")
        if topic.get('keywords'):
            print(f"   🏷️  Ключевые слова: {', '.join(topic['keywords'])}")


def main():
    """Основная функция с примерами API"""
    client = VKRTopicClient()
    
    print("🚀 Примеры использования API сервиса генерации тем ВКР")
    print("=" * 60)
    
    try:
        # Проверка здоровья сервиса
        print("\n1. Проверка здоровья сервиса...")
        health_response = requests.get(f"{client.base_url}/health")
        if health_response.status_code == 200:
            print("✅ Сервис работает")
        else:
            print("❌ Сервис недоступен")
            return
        
        # Получение поддерживаемых областей
        print("\n2. Поддерживаемые области знаний:")
        fields_data = client.get_supported_fields()
        print(f"   Области: {', '.join(fields_data['fields'])}")
        print(f"   Уровни: {', '.join(fields_data['levels'])}")
        
        # Генерация тем для информатики
        print("\n3. Генерация тем по информатике:")
        topics_data = client.generate_topics(
            field="Информатика",
            count=3,
            level="Бакалавриат"
        )
        print_topics(topics_data)
        
        # Генерация тем с специализацией
        print("\n4. Генерация тем с специализацией:")
        specialized_topics = client.generate_topics(
            field="Экономика",
            specialization="Цифровая экономика",
            count=2,
            level="Магистратура"
        )
        print_topics(specialized_topics)
        
        # Поиск тем
        print("\n5. Поиск тем по ключевому слову 'машинное обучение':")
        search_results = client.search_topics("машинное обучение", limit=5)
        print_topics(search_results)
        
        # Статистика
        print("\n6. Статистика по темам:")
        stats = client.get_stats()
        print(f"   📊 Всего тем: {stats['total_topics']}")
        print(f"   📈 По областям: {stats['by_field']}")
        print(f"   🎓 По уровням: {stats['by_level']}")
        print(f"   📋 По статусам: {stats['by_status']}")
        
        print("\n✅ Все примеры выполнены успешно!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к серверу")
        print("Убедитесь, что сервер запущен: python -m src.api.server")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()
