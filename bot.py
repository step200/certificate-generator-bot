from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import cert_generator

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🎓 Сгенерировать сертификат"))
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "🎓 **Привет! Я бот-генератор сертификатов и дипломов.**\n\n"
        "Я могу сгенерировать брендированный сертификат об окончании курса.\n\n"
        "Нажми **«🎓 Сгенерировать сертификат»**, чтобы начать!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())


@bot.message_handler(func=lambda msg: msg.text == "🎓 Сгенерировать сертификат")
def start_cert_creation(message):
    msg = bot.send_message(message.chat.id, "Введи **ФИО участника** (например: `Иванов Петр Алексеевич`):", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    name = message.text.strip()
    msg = bot.send_message(message.chat.id, "Укажи **название курса** (например: `Разработка на Python и Telebot`):", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_course, name)

def process_course(message, name):
    course = message.text.strip()
    date_str = datetime.now().strftime("%d.%m.%Y")

    bot.send_message(message.chat.id, "⏳ Генерирую сертификат высокого качества...")

    try:
        cert_buffer = cert_generator.generate_certificate_image(name, course, date_str)
        
        caption = (
            f"✅ **Сертификат успешно сформирован!**\n\n"
            f"👤 **Выпускник:** {name}\n"
            f"📚 **Курс:** {course}\n"
            f"📅 **Дата:** {date_str}"
        )
        
        cert_buffer.name = "certificate.png"
        
        bot.send_document(
            message.chat.id,
            document=cert_buffer,
            caption=caption,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка генерации: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка при генерации сертификата.")

if __name__ == '__main__':
    print("Бот-генератор сертификатов запущен...")
    bot.infinity_polling()