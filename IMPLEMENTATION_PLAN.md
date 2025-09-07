# План реализации сервиса генерации тем ВКР

## Обзор проекта

Сервис использует библиотеку [Open Deep Research](https://github.com/langchain-ai/open_deep_research) от LangChain для автоматической генерации актуальных и релевантных тем выпускных квалификационных работ (ВКР) по различным направлениям.

## Архитектура решения

### 1. Основные компоненты

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI API   │────│  VKR Topic Agent │────│  Open Deep      │
│   (REST API)    │    │  (LangChain)     │    │  Research       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Database      │    │   Search APIs    │    │   AI Models     │
│   (SQLite/      │    │   (Tavily,       │    │   (OpenAI,      │
│   PostgreSQL)   │    │   Google, Bing)  │    │   Anthropic)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 2. Поток данных

1. **Запрос пользователя** → FastAPI API
2. **Валидация параметров** → Pydantic модели
3. **Генерация тем** → VKR Topic Agent + Open Deep Research
4. **Поиск актуальной информации** → Search APIs (Tavily, Google)
5. **Анализ и синтез** → AI Models (GPT-4, Claude)
6. **Сохранение результатов** → Database
7. **Возврат ответа** → JSON API Response

## Этапы реализации

### Этап 1: Базовая инфраструктура ✅

- [x] Настройка проекта и зависимостей
- [x] Создание моделей данных (Pydantic)
- [x] Настройка конфигурации
- [x] Создание базовой структуры API

### Этап 2: Интеграция с Open Deep Research

#### 2.1 Адаптация агента для ВКР

```python
# src/agents/vkr_research_agent.py
class VKRResearchAgent:
    def __init__(self):
        # Инициализация Open Deep Research
        self.research_agent = DeepResearchAgent()
        
    async def research_topic_trends(self, field: str) -> Dict:
        """Исследование трендов в области"""
        research_query = f"Актуальные направления и тренды в области {field} 2024"
        return await self.research_agent.research(research_query)
    
    async def find_relevant_papers(self, topic: str) -> List[Dict]:
        """Поиск релевантных научных работ"""
        search_query = f"научные статьи исследования {topic} 2023 2024"
        return await self.research_agent.search_academic_papers(search_query)
```

#### 2.2 Настройка поисковых источников

```python
# src/config/search_config.py
SEARCH_SOURCES = {
    "academic": {
        "sources": ["arxiv", "pubmed", "scholar"],
        "time_range": "2023-2024"
    },
    "trends": {
        "sources": ["news", "blogs", "reports"],
        "time_range": "2024"
    }
}
```

### Этап 3: Расширенная генерация тем

#### 3.1 Многоэтапная генерация

```python
async def generate_comprehensive_topics(self, config: TopicGenerationConfig) -> List[VKRTopic]:
    """Комплексная генерация тем с исследованием"""
    
    # Этап 1: Исследование трендов
    trends = await self.research_agent.research_topic_trends(config.field)
    
    # Этап 2: Анализ актуальных проблем
    problems = await self.analyze_field_problems(config.field, trends)
    
    # Этап 3: Генерация тем на основе исследований
    topics = await self.generate_topics_from_research(problems, config)
    
    # Этап 4: Валидация и оценка качества
    validated_topics = await self.validate_topics(topics)
    
    return validated_topics
```

#### 3.2 Оценка качества тем

```python
async def evaluate_topic_quality(self, topic: VKRTopic) -> float:
    """Оценка качества темы"""
    
    # Проверка актуальности
    relevance_score = await self.check_topic_relevance(topic)
    
    # Проверка научной обоснованности
    scientific_score = await self.check_scientific_basis(topic)
    
    # Проверка практической значимости
    practical_score = await self.check_practical_value(topic)
    
    return (relevance_score + scientific_score + practical_score) / 3
```

### Этап 4: Интеграция с внешними источниками

#### 4.1 Академические базы данных

```python
# src/integrations/academic_apis.py
class AcademicAPIIntegration:
    def __init__(self):
        self.arxiv_client = ArxivClient()
        self.scholar_client = ScholarClient()
        self.pubmed_client = PubMedClient()
    
    async def search_recent_papers(self, query: str, field: str) -> List[Paper]:
        """Поиск недавних научных работ"""
        papers = []
        
        # Поиск в ArXiv
        arxiv_papers = await self.arxiv_client.search(query, field)
        papers.extend(arxiv_papers)
        
        # Поиск в Google Scholar
        scholar_papers = await self.scholar_client.search(query)
        papers.extend(scholar_papers)
        
        return papers
```

#### 4.2 Анализ трендов

```python
# src/integrations/trend_analysis.py
class TrendAnalyzer:
    def __init__(self):
        self.news_api = NewsAPIClient()
        self.trend_api = TrendAPIClient()
    
    async def analyze_field_trends(self, field: str) -> Dict:
        """Анализ трендов в области"""
        
        # Поиск новостей и публикаций
        news = await self.news_api.search(f"{field} research trends 2024")
        
        # Анализ ключевых слов
        keywords = await self.extract_trending_keywords(news)
        
        # Определение перспективных направлений
        directions = await self.identify_promising_directions(keywords)
        
        return {
            "trending_keywords": keywords,
            "promising_directions": directions,
            "recent_developments": news
        }
```

### Этап 5: Продвинутые функции

#### 5.1 Персонализация тем

```python
class PersonalizedTopicGenerator:
    def __init__(self):
        self.user_profiles = UserProfileManager()
        self.topic_recommender = TopicRecommender()
    
    async def generate_personalized_topics(self, user_id: str, config: TopicGenerationConfig) -> List[VKRTopic]:
        """Генерация персонализированных тем"""
        
        # Получение профиля пользователя
        profile = await self.user_profiles.get_profile(user_id)
        
        # Анализ предпочтений
        preferences = await self.analyze_user_preferences(profile)
        
        # Генерация тем с учетом предпочтений
        topics = await self.generate_topics_with_preferences(config, preferences)
        
        # Ранжирование по релевантности для пользователя
        ranked_topics = await self.rank_topics_for_user(topics, profile)
        
        return ranked_topics
```

#### 5.2 Коллаборативная фильтрация

```python
class CollaborativeFiltering:
    def __init__(self):
        self.user_interactions = UserInteractionTracker()
        self.similarity_calculator = SimilarityCalculator()
    
    async def find_similar_users(self, user_id: str) -> List[str]:
        """Поиск похожих пользователей"""
        
        user_interactions = await self.user_interactions.get_user_interactions(user_id)
        all_users = await self.user_interactions.get_all_users()
        
        similarities = []
        for other_user in all_users:
            if other_user != user_id:
                other_interactions = await self.user_interactions.get_user_interactions(other_user)
                similarity = await self.similarity_calculator.calculate_similarity(
                    user_interactions, other_interactions
                )
                similarities.append((other_user, similarity))
        
        # Сортировка по убыванию схожести
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [user_id for user_id, _ in similarities[:10]]
```

### Этап 6: Мониторинг и аналитика

#### 6.1 Метрики качества

```python
class QualityMetrics:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
    
    async def track_topic_quality(self, topic: VKRTopic, user_feedback: Dict):
        """Отслеживание качества тем"""
        
        metrics = {
            "relevance_score": topic.relevance_score,
            "user_rating": user_feedback.get("rating"),
            "adoption_rate": await self.calculate_adoption_rate(topic),
            "completion_rate": await self.calculate_completion_rate(topic)
        }
        
        await self.metrics_collector.record_metrics(topic.id, metrics)
```

#### 6.2 A/B тестирование

```python
class ABTesting:
    def __init__(self):
        self.experiment_manager = ExperimentManager()
    
    async def run_generation_experiment(self, config: TopicGenerationConfig) -> Dict:
        """A/B тестирование различных подходов к генерации"""
        
        # Вариант A: Стандартная генерация
        topics_a = await self.standard_generation(config)
        
        # Вариант B: Генерация с дополнительным исследованием
        topics_b = await self.enhanced_generation(config)
        
        # Сравнение результатов
        comparison = await self.compare_generation_approaches(topics_a, topics_b)
        
        return comparison
```

## Технические детали

### 1. Использование Open Deep Research

```python
# Интеграция с Open Deep Research
from open_deep_research import DeepResearchAgent, SearchConfig

class VKRDeepResearchAgent:
    def __init__(self):
        # Настройка поисковых источников
        search_config = SearchConfig(
            search_api="tavily",
            academic_sources=["arxiv", "pubmed", "scholar"],
            news_sources=["news", "blogs"],
            time_range="2023-2024"
        )
        
        # Инициализация агента
        self.research_agent = DeepResearchAgent(
            model="openai:gpt-4.1",
            search_config=search_config
        )
    
    async def research_field_trends(self, field: str) -> Dict:
        """Исследование трендов в области"""
        
        research_query = f"""
        Проведи глубокое исследование актуальных направлений и трендов 
        в области {field} за 2023-2024 годы. Включи:
        1. Новые научные открытия и разработки
        2. Перспективные направления исследований
        3. Практические применения и внедрения
        4. Проблемы и вызовы в области
        5. Рекомендации для студентов и исследователей
        """
        
        result = await self.research_agent.research(research_query)
        return result
```

### 2. Обработка различных областей знаний

```python
# Специализированные промпты для разных областей
FIELD_SPECIFIC_PROMPTS = {
    "Информатика": {
        "focus_areas": ["искусственный интеллект", "машинное обучение", "кибербезопасность"],
        "methodologies": ["экспериментальные исследования", "системный анализ", "математическое моделирование"],
        "practical_applications": ["разработка ПО", "анализ данных", "автоматизация процессов"]
    },
    "Экономика": {
        "focus_areas": ["цифровая экономика", "устойчивое развитие", "финансовые технологии"],
        "methodologies": ["эконометрический анализ", "статистические методы", "качественные исследования"],
        "practical_applications": ["бизнес-планирование", "финансовое моделирование", "рыночный анализ"]
    }
}
```

### 3. Оценка и ранжирование тем

```python
class TopicEvaluator:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4.1")
    
    async def evaluate_topic(self, topic: VKRTopic) -> Dict:
        """Комплексная оценка темы"""
        
        evaluation_prompt = f"""
        Оцени тему ВКР по следующим критериям (по шкале 1-10):
        
        Тема: {topic.title}
        Область: {topic.field}
        Уровень: {topic.level}
        
        Критерии:
        1. Актуальность и современность
        2. Научная новизна
        3. Практическая значимость
        4. Реализуемость в рамках учебного процесса
        5. Доступность источников и литературы
        6. Соответствие уровню образования
        
        Верни оценку в формате JSON.
        """
        
        response = await self.llm.ainvoke(evaluation_prompt)
        return json.loads(response.content)
```

## План развертывания

### Фаза 1: MVP (2-3 недели)
- [x] Базовая генерация тем
- [x] REST API
- [x] Простая веб-интерфейс
- [x] SQLite база данных

### Фаза 2: Расширенные функции (3-4 недели)
- [ ] Интеграция с Open Deep Research
- [ ] Анализ трендов
- [ ] Оценка качества тем
- [ ] Поиск и фильтрация

### Фаза 3: Персонализация (2-3 недели)
- [ ] Пользовательские профили
- [ ] Персонализированные рекомендации
- [ ] История генерации
- [ ] Избранные темы

### Фаза 4: Аналитика и оптимизация (2-3 недели)
- [ ] Метрики использования
- [ ] A/B тестирование
- [ ] Оптимизация промптов
- [ ] Улучшение качества генерации

## Ожидаемые результаты

### Количественные метрики
- **Время генерации**: < 30 секунд для 5 тем
- **Качество тем**: > 80% релевантных тем
- **Покрытие областей**: 12+ направлений
- **Пользовательская оценка**: > 4.0/5.0

### Качественные улучшения
- Автоматизация процесса выбора тем ВКР
- Повышение актуальности и качества тем
- Сокращение времени на поиск подходящих тем
- Улучшение образовательного процесса

## Риски и митигация

### Технические риски
- **Низкое качество генерации**: Тестирование и итеративное улучшение промптов
- **Медленная работа**: Кеширование и оптимизация запросов
- **Ошибки API**: Обработка исключений и fallback стратегии

### Бизнес-риски
- **Низкое принятие пользователями**: UX тестирование и обратная связь
- **Высокие затраты на API**: Мониторинг использования и оптимизация
- **Конкуренция**: Фокус на уникальных возможностях и качестве

## Заключение

Данный план реализации обеспечивает создание полнофункционального сервиса генерации тем ВКР с использованием современных технологий ИИ и глубокого исследования. Поэтапный подход позволяет быстро получить MVP и постепенно добавлять продвинутые функции.
