
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENCIAIS = BASE_DIR / "client_secrets.json"
TOKEN = BASE_DIR / "token.json"

ESCOPO = ["https://www.googleapis.com/auth/youtube.upload"]


def autenticar():
    credenciais = None

    if TOKEN.exists():
        credenciais = Credentials.from_authorized_user_file(
            str(TOKEN), ESCOPO
        )

    if credenciais and credenciais.expired and credenciais.refresh_token:
        credenciais.refresh(Request())

    if not credenciais or not credenciais.valid:
        fluxo = InstalledAppFlow.from_client_secrets_file(
            str(CREDENCIAIS), ESCOPO
        )
        credenciais = fluxo.run_local_server(port=0)

        TOKEN.write_text(
            credenciais.to_json(),
            encoding="utf-8"
        )

    return build("youtube", "v3", credentials=credenciais)


def publicar_video(caminho_video, tema):
    caminho_video = Path(caminho_video)

    if not caminho_video.is_file():
        raise FileNotFoundError(
            f"Vídeo não encontrado: {caminho_video}"
        )

    if not CREDENCIAIS.is_file():
        raise FileNotFoundError(
            "Arquivo client_secrets.json não encontrado."
        )

    youtube = autenticar()

    corpo = {
        "snippet": {
            "title": f"E se {tema}?",
            "description": (
                f"Imagine se {tema}!\n\n"
                "#ESe #Curiosidades #Shorts"
            ),
            "tags": ["E se", "curiosidades", "ciência", "shorts"],
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }

    arquivo_video = MediaFileUpload(
        str(caminho_video),
        mimetype="video/mp4",
        chunksize=5 * 1024 * 1024,
        resumable=True
    )

    requisicao = youtube.videos().insert(
        part="snippet,status",
        body=corpo,
        media_body=arquivo_video
    )

    resposta = None

    print("\nEnviando vídeo para o YouTube...")

    while resposta is None:
        status, resposta = requisicao.next_chunk()

        if status:
            progresso = int(status.progress() * 100)
            print(f"Upload: {progresso}%")

    video_id = resposta["id"]

    print("\nUpload concluído!")
    print(f"Link: https://www.youtube.com/watch?v={video_id}")
    print("Privacidade: privado")

    return video_id
