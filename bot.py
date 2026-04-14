import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8579382672:AAGIJ7z2dx886_vqaqf-8KEJy3RydywT38g"

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"✅ Health check на порту {port}")
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
        [InlineKeyboardButton("🎵 Слушать музыку", callback_data='music_menu')],
        [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
    ]
    await update.message.reply_text(
        "👋 Привет! Я бот для быстрого снятия стресса.\n\nВыбери, что хочешь сделать:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start — главное меню\n/help — помощь")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'exercises':
        keyboard = [
            [InlineKeyboardButton("🫁 Квадратное дыхание", callback_data='breath')],
            [InlineKeyboardButton("👁 5-4-3-2-1", callback_data='grounding')],
            [InlineKeyboardButton("🧍 Сканер тела", callback_data='body_scan')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        await query.edit_message_text("Выбери упражнение:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'music_menu':
        keyboard = [
            [InlineKeyboardButton("🎧 Lofi", callback_data='music_lofi')],
            [InlineKeyboardButton("🌧 Дождь", callback_data='music_rain')],
            [InlineKeyboardButton("🎹 Фортепиано", callback_data='music_piano')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        await query.edit_message_text("Выбери музыку:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]]
        await query.edit_message_text(
            "📘 Стресс — реакция организма на нагрузку.\n\n🚨 Признаки: усталость, раздражительность.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
            [InlineKeyboardButton("🎵 Музыка", callback_data='music_menu')],
            [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
        ]
        await query.edit_message_text("Главное меню:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'breath':
        text = "🫁 Вдох 4 сек — задержка 4 сек — выдох 4 сек — задержка 4 сек. Повтори 4-5 раз."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='exercises')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'grounding':
        text = "👁 Найди: 5 предметов, 4 ощущения, 3 звука, 2 запаха, 1 вкус."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='exercises')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == 'body_scan':
        text = "🧍 Расслабь ступни, ноги, поясницу, живот, плечи, лицо."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='exercises')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith('music_'):
        # Проверенные рабочие ссылки
        music_urls = {
            'music_lofi': 'https://www.chosic.com/wp-content/uploads/2021/07/purrple-cat-equinox.mp3',
            'music_rain': 'https://cdn.pixabay.com/download/audio/2022/03/10/audio_c8c8a73467.mp3',
            'music_piano': 'https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0c6a5d5c2.mp3'
        }
        await query.edit_message_text("🎵 Отправляю трек...")
        try:
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=music_urls[data],
                title="AntiStress Flow"
            )
            keyboard = [[InlineKeyboardButton("🔙 В меню музыки", callback_data='music_menu')]]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✅ Трек отправлен!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Ошибка: {e}"
            )

def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
