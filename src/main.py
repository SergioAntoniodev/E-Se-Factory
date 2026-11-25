
import asyncio
from publicacao import publicar_video
from gerador_imagens import gerar_dez_imagens

from gerador_roteiros import (
    gerar_roteiro,
    salvar_roteiro,
    converter_para_narracao
)

from narracao import gerar_narracao
from editor import criar_video


def executar_producao():

    print("================================")
    print("         ROBÔ E SE...?")
    print("================================")

    tema = input("\nDigite o tema do vídeo: ")

    print("\n[1/4] Gerando roteiro...")

    roteiro = gerar_roteiro(tema)
    caminho_roteiro = salvar_roteiro(roteiro)

    print("\n[2/4] Gerando narração...")

    texto = converter_para_narracao(roteiro)

    caminho_audio = asyncio.run(
        gerar_narracao(texto)
    )

    print("\n[3/5] Gerando 10 imagens com IA...")

    pasta_imagens = gerar_dez_imagens(roteiro)

    print("\n[4/5] Montando vídeo com as imagens...")  
   
    caminho_video = criar_video(caminho_audio, pasta_imagens)

    print("\n[5/5] Publicando no YouTube...")

    video_id = publicar_video(caminho_video, tema)

    print("\n================================")
    print("       PRODUÇÃO CONCLUÍDA!")
    print("================================")

    print(f"Roteiro: {caminho_roteiro}")
    print(f"Áudio: {caminho_audio}")
    print(f"Vídeo: {caminho_video}")
    print(f"ID YouTube: {video_id}")


if __name__ == "__main__":
    executar_producao()
