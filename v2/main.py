import discord
from discord.ext import commands
import datetime
import asyncio
from dotenv import load_dotenv
import os

from database.db_models import db, Encontro, Participante, EncontroParticipante
from config.settings import bot

# Importa Comandos
from actions.commands.pomodoro import pomodoro
from actions.commands.encontro import telas_encontro

# Importa Eventos
from actions.events.on_ready import on_ready
from actions.events.on_message import on_message
from actions.events.on_join import on_join

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura e Executa o bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")

    if token is None:
        raise ValueError("DISCORD_TOKEN não está definido no ambiente.")

    # Inicia o bot com a chave do bot
    bot.run(token)