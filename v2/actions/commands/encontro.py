import discord
from config.settings import bot
from ui.view.encontro_views import View_Encontro_Inicio


@bot.tree.command(name="encontro", description="Gerenciar Encontros")
async def telas_encontro(interaction: discord.Interaction):
    
    embed = discord.embeds.Embed(
        title="Gerenciar Encontros",
        description="Caso deseje criar um encontro clique no botão +!",
        colour=discord.Color.blue()
    )

    view = View_Encontro_Inicio()
    
    await interaction.response.send_message(embed=embed, view=view)