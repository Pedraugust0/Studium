import discord
import datetime
from database.db_models import Encontro, EncontroParticipante, Participante, db
import peewee
import datetime

class Modal_Encontro_Criar(discord.ui.Modal):

    data_inicio = discord.ui.TextInput(
        label='Data de Início',
        placeholder='DD/MM/AA HH:MM',
        max_length=17,
        required=True
    )

    data_fim = discord.ui.TextInput(
        label='Data Fim',
        placeholder='DD/MM/AA HH:MM',
        max_length=17,
        required=False
    )

    titulo_encontro = discord.ui.TextInput(
        label='Titulo do encontro',
        placeholder='Encontro brainstorm...',
        max_length=40,
        required=True
    )

    descricao_encontro = discord.ui.TextInput(
        label='Descrição do encontro',
        style=discord.TextStyle.paragraph,
        placeholder='Descreva brevemente o propósito e as atividades do encontro.',
        max_length=100,
        required=False
    )

    def __init__(self):
        super().__init__(title="Criar um encontro")
    
    async def on_submit(self, interaction: discord.Interaction):

        # Pegar os campos no modal
        criador = str(interaction.user.id)
        data_criacao = datetime.datetime.now()
        data_inicio = self.data_inicio.value
        data_fim = self.data_fim.value
        titulo = self.titulo_encontro.value
        descricao = self.descricao_encontro.value
        id_chat_criacao = str(interaction.channel_id)

        # Tenta converter a string em data
        try:
            data_inicio = datetime.datetime.strptime(data_inicio, r"%d/%m/%y %H:%M")
            data_fim = datetime.datetime.strptime(data_fim, r"%d/%m/%y %H:%M")

            if data_inicio <= datetime.datetime.now() or data_fim <= datetime.datetime.now() or data_fim < data_inicio:
                raise ValueError

        except ValueError:
            await interaction.response.defer()

            # Embed caso a data não esteja no formato correto
            embed_erro = discord.embeds.Embed(
                title="Erro na data!",
                colour=discord.Color.red()
            )

            embed_erro.add_field(name="Valor esperado Data de início:", value="13/11/25 12:00", inline=True)
            embed_erro.add_field(name="Valor inserido", value=data_inicio, inline=True)
            embed_erro.add_field(name="", value="", inline=False)
            embed_erro.add_field(name="Valor esperado Data de fim:", value="13/11/25 12:00", inline=True)
            embed_erro.add_field(name="Valor inserido", value=data_fim, inline=True)

            # Envio do embed
            await interaction.followup.send(embed=embed_erro)
            # Para o método para não dar erro de tipagem
            return

        try:
            # Pegar o id do usuário da interação, caso não exista ele cria um
            participante_id = Participante.get(discord_id=criador).id

        except peewee.DoesNotExist:
            participante_id = Participante.create(discord_id=criador).id

        # Adicionar encontro
        encontro = Encontro.create(
            criador=criador,
            data_criacao=data_criacao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            titulo=titulo,
            descricao=descricao,
            id_chat_criacao=id_chat_criacao,
            iniciado=False
        )

        # Adicionar Participante
        EncontroParticipante.create(
            participante=participante_id,
            encontro=Encontro.get_id(encontro)
        )

        # Criar o embed de confirmação que tudo deu certo
        embed_confirmacao = discord.embeds.Embed(
            title="Encontro Agendado!",
            colour=discord.Color.green()
        )

        embed_confirmacao.add_field(name="Titulo", value=titulo, inline=True)
        embed_confirmacao.add_field(name="Descrição", value=descricao, inline=True)
        embed_confirmacao.add_field(name="Criador", value=interaction.user.mention, inline=True)
        embed_confirmacao.add_field(name="Data inicio", value=data_inicio.strftime(r"%d/%m/%y %H:%M"), inline=True)
        embed_confirmacao.add_field(name="Data Fim", value=data_fim.strftime(r"%d/%m/%y %H:%M"), inline=True)
        embed_confirmacao.add_field(name="Data Criação", value=data_criacao.strftime(r"%d/%m/%y %H:%M"), inline=True)

        # Envio do embed
        await interaction.response.send_message(embed=embed_confirmacao)