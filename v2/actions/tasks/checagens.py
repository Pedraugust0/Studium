from discord.ext import tasks

@tasks.loop(minutes=10)
async def checar_datas():
    
    pass