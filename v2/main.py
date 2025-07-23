import discord
from discord.ext import commands
import datetime
import asyncio
from dotenv import load_dotenv
import os

from database.db_models import db, Encontro, Participante, EncontroParticipante
from ui.view.encontro_views import View_Encontro_Inicio

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="ola", description="comando de teste")
async def ola(interaction: discord.Interaction):
    membro = interaction.user
    
    await interaction.response.send_message(f"Olá {membro.mention}")


@bot.tree.command(name="pomodoro", description=r"1° tempo de estudo; 2° tempo de intervalo; (Em minutos)")
async def pomodoro(interaction: discord.Interaction, 
                   tempo_estudo: int, 
                   tempo_intervalo: int,
                ):

    await interaction.response.defer()

    usuario = interaction.user
    mensagem_erro = ""
    mensagens = []

    intervalo_contador = 5 # Tempo de intervalo entre as mensagens de contagem

    #Testar se existe um tempo inválido
    if tempo_estudo < 1 :
        mensagem_erro += f"Tempo de estudo muito pequeno!\n"

    if tempo_estudo > 60:
        mensagem_erro += f"Tempo de estudo muito grande!\n"

    if tempo_intervalo < 1:
        mensagem_erro += f"Tempo de intervalo muito pequeno!\n"

    if tempo_intervalo > 60:
        mensagem_erro += f"Tempo de intervalo muito grande!"
    
    # caso tenha algum erro
    if mensagem_erro:
        await interaction.response.send_message(f"/pomodoro tempo_estudo=**__{tempo_estudo}__** tempo_intervalo=**__{tempo_intervalo}__**\n\n**{mensagem_erro}** {usuario.mention}", ephemeral=True)
        return

    #Pomodoro
    mensagem_anterior = await interaction.followup.send(content=f"Iniciando Pomodoro! {usuario.mention}", wait=True)
    mensagens.append(mensagem_anterior)
    await asyncio.sleep(3)

    await comecar_contagem(tempo_estudo, intervalo_contador, mensagem_anterior)

    #Intervalo
    mensagem_anterior = await interaction.followup.send(content=f"Tempo de pomodoro acabou {usuario.mention}, iniciando descanso...", wait=True)
    mensagens.append(mensagem_anterior)
    await asyncio.sleep(3)

    await comecar_contagem(tempo_intervalo, intervalo_contador, mensagem_anterior)

    #Acabou o intervalo
    mensagem_anterior = await interaction.followup.send(content=f"Tempo de intervalo acabou {usuario.mention}!", wait=True)
    mensagens.append(mensagem_anterior)

    await asyncio.sleep(5)

    #Apagar as mensagens anteriores
    for mensagem in mensagens:
        await mensagem.delete()


async def comecar_contagem(tempo: int, intervalo_contador: int, mensagem: discord.Message):
    contador = datetime.timedelta(minutes=tempo)

    # Loop durante o tempo especificado
    while(contador.total_seconds() > 0):
        await mensagem.edit(content=f"Tempo restante! {contador}")
        await asyncio.sleep(intervalo_contador)

        contador -= datetime.timedelta(seconds=intervalo_contador)
    

@bot.tree.command(name="encontro", description="Gerenciar Encontros")
async def telas_encontro(interaction: discord.Interaction):
    
    embed = discord.embeds.Embed(
        title="Gerenciar Encontros",
        description="Caso deseje criar um encontro clique no botão +!",
        colour=discord.Color.blue()
    )

    view = View_Encontro_Inicio()
    
    await interaction.response.send_message(embed=embed, view=view)



@bot.event
async def on_join(guild: discord.Guild):
    print(f"Bot entrou no servidor: {guild.name} ({guild.id})")


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
    
    except discord.app_commands.CommandSyncFailure as error:
        print(f"Erro ao sincronizar os comandos. (dados inválidos, status: {error.status})")

    except discord.HTTPException as error:
        print(f"Erro ao sincronizar os comandos. (status: {error.status})")

@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)

    autor = message.author.name
    comando = False
    log = None

    # Verifica se a mensagem é um comando do bot
    if message.author.id == 1250664796139819100:
        autor = "Bot"
    
    # Verifica se a mensagem é um comando
    if message.guild is None:
        log = f"| User: {autor} ({message.author.id}) | Message: {message.clean_content} |"
    
    else:
        log = f"| Server: {message.guild.name} ({message.guild.id}) | User: {autor} ({message.author.id}) | Message: {message.clean_content} |"

    print(log)



if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")

    if token is None:
        raise ValueError("DISCORD_TOKEN não está definido no ambiente.")

    # Inicia o bot com a chave do bot
    bot.run(token)