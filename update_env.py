#!/usr/bin/env python3
"""
Обновление .env файла с новым API ключом
"""

def update_env_file():
    """Обновление .env файла"""
    print("🔑 ОБНОВЛЕНИЕ .ENV ФАЙЛА")
    print("=" * 40)
    
    # Читаем текущий .env
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Текущий ключ в .env:")
        for line in content.split('\n'):
            if 'OPENROUTER_API_KEY=' in line:
                print(f"  {line}")
                break
        
        print("\nВведите новый API ключ OpenRouter:")
        print("(или нажмите Enter для пропуска)")
        
        new_key = input("Новый ключ: ").strip()
        
        if not new_key:
            print("❌ Ключ не введен")
            return False
        
        # Обновляем ключ
        updated_content = content.replace(
            'OPENROUTER_API_KEY=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',
            f'OPENROUTER_API_KEY={new_key}'
        )
        
        # Записываем обновленный файл
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Ключ обновлен: {new_key[:20]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = update_env_file()
    
    if success:
        print("\n🎉 .env файл обновлен!")
        print("Теперь можете протестировать:")
        print("  conda run python test_direct_api.py")
    else:
        print("\n❌ Обновление не удалось")
