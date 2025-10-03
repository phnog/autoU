
# Dependências principais
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
import re
import fitz  

# LangChain + Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Pydantic para saída estruturada
from pydantic import BaseModel, Field
from typing import Literal, Dict


load_dotenv()
GOOGLE_API_KEY = getenv("GEMINI_API_KEY")


AI_PROMPT_EMAIL = (
    "Você é um agente de triagem de e-mails. Sua função é analisar o conteúdo de um e-mail "
    "e decidir se ele é PRODUTIVO ou NAO_PRODUTIVO.\n\n"
    "Regras:\n"
    "- PRODUTIVO: Quando o e-mail trata de trabalho, estudo, compromissos, tarefas importantes ou solicitações legítimas.\n"
    "- NAO_PRODUTIVO: Quando o e-mail é irrelevante, propaganda, spam ou não exige resposta.\n\n"
    "Retorne SEMPRE um JSON no seguinte formato:\n"
    "{\n"
    '  \"classificacao\": \"PRODUTIVO\" | \"NAO_PRODUTIVO\",\n'
    '  \"resposta_sugerida\": \"texto curto com sugestão de resposta caso seja PRODUTIVO, ou vazio caso NAO_PRODUTIVO\"\n'
    "}\n"
    "Se for PRODUTIVO, escreva uma resposta curta, educada e objetiva que o usuário poderia enviar."
)


class EmailOut(BaseModel):
    classificacao: Literal["PRODUTIVO", "NAO_PRODUTIVO"]
    resposta_sugerida: str = Field(default="")


llm_email = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY
)

# Cadeia com saída estruturada
email_chain = llm_email.with_structured_output(EmailOut)


def analisar_email(conteudo: str) -> Dict:
    saida: EmailOut = email_chain.invoke([
        SystemMessage(content=AI_PROMPT_EMAIL),
        HumanMessage(content=conteudo)
    ])
    return saida.model_dump()


def carregar_email(entrada: str) -> str:

    caminho = Path(entrada)
    if caminho.exists():
        if caminho.suffix.lower() == ".txt":
            return caminho.read_text(encoding="utf-8")
        elif caminho.suffix.lower() == ".pdf":
            doc = fitz.open(str(caminho))
            texto = " ".join([page.get_text() for page in doc])
            return texto.strip()
    return entrada


