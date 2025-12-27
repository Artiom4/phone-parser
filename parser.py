import asyncio
from telethon import TelegramClient
import csv
from datetime import datetime

API_ID = "ВСТАВЬ_API_ID"
API_HASH = "ВСТАВЬ_API_HASH"
PHONE = "+79991234567"

CHANNELS = ["perehvat_store_bot", "KIB_STORE", "PEREKUP_63"]

print("🚀 Парсер iPhone запущен")

async def main():
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start(PHONE)
    
    results = []
    
    for channel in CHANNELS:
        print(f"🔍 @{channel}")
        try:
            entity = await client.get_entity(channel)
            count = 0
            
            async for message in client.iter_messages(entity, limit=50):
                text = message.text or ""
                if 'iphone' in text.lower():
                    import re
                    match = re.search(r'(\d+)[\sкk]', text.lower())
                    if match:
                        price = int(match.group(1)) * 1000
                        results.append([text[:80], price, channel])
                        count += 1
            
            print(f"   Найдено: {count}")
        except:
            print("   ❌ Ошибка")
    
    if results:
        filename = f"prices_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Описание', 'Цена', 'Канал'])
            writer.writerows(results)
        
        print(f"\n💾 Сохранено: {len(results)} iPhone")
    else:
        print("\n📭 Ничего не найдено")
    
    await client.disconnect()

asyncio.run(main())  
