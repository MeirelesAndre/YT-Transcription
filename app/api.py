from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
import os
import sys
from contextlib import contextmanager
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.functions.baixar_audio_youtube import baixar_audio_youtube
from app.functions.transcrever_com_whisper import transcrever_com_whisper

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@contextmanager
def medir_tempo_execucao():
    inicio = time.time()
    yield lambda: time.time() - inicio

@app.get("/")
def form(request: Request):
    return templates.TemplateResponse("transcricao.html", {"request": request})

@app.get("/transcrever")
async def transcrever_url(request: Request, url: str):
    def etapas():
        yield "🔗 Recebendo URL...<br>\n"
        caminho_mp3 = baixar_audio_youtube(url)
        titulo = os.path.splitext(os.path.basename(caminho_mp3))[0]
        yield f"📥 Áudio baixado: {titulo}.mp3<br>\n"

        caminho_txt = os.path.join("downloads", f"{titulo}.txt")
        caminho_srt = os.path.join("downloads", f"{titulo}.srt")

        if os.path.exists(caminho_txt) and os.path.exists(caminho_srt):
            yield f"📝 Transcrição já existente: 📄{caminho_txt} e 🎬{caminho_srt}<br>\n"
            with open(caminho_txt, "r", encoding="utf-8") as f:
                yield f"<pre>{f.read()}</pre>"
            return

        yield "🧠 Carregando modelo Whisper...<br>\n"
        with medir_tempo_execucao() as tempo:
            texto = transcrever_com_whisper(caminho_mp3)
        yield f"📝 Transcrição completa ({tempo():.2f}s):<br><pre>{texto}</pre>"

    return StreamingResponse(etapas(), media_type="text/html")
