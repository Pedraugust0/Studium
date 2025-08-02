import peewee

DB_FILE = "database/banco.db"
db = peewee.SqliteDatabase(DB_FILE)

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Participante(BaseModel):
    discord_id = peewee.CharField(unique=True)
    
    def __str__(self):
        return str(self.discord_id)

class Encontro(BaseModel):
    criador = peewee.CharField()
    data_criacao = peewee.DateTimeField()
    data_inicio = peewee.DateTimeField()
    data_fim = peewee.DateTimeField()
    titulo = peewee.CharField()
    descricao = peewee.CharField()
    id_chat_criacao = peewee.CharField()
    iniciado = peewee.BooleanField(default=False)

    def __str__(self):
        return f"{self.criador}, {self.data_criacao}, {self.data_inicio}, {self.data_fim}, {self.titulo}, {self.descricao}, {self.id_chat_criacao}" 

class EncontroParticipante(BaseModel):
    participante = peewee.ForeignKeyField(model=Participante)
    encontro = peewee.ForeignKeyField(model=Encontro)

    def __str__(self):
        return f"{self.participante}, {self.encontro}"