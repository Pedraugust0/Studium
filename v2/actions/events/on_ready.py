import discord
from config.settings import bot
from database.db_models import db, Encontro, Participante, EncontroParticipante
from actions.tasks.checagens import esperar_ate_data

@bot.event
async def on_ready():
    print("Bot Online!!!")

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

        # começar a checar lembretes
        if not esperar_ate_data.is_running():
            print("Iniciando checagem de datas...")
            await esperar_ate_data.start()
    
    except discord.app_commands.CommandSyncFailure as error:
        print(f"Erro ao sincronizar os comandos. (dados inválidos, status: {error.status})")

    except discord.HTTPException as error:
        print(f"Erro ao sincronizar os comandos. (status: {error.status})")