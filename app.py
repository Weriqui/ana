from flask import Flask, render_template, request, jsonify
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import mysql.connector
import joblib

app = Flask(__name__)

#Verificar se ja se apresentou
def vericarSeApresentei(whatsid):
  # Conectar ao banco de dados
  conn = mysql.connector.connect(
      host="whats.c9zdqqj5d3xf.us-east-2.rds.amazonaws.com",
      port="3306",
      user="weriqui",
      password="Werique18",
      database="ana"
  )

  # Criar um cursor para executar comandos SQL
  cursor = conn.cursor()

  # Executar uma consulta
  cursor.execute(f"SELECT * FROM conversa WHERE whatsappid = '{whatsid}'")

  # Obter os resultados da consulta
  resultados = cursor.fetchall()

  # Fechar a conexão
  conn.close()
  return resultados

def apresentei(whatsid,apresentei:bool,desliga:bool):
  # Conectar ao banco de dados
  conn = mysql.connector.connect(
      host="whats.c9zdqqj5d3xf.us-east-2.rds.amazonaws.com",
      port="3306",
      user="weriqui",
      password="Werique18",
      database="ana"
  )

  # Criar um cursor para executar comandos SQL
  cursor = conn.cursor()

  # Executar uma consulta
  cursor.execute(f"INSERT INTO conversa VALUES ('{whatsid}','{apresentei}','{desliga}')")

  # Confirmar as alterações
  conn.commit()

  # Fechar o cursor e a conexão
  cursor.close()
  return conn.close()

def desliga(whatsid,desliga:bool):
  # Conectar ao banco de dados
  conn = mysql.connector.connect(
      host="whats.c9zdqqj5d3xf.us-east-2.rds.amazonaws.com",
      port="3306",
      user="weriqui",
      password="Werique18",
      database="ana"
  )
def atualiza(whatsid,apresentei:bool):
  # Conectar ao banco de dados
  conn = mysql.connector.connect(
      host="whats.c9zdqqj5d3xf.us-east-2.rds.amazonaws.com",
      port="3306",
      user="weriqui",
      password="Werique18",
      database="ana"
  )

  # Criar um cursor para executar comandos SQL
  cursor = conn.cursor()

  # Executar uma consulta
  cursor.execute(f"UPDATE conversa SET desativar ='{desliga}' WHERE ja_me_apresentei = {apresentei}")

  # Confirmar as alterações
  conn.commit()

  # Fechar o cursor e a conexão
  cursor.close()
  return conn.close()


# Verifique se os modelos já foram salvos em disco
try:
    nlp = joblib.load('spacy_model.pkl')
    tokenizer = joblib.load('bert_tokenizer.pkl')
    model = joblib.load('bert_model.pkl')
except FileNotFoundError:
    # Se os modelos não foram salvos, carregue-os e salve-os em disco
    nlp = spacy.load('pt_core_news_sm')
    tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
    model = AutoModel.from_pretrained("neuralmind/bert-base-portuguese-cased")
    
    joblib.dump(nlp, 'spacy_model.pkl')
    joblib.dump(tokenizer, 'bert_tokenizer.pkl')
    joblib.dump(model, 'bert_model.pkl')


nome_empresa = "Empresa do fulano"
nome ="Fulano de tal"
nome_assistente = 'Jurandi'
respostas = {
        "DECISOR CONFIRMADO":[
            f'Olá! Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "2DECISOR CONFIRMADO":[
            "Que bom!",
            f'Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "3DECISOR CONFIRMADO":[
            f'Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "PERDAO":[
            "Perdão",
            f'Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "QUE EMPRESA":[nome_empresa,
            f'Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "QUE EMPRESA/JA ME APRESENTEI":[
               nome_empresa
        ],
        "BEM E VOCE":[
            "Quem ótimo",
            "Aqui está tudo bem!",
            f'Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "BEM E VOCE/JA ME APRESENTEI":[
            "Quem ótimo",
            "Aqui está tudo bem!"
        ],
        "BEM":[
            "Quem ótimo",
            f'Me chamo {nome_assistente}, da Villela Bank.',
            'Nós temos um Software que identifica oportunidade de redução de custos operacionais para aumentar a lucratividade da empresa.',
            'Assim, dentro do nosso banco, existe o setor de Auditoria e Compliance Fiscal, onde conseguimos revisar as divergências de impostos cobrados a mais, por parte da Receita Federal.',
            'Somos especialistas no ramo de supermercados, onde já ajudamos mais de 50 mil empresas a reduzir sua malha fiscal com compensação de seus direitos créditórios em seus impostos e/ou dívidas.',
            f'Assim, queremos conversar 1 min sobre as oportunidades para a {nome_empresa}.',
            'Posso te ligar agora?'
        ],
        "BEM/JA ME APRESENTEI":[
            "Quem ótimo"
        ],
        "COMO CONSEGUIU MEU NÚMERO?":[
              'Nós somos uma fintech. Assim, com o Open Banking, que é o sistema bancário aberto, temos o seu contato vinculado a essa empresa.',
              'Minha intenção é trazer uma boa notícia para você que acaba sofrendo com as cobranças de muitos impostos.',
              'Agora, se esse contato não tiver vínculo com essa empresa, peço desculpas pelo inconveniente.'
        ],
        "MINHA CONTABILIDADE/JURÍDICO JÁ FAZ":[
           "NÃO LER"
        ],
        "NÃO TEM INTERESSE":[
            "NÃO LER"
        ],
        "PEDIU PRA LIGAR":[
            "PEDIU PARA LIGAR"
        ],
        "JÁ FAÇO ESSE SERVIÇO":[
            "NÃO LER"
        ],
        "TELEFONES INCORRETOS":[
            f"Olá, me {nome_assistente}, da Villela Brasil Bank",
            "Acredito que me enganei... estou tentando conato com:",
            f"{nome_empresa} ou {nome}",
            "Desculpe o inconveniente.",
            "Att"
        ],
        "TELEFONES INCORRETOS/JA ME APRESENTEI":[
            "Acredito que me enganei... estou tentando contato com:",
            f"{nome_empresa} ou {nome}",
            "Desculpe o inconveniente.",
            "Att"
        ]
}

# Perguntas padrão e respostas correspondentes
perguntas_respostas = {"quem é?":[respostas["3DECISOR CONFIRMADO"],['']],
    "oque você quer?":[respostas["3DECISOR CONFIRMADO"],['']],
    "sim sou eu":[respostas["2DECISOR CONFIRMADO"],['']],
    "sou eu":[respostas["2DECISOR CONFIRMADO"],['']],
    "opa":[respostas["DECISOR CONFIRMADO"],['']],
    "eae":[respostas["DECISOR CONFIRMADO"],['']],
    "diga":[respostas["3DECISOR CONFIRMADO"],['']],
    "se apresenta":[respostas["PERDAO"],["Perdão", f"Me Chamo {nome_assistente}"]],
    "sou eu mesmo":[respostas["2DECISOR CONFIRMADO"],['']],
    "ele mesmo":[respostas["2DECISOR CONFIRMADO"],['']],
    "fala mulher":[respostas["DECISOR CONFIRMADO"],['']],
    "fala moça":[respostas["DECISOR CONFIRMADO"],['']],
    "diga mulher":[respostas["DECISOR CONFIRMADO"],['']],
    "diga moça":[respostas["DECISOR CONFIRMADO"],['']],
    "pode falar":[respostas["3DECISOR CONFIRMADO"],['']],
    "como conseguiu meu número?":[respostas["COMO CONSEGUIU MEU NÚMERO?"],respostas["COMO CONSEGUIU MEU NÚMERO?"]],
    "como conseguiu meu contato?":[respostas["COMO CONSEGUIU MEU NÚMERO?"],respostas["COMO CONSEGUIU MEU NÚMERO?"]],
    "onde conseguiu meu número?":[respostas["COMO CONSEGUIU MEU NÚMERO?"],respostas["COMO CONSEGUIU MEU NÚMERO?"]],
    "quem te passou meu contato?":[respostas["COMO CONSEGUIU MEU NÚMERO?"],respostas["COMO CONSEGUIU MEU NÚMERO?"]],
    "quem te passou meu número?":[respostas["COMO CONSEGUIU MEU NÚMERO?"],respostas["COMO CONSEGUIU MEU NÚMERO?"]],
    "agradeço, nosso juridico já está cuidando disso":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "está sendo visto isso":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "já estou dando um jeito nisso":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "já tenho advogado":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "já tenho contador":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "já tenho advogado":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "já tenho contador":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "tem uma empresa resolvendo isso":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "estou cuidando disso":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "estou cuidando disso":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "já está sendo resolvido":[respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"],respostas["MINHA CONTABILIDADE/JURÍDICO JÁ FAZ"]],
    "não tenho interesse":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "obrigada Ana júlia mas não temos interesse no momento":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "obrigado não tenho interesse":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "no momento não":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "deixa pra proxima":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "não quero":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "não to afim":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "quem sabe numa proxima":[respostas["NÃO TEM INTERESSE"],respostas["NÃO TEM INTERESSE"]],
    "já faço esse serviço":[respostas["JÁ FAÇO ESSE SERVIÇO"],respostas["JÁ FAÇO ESSE SERVIÇO"]],
    "não sou o socio":[respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "qual o motivo do contato":[respostas["3DECISOR CONFIRMADO"],['']],
    "qual a razão do contato":[respostas["3DECISOR CONFIRMADO"],['']],
    "sobre oque seria o contato":[respostas["3DECISOR CONFIRMADO"],['']],
    "qual a palta":[respostas["3DECISOR CONFIRMADO"],['']],
    "sobre oque":[respostas["3DECISOR CONFIRMADO"],['']],
    "do que se trata":[respostas["3DECISOR CONFIRMADO"],['']],
    "fala oque você quer":[respostas["3DECISOR CONFIRMADO"],['']],
    "de qual assunto":[respostas["3DECISOR CONFIRMADO"],['']],
    "quem está falando":[respostas["3DECISOR CONFIRMADO"],['']],
    "quem é você":[respostas["3DECISOR CONFIRMADO"],['']],
    "contato errado":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "não sou eu":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "não conheço":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "não tem ninguem aqui com esse nome":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "nunca ouvi falar":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "numero errado":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "acho que você se enganou":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "você está enganado":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "tudo bem e você?":[respostas["BEM E VOCE"],respostas["BEM E VOCE/JA ME APRESENTEI"]],
    "bem e você?":[respostas["BEM E VOCE"],respostas["BEM E VOCE/JA ME APRESENTEI"]],
    "sim e vc ?":[respostas["BEM E VOCE"],respostas["BEM E VOCE/JA ME APRESENTEI"]],
    "bem e vc ?":[respostas["BEM E VOCE"],respostas["BEM E VOCE/JA ME APRESENTEI"]],
    "boa tarde, com quem falo?":[["Boa tarde!"]+respostas["3DECISOR CONFIRMADO"],['']],
    "Boa tarde":[["Boa tarde!"]+respostas["3DECISOR CONFIRMADO"],['Boa tarde!']],
    "boa tarde falo com quem":[["Boa tarde!"]+respostas["3DECISOR CONFIRMADO"],['']],
    "bom dia, com quem falo?":[["Bom dia!"]+respostas["3DECISOR CONFIRMADO"],['']],
    "bom dia falo com quem":[["Bom dia!"]+respostas["3DECISOR CONFIRMADO"],['']],
    "td sim":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "tudo ótimo ! quem é ?":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "td sim, no que posso ajudar":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "tudo bem sim, no que posso te ajudar":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "td sim, oque seria":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "td sim, sobre oque seria":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "tudo bem, no que te ajudo":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "tudo bem, sobre oque seria o assunto":[respostas["BEM"],respostas["BEM/JA ME APRESENTEI"]],
    "oi":[["Oii"]+respostas["3DECISOR CONFIRMADO"],['Oii']],
    "oie":[["Oii"]+respostas["3DECISOR CONFIRMADO"],['Oii']],
    "oii":[["Oii"]+respostas["3DECISOR CONFIRMADO"],['Oii']],
    "ola":[["Oii"]+respostas["3DECISOR CONFIRMADO"],['Oii']],
    "no que posso te ajudar?":[respostas["3DECISOR CONFIRMADO"],['']],
    "boa noite":[["Boa noite!"]+respostas["3DECISOR CONFIRMADO"],['Boa noite!']],
    "assunto?":[respostas["3DECISOR CONFIRMADO"],['']],
    "qual assunto?":[respostas["3DECISOR CONFIRMADO"],['']],
    "sim, sobre o que seria?":[respostas["2DECISOR CONFIRMADO"],['']],
    "fale":[respostas["3DECISOR CONFIRMADO"],['']],
    "você não se apresentou..não sei do que se trata, por isso não deu retorno":[respostas["PERDAO"],["Perdão", f"Me Chamo {nome_assistente}"]],
    "segue":[respostas["3DECISOR CONFIRMADO"],['']],
    "prossiga":[respostas["3DECISOR CONFIRMADO"],['']],
    "referente?":[respostas["3DECISOR CONFIRMADO"],['']],
    "sobre o que seria ?":[respostas["3DECISOR CONFIRMADO"],['']],
    "não é esse número.":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "tudo certo":[respostas["BEM"],["Que ótimo"]],
    "qm ?":[respostas["3DECISOR CONFIRMADO"],['']],
    "não teu seu contato salvo!":[respostas["PERDAO"],["Perdão", f"Me Chamo {nome_assistente}"]],
    "quem é, por favor?":[respostas["PERDAO"],["Perdão", f"{nome_assistente}"]],
    "olá. quem e?":[respostas["PERDAO"],["Perdão", f"Me Chamo {nome_assistente}"]],
    "não te conheso":[respostas["PERDAO"],["Perdão", f"Me Chamo {nome_assistente}"]],
    "boa tarde! desculpe, mas não tenho seu número registrado.":[respostas["PERDAO"],["Perdão", f"Me Chamo {nome_assistente}"]],
    "tudo na paz 🤣💚":[respostas["BEM"],["Que ótimo"]],
    "td bem!":[respostas["BEM"],["Que ótimo"]],
    "de qual empresa? sobre o que?":[respostas["QUE EMPRESA"],[nome_empresa]],
    "você é da vilela?":[['Sim']+respostas["3DECISOR CONFIRMADO"],['Sim']],
    "quem está falando?":[respostas["3DECISOR CONFIRMADO"],['']],
    "boa tarde… pode ser comigo":[respostas["DECISOR CONFIRMADO"],['']],
    "este telefone não é de nenhuma empresa":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "este numero ou telefone não pertence a ele ou ela":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "este numero ou telefone não é de nenhum":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "Bom dia,  esse número não é de jose":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "boa tarde não":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "boa tarde ana":[[f"Boa tarde {nome}"]+respostas["3DECISOR CONFIRMADO"],[f"Boa tarde {nome}"]],
    "bom dia ana":[[f"Bom dia {nome}"]+respostas["3DECISOR CONFIRMADO"],[f"Bom dia {nome}"]],
    "boa noite ana":[[f"Boa noite {nome}"]+respostas["3DECISOR CONFIRMADO"],[f"Boa noite {nome}"]],
    "fala ana":[[f"Oii {nome}"]+respostas["3DECISOR CONFIRMADO"],[f"Oii {nome}"]],
    "De qual empresa":[[nome_empresa]+respostas["3DECISOR CONFIRMADO"],[nome_empresa]],
    "Sobre qual empresa":[[nome_empresa]+respostas["3DECISOR CONFIRMADO"],[nome_empresa]],
    "Qual empresa gostaria de falar":[[nome_empresa]+respostas["3DECISOR CONFIRMADO"],[nome_empresa]],
    "Boa tarde de qual empresa vc está falando meu amigo?":[[nome_empresa]+respostas["3DECISOR CONFIRMADO"],[nome_empresa]],
    "Que empresa":[[nome_empresa]+respostas["3DECISOR CONFIRMADO"],[nome_empresa]],
    "estou em reunião agora, daqui a pouco falo contigo":[respostas["PEDIU PRA LIGAR"],respostas["PEDIU PRA LIGAR"]],
    "Sou eu mesma mas no momento já sai":[respostas["PEDIU PRA LIGAR"],respostas["PEDIU PRA LIGAR"]],
    "Estou ocupado nesse momento":[respostas["PEDIU PRA LIGAR"],respostas["PEDIU PRA LIGAR"]],
    "Me liga daqui uma hora":[respostas["PEDIU PRA LIGAR"],respostas["PEDIU PRA LIGAR"]],
    "To ocupado agora ana":[respostas["PEDIU PRA LIGAR"],respostas["PEDIU PRA LIGAR"]],
    "Tudo bem com você?":[["Tudo ótimo"]+respostas["3DECISOR CONFIRMADO"],['Tudo ótimo']],
    "Você ta bem?":[["Tudo ótimo"]+respostas["3DECISOR CONFIRMADO"],['Tudo ótimo']],
    "Como você ta?":[["Tudo ótimo"]+respostas["3DECISOR CONFIRMADO"],['Tudo ótimo']],
    "Ta bem?":[["Tudo ótimo"]+respostas["3DECISOR CONFIRMADO"],['Tudo ótimo']],
    "Tudo bem Ana?":[["Tudo ótimo"]+respostas["3DECISOR CONFIRMADO"],['Tudo ótimo']],
    "Olá Cliente FGTS! Seu Saldo FGTS foi atualizado! Quer saber mais responda SIM agora para simular!!":[[''],['']],
    "Pizzaria Diegos 🍕🍕🍕 Boa noite, Para Acessar o Cardápio e fazer seu pedido mais rápido clique no link abaixo e faça seu pedido https://xmenu.com.br/pedidos/?loja=18582 Qualquer dúvida digite '2' para falar com atendente":[[''],['']],
    "Pizzaria Diegos boa Noite estamos fora do horário de atendimento iniciamos a partir das 18:00 🍕🍕🍕":[[''],['']],
    "Oi tudo bem? Me passa seu.. Nome: Bairro: Tamanho: Logo vamos atender 🥰":[[''],['']],
    "O Guincho República agradece seu contato. Como podemos ajudar?":[[''],['']],
    "Agradecemos sua mensagem. Em que podemos ajudar? Guincho República 24horas.🚦🛑":[[''],['']],
    "Olá, agradecemos pelo contato. 📝 Para agilizar o seu atendimento me informe por gentileza seu Nome e como posso ajudá-lo, aguarde em alguns instantes já iremos lhe atender 😉 🕒 Nosso Horário de Atendimento na Loja Física e online (Whatsapp) é de Segunda à Sábado das 08hs às 18hs. ✅ Visite e siga nossa página no Instagram 😉 https://www.instagram.com/livrarialevonah/":[[''],['']],
    "Boa tarde esse telefone não é do Ronaldo Barbosa não esse telefone é meu meu nome é Fabiana de Melo":[respostas["TELEFONES INCORRETOS"],respostas["TELEFONES INCORRETOS/JA ME APRESENTEI"]],
    "Com quem eu falo?":[respostas["3DECISOR CONFIRMADO"],["Me chamo Ana Júlia"]],
    "Quem ta falando?":[respostas["3DECISOR CONFIRMADO"],["Me chamo Ana Júlia"]],
    "Com quem você quer falar?":[[""],[""]]
}

# Função para extrair embeddings BERT de um texto
def obter_embedding(texto):
    input_ids = tokenizer.encode(texto, add_special_tokens=True)
    input_ids = np.array(input_ids).reshape(1, -1)
    with torch.no_grad():
        outputs = model(torch.tensor(input_ids))
    return outputs.last_hidden_state.mean(dim=1).numpy()

# Pré-calcular os embeddings BERT para todas as perguntas
perguntas_embeddings = {pergunta:obter_embedding(pergunta) for pergunta in perguntas_respostas.keys()}

# Função para encontrar a melhor correspondência usando BERT e embeddings pré-calculados
def encontrar_correspondencia(mensagem):
    melhor_correspondencia = None
    melhor_similaridade = 0

    # Vetor de embedding da mensagem usando BERT
    mensagem_embedding = obter_embedding(mensagem)

    for pergunta, pergunta_embedding in perguntas_embeddings.items():
        # Calcular a similaridade de cosseno entre os embeddings pré-calculados e a mensagem
        similaridade = cosine_similarity(mensagem_embedding, pergunta_embedding.reshape(1, -1)).item()

        if similaridade > melhor_similaridade:
            melhor_similaridade = similaridade
            melhor_correspondencia = perguntas_respostas[pergunta]

    return melhor_correspondencia, melhor_similaridade

# Função para obter resposta do chatbot
def obter_resposta(mensagem_usuario,nome,nome_empresa, nome_assistente):
    doc = nlp(mensagem_usuario)
    palavras_mensagem = [token.text.lower() for token in doc]
    mensagem_processada = ' '.join(palavras_mensagem)
    correspondencia, similaridade = encontrar_correspondencia(mensagem_processada)

    if similaridade > 0.7:
      p = []
      s = []
      for i in correspondencia[0]:
          i = i.replace("Fulano de tal",nome)
          i = i.replace("Empresa do fulano",nome_empresa)
          i = i.replace("Jurandi",nome_assistente)
          p.append(i)

      for i in correspondencia[1]:
          i = i.replace("Fulano de tal",nome)
          i = i.replace("Jurandi",nome_assistente)
          s.append(i)

      retorna = [p,s]
      return retorna
    else:
        return [""]

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    mensagem_usuario = request.json['mensagem']
    nome = request.json['nome']
    nome_empresa = request.json['nome_empresa']
    whatsid = request.json['whatsid']
    nome_assistente = request.json['nome_assistente']

    if len(vericarSeApresentei(whatsid)) > 0:
        verifica = vericarSeApresentei(whatsid)[0]
        resposta_bot = obter_resposta(mensagem_usuario,nome,nome_empresa)
        if verifica[2] == 0:
            if verifica[1] == 0:
                if f"Olá, me chamo {nome_assistente}, da Villela Bank." in resposta_bot[0] or f"Me chamo {nome_assistente}, da Villela Bank." in resposta_bot[0]:
                    atualiza(whatsid,1)
                elif "NÃO LER" in resposta_bot[0] or "PEDIU PRA LIGAR" in resposta_bot[0]:
                    desliga(whatsid,1)
                return jsonify({'resposta':resposta_bot[0]})
            else: 
                if "NÃO LER" in resposta_bot[1] or "PEDIU PRA LIGAR" in resposta_bot[1]:
                    desliga(whatsid,1)
                return jsonify({'resposta':resposta_bot[1]})
        else:
            return jsonify({'resposta':['']})
    else:
        resposta_bot = obter_resposta(mensagem_usuario,nome,nome_empresa)
        if f"Olá, me {nome_assistente}, da Villela Bank." in resposta_bot[0] or "Me chamo {nome_assistente}, da Villela Bank." in resposta_bot[0]:
            apresentei(whatsid,1,0)
        elif "NÃO LER" in resposta_bot[0] or "PEDIU PRA LIGAR" in resposta_bot[0]:
            apresentei(whatsid,0,1)
        return jsonify({'resposta':resposta_bot[0]})
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)
