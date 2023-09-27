import os

import disnake
from disnake.ext import commands

#  Создается объект intents, который включает все разрешения для бота.
#  Создается экземпляр класса Bot с префиксом команд "!" и указанными разрешениями.
intents = disnake.Intents.all()  # Подключаем все разрешения
bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[758360740217487420])  # Вместо 1234567890 указать id сервера

@bot.event
async def on_ready():
    print(f'{bot.user.name} запущен. А ничё нормально общайся, да.')

bot.load_extension("cogs.avatar")
bot.load_extension("cogs.select-menu")
bot.load_extension("cogs.buttons-role")

bot.run('OTE5NTQ5NDk4NjQzMDc5MTc5.G1mnwS.t_NxyoYnMi7putpP4IvZCvqEwPTt33adgugRA0')