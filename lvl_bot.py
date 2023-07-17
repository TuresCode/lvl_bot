from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import time
from dotenv import load_dotenv
import os
load_dotenv()
telegram_token = os.getenv('telegram_token')

tv=TvDatafeed()
def get_support_resistance(ticker, broker, interval=Interval.in_daily): #if no arg is given, the default is daily
    #get all intervals and annotate the correct one eg. 1D for Interval.in_daily etc
    if interval == '1':
        interval = Interval.in_1_minute
    if interval == '5':
        interval = Interval.in_5_minute
    if interval == '15':
        interval = Interval.in_15_minute
    if interval == '30':
        interval = Interval.in_30_minute
    if interval == '1H':
        interval = Interval.in_1_hour
    if interval == '2H':
        interval = Interval.in_2_hour
    if interval == '4H':
        interval = Interval.in_4_hour
    if interval == '1D':
        interval = Interval.in_daily
    if interval == '1W':
        interval = Interval.in_weekly
    if interval == '1M':
        interval = Interval.in_monthly

    smi = tv.get_hist(ticker,broker, interval=interval, n_bars=120)
    smi['Date'] = pd.to_datetime(smi.index)
    smi['Date'] = smi['Date'].apply(mpl_dates.date2num)
    smi = smi.loc[:,['Date', 'open', 'high', 'low', 'close']]
    s =  np.mean(smi['high'] - smi['low'])
    levels = []
    for i in range(2,smi.shape[0]-2):
        if isSupport(smi,i):
            l = smi['low'][i]

            if isFarFromLevel(l,s,levels):
                levels.append((i,l))

        elif isResistance(smi,i):
            l = smi['high'][i]

            if isFarFromLevel(l,s,levels):
                levels.append((i,l))
    return levels,smi

    
def isFarFromLevel(l,s,levels):
    
    return np.sum([abs(l-x) < s  for x in levels]) == 0
    
def isSupport(df,i):
    support = df['low'][i] < df['low'][i-1]  and df['low'][i] < df['low'][i+1] \
      and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]
    return support

def isResistance(df,i):
    resistance = df['high'][i] > df['high'][i-1]  and df['high'][i] > df['high'][i+1] \
      and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2] 
    return resistance

        
def plot_all(df, levels):
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14) 
    fig, ax = plt.subplots()

    df['date'] = df.index
    time_diff = df['date'].diff().min().seconds/60
    (width, date_format) = calculate_candlestick_params(time_diff)


    candlestick_ohlc(ax,df.values,width=width, \
                   colorup='green', colordown='red', alpha=0.5)
    #date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.tight_layout()

    for level in levels:
        plt.hlines(level[1],xmin=df['Date'][level[0]],\
               xmax=max(df['Date']),colors='blue')
    fig.savefig('level.jpeg')
    plt.close()
    return 

def calculate_candlestick_params(timeframe_minutes):
    # A rough heuristic to calculate width based on the timeframe
    one_day_in_minutes = 24 * 60
    width_multiplier = 0.2  # You can adjust this multiplier to fine-tune the width
    width = width_multiplier * (timeframe_minutes / one_day_in_minutes)
    width = max(width, 0.001)  # Ensure a minimum width of 0.001

    if timeframe_minutes <= 60:
        date_format = mpl_dates.DateFormatter('%d %b %Y %H:%M')
    elif timeframe_minutes <= 1440:
        date_format = mpl_dates.DateFormatter('%d %b %Y %H:%M')
    elif timeframe_minutes <= 7 * 1440:
        date_format = mpl_dates.DateFormatter('%d %b %Y')
    else:
        date_format = mpl_dates.DateFormatter('%b %Y')

    return width, date_format

def calculate_levels(ticker, broker, interval):
    
    (levels,df) = get_support_resistance(ticker, broker, interval)
    lev = [levels[x][1] for x in range(len(levels))]
    lev.sort()

    level_msg = f'Ich habe die folgendenen Resistenz- und Support- Linien für {ticker} {broker} berrechnet: {lev}'

    plot_all(df,levels)
    
    return level_msg


import logging
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Define the function that will be called by the command handler
def lvl(update, context):
    # Extract the two arguments from the command
    args = context.args
    if len(args) < 2:
        update.message.reply_text('2 Argumente werden benötigt zB. /lvl SW20 CAPITALCOM, siehe /help')
        return
    if len(args) == 2:
        arg1, arg2 = args
        try:
            text = calculate_levels(arg1.upper(), arg2.upper(), '1D')
        except:
            update.message.reply_text('Nicht unterstützte Kombination. Bitte wähle eine andere Kombination aus Ticker und Broker')
            return

    if len(args) == 3:
        arg1, arg2, arg3 = args
        print(arg1, arg2, arg3)
        try:
            text = calculate_levels(arg1.upper(), arg2.upper(), arg3.upper())
        except:
            update.message.reply_text('Nicht unterstützte Kombination. Bitte wähle eine andere Kombination aus Ticker und Broker')
            return
    if len(args) > 3:
        update.message.reply_text('Zuviele Argumente siehe /help. Bitte wähle eine andere Kombination aus Ticker und Broker')
        return
   


    # Reply to the user with the result
    update.message.reply_text('Result: {}'.format(text))
    time.sleep(1) # wait for the message to be sent
    update.message.reply_photo(photo=open('level.jpeg', 'rb'))

#define helper helper function to explain bot
def help(update, context):
    update.message.reply_text('Dieser Bot berechnet die Support- und Resistenzlinien für einen Ticker und Broker. \n'
                                'Die folgenden Kombinationen sind möglich: \n'

                                'z.B. /lvl SW20 CAPITALCOM oder mit Angabe des Tradingbereichs: \n'
                                'z.B. /lvl SW20 CAPITALCOM 1D \n'
                                'Gross oder Kleinschreibung ist egal. \n'

                                'Die folgenden Tradingbereiche sind möglich: \n'
                                '1M, 1W, 1D, 4H, 2H, 1H, 30, 15, 5, 1 \n'
                                '1M = 1 Monat, 1W = 1 Woche, 1D = 1 Tag, 4H = 4 Stunden, 2H = 2 Stunden, 1H = 1 Stunde, 30 = 30 Minuten, 15 = 15 Minuten, 5 = 5 Minuten, 1 = 1 Minute\n'
                                'Die Standardangabe ist 1D \n'
    )


def main():
    # Create an instance of the Updater class and pass in your bot token
    updater = Updater(telegram_token)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the command handler
    dispatcher.add_handler(CommandHandler('lvl', lvl))

    # Register the command handler
    dispatcher.add_handler(CommandHandler('help', help))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()