# Use uma imagem base Python
FROM python:3.9

# Diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do seu diretório local para o diretório de trabalho no contêiner
COPY . /app

# Adicione o comando para baixar o modelo do spaCy
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm

# Expor a porta 3000 (seu aplicativo está ouvindo nessa porta?)
EXPOSE 3000

# Comando para iniciar o aplicativo
CMD python ./app.py
