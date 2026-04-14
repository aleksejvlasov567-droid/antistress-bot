import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== НАСТРОЙКИ ==========
# Вставь сюда токен, который прислал BotFather
TOKEN = "8579382672:AAGIJ7z2dx886_vqaqf-8KEJy3RydywT38g"

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
        "• Рассказывать о природе стресса\n\n"
        "Если что-то не работает — напиши /start для перезапуска."
    )
    await update.message.reply_text(help_text)

# ========== ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # ---------- РАЗДЕЛ "УПРАЖНЕНИЯ" ----------
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
    
    # ---------- РАЗДЕЛ "МУЗЫКА" ----------
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
            "🎧 Lofi — спокойный бит для учёбы и отдыха\n"
            "🌧 Дождь — природные звуки для расслабления\n"
            "🎹 Фортепиано — нежная инструментальная музыка",
            reply_markup=reply_markup
        )
    
    # ---------- РАЗДЕЛ "О СТРЕССЕ" ----------
    elif data == 'info':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        info_text = (
            "📘 ЧТО ТАКОЕ СТРЕСС?\n\n"
            "Стресс — это реакция организма на нагрузку. "
            "В небольших дозах он полезен, но если напряжение копится, это вредит здоровью.\n\n"
            "🚨 ПРИЗНАКИ СТРЕССА:\n"
            "• Трудно сосредоточиться\n"
            "• Быстрая утомляемость\n"
            "• Раздражительность\n"
            "• Проблемы со сном\n\n"
            "💡 ЧТО ДЕЛАТЬ?\n"
            "1. Дыши медленно (попробуй упражнение в боте)\n"
            "2. Слушай спокойную музыку\n"
            "3. Переключай внимание на тело и органы чувств\n\n"
            "Этот бот создан, чтобы помочь тебе быстро прийти в себя 💙"
        )
        await query.edit_message_text(info_text, reply_markup=reply_markup)
    
    # ---------- ВОЗВРАТ В ГЛАВНОЕ МЕНЮ ----------
    elif data == 'back_to_main':
        keyboard = [
            [InlineKeyboardButton("🧠 Упражнения", callback_data='exercises')],
            [InlineKeyboardButton("🎵 Слушать музыку", callback_data='music_menu')],
            [InlineKeyboardButton("ℹ️ О стрессе", callback_data='info')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "👋 Главное меню. Выбери раздел:",
            reply_markup=reply_markup
        )
    
    # ---------- УПРАЖНЕНИЕ: КВАДРАТНОЕ ДЫХАНИЕ ----------
    elif data == 'breath':
        breath_text = (
            "🫁 КВАДРАТНОЕ ДЫХАНИЕ\n\n"
            "Это простая техника, которая быстро успокаивает нервную систему.\n\n"
            "📋 ИНСТРУКЦИЯ:\n"
            "1️⃣ ВДОХ через нос — считай до 4\n"
            "2️⃣ ЗАДЕРЖКА дыхания — считай до 4\n"
            "3️⃣ ВЫДОХ через рот — считай до 4\n"
            "4️⃣ ЗАДЕРЖКА дыхания — считай до 4\n\n"
            "🔄 Повтори 4–5 раз.\n\n"
            "⏱ Это займёт всего 1–2 минуты. Сделай прямо сейчас!"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Готово, хочу ещё упражнение", callback_data='exercises')],
            [InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(breath_text, reply_markup=reply_markup)
    
    # ---------- УПРАЖНЕНИЕ: 5-4-3-2-1 ----------
    elif data == 'grounding':
        grounding_text = (
            "👁 ТЕХНИКА 5-4-3-2-1 (ЗАЗЕМЛЕНИЕ)\n\n"
            "Это упражнение помогает вернуться в настоящий момент, когда тревожно или паника.\n\n"
            "📋 ПОСМОТРИ ВОКРУГ И НАЗОВИ:\n"
            "5️⃣ ПЯТЬ предметов, которые ты ВИДИШЬ (лампа, книга, окно...)\n"
            "4️⃣ ЧЕТЫРЕ вещи, которые ты можешь ПОТРОГАТЬ (стол, одежда, телефон...)\n"
            "3️⃣ ТРИ звука, которые ты СЛЫШИШЬ (гул улицы, дыхание, тиканье часов...)\n"
            "2️⃣ ДВА запаха, которые ты ЧУВСТВУЕШЬ (кофе, воздух, духи...)\n"
            "1️⃣ ОДИН вкус, который ты ощущаешь во рту (или сделай глоток воды)\n\n"
            "💭 После этого тревога обычно снижается. Попробуй!"
        )
        keyboard = [
            [InlineKeyboardButton("✅ Готово, хочу ещё упражнение", callback_data='exercises')],
            [InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(grounding_text, reply_markup=reply_markup)
    
    # ---------- УПРАЖНЕНИЕ: СКАНЕР ТЕЛА ----------
    elif data == 'body_scan':
        body_text = (
            "🧍 СКАНЕР ТЕЛА\n\n"
            "Упражнение для расслабления мышц, которые зажаты от стресса.\n\n"
            "📋 ИНСТРУКЦИЯ:\n"
            "Сядь удобно, закрой глаза и медленно пройдись вниманием по телу.\n\n"
            "👣 Ступни — расслабь пальцы ног\n"
            "🦵 Ноги — почувствуй, как они тяжелеют\n"
            "🍑 Таз и поясница — отпусти напряжение\n"
            "🤲 Живот и грудь — дыши спокойно\n"
            "💪 Плечи и руки — опусти плечи вниз\n"
            "🧠 Шея и лицо — разожми челюсть, расслабь лоб\n\n"
            "⏱ Удели этому 2–3 минуты. Ты почувствуешь, как тело становится мягче и теплее."
        )
        keyboard = [
            [InlineKeyboardButton("✅ Готово, хочу ещё упражнение", callback_data='exercises')],
            [InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(body_text, reply_markup=reply_markup)
    
    # ---------- ОТПРАВКА МУЗЫКИ: LOFI ----------
    elif data == 'music_lofi':
        await query.edit_message_text("🎧 Отправляю Lofi трек... Подожди секунду.")
        audio_path = os.path.join(os.getcwd(), 'music', 'lofi1.mp3')
        try:
            with open(audio_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio,
                    title="Lofi Hip Hop для учёбы и отдыха",
                    performer="AntiStress Flow"
                )
            keyboard = [[InlineKeyboardButton("🔙 В меню музыки", callback_data='music_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="🎵 Трек отправлен! Приятного прослушивания.",
                reply_markup=reply_markup
            )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="❌ Ошибка: музыкальный файл не найден. Проверь папку music."
            )
    
    # ---------- ОТПРАВКА МУЗЫКИ: ДОЖДЬ ----------
    elif data == 'music_rain':
        await query.edit_message_text("🌧 Отправляю звуки дождя... Подожди секунду.")
        audio_path = os.path.join(os.getcwd(), 'music', 'rain.mp3')
        try:
            with open(audio_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio,
                    title="Звуки дождя для сна и релаксации",
                    performer="AntiStress Flow"
                )
            keyboard = [[InlineKeyboardButton("🔙 В меню музыки", callback_data='music_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="🌧 Трек с дождём отправлен. Расслабляйся!",
                reply_markup=reply_markup
            )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="❌ Ошибка: музыкальный файл не найден."
            )
    
    # ---------- ОТПРАВКА МУЗЫКИ: ФОРТЕПИАНО ----------
    elif data == 'music_piano':
        await query.edit_message_text("🎹 Отправляю фортепианную музыку... Подожди секунду.")
        audio_path = os.path.join(os.getcwd(), 'music', 'piano.mp3')
        try:
            with open(audio_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio,
                    title="Нежное фортепиано для души",
                    performer="AntiStress Flow"
                )
            keyboard = [[InlineKeyboardButton("🔙 В меню музыки", callback_data='music_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="🎹 Фортепианный трек отправлен. Приятного прослушивания!",
                reply_markup=reply_markup
            )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="❌ Ошибка: музыкальный файл не найден."
            )
# ========== ЗАПУСК БОТА ==========
# ========== ЗАПУСК БОТА С ПРОКСИ ==========
def main():
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Бот запущен и готов к работе...")
    app.run_polling()

if __name__ == '__main__':
    main()
            
