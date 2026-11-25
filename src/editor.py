
import subprocess
import json

from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

MUSICA = BASE_DIR / "audios" / "musica.mp3"
PASTA_VIDEOS = BASE_DIR / "videos"


def criar_video(audio, pasta_imagens):

    audio = Path(audio)
    pasta_imagens = Path(pasta_imagens)

    # Verificar arquivos
    if not audio.is_file():
        raise FileNotFoundError(f"Áudio não encontrado: {audio}")

    if not MUSICA.is_file():
        raise FileNotFoundError(f"Música não encontrada: {MUSICA}")

    # Localizar as 10 imagens
    imagens = sorted(pasta_imagens.glob("cena_*.jpg"))

    if len(imagens) != 10:
        raise ValueError(
            f"Esperadas 10 imagens, mas foram encontradas {len(imagens)}."
        )

    # Descobrir duração da narração
    comando_duracao = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(audio)
    ]

    resultado = subprocess.run(
        comando_duracao,
        capture_output=True,
        text=True,
        check=True
    )

    duracao_audio = float(
        json.loads(resultado.stdout)["format"]["duration"]
    )

    duracao_cena = duracao_audio / len(imagens)

    print(f"\nDuração do áudio: {duracao_audio:.2f} segundos")
    print(f"Duração de cada cena: {duracao_cena:.2f} segundos")

    # Preparar entradas do FFmpeg
    comando = ["ffmpeg", "-y"]

    for imagem in imagens:
        comando.extend([
            "-loop", "1",
            "-framerate", "30",
            "-t", str(duracao_cena),
            "-i", str(imagem)
        ])

    indice_audio = len(imagens)

    comando.extend(["-i", str(audio)])

    indice_musica = indice_audio + 1

    comando.extend([
        "-stream_loop", "-1",
        "-i", str(MUSICA)
    ])

    # Criar filtros das dez cenas
    filtros = []

    for i in range(len(imagens)):
        filtro = (
            f"[{i}:v]"
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "zoompan=z='min(zoom+0.0005,1.15)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            "d=1:s=1080x1920:fps=30,"
            f"trim=duration={duracao_cena},"
            "setpts=PTS-STARTPTS,"
            "format=yuv420p"
            f"[v{i}]"
        )

        filtros.append(filtro)

    entradas = "".join(
        f"[v{i}]" for i in range(len(imagens))
    )

    filtros.append(
        f"{entradas}concat=n=10:v=1:a=0[v];"
        f"[{indice_audio}:a]volume=1.0[voz];"
        f"[{indice_musica}:a]volume=0.12[musica];"
        "[voz][musica]"
        "amix=inputs=2:duration=first:dropout_transition=2[audio]"
    )

    filter_complex = ";".join(filtros)

    # Definir arquivo de saída
    PASTA_VIDEOS.mkdir(parents=True, exist_ok=True)

    nome = datetime.now().strftime(
        "video_%Y%m%d_%H%M%S.mp4"
    )

    saida = PASTA_VIDEOS / nome

    # Finalizar comando
    comando.extend([
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[audio]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(saida)
    ])

    print("\nMontando vídeo com as 10 imagens...")

    subprocess.run(comando, check=True)

    print(f"\nVídeo criado: {saida}")

    return saida
