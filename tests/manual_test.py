"""
Ручное тестирование API сервиса генерации тем ВКР
"""

import requests
import json
import time
from typing import Dict, Any


class APITester:
    """Класс для ручного тестирования API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self) -> bool:
        """Тест проверки здоровья сервиса"""
        print("🔍 Проверка здоровья сервиса...")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Сервис работает: {data['status']}")
                print(f"   Модель: {data.get('model', 'N/A')}")
                return True
            else:
                print(f"❌ Сервис недоступен: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False
    
    def test_supported_fields(self) -> bool:
        """Тест получения поддерживаемых областей"""
        print("\n📚 Получение поддерживаемых областей...")
        
        try:
            response = self.session.get(f"{self.base_url}/fields")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Области знаний: {', '.join(data['fields'][:5])}...")
                print(f"   Уровни образования: {', '.join(data['levels'])}")
                return True
            else:
                print(f"❌ Ошибка получения областей: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def test_generate_topics(self, field: str = "Информатика", count: int = 3) -> Dict[str, Any]:
        """Тест генерации тем"""
        print(f"\n🤖 Генерация {count} тем по направлению '{field}'...")
        
        request_data = {
            "field": field,
            "count": count,
            "level": "Бакалавриат",
            "include_trends": True,
            "include_methodology": True
        }
        
        try:
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/generate-topics", json=request_data)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Успешно сгенерировано {data['total_count']} тем")
                print(f"   Время генерации: {data['generation_time']:.2f}с")
                print(f"   Модель: {data['model_used']}")
                
                # Выводим темы
                for i, topic in enumerate(data['topics'], 1):
                    print(f"\n   {i}. {topic['title']}")
                    if topic.get('description'):
                        print(f"      Описание: {topic['description'][:100]}...")
                    if topic.get('keywords'):
                        print(f"      Ключевые слова: {', '.join(topic['keywords'])}")
                
                return data
            else:
                print(f"❌ Ошибка генерации: {response.status_code}")
                print(f"   Ответ: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return {}
    
    def test_search_topics(self, query: str = "машинное обучение") -> Dict[str, Any]:
        """Тест поиска тем"""
        print(f"\n🔍 Поиск тем по запросу '{query}'...")
        
        params = {
            "query": query,
            "limit": 5
        }
        
        try:
            response = self.session.get(f"{self.base_url}/topics", params=params)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Найдено {data['total_count']} тем")
                
                for i, topic in enumerate(data['topics'], 1):
                    print(f"   {i}. {topic['title']}")
                    print(f"      Область: {topic['field']}, Уровень: {topic['level']}")
                
                return data
            else:
                print(f"❌ Ошибка поиска: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return {}
    
    def test_get_stats(self) -> Dict[str, Any]:
        """Тест получения статистики"""
        print("\n📊 Получение статистики...")
        
        try:
            response = self.session.get(f"{self.base_url}/stats")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Статистика получена")
                print(f"   Всего тем: {data['total_topics']}")
                print(f"   По областям: {data['by_field']}")
                print(f"   По уровням: {data['by_level']}")
                return data
            else:
                print(f"❌ Ошибка получения статистики: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return {}
    
    def test_error_handling(self) -> bool:
        """Тест обработки ошибок"""
        print("\n⚠️  Тестирование обработки ошибок...")
        
        # Тест невалидного запроса
        invalid_request = {
            "field": "Информатика",
            "count": 25  # Слишком много тем
        }
        
        try:
            response = self.session.post(f"{self.base_url}/generate-topics", json=invalid_request)
            if response.status_code == 422:
                print("✅ Валидация работает корректно")
                return True
            else:
                print(f"❌ Ожидалась ошибка валидации, получен код: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def test_performance(self, num_requests: int = 5) -> bool:
        """Тест производительности"""
        print(f"\n⚡ Тестирование производительности ({num_requests} запросов)...")
        
        request_data = {
            "field": "Информатика",
            "count": 1,
            "level": "Бакалавриат"
        }
        
        times = []
        successful_requests = 0
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = self.session.post(f"{self.base_url}/generate-topics", json=request_data)
                end_time = time.time()
                
                if response.status_code == 200:
                    successful_requests += 1
                    times.append(end_time - start_time)
                    print(f"   Запрос {i+1}: {times[-1]:.2f}с")
                else:
                    print(f"   Запрос {i+1}: Ошибка {response.status_code}")
            except Exception as e:
                print(f"   Запрос {i+1}: Исключение {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"✅ Успешных запросов: {successful_requests}/{num_requests}")
            print(f"   Среднее время: {avg_time:.2f}с")
            print(f"   Минимальное время: {min(times):.2f}с")
            print(f"   Максимальное время: {max(times):.2f}с")
            return successful_requests >= num_requests * 0.8  # 80% успешных
        else:
            print("❌ Нет успешных запросов")
            return False
    
    def run_all_tests(self) -> bool:
        """Запуск всех тестов"""
        print("🧪 РУЧНОЕ ТЕСТИРОВАНИЕ API СЕРВИСА ГЕНЕРАЦИИ ТЕМ ВКР")
        print("=" * 60)
        
        tests = [
            ("Проверка здоровья", self.test_health),
            ("Поддерживаемые области", self.test_supported_fields),
            ("Генерация тем", lambda: self.test_generate_topics("Информатика", 2)),
            ("Поиск тем", lambda: self.test_search_topics("машинное обучение")),
            ("Статистика", self.test_get_stats),
            ("Обработка ошибок", self.test_error_handling),
            ("Производительность", lambda: self.test_performance(3))
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{'='*40}")
            print(f"🔬 {test_name}")
            print(f"{'='*40}")
            
            try:
                result = test_func()
                if result is not False and result is not None:
                    passed += 1
                    print(f"✅ {test_name} - ПРОЙДЕН")
                else:
                    print(f"❌ {test_name} - НЕ ПРОЙДЕН")
            except Exception as e:
                print(f"❌ {test_name} - ОШИБКА: {e}")
        
        print(f"\n{'='*60}")
        print(f"📊 ИТОГОВЫЙ РЕЗУЛЬТАТ")
        print(f"{'='*60}")
        print(f"✅ Пройдено: {passed}/{total}")
        print(f"❌ Не пройдено: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            return True
        else:
            print(f"\n⚠️  {total - passed} ТЕСТОВ НЕ ПРОЙДЕНЫ")
            return False


def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ручное тестирование API")
    parser.add_argument("--url", default="http://localhost:8000", help="URL сервиса")
    parser.add_argument("--field", default="Информатика", help="Область для тестирования")
    parser.add_argument("--count", type=int, default=3, help="Количество тем для генерации")
    parser.add_argument("--query", default="машинное обучение", help="Запрос для поиска")
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    
    print(f"🌐 Тестирование сервиса: {args.url}")
    print(f"📚 Область: {args.field}")
    print(f"🔢 Количество тем: {args.count}")
    print(f"🔍 Поисковый запрос: {args.query}")
    
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Сервис готов к использованию!")
        return 0
    else:
        print("\n🔧 Требуется исправление ошибок")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
