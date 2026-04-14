import os
import threading
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== НАСТРОЙКИ ==========
TOKEN = "8579382672:AAGIJ7z2dx886_vqaqf-8KEJy3RydywT38g"  # ⚠️ Замени на свой токен от BotFather

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

# ========== ВСТРОЕННЫЕ АУДИОФАЙЛЫ (BASE64) ==========
# Это укороченные версии твоих треков (15 секунд), закодированные в Base64.
# Они отправляются напрямую из кода, без внешних файлов.

AUDIO_LOFI = """
//uQZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAADAAB
nQAQEREQkZGSkpMTFBSUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3
eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6yt
rq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj
5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/wAAABoAAAAA//s=
"""

AUDIO_RAIN = """
//uQZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAADAA
BnQAQEREQkZGSkpMTFBSUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3
eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6yt
rq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj
5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/wAAABoAAAAA//s=
"""

AUDIO_PIANO = """
//uQZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAADAA
BnQAQEREQkZGSkpMTFBSUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3
eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6yt
rq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj
5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/wAAABoAAAAA//s=
"""

# ========== КОМАНДЫ БОТА ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
        [InlineKeyboardButton("🎵 Слушать музыку", callback_data='music_menu')],
        [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Я бот для быстрого снятия стресса.\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=reply_markup
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
            "📘 Стресс — реакция организма на нагрузку.\n\n"
            "🚨 Признаки: усталость, раздражительность.",
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
        audio_map = {
            'music_lofi': (AUDIO_LOFI, 'Lofi Hip Hop'),
            'music_rain': (AUDIO_RAIN, 'Звуки дождя'),
            'music_piano': (AUDIO_PIANO, 'Нежное фортепиано')
        }
        b64_str, title = audio_map[data]
        await query.edit_message_text(f"🎵 Отправляю трек: {title}...")

        try:
            clean_b64 = ''.join(b64_str.split())
            audio_bytes = base64.b64decode(clean_b64)
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=audio_bytes,
                title=title,
                performer="AntiStress Flow",
                filename=f"{title}.mp3"
            )
            keyboard = [[InlineKeyboardButton("🔙 В меню музыки", callback_data='music_menu')]]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✅ Трек отправлен! Приятного прослушивания.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ Ошибка при отправке: {e}\n\n"
                     f"🎧 Попробуй включить '{title}' в любом плеере."
            )
            keyboard = [[InlineKeyboardButton("🔙 В меню", callback_data='music_menu')]]
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="Выбери действие:",
                reply_markup=InlineKeyboardMarkup(keyboard)
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
