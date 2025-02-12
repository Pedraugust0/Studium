import pyodbc
from dadosPrivados import string_connection
from random import choice

def channel_setwhitelist(channel_id):
    cnxn_str = (string_connection)
    conn = pyodbc.connect(cnxn_str)
    cursor = conn.cursor()
    
    id_ = channel_id
    
    query = f"""
    USE PythonSQL
    INSERT INTO channels_whitelist(channel_id)
    VALUES ({id_});
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def channel_unwhitelist(channel_id):
    cnxn_str = (string_connection)
    conn = pyodbc.connect(cnxn_str)
    cursor = conn.cursor()
    
    id_ = channel_id
    
    query = f"""
    USE PythonSQL
    DELETE FROM channels_whitelist WHERE channel_id={id_}
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def getChannel():
    cnxn_str = (string_connection)
    conn = pyodbc.connect(cnxn_str)
    cursor = conn.cursor()
    
    channel_ids = []
    
    cursor.execute('SELECT channel_id FROM channels_whitelist')
    
    for row in cursor.fetchall():
        channel_ids.append(row.channel_id)
    
    cursor.close()
    conn.close()
    return channel_ids

def frase_motivacao():
    frases_motivação = [
    "O sucesso é a soma de pequenos esforços repetidos dia após dia. - Robert Collier",
    "A educação é a arma mais poderosa que você pode usar para mudar o mundo. - Nelson Mandela",
    "A aprendizagem nunca esgota a mente. - Leonardo da Vinci",
    "O caminho para o sucesso é a atitude constante de aprender. - Zig Ziglar",
    "O único lugar onde o sucesso vem antes do trabalho é no dicionário. - Vidal Sassoon"]
    
    frase = choice(frases_motivação)
    
    return frase

def frase_parabenizacao():
    frases_parabenizacao = [
    "Parabéns pelo seu incrível sucesso! Seu esforço valeu a pena!",
    "Você fez um trabalho excelente! Parabéns por alcançar seu objetivo!",
    "Seus esforços foram recompensados. Parabéns pela sua conquista!",
    "Parabéns pela vitória! Seu empenho e dedicação são inspiradores!",
    "Você é um exemplo de persistência e determinação. Parabéns!"]
    
    frase = choice(frases_parabenizacao)
    
    return frase
