#!/usr/bin/env python3
"""
ПАРСЕР iPhone 12-17
Один файл — всё работает
"""

import asyncio
import sys
import csv
from datetime import datetime

print("🚀 iPhone ПАРСЕР - ЗАПУСК")
print("=" * 50)

async def main():
    try:
        # Пробуем импортировать telethon
        from telethon import TelegramClient, events
        print("✅ Библиотеки загружены")
    except:
        print("❌ Установите библиотеку: pip install telethon")
        print("   Команда: pip install telethon --user")
        return
    
    # Твои настройки (можно менять)
    API_ID = "ВСТАВЬ_API_ID"        # ← замени на свои
    API_HASH = "ВСТАВЬ_API_HASH"    # ← замени на свои
    PHONE = "+79991234567"          # ← твой номер
    
    # Твои каналы
    CHANNELS = [
        "perehvat_store_bot",
        "KIB_STORE", 
        "PEREKUP_63"
    ]
    
    print(f"🔍 Каналов для проверки: {len(CHANNELS)}")
    
    # Создаём клиент
    client = TelegramClient('iphone_session', API_ID, API_HASH)
    
    try:
        # Подключаемся
        print("\n1. Подключаюсь к Telegram...")
        await client.start(PHONE)
        print("   ✅ Успешное подключение!")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        print("   🔧 Получи API ключи: my.telegram.org")
        return
    
    # Собираем iPhone
    all_iphones = []
    
    for channel in CHANNELS:
        print(f"\n2. Проверяю: @{channel}")
        try:
            entity = await client.get_entity(channel)
            found = 0
            
            async for message in client.iter_messages(entity, limit=50):
                text = message.text or ""
                text_lower = text.lower()
                
                # Ищем iPhone
                if 'iphone' in text_lower or 'айфон' in text_lower:
                    # Ищем цену
                    import re
                    price_match = re.search(r'(\d+)[\sкk]', text_lower)
                    if price_match:
                        price = int(price_match.group(1)) * 1000
                        
                        all_iphones.append({
                            'text': text[:80],
                            'price': price,
                            'channel': channel,
                            'date': message.date.strftime('%H:%M')
                        })
                        found += 1
            
            print(f"   Найдено iPhone: {found}")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {str(e)[:40]}")
    
    # Сохраняем результаты
    if all_iphones:
        filename = "iphones_found.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Описание', 'Цена', 'Канал', 'Время'])
            for item in all_iphones:
                writer.writerow([item['text'], item['price'], item['channel'], item['date']])
        
        print(f"\n💾 Сохранено: {filename}")
        print(f"📊 Всего iPhone: {len(all_iphones)}")
        
        # Показываем самые дешёвые
        print("\n🏆 САМЫЕ ДЕШЁВЫЕ:")
        sorted_iphones = sorted(all_iphones, key=lambda x: x['price'])[:3]
        for i, item in enumerate(sorted_iphones, 1):
            print(f"{i}. {item['price']:,}₽ - @{item['channel']}")
            print(f"   {item['text']}")
            print()
    
    else:
        print("\n📭 iPhone не найдено")
    
    await client.disconnect()
    print("✅ Готово! Файл: iphones_found.csv")

# Запускаем
if __name__ == "__main__":
    asyncio.run(main())
