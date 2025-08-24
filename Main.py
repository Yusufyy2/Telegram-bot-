import os, asyncio, logging, aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN ortam değişkeni eksik!")

bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def start(m: Message):
    await m.answer("Merhaba! /veri yaz, bir API'den örnek veri getireyim. 🔌")

@router.message(Command("veri"))
async def veri(m: Message):
    # ÖRNEK: dış bir API'den veri çekiyoruz
    # İstersen bu URL'yi kendi kullanmak istediğin API ile değiştir.
    url = "https://api.quotable.io/random"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as r:
                data = await r.json()
                metin = data.get("content", "Veri bulunamadı")
                yazar = data.get("author", "Bilinmeyen")
                await m.answer(f"\"{metin}\"\n— {yazar}")
    except Exception as e:
        await m.answer(f"Üzgünüm, API çağrısında hata oluştu: {e}")

dp.include_router(router)

# Koyeb sağlıklı çalışıyor kabul etsin diye minik bir HTTP sunucu
async def health(_):
    return web.Response(text="ok")

async def main():
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Health server {port} portunda.")

    logging.info("Bot başlıyor (polling)…")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
