# discord bot interacts and shows coinbase pro data 
from secret import Secret
from coin import Coin

import hikari
import lightbulb
import pandas as pd


c = Coin()

# instantiate bot app object
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



bot.run()
