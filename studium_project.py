import discord
from discord.ext import commands
from datetime import timedelta
from funcoes import getChannel, channel_unwhitelist, channel_setwhitelist
from funcoes import frase_motivacao, frase_parabenizacao
from dadosPrivados import bot_key, canal_id
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- SETUP VARS ---- #

tarefas = []
tarefas_mensagem = []

# ----- COMANDOS ----- #

@bot.command()
async def ola(ctx:commands.Context):
    await ctx.reply("Olá!!!")

@bot.command()
async def setchannel(ctx:commands.Context, channel_id:int):
    # Pegar cada canal no servidor e comparar o id com o fornecido
    for channel in ctx.guild.channels: 
        if channel.id == channel_id:
            nome = channel.name
    
    channel_setwhitelist(channel_id) # Adiciona o canal a whitelist
    
    await ctx.reply(f"Canal {nome} foi adicionado a whitelist")

@bot.command()
async def unsetchannel(ctx:commands.Context, channel_id:int):
    for channel in ctx.guild.channels: 
        if channel.id == channel_id:
            nome = channel.name
    
    channel_unwhitelist(channel_id)
    
    await ctx.reply(f"Canal {nome} foi removido da whitelist")

@bot.command()
async def pomodoro(ctx:commands.Context, total:int, tempo:int):
    #Primeiro item = minutos totais de estudo e o segundo tempo de estudo e tempo de descanso
    cronograma = [total, tempo]

    hora_total = cronograma[0]
    hora_rodada = cronograma[1]

    #var para altenar a mensagem entre terminou estudo e descanso 
    modos = False

    total_time = timedelta(minutes=hora_total)
    study_time = timedelta(minutes=hora_rodada)

    message_time = await ctx.reply("Iniciando estudos...")
    message_warns = await ctx.reply(f"(tempo total: {hora_total}:00)")
    
    #Loop de tempo total
    while total_time.total_seconds() > 0:
        #loop de tempo de estudo
        while study_time.total_seconds() > 0:
            await asyncio.sleep(1)
            
            study_time -= timedelta(seconds=1)
            
            await message_time.edit(content=f"Tempo restante {study_time}")
        
        total_time -= timedelta(minutes=hora_rodada)
        study_time = timedelta(minutes=hora_rodada)
        
        if total_time == timedelta(minutes=0):
            await ctx.reply("Pomodoro Terminou!!")
        
        elif modos == False:
            modos = True
            await message_warns.edit(content="Tempo de estudo acabou! iniciando Descanso...")
        
        else:
            modos = False
            await message_warns.edit(content="Tempo de descanso acabou! voltando aos Estudos...")
        
        #IF caso o usuário coloque tempos inválidos
        if total_time < timedelta(seconds=0):
            total_time = timedelta(minutes=0)
        
            await ctx.reply(f"Faltam {total_time} de pomodoro")

@bot.command()
async def adicionartarefa(ctx,*,tarefa:str=None):
    if tarefa != None:
        tarefas.append(tarefa)
        tarefas_mensagem.append(f"- {tarefa} :x:")
        
        await ctx.send(f'{tarefa} Adicionada com sucesso!')
    else:
        await ctx.send('Por Favor, Forneça uma descrição para a tarefa')

@bot.command()
async def marcartarefa(ctx, *, tarefa:str):
    tarefa_uncheck = f'- {tarefa} :x:'
    tarefa_check = f'- {tarefa} :white_check_mark:'
    
    if tarefa in tarefas:
        if tarefa_uncheck in tarefas_mensagem:
            indice = tarefas_mensagem.index(f'- {tarefa} :x:')
            tarefas_mensagem[indice] = tarefa_check
            
            parabens = frase_parabenizacao()
            
            await ctx.send(parabens)
        
        else:
            indice = tarefas_mensagem.index(f'- {tarefa} :white_check_mark:')
            tarefas_mensagem[indice] = tarefa_uncheck
            
            motivacao = frase_motivacao()
            
            await ctx.send(motivacao)
    else:
        await ctx.send('Tarefa não encontrada! (Use !listartarefas para ver todas as tarefas)')

@bot.command()
async def removertarefa(ctx,*,tarefa:str):
        if tarefa in tarefas:
            tarefas.remove(tarefa)
            try:
                tarefas_mensagem.remove(f"- {tarefa} :x:")
            except:
                tarefas_mensagem.remove(f"- {tarefa} :white_check_mark:")
            await ctx.send(f'"{tarefa}" excluída com sucesso!')
        else: 
            await ctx.send('Não existem tarefas')

@bot.command()
async def listartarefas(ctx):
    if tarefas_mensagem:
        await ctx.send(f'**Tarefas:** \n{'\n'.join(tarefas_mensagem)}')
    else:
        await ctx.send('Lista de tarefas vazia (Use !adicionartarefa para criar uma).')

@bot.command()
async def editartarefa(ctx,*,tarefa:str):
        partes = tarefa.split('|')
        
        if len(partes) == 2:
            antiga, nova = partes[0].strip(), partes[1].strip()
            
            if antiga in tarefas:
                index = tarefas.index(antiga)
                tarefas[index] = nova
                tarefas_mensagem[index] = f'- {nova} :x:'
                await ctx.send(f'Sua tarefa "{antiga}" foi substituída por "{nova}" com sucesso.')
            
            else:
                await  ctx.send('Tarefa antiga não encontrada.')
        
        else:   
            await ctx.send('Por favor, informe a tarefa antiga e nova descrição separadas por |')

@bot.command()
async def ajuda(ctx):
    await ctx.send(f'''
        Comandos disponíveis:
        !ola
        
        **!setchannel [ id do canal que você quer setar para o bot poder falar]**
        (Caso nenhum canal esteja setado, o bot vai funcionar em todos os canais)
        
        **!unsetchannel [ id do canal que você quer tirar para que o bot não mande mensagem]**
        
        **!pomodoro [ tempo total de estudo (em minutos) ] [ tempo em minutos de estudo e de pausas ]**
        (Ex: !pomodoro 60 5 || Você fará um pomodoro de 60 minutos e a cada 5 minutos você irá estudar e descansar.)
        
        **!adicionartarefa [ tarefa ]**
        
        **!removertarefa [ tarefa que você quer remover ]**
        
        **!editartarefa [ tarefaantiga ] | [ tarefanova ]**
        
        **!listartarefas**
        
        **!marcartarefa [ tarefa ]**
        
        ''')

# ----- EVENTOS ----- #
@bot.event
async def on_ready():
    print(f"Bot online")

@bot.event
async def on_message(message:discord.Message):
    if message.author.bot:
        return
    
    channels_ids = getChannel() # Pega o id de todos os canais na whitelist
    
    if str(message.channel.id) not in channels_ids: # Compara se a mensagem enviada não está na whitelist
        if len(channels_ids) >= 1:
            return
    
    await bot.process_commands(message) # Caso esteja na whitelist ele executa o comando

@bot.event
async def on_member_join(member:discord.Member):
    embed = discord.Embed(
        title="Bem Vindo!!!",
        description=f"Seja bem vindo ao servidor {member.mention}!",
        color= discord.Color.green()
    )
    
    embed.set_author(name="August0", icon_url="https://pbs.twimg.com/profile_images/1011335349564526597/OBOiwL6R_400x400.jpg")
    embed.set_image(url=member.avatar.url)
    embed.set_footer(text="Aproveite o Servidor!!!")
    
    channel = bot.get_channel(canal_id)
    
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member:discord.Member):
    embed = discord.Embed(
        title="Tchau!!! :pleading_face:",
        description=f"O membro {member.mention} nos deixou :pleading_face:",
        color=discord.Color.green()
    )
    
    embed.set_author(name="August0", icon_url="https://pbs.twimg.com/profile_images/1011335349564526597/OBOiwL6R_400x400.jpg")
    embed.set_image(url=member.avatar.url)
    
    channel = bot.get_channel(1249135197698658438)
    
    await channel.send(embed=embed)

bot.run(bot_key)
