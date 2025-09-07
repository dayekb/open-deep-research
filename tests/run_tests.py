"""
Скрипт для запуска всех тестов
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Запуск команды с выводом результата"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Успешно выполнено")
        if result.stdout:
            print("Вывод:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e}")
        if e.stdout:
            print("Вывод:")
            print(e.stdout)
        if e.stderr:
            print("Ошибки:")
            print(e.stderr)
        return False


def main():
    """Основная функция запуска тестов"""
    print("🧪 Запуск тестов сервиса генерации тем ВКР")
    print("=" * 60)
    
    # Проверяем, что мы в правильной директории
    if not Path("src").exists():
        print("❌ Ошибка: Запустите скрипт из корневой директории проекта")
        sys.exit(1)
    
    # Список тестов для запуска
    test_commands = [
        {
            "command": "python -m pytest tests/test_models.py -v",
            "description": "Тесты моделей данных"
        },
        {
            "command": "python -m pytest tests/test_agents.py -v",
            "description": "Тесты агентов генерации"
        },
        {
            "command": "python -m pytest tests/test_database.py -v",
            "description": "Тесты базы данных"
        },
        {
            "command": "python -m pytest tests/test_api.py -v",
            "description": "Тесты API"
        },
        {
            "command": "python -m pytest tests/test_performance.py -v -s",
            "description": "Тесты производительности"
        }
    ]
    
    # Запуск всех тестов
    success_count = 0
    total_tests = len(test_commands)
    
    for test_cmd in test_commands:
        if run_command(test_cmd["command"], test_cmd["description"]):
            success_count += 1
    
    # Итоговый отчет
    print(f"\n{'='*60}")
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print(f"{'='*60}")
    print(f"✅ Успешно выполнено: {success_count}/{total_tests}")
    print(f"❌ Неудачно: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("\n🎉 Все тесты прошли успешно!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - success_count} тестов завершились с ошибками")
        return 1


if __name__ == "__main__":
    sys.exit(main())
