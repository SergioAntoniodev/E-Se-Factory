
import os
import requests
import base64

from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_IMAGENS = BASE_DIR / "imagens"

load_dotenv(BASE_DIR / ".env")

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

MODELO = "@cf/black-forest-labs/flux-1-schnell"


def gerar_imagem(prompt, caminho_saida):
    if not ACCOUNT_ID or not API_TOKEN:
        raise ValueError("Credenciais da Cloudflare não encontradas.")

    PASTA_IMAGENS.mkdir(parents=True, exist_ok=True)

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{ACCOUNT_ID}/ai/run/{MODELO}"
    )

    cabecalhos = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    dados = {
        "prompt": prompt
    }

    resposta = requests.post(
        url,
        headers=cabecalhos,
        json=dados,
        timeout=180
    )

    if resposta.status_code != 200:
        raise RuntimeError(
            f"Erro Cloudflare: {resposta.status_code} - {resposta.text}"
        )

    resultado = resposta.json()

    imagem_base64 = resultado["result"]["image"]

    imagem_bytes = base64.b64decode(imagem_base64)

    caminho = Path(caminho_saida)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(imagem_bytes)

    print(f"Imagem criada: {caminho}")

    return caminho



def gerar_dez_imagens(roteiro):

    # Utilizar as 10 cenas criadas pela IA
    cenas = roteiro["cenas"]

    if len(cenas) != 10:
        raise ValueError("O roteiro precisa conter exatamente 10 cenas.")

    print("\nIniciando geração das 10 cenas...")

    from datetime import datetime

    pasta_video = PASTA_IMAGENS / datetime.now().strftime(
        "video_%Y%m%d_%H%M%S"
    )

    pasta_video.mkdir(parents=True, exist_ok=True)

    for indice, descricao in enumerate(cenas, start=1):

        prompt = (
            f"{descricao}. "
            "Cinematic photorealistic photography, "
            "realistic human anatomy, dramatic cinematic lighting, "
            "high detail, coherent visual storytelling, "
            "vertical 9:16 composition, "
            "no text, no watermark."
        )

        print(f"\nGerando cena {indice}/10...")
        print(f"Descrição: {descricao}")

        caminho = pasta_video / f"cena_{indice:02d}.jpg"

        gerar_imagem(prompt, caminho)

    print("\nAs 10 cenas foram geradas!")

    return pasta_video


if __name__ == "__main__":

    roteiro_teste = {
        "gancho": "Um enorme asteroide está se aproximando da Terra.",
        "contexto": "Cientistas detectam o asteroide e alertam os governos.",
        "desenvolvimento": "As cidades começam a entrar em pânico.",
        "climax": "O asteroide atravessa a atmosfera e ilumina o céu.",
        "encerramento": "A humanidade observa o impacto iminente."
    }

    gerar_dez_imagens(roteiro_teste)
