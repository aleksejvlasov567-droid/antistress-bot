import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== НАСТРОЙКИ ==========
TOKEN = "8579382672:AAGIJ7z2dx886_vqaqf-8KEJy3RydywT38g"  # ⚠️ Замени на токен от BotFather

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
    print(f"✅ Health check сервер запущен на порту {port}")
    server.serve_forever()

# ========== КОМАНДА /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
        [InlineKeyboardButton("🎵 Слушать музыку", callback_data='music_menu')],
        [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 Привет! Я бот для быстрого снятия стресса.\n\n"
        "Выбери, что хочешь сделать:\n"
        "🧠 Упражнения — дыхание и техники заземления\n"
        "🎵 Музыка — спокойные треки для отдыха\n"
        "ℹ️ О стрессе — короткая информация"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# ========== КОМАНДА /help ==========
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 ПОМОЩЬ ПО БОТУ\n\n"
        "/start — открыть главное меню\n"
        "/help — показать это сообщение\n\n"
        "🤖 Что умеет бот:\n"
        "• Показывать дыхательные упражнения\n"
        "• Отправлять спокойную музыку\n"
        "• Рассказывать о природе стресса"
    )
    await update.message.reply_text(help_text)

# ========== ОБРАБОТЧИК КНОПОК ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- Упражнения ---
    if data == 'exercises':
        keyboard = [
            [InlineKeyboardButton("🫁 Квадратное дыхание", callback_data='breath')],
            [InlineKeyboardButton("👁 Техника 5-4-3-2-1", callback_data='grounding')],
            [InlineKeyboardButton("🧍 Сканер тела", callback_data='body_scan')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🧠 Выбери упражнение:\n\n"
            "🫁 Квадратное дыхание — успокаивает за 1 минуту\n"
            "👁 5-4-3-2-1 — помогает при тревоге и панике\n"
            "🧍 Сканер тела — расслабляет мышцы",
            reply_markup=reply_markup
        )

    # --- Меню музыки ---
    elif data == 'music_menu':
        keyboard = [
            [InlineKeyboardButton("🎧 Lofi Hip Hop", callback_data='music_lofi')],
            [InlineKeyboardButton("🌧 Звуки дождя", callback_data='music_rain')],
            [InlineKeyboardButton("🎹 Спокойное фортепиано", callback_data='music_piano')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎵 Выбери тип музыки:\n\n"
            "🎧 Lofi — спокойный бит\n"
            "🌧 Дождь — звуки природы\n"
            "🎹 Фортепиано — нежная музыка",
            reply_markup=reply_markup
        )

    # --- Информация о стрессе ---
    elif data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        info_text = (
            "📘 ЧТО ТАКОЕ СТРЕСС?\n\n"
            "Стресс — это реакция организма на нагрузку.\n\n"
            "🚨 ПРИЗНАКИ:\n"
            "• Трудно сосредоточиться\n"
            "• Быстрая утомляемость\n"
            "• Раздражительность\n\n"
            "💡 ЧТО ДЕЛАТЬ?\n"
            "1. Дыши медленно\n"
            "2. Слушай спокойную музыку\n"
            "3. Переключай внимание"
        )
        await query.edit_message_text(info_text, reply_markup=reply_markup)

    # --- Назад в главное меню ---
    elif data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
            [InlineKeyboardButton("🎵 Слушать музыку", callback_data='music_menu')],
            [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("👋 Главное меню:", reply_markup=reply_markup)

    # --- Упражнение: Квадратное дыхание ---
    elif data == 'breath':
        text = (
            "🫁 КВАДРАТНОЕ ДЫХАНИЕ\n\n"
            "1️⃣ ВДОХ через нос — 4 секунды\n"
            "2️⃣ ЗАДЕРЖКА — 4 секунды\n"
            "3️⃣ ВЫДОХ через рот — 4 секунды\n"
            "4️⃣ ЗАДЕРЖКА — 4 секунды\n\n"
            "🔄 Повтори 4–5 раз."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Готово", callback_data='exercises')],
            [InlineKeyboardButton("🔙 В меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    # --- Упражнение: 5-4-3-2-1 ---
    elif data == 'grounding':
        text = (
            "👁 ТЕХНИКА 5-4-3-2-1\n\n"
            "Найди вокруг:\n"
            "5️⃣ ПЯТЬ предметов\n"
            "4️⃣ ЧЕТЫРЕ ощущения\n"
            "3️⃣ ТРИ звука\n"
            "2️⃣ ДВА запаха\n"
            "1️⃣ ОДИН вкус"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Готово", callback_data='exercises')],
            [InlineKeyboardButton("🔙 В меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    # --- Упражнение: Сканер тела ---
    elif data == 'body_scan':
        text = (
            "🧍 СКАНЕР ТЕЛА\n\n"
            "Расслабь по очереди:\n"
            "👣 Ступни\n"
            "🦵 Ноги\n"
            "🍑 Поясницу\n"
            "🤲 Живот и грудь\n"
            "💪 Плечи и руки\n"
            "🧠 Лицо и челюсть"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Готово", callback_data='exercises')],
            [InlineKeyboardButton("🔙 В меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    # --- Отправка музыки ---
    elif data.startswith('music_'):
        music_map = {
            'music_lofi': 'https://www.chosic.com/wp-content/uploads/2021/07/purrple-cat-equinox.mp3',
            'music_rain': 'https://www.chosic.com/wp-content/uploads/2021/04/rain.mp3',
            'music_piano': 'https://www.chosic.com/wp-content/uploads/2021/04/soft-piano.mp3'
        }
        url = music_map[data]
        await query.edit_message_text("🎵 Отправляю трек...")
        await context.bot.send_audio(
            chat_id=query.message.chat_id,
            audio=url,
            title="AntiStress Flow"
        )
        keyboard = [[InlineKeyboardButton("🔙 В меню музыки", callback_data='music_menu')]]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✅ Трек отправлен!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
# ========== ЗАПУСК ==========
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
