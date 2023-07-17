# Lvl Bot

Lvl Bot is a Telegram bot that calculates support and resistance lines for a given ticker and broker. It uses the `calculate_levels` function to calculate the levels and sends the result along with a chart to the user.

## Getting Started

To use the bot, you need to have a Telegram account and create a new bot using the [BotFather](https://core.telegram.org/bots#6-botfather) bot. Once you have created the bot, you will receive a token that you can use to authenticate with the Telegram API.

### Prerequisites

To run the bot, you need to have Python 3 installed on your system. You also need to install the following packages:

- `python-telegram-bot`
- `pandas`
- `mplfinance`

You can install these packages using `pip`:

```
pip install python-telegram-bot pandas mplfinance
```

### Installing

To install the bot, you need to follow these steps:

1. Clone the repository to your local machine:
```
git clone https://github.com/your_username/lvl_bot.git
```
2. Navigate to the `lvl_bot` directory:
```
cd lvl_bot
```
3. Create a new virtual environment:
```
python3 -m venv venv
```
4. Activate the virtual environment:
```
source venv/bin/activate
```
5. Install the required packages:
```
pip install -r requirements.txt
```
6. Create a new file named `.env` in the root directory of the project and add the following line:
```
TELEGRAM_TOKEN=your_telegram_token_here
```
7. Replace `your_telegram_token_here` with your actual Telegram bot token.
8. Run the bot:
```
python lvl_bot.py
```

## Usage

To use the bot, you need to send a message to the bot in the following format:

```
/lvl ticker broker [timeframe]
```

- `ticker`: The ticker symbol of the stock or asset you want to calculate the levels for.
- `broker`: The broker you are using to trade the stock or asset.
- `timeframe` (optional): The timeframe you want to use for the calculation. The default value is `1D`. Possible values are: `1M`, `1W`, `1D`, `4H`, `2H`, `1H`, `30`, `15`, `5`, `1`.

For example, to calculate the levels for the stock `SW20` with the broker `CAPITALCOM` using a timeframe of `1D`, you would send the following message to the bot:

```
/lvl SW20 CAPITALCOM 1D
```

## Contributing

If you want to contribute to the project, you can fork the repository and create a new branch for your changes. Once you have made your changes, you can create a pull request to merge your changes into the main branch.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.