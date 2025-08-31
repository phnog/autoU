from flask import Flask, request, jsonify
import joblib
import io
import string
import PyPDF2
import os
import re

app = Flask(
    __name__,
    static_folder='frontend',
    static_url_path=''
)


VECTOR_PATH = 'model/vectorizer.joblib'
MODEL_PATH  = 'model/model.joblib'

vectorizer = joblib.load(VECTOR_PATH)
model      = joblib.load(MODEL_PATH)

def preprocess(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))

def extract_text_from_bytes(raw_bytes, filename):
    if filename.lower().endswith('.pdf'):
        reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return raw_bytes.decode('utf-8', errors='ignore')

def classify_text(text):
    cleaned = preprocess(text)
    return model.predict(vectorizer.transform([cleaned]))[0]

def gerar_resposta(texto_email):
    """
    Gera respostas mais personalizadas:
    - Extrai prazo (ex: até sexta, até amanhã, até 10h)
    - Detecta tópicos chave (relatório, reunião, orçamento, proposta)
    - Monta uma frase natural de confirmação
    """
    t = texto_email.strip()


    prazo = None
    m = re.search(r'at[eé]\s+([^\.,;!\n]+)', t, re.IGNORECASE)
    if m:
        prazo = m.group(1).strip()


    topicos = {
        'relatório': 'relatório',
        'reunião': 'reunião',
        'orçamento': 'orçamento',
        'proposta': 'proposta',
        'documento': 'documento',
        'campanha': 'campanha',
        'dados': 'dados'
    }
    topico_encontrado = None
    for chave, nome in topicos.items():
        if re.search(rf'\b{chave}\b', t, re.IGNORECASE):
            topico_encontrado = nome
            break


    partes = ["Olá,"]

    if topico_encontrado:
        if prazo:
            partes.append(
                f"entendi o {topico_encontrado} e você precisa dele até {prazo}. "
                "Vou providenciar e te envio dentro desse prazo."
            )
        else:
            partes.append(
                f"recebi o {topico_encontrado} e já estou trabalhando nele."
            )
    else:
        if prazo:
            partes.append(f"vou garantir que esteja tudo pronto até {prazo}.")
        else:
            partes.append("vou analisar e retorno em breve.")

    partes.append("Qualquer coisa, estou à disposição.")
    return " ".join(partes)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/classificar', methods=['POST'])
def classify_endpoint():
    uploaded = request.files.get('emailFile')
    if uploaded and uploaded.filename:
        filename  = uploaded.filename
        raw_bytes = uploaded.read()
        text      = extract_text_from_bytes(raw_bytes, filename)
    else:
        title    = request.form.get('emailTitle', '').strip()
        filename = title if title else 'texto_colado'
        text     = request.form.get('emailText', '')

    categoria = classify_text(text)

    resposta = ""
    if categoria == "Produtivo":
        resposta = gerar_resposta(text)

    return jsonify(filename=filename, categoria=categoria, resposta=resposta)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
