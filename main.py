import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot # Importing the Telegram bot API library
import threading
import time
import wikipedia
import requests
import gtts # Import the gtts library
from io import BytesIO
from datetime import datetime
import random


TOKEN = "7764988835:AAGpk8QTewqKAeqkGRRmV2xFeBRBoWM_GrI"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
 bot.send_message(message.chat.id,
 f"{greeting()} Warmest welcome to Malévita!❤️‍🩹 How do you feel today?🫶",
reply_markup=main_menu())

def greeting():
  hour = datetime.now().hour
  if hour < 12:
     return "Good morning!🌻☀️✨ "
  elif hour < 18:
     return "Good afternoon!🌞 "
  else:
     return "Good evening!🌙 "



user_orders = {}

@bot.message_handler(commands=['order'])
def start_order(message):
    user_orders[message.chat.id] = {}
    bot.send_message(message.chat.id, "What are you thinking about?")

@bot.message_handler(func=lambda message: message.chat.id in user_orders and 'product' not in user_orders[message.chat.id])
def order_product(message):
    user_orders[message.chat.id]['product'] = message.text
    bot.send_message(message.chat.id, "How do you feel about this?")

@bot.message_handler(func=lambda message: message.chat.id in user_orders and 'quantity' not in user_orders[message.chat.id])
def order_quantity(message):
    user_orders[message.chat.id]['quantity'] = message.text
    bot.send_message(message.chat.id, "Please share your contact details (phone number, or anything you'd like to be reached at).")

@bot.message_handler(func=lambda message: message.chat.id in user_orders and 'address' not in user_orders[message.chat.id])
def order_address(message):
    user_orders[message.chat.id]['address'] = message.text
    bot.send_message(message.chat.id, "Thank you for your order! We will contact you shortly.")
    order_summary = f"""Order Summary:
    Product: {user_orders[message.chat.id]['product']}
    Quantity: {user_orders[message.chat.id]['quantity']}
    Address: {user_orders[message.chat.id]['address']}
    """

quotes = [
    "The body whispers what the mind cannot bear to hear.",
    "Every thought we think is creating our future, including the future of our health. (Louise Hay)",
    "Unexpressed emotions will never die. They are buried alive and will come forth later in uglier ways. (Sigmund Freud)",
    "The mind is like a garden; what you plant in it will grow in your body.",
    "Your biography becomes your biology. (Caroline Myss) ",
    "Stress, if left unchecked, can manifest as disease. Listen to your body before it screams for help.",
    "Healing begins where the mind surrenders to the wisdom of the body.",
    "Pain that is not transformed is transmitted—to the body, to others, or to the world.",
    "The body keeps score of every unresolved emotion and untold story. (Bessel van der Kolk)",
    "Your body hears everything your mind says. Be kind to yourself.",
    "The body speaks the mind’s unspoken words.",
    "What the mind suppresses, the body expresses.",
    "Healing is not just about the body; it's about the mind learning to let go.",
    "Every emotion you refuse to feel finds a home in your body.",
    "Your body is the autobiography of your soul’s experiences.",
    "The subconscious mind writes its stories on the canvas of the body.",
    "If you listen to your body when it whispers, you won’t have to hear it scream.",
    "Sickness is often the body’s last attempt to get the mind’s attention.",
    "Anxiety held in the mind becomes tension held in the body.",
    "True healing happens when you treat the cause, not just the symptom.",
]
@bot.message_handler(commands=['quote'])
def send_quote(message):
 bot.send_message(message.chat.id, random.choice(quotes))


faq_answers = {
  "Who we are?": "Malevita is a caring non-profit that supports mental well-being across the world. We focus on the deep connection between mind and body, offering gentle and effective ways to heal. Our compassionate team is here to help you through trauma and stress, providing guidance, comfort, and empowerment on your journey to feeling whole again.💙",
   "Why should I trust you?": "Dear, trust is built through experience and understanding. Psychosomatic therapy, as highlighted in the article (here: https://www.intapt.com/why-psychosomatic-therapy) from International Association of Psychosomatic Therapy, emphasizes the deep connection between mind and body. Similarly, I focus on providing insights that align with research and holistic approaches to well-being. If something doesn’t resonate with you, I always encourage curiosity and verification. Let’s explore together☺️.",
  "What are your working hours?": "We try to work 24 hours by 7 days a week.❤️",
  "Where are you located?": "In Tashkent, Uzbelistan. If you want we can meet anywhere. We will orginize it in order you to feel an absolute comfort. ❤️‍🔥",
   "How can I reach you?": "You can call +998946385575 at this number or send a text message. If you want you can also send us an email at disuniterio@gmail.com or via telegram to @disuniter. Feel free to reach. 💓"
}

@bot.message_handler(commands=['faq'])
def send_faq(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for question in faq_answers.keys():
        markup.add(KeyboardButton(question))
    bot.send_message(message.chat.id, "Choose a question:", reply_markup=markup)
    
@bot.message_handler(func=lambda message: message.text in faq_answers)
def faq_answer(message):
 bot.send_message(message.chat.id, faq_answers[message.text])

@bot.message_handler(content_types=['document'])
def handle_document(message):
 bot.send_message(message.chat.id, "Thanks for sending your file! We’ll process it shortly and keep you updated. 😊")






@bot.message_handler(func=lambda message: message.text not in ["Emotional Support",
"Trauma Guidance", "Self-Care", "/start", "/order", "/services", "/remind", "/wiki", "/convert", "/voice", "/contact", "/location", "/order", "/help", "❤ What we can do for you?", "❇️ Call us if you want someone", "ℹ️Who we are?", "Back to Menu"])
def fallback_response(message):
 bot.send_message(message.chat.id, "It's okay if things feel a bit overwhelming. Take your time. 💙 Whenever you're ready, just choose the option that feels right for you—we're here to support you.")

def main_menu():
 markup = ReplyKeyboardMarkup(resize_keyboard=True)
 markup.add(KeyboardButton("❤ What we can do for you?"))
 markup.add(KeyboardButton("❇️ Call us if you want someone"))
 return markup



@bot.message_handler(func=lambda message: message.text == "❤ What we can do for you?")
def show_products(message):
 bot.send_message(message.chat.id, "Take your time—choose the support that feels right for you💜",
reply_markup=product_menu())


def product_menu():
 markup = InlineKeyboardMarkup()
 markup.add(InlineKeyboardButton("🫂Emotional Support", callback_data="Emotional Support"))
 markup.add(InlineKeyboardButton("💔Trauma Guidance", callback_data="Trauma Guidance"))
 markup.add(InlineKeyboardButton("🌿 Self-Care Tips", callback_data="Self-Care"))  # New option


 return markup
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
 if call.data == "Emotional Support":
  try:
   bot.send_photo(call.message.chat.id,
    photo="https://media.istockphoto.com/id/1425842853/vector/human-hand-supports-a-sad-woman-to-get-rid-of-stress-and-depression-concept-of-help-and-care.jpg?s=612x612&w=0&k=20&c=MhZ2KnQBQUIpPhyD5XmHqcm80jqrZWpT9v3ZKTQvh7A=", 
    caption="You are not alone. No matter what you're feeling right now, you deserve kindness, warmth, and support. Take a deep breath—you're in a safe space. Let go of the weight on your shoulders, even just for a moment. You are valued, you are seen, and you are worthy of care. If you need comfort, encouragement, or just a quiet moment of understanding, we're here for you. Always💙")
  except Exception as e:
   bot.send_message(call.message.chat.id, "You're not alone. We're here for you. If you need a listening ear, encouragement, or just a moment of kindness, take a deep breath—you're in a safe space. 💙")
   print(f"Error sending photo: {e}")
 elif call.data == "Trauma Guidance":
  try:
   bot.send_photo(call.message.chat.id,
    photo="https://imgur.com/a/0awCIZZ", 
    caption="Healing is a journey, and support makes all the difference. Here are some helpful resources to guide you through this process. You are not alone. We're here for you. If you need a listening ear, encouragement, or just a moment of kindness, take a deep breath—you're in a safe space. 💜")
  except Exception as e:
   bot.send_message(call.message.chat.id, "We're here for you. If you need a listening ear, encouragement, or just a moment of kindness, take a deep breath—you're in a safe space. 💜")
   print(f"Error sending photo: {e}")
 elif call.data == "Self-Care":  # New option
  try:
   bot.send_photo(call.message.chat.id,
    photo="https://imgur.com/a/ibIO3hF",
    caption="Taking care of yourself is important. Here are some self-care tips to help you feel better and recharge. 🌿💖")
  except Exception as e:
   bot.send_message(call.message.chat.id, "Taking care of yourself is important. Here are some self-care tips to help you feel better and recharge. 🌿💖")
   print(f"Error sending photo: {e}")






@bot.message_handler(commands=['help']) 
def help_command(message):
 bot.send_message(message.chat.id, "List of available commands:\n"
                                   "/start - Start the bot\n" "/order - Place an order\n"
                                   "/services - See available propositions\n"
                                   "/quote - Get a random quote\n"
                                   "/remind - Set a reminder\n"
                                   "/wiki - Search from Wikipedia\n"
                                   "/convert - Convert a currency into yours\n"
                                   "/voice - Text-to-Speech (Voice Messages)\n"
                                   "/contact - Contact information\n" 
                                   "/location - Get store location\n" 
                                   "/order - Order a free consultation\n"
                                   "/feedback - Give us your feedback\n" 
                                   "/faq - Frequently Asked Questions\n"
                                   "/help - Get list of commands")


@bot.message_handler(commands=['contact'])
def send_contact_info(message):
 bot.send_message(message.chat.id, 
    "📞Phone: +998946385575\n 💌Mail: disuniterio@gmail.com\n📍Address: University St 1/3, Salar, Tashkent region, Uzbekistan")


@bot.message_handler(commands=['order'])
def order_process(message):
 bot.send_message(message.chat.id, "Please select a product and send its name.")


@bot.message_handler(commands=['location'])
def send_location(message):
 bot.send_location(message.chat.id, latitude=41.380650,longitude=69.352261)


def reminder(chat_id, text, delay):
 time.sleep(delay)
 bot.send_message(chat_id, f" Reminder: {text}")
@bot.message_handler(commands=['remind'])
def set_reminder(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.reply_to(message, "Format: /remind <time in seconds> <message>")
        return
    try:
        delay = int(parts[1])
        text = parts[2]
        threading.Thread(target=reminder, args=(message.chat.id, text, delay)).start()
        bot.reply_to(message, f"✅ Reminder set for {delay} seconds.")
    except ValueError:
        bot.reply_to(message, "Error! Time must be a number.")


@bot.message_handler(commands=['wiki'])
def wiki_search(message):
    wikipedia.set_lang("en")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Format: /wiki <query>")
        return
    query = parts[1]
    try:
        summary = wikipedia.summary(query, sentences=2)
        bot.reply_to(message, f"{summary}")
    except wikipedia.exceptions.PageError:
        bot.reply_to(message, "❌ No results found.")


@bot.message_handler(commands=['convert'])
def currency_converter(message):
    parts = message.text.split()
    if len(parts) != 4:
        bot.reply_to(message, "Format: /convert <amount> <from currency> <to currency> (e.g., /convert 100 USD EUR)")
        return
    amount, from_currency, to_currency = parts[1], parts[2].upper(), parts[3].upper()
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url).json()
    if "rates" in response and to_currency in response["rates"]:
        rate = response["rates"][to_currency]
        converted_amount = round(float(amount) * rate, 2)
        bot.reply_to(message, f"{amount} {from_currency} = {converted_amount} {to_currency}")
    else:
        bot.reply_to(message, "Error! Check the currency codes.")


@bot.message_handler(commands=['voice'])
def send_voice_message(message):
    text = message.text.replace('/voice ', '')
    if not text:
        bot.reply_to(message, "Enter text after /voice command")
        return
    tts = gtts.gTTS(text, lang="en")
    voice = BytesIO()
    tts.write_to_fp(voice)
    voice.seek(0)
    bot.send_voice(message.chat.id, voice)


def contactus_button():
 markup = ReplyKeyboardMarkup(resize_keyboard=True,
one_time_keyboard=True)
 markup.add(KeyboardButton("📍Share Location", request_location=True))
 markup.add(KeyboardButton("📞Share Contact", request_contact=True))
 markup.add(KeyboardButton("🔙Back to Menu")) # Добавлена кнопка возврата в меню
 return markup

@bot.message_handler(func=lambda message: message.text == "❇️ Call us if you want someone")
def request_location(message):
 bot.send_message(message.chat.id, "Please share your location or go back to menu:", reply_markup= contactus_button())

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
 bot.send_message(message.chat.id, "Thank you for sharing your contact!",
reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "Back to Menu")
def back_to_menu(message):
 bot.send_message(message.chat.id, "Returning to main menu.",
reply_markup=main_menu())
@bot.message_handler(content_types=['location'])
def handle_location(message):
 bot.send_message(message.chat.id, "Thank you for sharing your location!", reply_markup=main_menu())



bot.polling(none_stop=True)
