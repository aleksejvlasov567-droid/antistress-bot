import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== НАСТРОЙКИ ==========
TOKEN = "8579382672:AAGIJ7z2dx886_vqaqf-8KEJy3RydywT38g"  

# ========== HTTP-СЕРВЕР ДЛЯ RENDER HEALTH CHECK ==========
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

# ========== КОМАНДЫ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
        [InlineKeyboardButton("🎵 Слушать музыку", callback_data='music_menu')],
        [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
    ]
    await update.message.reply_text(
        "👋 Привет! Выбери раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start — меню\n/help — помощь")

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
            "📘 Стресс — реакция на нагрузку.\n🚨 Признаки: усталость, раздражительность.",
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
        music_map = {
            'music_lofi': ('lofi1.mp3', 'Lofi Hip Hop'),
            'music_rain': ('rain.mp3', 'Звуки дождя'),
            'music_piano': ('piano.mp3', 'Нежное фортепиано')
        }
        filename, title = music_map[data]
        await query.edit_message_text(f"🎵 Отправляю: {title}...")

        # Путь к файлу в Docker-контейнере
        audio_path = os.path.join(os.path.dirname(__file__), 'music', filename)

        try:
            with open(audio_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio,
                    title=title,
                    performer="AntiStress Flow"
                )
            keyboard = [[InlineKeyboardButton("🔙 В меню", callback_data='music_menu')]]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✅ Готово!",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Файл {filename} не найден.\nПроверь папку music на GitHub."
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
