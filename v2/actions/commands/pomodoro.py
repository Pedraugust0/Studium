import discord
from config.settings import bot
import asyncio
import datetime

@bot.tree.command(name="pomodoro", description=r"1° tempo de estudo; 2° tempo de intervalo; (Em minutos)")
async def pomodoro(interaction: discord.Interaction, 
                   tempo_estudo: int, 
                   tempo_intervalo: int,
                ):

    await interaction.response.defer()

    usuario = interaction.user
    mensagem_erro = ""
    mensagens = []
    continuar = True
    emojis = ["👍", "👎"]

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

    while continuar:

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

        mensagem_anterior = await interaction.followup.send(content="Pomodoro terminou, quer começar outro?", wait=True)
        mensagens.append(mensagem_anterior)

        # Adiciona o sensor para checar a reação
        reacao = await mensagem_confirmacao(mensagem_anterior, emojis)

        if reacao.emoji == emojis[0]:
            continuar = True
        else:
            continuar = False
        
        await asyncio.sleep(1)

    # Apagar as mensagens anteriores
    for mensagem in mensagens:
            try:
                await mensagem.delete()
            except discord.errors.NotFound:
                continue




async def comecar_contagem(tempo: int, intervalo_contador: int, mensagem: discord.Message):
    contador = datetime.timedelta(minutes=tempo)

    # Loop durante o tempo especificado
    while(contador.total_seconds() > 0):
        await mensagem.edit(content=f"Tempo restante! {contador}")
        await asyncio.sleep(intervalo_contador)

        contador -= datetime.timedelta(seconds=intervalo_contador)


async def mensagem_confirmacao(mensagem: discord.Message, emojis: list) -> discord.Reaction:
    for emoji in emojis:
        await mensagem.add_reaction(emoji)

    # Checa se não é o bot, se for o emoji correto na mensagem correta
    def check_reaction(reaction: discord.Reaction, user: discord.User):
        return user != bot.user and str(reaction) in emojis and reaction.message.id == mensagem.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check_reaction)
        return reaction
            
    except TimeoutError:
        return discord.Reaction()
