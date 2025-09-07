#!/usr/bin/env python3
"""
Простой скрипт для установки нового API ключа
"""

# ЗАМЕНИТЕ ЭТОТ КЛЮЧ НА ВАШ НОВЫЙ
NEW_API_KEY = "sk-or-v1-YOUR_NEW_KEY_HERE"

def update_key():
    """Обновление ключа"""
    print("🔑 УСТАНОВКА НОВОГО API КЛЮЧА")
    print("=" * 40)
    
    if NEW_API_KEY == "sk-or-v1-YOUR_NEW_KEY_HERE":
        print("❌ Сначала замените NEW_API_KEY в скрипте на ваш новый ключ")
        print("   Откройте файл set_new_key.py и замените значение")
        return False
    
    try:
        # Читаем .env файл
        with open('.env', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Обновляем ключ
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('OPENROUTER_API_KEY='):
                lines[i] = f'OPENROUTER_API_KEY={NEW_API_KEY}\n'
                updated = True
                break
        
        if not updated:
            # Добавляем ключ если его нет
            lines.append(f'OPENROUTER_API_KEY={NEW_API_KEY}\n')
        
        # Записываем обратно
        with open('.env', 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"✅ Ключ обновлен: {NEW_API_KEY[:20]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = update_key()
    
    if success:
        print("\n🎉 Ключ установлен!")
        print("Теперь можете протестировать:")
        print("  conda run python test_direct_api.py")
    else:
        print("\n❌ Не удалось установить ключ")
