import discord
from config.settings import bot

# Eventos
@bot.event
async def on_join(guild: discord.Guild):
    print(f"Bot entrou no servidor: {guild.name} ({guild.id})")