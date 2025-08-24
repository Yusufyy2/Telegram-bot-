import telebot, requests

BOT_TOKEN = "6222500287:AAENdFeT-prd6l4E08hPSmanf8sM1jmdKTk"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['tc'])
def tc_sorgu(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "TC giriniz: /tc 11111111110")
            return
        tc = args[1]
        url = f"https://api.kahin.org/kahinapi/tc?tc={tc}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/127.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        data = r.json()["data"][0]
        cevap = f"""
<b>TC:</b> {data['TC']}
<b>Adı:</b> {data['ADI']}
<b>Soyadı:</b> {data['SOYADI']}
<b>Doğum Tarihi:</b> {data['DOGUMTARIHI']}
<b>Nüfus İl:</b> {data['NUFUSIL']}
<b>Nüfus İlçe:</b> {data['NUFUSILCE']}
<b>Anne Adı:</b> {data['ANNEADI']}
<b>Anne TC:</b> {data['ANNETC']}
<b>Baba Adı:</b> {data['BABAADI']}
<b>Baba TC:</b> {data['BABATC']}
"""
        bot.reply_to(message, cevap)
    except:
        bot.reply_to(message, "Sorgu başarısız.")

bot.infinity_polling()
