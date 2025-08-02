from config.settings import bot
import discord


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
        log = f"| Server: Particular | User: {autor} ({message.author.id}) | Message: {message.clean_content}"
    else:
        log = f"| Server: {message.guild.name} ({message.guild.id}) | User: {autor} ({message.author.id}) | Message: {message.clean_content}"

    print(log)