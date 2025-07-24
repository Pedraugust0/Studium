import discord
from config.settings import bot
import asyncio
from database.db_models import db, Encontro, Participante, EncontroParticipante
from actions.tasks.checagens import checar_datas

@bot.event
async def on_ready():
    print("Bot Online!!!")
    
    # começar a checar lembretes
    if not checar_datas.is_running():
        print("Iniciando checagem de datas...")
        await checar_datas.start()

    try:
        comandos = await bot.tree.sync()

        # Lista os comandos sincronizados
        for comando in comandos:
            print("/" + comando.name, comando.description)

        print()
        print("comandos sincronizados!")

        # Conecta ao banco de dados e cria as tabelas se não existirem
        db.connect()
        db.create_tables([Participante, Encontro, EncontroParticipante])
    
    except discord.app_commands.CommandSyncFailure as error:
        print(f"Erro ao sincronizar os comandos. (dados inválidos, status: {error.status})")

    except discord.HTTPException as error:
        print(f"Erro ao sincronizar os comandos. (status: {error.status})")