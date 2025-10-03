# Classificador de Emails Produtivos

Este projeto oferece uma aplicação web para classificar mensagens como produtivas ou improdutivas. Emails identificados como produtivos recebem uma resposta sugerida automaticamente. O frontend é estático (HTML/CSS/JS) e o backend roda em Flask com um classificador Naive Bayes implementado em Python puro.

---

## 🚀 Funcionalidades

- Classificação de texto colado ou upload de arquivo (.txt / .pdf)  
- Tag indicativa de categoria (Produtivo / Improdutivo)  
- Resposta sugerida automática para emails produtivos  
- Interface interativa: clique para revelar ou ocultar a resposta  
- Modelo leve sem dependências pesadas de machine learning  

---



## 🔧 Pré-requisitos

- Python 3.8 ou superior  
- pip instalado no sistema  

---

## ⚙️ Instalação

1. Clone o repositório  

2. Instale as dependências  
```bash
pip install -r requirements.txt
```

---

## 🧠 Treinamento do Modelo

O script `train.py` gera o arquivo `model/model.json` com as estatísticas do classificador Naive Bayes:

```bash
python train_model.py
```

---

## 🧪 Executando Localmente

Acesse a pasta 'api'

```
cd api
```
Inicie o servidor Flask:

```bash
python app.py
```

Abra no navegador:

```
http://localhost:5000
```
---
## Deploy no Render

O deploy no render precisa de 50segs para iniciar. 
https://autou-vclb.onrender.com

