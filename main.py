
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

CHOOSING, QUESTIONS, CONTACT = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['🤖 Хочу ассистента']]
    await update.message.reply_text(
        "👋 Привет! Вы в LDN AI Studio.\n\n"
        "Мы создаём ИИ-ассистентов для Telegram, сайтов и бизнеса:\n"
        "– Умные чат-боты\n– Автоматизация процессов\n"
        "– Интеграции с CRM, доставкой, Notion, Google Sheets\n"
        "– Индивидуальные решения под задачи клиента\n\n"
        "Хочешь узнать, подойдёт ли ИИ для твоего бизнеса?\n"
        "Нажми кнопку ниже 👇",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CHOOSING

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Отлично! Чтобы предложить вам лучшее решение, уточню пару моментов 👇\n\n"
        "1️⃣ Где вы хотите использовать ассистента?\n"
        "(например: Telegram, сайт, WhatsApp, CRM...)\n\n"
        "2️⃣ Что он должен уметь делать?\n"
        "(принимать заказы, оформлять доставку, вести диалог, давать консультации и т.д.)\n\n"
        "3️⃣ Нужны ли вам интеграции?\n"
        "(например: с Новой Почтой, Google Таблицей, Bitrix24...)\n\n"
        "4️⃣ Что особенно важно в работе ассистента?\n"
        "(скорость, точность, индивидуальные ответы и т.д.)\n\n"
        "✍️ Напишите ответ на эти вопросы одним сообщением или по отдельности."
    )
    return QUESTIONS

async def handle_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['answers'] = update.message.text
    await update.message.reply_text(
        "Спасибо! Теперь оставьте, пожалуйста, ваши данные — и мы свяжемся с вами:\n\n"
        "– Имя\n– Telegram @юзернейм или номер телефона\n– Удобное время для связи"
    )
    return CONTACT

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers = context.user_data.get('answers', '')
    contact_info = update.message.text
    summary = f"🧾 Новый запрос:\n\n📌 Ответы:\n{answers}\n\n📇 Контакты:\n{contact_info}"
    
    await update.message.reply_text("✅ Спасибо! Мы скоро с вами свяжемся.")
    await update.message.reply_text(summary)
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Разговор отменён.")
    return ConversationHandler.END

def main():
    import os
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(filters.Regex('^(🤖 Хочу ассистента)$'), handle_choice)],
            QUESTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_questions)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_contact)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)
    print("Бот запущен")
    app.run_polling()

if __name__ == '__main__':
    main()
