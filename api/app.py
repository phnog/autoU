from flask import Flask, request, jsonify, send_from_directory
import io
import os
import PyPDF2

# Importa funções do agente
from main import carregar_email, analisar_email

# Caminho absoluto para frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

app = Flask(
    __name__,
    static_folder=frontend_path,   # caminho absoluto
    static_url_path=""
)

def extract_text_from_bytes(raw_bytes, filename):
    """Extrai texto de arquivos PDF ou TXT enviados pelo front"""
    if filename.lower().endswith('.pdf'):
        reader = PyPDF2.PdfReader(io.BytesIO(raw_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return raw_bytes.decode('utf-8', errors='ignore')

# Serve o index.html corretamente
@app.route('/')
def index():
    return send_from_directory(frontend_path, 'index.html')

# Serve arquivos estáticos (css, js, assets)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(frontend_path, path)

# Endpoint principal
@app.route('/classificar', methods=['POST'])
def classify_endpoint():
    uploaded = request.files.get('emailFile')
    if uploaded and uploaded.filename:
        filename = uploaded.filename
        raw_bytes = uploaded.read()
        text = extract_text_from_bytes(raw_bytes, filename)
    else:
        title = request.form.get('emailTitle', '').strip()
        filename = title if title else 'texto_colado'
        text = request.form.get('emailText', '')

    resultado = analisar_email(text)

    return jsonify(
        filename=filename,
        categoria=resultado["classificacao"],
        resposta=resultado["resposta_sugerida"]
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)

