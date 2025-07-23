import discord
import datetime
from database.db_models import Encontro
from ui.modal.encontro_modais import Modal_Encontro_Criar, Embed_Encontro_Listar

# Classe com os botões de interação com os encontros iniciais
class View_Encontro_Inicio(discord.ui.View):
    
    def __init__(self):
        super().__init__(timeout=180)

    # Criar
    @discord.ui.button(label="Criar Encontro", style=discord.ButtonStyle.primary, emoji="➕")
    async def botao_criar(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        # Mostra o modal para criar o encontro
        await interaction.response.send_modal(Modal_Encontro_Criar())
    
    # Listar (iterar e remover)
    @discord.ui.button(label="Listar Encontros", style=discord.ButtonStyle.primary, emoji="🧐")
    async def listar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        embed = await Embed_Encontro_Listar().mostrar_encontro(interaction)

        # Se não houver encontros, envia uma mensagem        
        if embed is None:
            await interaction.followup.send("Nenhum encontro encontrado!", ephemeral=True)
            return
        
        await interaction.followup.send(embed=embed, view=View_Encontro_Listar(), ephemeral=True)


# Classe para os botões de listagem dos encontros
class View_Encontro_Listar(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

        self.embed_encontro = Embed_Encontro_Listar() # Inicializa a classe de listagem de encontros
    
    # Anterior
    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.secondary, emoji="◀️")
    async def anterior(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed_encontro.encontro_atual -= 1

        # Caso tente pegar um encontro anterior que não existe
        if self.embed_encontro.encontro_atual < 0:
            self.embed_encontro.encontro_atual = 0
            await interaction.response.send_message("Chegou no primeiro encontro!", ephemeral=True)
            return

        embed = await self.embed_encontro.mostrar_encontro(interaction)

        # Caso não encontre nenhum encontro
        if embed is None:
            await interaction.response.send_message("Nenhum encontro encontrado para este usuário.", ephemeral=True)

        else:
            #Edita a mensagem com as novas informaç~eos do encontro anterior
            await interaction.response.edit_message(embed=embed, view=self)

    # Próximo
    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.primary, emoji="▶️")
    async def proximo(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed_encontro.encontro_atual += 1

        # Caso tente pegar um encontro posterior que não existe
        if self.embed_encontro.encontro_atual >= len(self.embed_encontro.encontros):
            self.embed_encontro.encontro_atual -= 1
            await interaction.response.send_message("Chegou no último encontro!", ephemeral=True)
            return
        
        embed = await self.embed_encontro.mostrar_encontro(interaction)

        # Caso não encontre nenhum encontro
        if embed is None:
            await interaction.response.send_message("Nenhum encontro encontrado para este usuário.", ephemeral=True)
        
        else:
            # Edita a mensagem com as novas informações do próximo encontro
            await interaction.response.edit_message(embed=embed, view=self)

    # Deletar
    @discord.ui.button(label="Deletar", style=discord.ButtonStyle.primary, emoji="❌")
    async def deletar(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        # Pega o encontro atual selecionado
        encontro_atual = self.embed_encontro.encontros[self.embed_encontro.encontro_atual]
        encontro_atual.delete_instance()

        # Atualiza a lista de encontros
        self.embed_encontro.encontros = Encontro.select()

        # Atualiza o encontro atual para o último encontro ou o primeiro se não houver encontros
        if self.embed_encontro.encontro_atual >= len(self.embed_encontro.encontros):
            self.embed_encontro.encontro_atual = max(0, len(self.embed_encontro.encontros) - 1)

        # Se não houver encontros, envia uma mensagem
        if len(self.embed_encontro.encontros) == 0:
            await interaction.response.send_message("Nenhum encontro encontrado!", ephemeral=True)
            return
        
        embed = await self.embed_encontro.mostrar_encontro(interaction)

        await interaction.response.send_message(embed=embed, view=self)