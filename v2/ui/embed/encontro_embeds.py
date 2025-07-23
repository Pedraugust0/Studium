import discord
from v2.database.db_models import Encontro, Participante
import peewee

# Classe para mostrar os detalhes do encontro
class Embed_Encontro_Listar:

    def __init__(self):
        self.encontro_atual = 0
        self.encontros = Encontro.select()

    # Retorna o embed do usuário respectivo (com base no encontro_atual)
    async def mostrar_encontro(self, interaction: discord.Interaction) -> discord.Embed | None:
        try:
            encontro = self.encontros[self.encontro_atual]

            id_criador = Participante.get(discord_id=encontro.criador).discord_id

            criador = await interaction.client.fetch_user(int(id_criador))

        except IndexError:
            print("Nenhum encontro encontrado.")
            return None

        except peewee.DoesNotExist:
            print("Nenhum encontro encontrado para este usuário.")
            return None

        data_criacao = encontro.data_criacao
        data_inicio = encontro.data_inicio
        data_fim = encontro.data_fim
        titulo = encontro.titulo
        descricao = encontro.descricao

        embed_confirmacao = discord.embeds.Embed(
            title="Encontro Detalhes",
            colour=discord.Color.purple()
        )

        embed_confirmacao.add_field(name="Titulo", value=titulo, inline=True)
        embed_confirmacao.add_field(name="Descrição", value=descricao, inline=True)
        embed_confirmacao.add_field(name="Criador", value=criador.mention, inline=True)
        embed_confirmacao.add_field(name="Data inicio", value=data_inicio.strftime(r"%d/%m/%y %H:%M"), inline=True)
        embed_confirmacao.add_field(name="Data Fim", value=data_fim.strftime(r"%d/%m/%y %H:%M"), inline=True)
        embed_confirmacao.add_field(name="Data Criação", value=data_criacao.strftime(r"%d/%m/%y %H:%M"), inline=True)

        return embed_confirmacao