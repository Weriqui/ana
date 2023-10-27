# Use uma imagem base Python
FROM python:3.9

# Diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do seu diretório local para o diretório de trabalho no contêiner
COPY . /app

# Adicione o comando para baixar o modelo do spaCy
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm


#Baixar os arquivos para o conteiner
RUN python import joblib
RUN python import spacy
RUN python from sklearn.metrics.pairwise import cosine_similarity
RUN python from transformers import AutoTokenizer, AutoModel

RUN python nlp = spacy.load('pt_core_news_sm')
RUN python tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
RUN python model = AutoModel.from_pretrained("neuralmind/bert-base-portuguese-cased")

RUN python joblib.dump(nlp, 'spacy_model.pkl')
RUN python joblib.dump(tokenizer, 'bert_tokenizer.pkl')
RUN python joblib.dump(model, 'bert_model.pkl')

# Expor a porta 3000 (seu aplicativo está ouvindo nessa porta?)
EXPOSE 3000

# Comando para iniciar o aplicativo
CMD python ./app.py
