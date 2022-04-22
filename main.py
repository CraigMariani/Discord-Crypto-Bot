# discord bot interacts and shows coinbase pro data 
import time
from secret import Secret
from coin import Coin

import hikari
import lightbulb
import pandas as pd
import discord

c = Coin()
 # instantiate bot app object for slash commands
bot = lightbulb.BotApp(token=Secret.bot_token, default_enabled_guilds=(Secret.guild_id))

# listing all available trading pairs on coinbase pro
@bot.command() # command decorater  used for setting up basic commands 
@lightbulb.option('base_currency', 'Select one of the following as base currency (USD/USDT/USDC)', type=str) # 
@lightbulb.command("list_pairs", "List all available trading pairs on exchange") # name of command 
@lightbulb.implements(lightbulb.SlashCommand) # set up slashcommand
async def list_pairs(ctx):
    pairs = c.all_available_pairs()

    # list all available 
    if ctx.options.base_currency == 'USDC':
        pairs = pairs[pairs['id'].str.contains('USDC') == True]
        await ctx.respond(pairs['id'].to_string())
    
    if ctx.options.base_currency == 'USDT':
        pairs = pairs[pairs['id'].str.contains('USDT') == True]
        # await ctx.respond(pairs['id'].to_string())

        for i in range(0,len(pairs), 20):
            await ctx.respond(pairs['id'].iloc[i:i+20].to_string())
    
    if ctx.options.base_currency == 'USD':
        pairs = pairs[pairs['id'].str.contains('USD') == True]
        pairs = pairs[pairs['id'].str.contains('USDT') == False]
        pairs = pairs[pairs['id'].str.contains('USDC') == False]
        # await ctx.respond(pairs['id'].to_string())

        for i in range(0,len(pairs), 20):
            await ctx.respond(pairs['id'].iloc[i:i+20].to_string())
    # print(pairs.to_string())
    

#####################
# list recent trades
@bot.command()
@lightbulb.option('trade_count', 'Select how many recent trades to look back', type=int) #trade count/number of most recent trades 
@lightbulb.option('ticker_label','Select the ticker of recent trades you want to see', type=str)
@lightbulb.command("list_trades", "List all recent trades") # name of command 
@lightbulb.implements(lightbulb.SlashCommand) # set up slashcommand
async def list_trades(ctx):
    trade_data = c.recent_trades(ctx.options.ticker_label, ctx.options.trade_count)
    trades = pd.DataFrame.from_dict(trade_data)
    await ctx.respond(trades)
    # print(type(trade_data[0]))
    # await ctx.respond(trade_data)

    # print the time, trade_id, size, price, side


#################
### sending trading signals 
@bot.listen()
async def create(event: hikari.GuildMessageCreateEvent):
    if event.content.strip() == "start_signals":
        while True:

            tickers = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'MATIC-USD']    
            signal_data = []
            for ticker in tickers:
                signal = c.trade_signal(ticker)
                signal_data.append({
                    'ticker' : signal[1], 
                    'signal' : signal[0]
                })

            # await event.message.respond('trading data')
            signal_message = pd.DataFrame(signal_data)
            await event.message.respond(signal_message)

            time.sleep(3600)


#####
# sending charts through discord 
@bot.command()
@lightbulb.option('trading_pair', 'Select the trading pair that you want to see', type=str) #trade count/number of most recent trades 
@lightbulb.command("show_chart", "Show most recent price chart for selected crypto pair") # name of command 
@lightbulb.implements(lightbulb.SlashCommand) # set up slashcommand
async def show_chart(ctx):
    c.trade_charts(ctx.options.trading_pair)
    with open("charts/{}.png".format(ctx.options.trading_pair), "rb") as fh:
        f = hikari.File("charts/{}.png".format(ctx.options.trading_pair))
    await ctx.respond(f)
bot.run()
