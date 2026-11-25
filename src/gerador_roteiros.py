
import os
import json
import requests

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_ROTEIROS = BASE_DIR / "roteiros"

load_dotenv(BASE_DIR / ".env")

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

MODELO = "@cf/zai-org/glm-4.7-flash"


def gerar_roteiro(tema):

    if not ACCOUNT_ID or not API_TOKEN:
        raise ValueError("Credenciais da Cloudflare não encontradas no .env")

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{ACCOUNT_ID}/ai/run/{MODELO}"
    )

    instrucoes = f"""
Você é um roteirista profissional especializado em vídeos
cinematográficos para YouTube Shorts.

Sua missão é transformar o tema abaixo em uma história
envolvente, visualmente interessante e cientificamente responsável.

TEMA: {tema}

REGRAS DE QUALIDADE:

1. PRECISÃO:
- Não invente fatos científicos.
- Não apresente especulações como fatos comprovados.
- Não invente números, datas ou estatísticas.
- Respeite as leis conhecidas da física, biologia e natureza.
- Quando houver incerteza científica, deixe isso claro.
- Diferencie consequências imediatas de consequências
  que poderiam acontecer ao longo de milhares ou milhões de anos.

2. NARRATIVA:
- Escreva em português brasileiro.
- Comece com um gancho muito impactante.
- Crie uma história com começo, desenvolvimento e conclusão.
- Apresente acontecimentos específicos relacionados ao tema.
- Mantenha uma sequência cronológica.
- Aumente a tensão gradualmente.
- Crie um clímax surpreendente, mas plausível.
- Termine com uma pergunta interessante para o público.
- Evite frases genéricas e explicações repetitivas.
- Não repita informações entre os parágrafos.

3. DURAÇÃO:
- A narração deve durar aproximadamente 60 segundos.
- Utilize frases naturais e fáceis de narrar.
- Evite textos excessivamente longos.
- Priorize informações interessantes e relevantes.

4. COERÊNCIA:
- Tudo o que acontecer na história deve ter relação com o tema.
- Não introduza acontecimentos sem explicação.
- Não contradiga informações apresentadas anteriormente.
- Não crie fenômenos impossíveis apenas para aumentar o drama.

5. CENAS VISUAIS:
Crie exatamente 10 cenas visuais diferentes.

Cada cena deve:
- Representar um acontecimento da história.
- Seguir a ordem cronológica da narrativa.
- Ser visualmente detalhada.
- Descrever cenário, objetos, personagens e ações.
- Informar iluminação e atmosfera.
- Ter aparência de fotografia cinematográfica realista.
- Manter continuidade visual entre as cenas.
- Não apresentar elementos que contradigam a narração.
- Não repetir o mesmo enquadramento ou acontecimento.

6. ESTILO VISUAL:
- Realismo cinematográfico.
- Aparência de produção de cinema.
- Iluminação dramática e natural.
- Composição vertical 9:16.
- Alta riqueza de detalhes.
- Sem textos, legendas ou marcas d'água.

IMPORTANTE:
As imagens devem ilustrar exatamente o que está sendo narrado.
Não crie imagens apenas porque são visualmente impressionantes.

Responda SOMENTE com JSON válido neste formato:

{{
    "tema": "tema do vídeo",
    "gancho": "abertura impactante",
    "contexto": "contextualização",
    "desenvolvimento": "desenvolvimento da história",
    "climax": "momento de maior impacto",
    "encerramento": "pergunta final",
    "cenas": [
        "descrição detalhada da cena 1",
        "descrição detalhada da cena 2",
        "descrição detalhada da cena 3",
        "descrição detalhada da cena 4",
        "descrição detalhada da cena 5",
        "descrição detalhada da cena 6",
        "descrição detalhada da cena 7",
        "descrição detalhada da cena 8",
        "descrição detalhada da cena 9",
        "descrição detalhada da cena 10"
    ]
}}
"""

    resposta = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um roteirista criativo e especialista em narrativa cinematográfica. Responda somente com o resultado solicitado."
                },
                {
                    "role": "user",
                    "content": instrucoes
                }
            ],
            "max_completion_tokens": 4000,
            "temperature": 0.7,
            "response_format": {
                "type": "json_object"
            },
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
        timeout=(20, 300)
    )

    resposta.raise_for_status()

    dados = resposta.json()

    if not dados.get("success"):
        raise RuntimeError(f"Erro da Cloudflare: {dados}")

    mensagem = dados["result"]["choices"][0]["message"]

    conteudo = mensagem.get("content")

    if not conteudo:
        raise ValueError(
            f"A IA não retornou conteúdo. "
            f"Finalização: {dados['result']['choices'][0].get('finish_reason')}"
        )

    roteiro = json.loads(conteudo)

    if len(roteiro.get("cenas", [])) != 10:
        raise ValueError("A IA não retornou exatamente 10 cenas.")

    print("\nRoteiro criado pela IA com sucesso!")

    return roteiro


def salvar_roteiro(roteiro):

    PASTA_ROTEIROS.mkdir(parents=True, exist_ok=True)

    nome = datetime.now().strftime(
        "roteiro_%Y%m%d_%H%M%S.txt"
    )

    caminho = PASTA_ROTEIROS / nome

    with open(caminho, "w", encoding="utf-8") as arquivo:

        for parte, texto in roteiro.items():

            arquivo.write(f"\n{parte.upper()}\n")

            if isinstance(texto, list):
                for indice, item in enumerate(texto, start=1):
                    arquivo.write(f"{indice}. {item}\n")
            else:
                arquivo.write(texto + "\n")

    return caminho


def converter_para_narracao(roteiro):

    partes = [
        roteiro["gancho"],
        roteiro["contexto"],
        roteiro["desenvolvimento"],
        roteiro["climax"],
        roteiro["encerramento"]
    ]

    return " ".join(partes)


if __name__ == "__main__":

    tema = input("Digite o tema do vídeo: ")

    roteiro = gerar_roteiro(tema)

    caminho = salvar_roteiro(roteiro)

    print(f"\nRoteiro salvo em: {caminho}")
    print("\nTexto para narração:")
    print(converter_para_narracao(roteiro))

    print("\nCENAS VISUAIS:")
    for indice, cena in enumerate(roteiro["cenas"], start=1):
        print(f"{indice}. {cena}")
