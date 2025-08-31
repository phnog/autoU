

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import string

from model.stopwords_pt import STOP_WORDS_PT

os.makedirs('model', exist_ok=True)

emails = [
    ("Por favor, envie o relatório financeiro até sexta-feira", "Produtivo"),
    ("Precisamos revisar o contrato antes da reunião", "Produtivo"),
    ("Você pode atualizar o status das tarefas no sistema?", "Produtivo"),
    ("Segue em anexo o planejamento estratégico do trimestre", "Produtivo"),
    ("Vamos agendar uma reunião para discutir o projeto", "Produtivo"),
    ("O cliente solicitou uma proposta até amanhã", "Produtivo"),
    ("Favor encaminhar os dados da última campanha", "Produtivo"),
    ("Não esqueça de enviar o orçamento revisado", "Produtivo"),
    ("A equipe precisa alinhar os próximos passos", "Produtivo"),
    ("O relatório deve ser entregue até sexta", "Produtivo"),
    ("Podemos marcar uma call para revisar o escopo?", "Produtivo"),
    ("Atualizei a planilha com os novos valores", "Produtivo"),
    ("O documento está pronto para assinatura", "Produtivo"),
    ("Precisamos validar o cronograma com o cliente", "Produtivo"),
    ("Você pode revisar o material antes da apresentação?", "Produtivo"),
    ("A entrega está prevista para quarta-feira", "Produtivo"),
    ("Vamos discutir a estratégia de lançamento", "Produtivo"),
    ("O time está aguardando o feedback do cliente", "Produtivo"),
    ("Encaminhei os arquivos solicitados", "Produtivo"),
    ("A reunião foi confirmada para amanhã às 14h", "Produtivo"),
    ("Olha esse meme que me mandaram, é hilário!", "Improdutivo"),
    ("Bora marcar um happy hour na sexta?", "Improdutivo"),
    ("Você viu o último episódio daquela série?", "Improdutivo"),
    ("Vamos organizar um churrasco no fim de semana", "Improdutivo"),
    ("Achei esse vídeo engraçado, olha só", "Improdutivo"),
    ("Que tal um café para colocar o papo em dia?", "Improdutivo"),
    ("Passa o link daquele jogo que falamos?", "Improdutivo"),
    ("Confira essas fotos da viagem que fizemos", "Improdutivo"),
    ("Vamos planejar uma viagem juntos?", "Improdutivo"),
    ("Tem um meme novo que você precisa ver", "Improdutivo"),
    ("Bora marcar um cinema no sábado?", "Improdutivo"),
    ("Você viu aquele vídeo viral que está circulando?", "Improdutivo"),
    ("Vamos fazer uma pausa para o café?", "Improdutivo"),
    ("Olha esse artigo interessante que encontrei", "Improdutivo"),
    ("E aí, como foi o fim de semana?", "Improdutivo"),
    ("Vamos almoçar fora hoje?", "Improdutivo"),
    ("Achei um restaurante novo, bora conhecer?", "Improdutivo"),
    ("Você viu o jogo ontem?", "Improdutivo"),
    ("Vamos combinar de sair mais tarde?", "Improdutivo"),
    ("Tem uma promoção legal rolando, olha isso", "Improdutivo"),
]

def preprocess(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))

texts, labels = zip(*emails)
texts = [preprocess(t) for t in texts]


vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words=STOP_WORDS_PT,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(texts)


model = MultinomialNB()
model.fit(X, labels)


os.makedirs('model', exist_ok=True)
joblib.dump(vectorizer, 'model/vectorizer.joblib')
joblib.dump(model, 'model/model.joblib')

print("Treinamento concluido.")