# Use uma imagem base Python
FROM python:3.9

# Diretório de trabalho no contêiner
WORKDIR app

# Copiar os arquivos do seu diretório local para o diretório de trabalho no contêiner
COPY . /app

# Adicione o comando para baixar o modelo do spaCy e instalar as dependências
RUN pip install -r requirements.txt
RUN python -m spacy download pt_core_news_sm

# Executar os comandos para importar bibliotecas e criar objetos
RUN python -c "import joblib"
RUN python -c "import spacy"
RUN python -c "from sklearn.metrics.pairwise import cosine_similarity"
RUN python -c "from transformers import AutoTokenizer, AutoModel"

# Carregar os objetos e salvá-los
RUN python -c "import joblib; nlp = spacy.load('pt_core_news_sm'); joblib.dump(nlp, 'spacy_model.pkl')"
RUN python -c "import joblib; tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased'); joblib.dump(tokenizer, 'bert_tokenizer.pkl')"
RUN python -c "import joblib; model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased'); joblib.dump(model, 'bert_model.pkl')"

# Expor a porta 3000 (seu aplicativo está ouvindo nessa porta?)
EXPOSE 3000

# Comando para iniciar o aplicativo
CMD ["python", "app.py"]
