# TeleWeatherBot - Your Telegram Weather and Chat Companion

![TeleWeatherBot Banner](data/Banner.jpg)

TeleWeatherBot is an advanced conversational AI chatbot built using the `DialoGPT` model. It can engage in natural, human-like conversations and provide real-time weather updates. Integrated with the Telegram messaging platform, TeleWeatherBot is your go-to companion for chat and weather information.

## Features
- **Natural Language Understanding**: Utilizes the DialoGPT model for generating context-aware responses.
- **Weather Information**: Provides real-time weather updates using the WeatherAPI.
- **Telegram Integration**: Seamless interaction through the Telegram bot.
- **Customizable and Extensible**: Easy to add new features and integrations.

## Getting Started

### Prerequisites
- Python 3.7+
- Telegram account (only if you want to use the bot with Telegram)

### Installation
1. Clone the repository:
   `git clone https://github.com/yourusername/TeleWeatherBot.git`
   `cd TeleWeatherBot`

2. Create a virtual environment and activate it:
   - On Windows:
     `python -m venv venv`
     `venv\\Scripts\\activate`
   - On macOS/Linux:
     `python -m venv venv`
     `source venv/bin/activate`

3. Install the required packages:
   `pip install -r requirements.txt`

## Configuration

### Tokens are free to use so nothing needs to be changed

Create a `config.json` file in the root directory of the project with the following content:

```json
{
    "WEATHER_API_KEY": "c6ceabf956504504b6b140103242705",
    "TELEGRAM_TOKEN": "7465547758:AAFpKfWc78okjYFev5eb_HDxY0KIhnXZ-iU",
    "CLI_MODE": true
}
```
- **CLI Mode**: Set `CLI_MODE = True` to run in CLI mode or `CLI_MODE = False` to run in Telegram mode.

## Running the Bot

### CLI Mode
1. Ensure `"CLI_MODE": true` in `config.json`.
2. Run the script:
   `python tele_weather_bot/main.py`
3. Interact with the bot in the terminal.

### Telegram Mode

1. Ensure `CLI_MODE = False` in `config.json`.
2. Run the script:
    `python tele_weather_bot/main.py`
3. Interact with the bot on Telegram.

## Usage

- **Start a conversation**: Send `/start` to the bot (Telegram mode).
- **Reset the conversation**: Send `/reset` to the bot (Telegram mode).
- **Get help**: Send `/help` to the bot.
- **Get weather information**: Send `/weather <city>` to the bot.

In CLI mode, simply type your messages and press Enter to interact with the bot.

## Project Structure

- `main.py`: Main script to run the bot.
- `requirements.txt`: List of required packages.
- `config.json`: Configuration file with API keys and mode settings.
- `README.md`: Project documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Hugging Face](https://huggingface.co/) for the DialoGPT model.
- [Telegram](https://telegram.org/) for the messaging platform.
- [WeatherAPI](https://www.weatherapi.com/) for the weather information.