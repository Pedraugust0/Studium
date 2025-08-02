from discord.ext import tasks
from database.db_models import Encontro
import datetime
import discord
from config.settings import bot

encontros = []
tempo_loop = 5

@tasks.loop(seconds=tempo_loop)
async def esperar_ate_data():
    encontros = Encontro.select()

    if len(encontros) > 0:

        encontros = sorted(encontros, key=lambda encontro: encontro.data_inicio)

        embed = None

        # Pegar somente os encontros que tem mesma data do mais recente
        encontros_recentes = [encontro_vez for encontro_vez in encontros if encontro_vez.data_inicio < datetime.datetime.now()]

        for encontro_vez in encontros_recentes:
            # Se o encontro terminou
            if datetime.datetime.now() >= encontro_vez.data_fim:
                embed = discord.Embed(
                    color=discord.Color.blue(),
                    title="Encontro Terminado!",
                    description=encontro_vez.titulo
                )
                    
                Encontro.delete_by_id(encontro_vez.id)
            
            
            elif datetime.datetime.now() >= encontro_vez.data_inicio and not encontro_vez.iniciado:
                encontro_vez.iniciado = True
                Encontro.save(encontro_vez)
                
                embed = discord.Embed(
                    color=discord.Color.blue(),
                    title="Encontro iniciado!",
                    description=encontro_vez.titulo
                )
            
            else:
                continue

            try:
                canal = await bot.fetch_channel(encontro_vez.id_chat_criacao)
                criador = await bot.fetch_user(encontro_vez.criador)

                embed.add_field(
                    name="Data de Início:", value=encontro_vez.data_inicio, inline=True
                )

                embed.add_field(
                    name="Data de Fim:", value=encontro_vez.data_fim, inline=True
                )

                embed.add_field(
                    name="Criador:", value=criador.mention, inline=False
                )

                await canal.send(embed=embed)
                
            except discord.NotFound:
                continue