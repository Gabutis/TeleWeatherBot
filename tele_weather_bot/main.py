import logging
import requests
import asyncio
import json
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline, Conversation, AutoTokenizer

with open('../config.json') as config_file:
    config = json.load(config_file)

WEATHER_API_KEY = config['WEATHER_API_KEY']
TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
CLI_MODE = config['CLI_MODE']

chatbot = pipeline('conversational', model='microsoft/DialoGPT-medium')
tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger('httpx').setLevel(logging.WARNING)

user_conversations = {}


def handle_commands_query():
    commands_list = [
        "/start - Start a conversation",
        "/reset - Reset the conversation",
        "/help - Get help information",
        "/weather <city> - Get weather information for a city"
    ]
    return "Here are some things I can do:\n" + "\n".join(commands_list)


def get_weather(city: str) -> str:
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['current']['condition']['text']
        temp = data['current']['temp_c']
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't get the weather information right now."


async def handle_message(user_input: str, user_id: int) -> str:
    if any(keyword in user_input.lower() for keyword in ["commands", "what can you do", "help"]):
        return handle_commands_query()

    if user_input.lower().startswith("/weather"):
        try:
            city = user_input.split(" ", 1)[1]
            return get_weather(city)
        except IndexError:
            return "Please specify a city. Usage: /weather <city>"

    if "weather" in user_input.lower():
        return "Please use the command /weather <city> to get weather information."

    if user_id not in user_conversations:
        user_conversations[user_id] = {'conversation': Conversation(), 'history': []}

    conversation_data = user_conversations[user_id]
    conversation = conversation_data['conversation']
    conversation.add_user_input(user_input)

    try:
        response = chatbot(conversation, pad_token_id=tokenizer.eos_token_id)
        bot_response = response.generated_responses[-1]

        conversation_data['history'].append(bot_response)

        if len(conversation_data['history']) > 3:
            if len(set(conversation_data['history'][-3:])) == 1:
                bot_response = "I'm sorry, can you please ask something else?"
                conversation_data['conversation'] = Conversation()
                conversation_data['history'] = []

        if len(conversation_data['history']) > 20:
            conversation_data['conversation'] = Conversation()
            conversation_data['history'] = []

        if not bot_response.strip():
            bot_response = "I'm sorry, I didn't understand that. Can you ask something else?"

    except Exception as e:
        bot_response = "Sorry, I couldn't process that. Please try again."
        logger.error(f"Error in chatbot response: {e}")

    return bot_response


def chat_with_bot_cli():
    print("Chat with TeleWeatherBot! Type 'exit' to end the conversation.")
    user_id = "cli_user"  # Use a fixed user ID for CLI mode
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        bot_response = asyncio.run(handle_message(user_input, user_id))
        print("Bot:", bot_response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f'Update {update} caused error {context.error}')
    await update.message.reply_text('An error occurred. Please try again later.')


def main():
    if CLI_MODE:
        chat_with_bot_cli()
    else:
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await update.message.reply_text('Hi! I am your GPT-based chatbot. How can I help you today?')

        async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            user_id = update.message.from_user.id
            user_conversations.pop(user_id, None)
            await update.message.reply_text('Conversation reset. How can I help you today?')

        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            help_text = handle_commands_query()
            await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

        async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            user_id = update.message.from_user.id
            user_input = update.message.text
            bot_response = await handle_message(user_input, user_id)
            await update.message.reply_text(bot_response)

        async def handle_weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            user_id = update.message.from_user.id
            user_input = update.message.text
            bot_response = await handle_message(user_input, user_id)
            await update.message.reply_text(bot_response)

        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("reset", reset))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("weather", handle_weather_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))

        application.add_error_handler(error_handler)

        logger.info("Bot started")
        application.run_polling()


if __name__ == '__main__':
    main()
