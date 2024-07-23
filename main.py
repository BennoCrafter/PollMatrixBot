import os
import simplematrixbotlib as botlib

creds = botlib.Creds(homeserver=os.environ['HOMESERVER'], username=os.environ['USERNAME'], password=os.environ['PASSWORD'])
bot = botlib.Bot(creds)
PREFIX = '!poll'

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("create"):

        await bot.api.send_reaction(room.room_id, message, "👍")


bot.run()
