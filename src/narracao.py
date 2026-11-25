
import asyncio
import edge_tts

from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_AUDIOS = BASE_DIR / "audios"

VOZ = "pt-BR-AntonioNeural"


async def gerar_narracao(texto):

    PASTA_AUDIOS.mkdir(parents=True, exist_ok=True)

    nome = datetime.now().strftime(
        "narracao_%Y%m%d_%H%M%S.mp3"
    )

    caminho = PASTA_AUDIOS / nome

    comunicacao = edge_tts.Communicate(
        text=texto,
        voice=VOZ,
        rate="-5%",
        volume="+0%"
    )

    await comunicacao.save(str(caminho))

    print(f"Narração criada: {caminho}")

    return caminho


if __name__ == "__main__":

    texto = input("Digite o texto para narrar: ")

    asyncio.run(gerar_narracao(texto))
