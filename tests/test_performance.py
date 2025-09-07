"""
Тесты производительности
"""

import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import AsyncMock, patch

from src.agents import VKRTopicAgent, TopicGenerationConfig
from src.models import EducationLevel


class TestPerformance:
    """Тесты производительности"""
    
    @pytest.mark.asyncio
    async def test_generation_speed(self, mock_llm):
        """Тест скорости генерации тем"""
        # Настройка мока для быстрого ответа
        mock_response = AsyncMock()
        mock_response.content = """
        1. Быстрая тема 1
        Актуальность: Важная тема.
        Ключевые слова: тема1, важность
        Методология: Исследование
        Ожидаемые результаты: Результаты
        
        2. Быстрая тема 2
        Актуальность: Важная тема.
        Ключевые слова: тема2, важность
        Методология: Анализ
        Ожидаемые результаты: Результаты
        """
        mock_llm.ainvoke.return_value = mock_response
        
        with patch('src.agents.vkr_topic_agent.ChatOpenAI') as mock_openai:
            mock_openai.return_value = mock_llm
            
            agent = VKRTopicAgent()
            
            # Измеряем время генерации
            start_time = time.time()
            topics = await agent.generate_topics_simple(
                field="Информатика",
                count=2
            )
            end_time = time.time()
            
            generation_time = end_time - start_time
            
            # Проверяем, что генерация заняла разумное время
            assert generation_time < 5.0  # Менее 5 секунд
            assert len(topics) == 2
            print(f"Время генерации 2 тем: {generation_time:.2f} секунд")
    
    @pytest.mark.asyncio
    async def test_concurrent_generation(self, mock_llm):
        """Тест параллельной генерации тем"""
        # Настройка мока
        mock_response = AsyncMock()
        mock_response.content = """
        1. Параллельная тема
        Актуальность: Важная тема.
        Ключевые слова: параллель, тема
        Методология: Исследование
        Ожидаемые результаты: Результаты
        """
        mock_llm.ainvoke.return_value = mock_response
        
        with patch('src.agents.vkr_topic_agent.ChatOpenAI') as mock_openai:
            mock_openai.return_value = mock_llm
            
            agent = VKRTopicAgent()
            
            # Создаем несколько задач для параллельного выполнения
            tasks = []
            for i in range(5):
                task = agent.generate_topics_simple(
                    field=f"Область {i}",
                    count=1
                )
                tasks.append(task)
            
            # Измеряем время параллельного выполнения
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            
            parallel_time = end_time - start_time
            
            # Проверяем результаты
            assert len(results) == 5
            for topics in results:
                assert len(topics) == 1
            
            print(f"Время параллельной генерации 5 тем: {parallel_time:.2f} секунд")
    
    @pytest.mark.asyncio
    async def test_memory_usage(self, mock_llm, topic_repository):
        """Тест использования памяти при создании большого количества тем"""
        import psutil
        import os
        
        # Получаем текущий процесс
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Настройка мока
        mock_response = AsyncMock()
        mock_response.content = """
        1. Тема для теста памяти
        Актуальность: Важная тема.
        Ключевые слова: память, тест
        Методология: Исследование
        Ожидаемые результаты: Результаты
        """
        mock_llm.ainvoke.return_value = mock_response
        
        with patch('src.agents.vkr_topic_agent.ChatOpenAI') as mock_openai:
            mock_openai.return_value = mock_llm
            
            agent = VKRTopicAgent()
            
            # Создаем много тем
            topics = []
            for i in range(100):
                topic = VKRTopic(
                    title=f"Тема {i}",
                    field="Информатика",
                    level=EducationLevel.BACHELOR,
                    description=f"Описание темы {i}",
                    keywords=[f"ключевое_слово_{i}"]
                )
                topics.append(topic)
                
                # Сохраняем в базу данных
                await topic_repository.create_topic(topic)
        
        # Проверяем использование памяти
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Увеличение использования памяти: {memory_increase:.2f} MB")
        
        # Проверяем, что увеличение памяти разумное (менее 100 MB)
        assert memory_increase < 100.0
        
        # Проверяем, что темы сохранились
        stats = await topic_repository.get_stats()
        assert stats.total_topics >= 100
    
    def test_api_response_time(self, test_client):
        """Тест времени ответа API"""
        # Тестируем время ответа на простые запросы
        endpoints = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/fields", "GET"),
            ("/stats", "GET")
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            
            if method == "GET":
                response = test_client.get(endpoint)
            else:
                response = test_client.post(endpoint)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Проверяем, что ответ получен быстро
            assert response_time < 1.0  # Менее 1 секунды
            assert response.status_code in [200, 404]  # 404 для /stats без данных
            
            print(f"Время ответа {endpoint}: {response_time:.3f} секунд")
    
    @pytest.mark.asyncio
    async def test_database_query_performance(self, topic_repository):
        """Тест производительности запросов к базе данных"""
        # Создаем тестовые данные
        topics_data = []
        for i in range(1000):
            topic = VKRTopic(
                title=f"Тема {i}",
                field="Информатика" if i % 2 == 0 else "Экономика",
                level=EducationLevel.BACHELOR if i % 3 == 0 else EducationLevel.MASTER,
                description=f"Описание темы {i}",
                keywords=[f"ключевое_слово_{i}"]
            )
            topics_data.append(topic)
        
        # Измеряем время создания
        start_time = time.time()
        for topic in topics_data:
            await topic_repository.create_topic(topic)
        creation_time = time.time() - start_time
        
        print(f"Время создания 1000 тем: {creation_time:.2f} секунд")
        
        # Измеряем время поиска
        start_time = time.time()
        search_request = TopicSearchRequest(
            query="тема",
            limit=100,
            offset=0
        )
        topics, total_count = await topic_repository.search_topics(search_request)
        search_time = time.time() - start_time
        
        print(f"Время поиска тем: {search_time:.3f} секунд")
        print(f"Найдено тем: {len(topics)} из {total_count}")
        
        # Проверяем производительность
        assert creation_time < 30.0  # Создание менее 30 секунд
        assert search_time < 1.0  # Поиск менее 1 секунды
        assert len(topics) == 100  # Найдено ожидаемое количество
    
    def test_concurrent_api_requests(self, test_client):
        """Тест параллельных API запросов"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                start_time = time.time()
                response = test_client.get("/health")
                end_time = time.time()
                
                results.put({
                    "status_code": response.status_code,
                    "response_time": end_time - start_time,
                    "success": response.status_code == 200
                })
            except Exception as e:
                results.put({
                    "error": str(e),
                    "success": False
                })
        
        # Создаем несколько потоков для параллельных запросов
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()
        
        # Анализируем результаты
        successful_requests = 0
        total_response_time = 0
        
        while not results.empty():
            result = results.get()
            if result["success"]:
                successful_requests += 1
                total_response_time += result["response_time"]
        
        avg_response_time = total_response_time / successful_requests if successful_requests > 0 else 0
        
        print(f"Успешных запросов: {successful_requests}/10")
        print(f"Среднее время ответа: {avg_response_time:.3f} секунд")
        
        # Проверяем, что большинство запросов успешны
        assert successful_requests >= 8  # Не менее 80% успешных запросов
        assert avg_response_time < 2.0  # Среднее время ответа менее 2 секунд


class TestLoadTesting:
    """Тесты нагрузки"""
    
    @pytest.mark.asyncio
    async def test_high_load_generation(self, mock_llm):
        """Тест генерации при высокой нагрузке"""
        # Настройка мока для имитации медленного ответа
        async def slow_response(*args, **kwargs):
            await asyncio.sleep(0.1)  # Имитация задержки
            mock_response = AsyncMock()
            mock_response.content = """
            1. Тема под нагрузкой
            Актуальность: Важная тема.
            Ключевые слова: нагрузка, тест
            Методология: Исследование
            Ожидаемые результаты: Результаты
            """
            return mock_response
        
        mock_llm.ainvoke = slow_response
        
        with patch('src.agents.vkr_topic_agent.ChatOpenAI') as mock_openai:
            mock_openai.return_value = mock_llm
            
            agent = VKRTopicAgent()
            
            # Создаем много задач одновременно
            tasks = []
            for i in range(20):
                task = agent.generate_topics_simple(
                    field=f"Область {i % 5}",  # 5 разных областей
                    count=1
                )
                tasks.append(task)
            
            # Измеряем время выполнения
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()
            
            total_time = end_time - start_time
            
            # Подсчитываем успешные результаты
            successful_results = [r for r in results if not isinstance(r, Exception)]
            failed_results = [r for r in results if isinstance(r, Exception)]
            
            print(f"Время выполнения 20 задач: {total_time:.2f} секунд")
            print(f"Успешных: {len(successful_results)}, Неудачных: {len(failed_results)}")
            
            # Проверяем, что большинство задач выполнились успешно
            assert len(successful_results) >= 18  # Не менее 90% успешных
            assert len(failed_results) <= 2  # Не более 10% неудачных
            assert total_time < 10.0  # Общее время менее 10 секунд
