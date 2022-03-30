import discord
import os

from discord.ext import commands

# Discord related variables
bot = commands.Bot(command_prefix="$")
token_file = open("token.txt", "r")
token = token_file.readline()

# Bot variables
owner = "Akselmo"
msg_rate = 3
cooldown_seconds = 3
printer_command = "/tmp/DEVTERM_PRINTER_IN"
#printer_command = "test.txt"
illegal_chars = set(r'&|;$><`\!')

# Test command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Send message to devterm
@bot.command()
@commands.cooldown(msg_rate, cooldown_seconds, commands.BucketType.guild) #whole guild is in cooldown
async def print(ctx, arg):
    await ctx.send('Okay, printing "{}" from {}\'s Devterm printer...'.format(str(arg), owner))
    if any((c in illegal_chars) for c in str(arg)):
        await ctx.send("Illegal chars in message!")
    else:
        user_line = '{0.author} sent: \n'.format(ctx)
        message = '{} \n \n \n'.format(str(arg))
        cmd = 'echo -e "{}{}" > {}'.format(user_line, message, printer_command)
        os.system(cmd)

#Prints error during cooldown
@print.error
async def print_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Hold on let me cool down!")


bot.run(str(token))
