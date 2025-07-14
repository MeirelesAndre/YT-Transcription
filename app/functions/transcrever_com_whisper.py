import whisper
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from util.transcricoes import salvar_transcricao_txt, salvar_transcricao_srt 

def transcrever_com_whisper(caminho_audio, modelo="base", forcar=False):
    """
    Transcreve o áudio com Whisper e salva a transcrição 
    como um arquivo .txt e .srt no mesmo diretório do áudio.
    """
    print("🧠 Carregando modelo Whisper...")
    model = whisper.load_model(modelo)

    pasta = os.path.dirname(caminho_audio)
    caminho_txt = os.path.join(pasta, "letra_extraida.txt")
    caminho_srt = os.path.join(pasta, "legenda.srt")

    texto = None
    resultado = None
    if not forcar:
        if os.path.exists(caminho_txt) and not os.path.exists(caminho_srt):
            print(f"📄 Transcrição texto já existe: {caminho_txt}")
            with open(caminho_txt, "r", encoding="utf-8") as f:
                texto = f.read()
            print("🎬 Gerando apenas o .srt...")
            resultado = model.transcribe(caminho_audio)
            salvar_transcricao_srt(resultado["segments"], caminho_srt)
            return texto

        if not os.path.exists(caminho_txt) and os.path.exists(caminho_srt):
            print(f"🎬 Transcrição SRT já existe: {caminho_srt}")
            print("📄 Gerando apenas o .txt...")
            resultado = model.transcribe(caminho_audio)
            texto = resultado["text"]
            salvar_transcricao_txt(texto, caminho_txt)
            return texto

        if os.path.exists(caminho_txt) and os.path.exists(caminho_srt):
            print(f"Transcrição já existente: 📄{caminho_txt} e 🎬{caminho_srt}")
            with open(caminho_txt, "r", encoding="utf-8") as f:
                return f.read()

    print("🚀 Forçando transcrição" if forcar else "🚀 Transcrevendo...")
    resultado = model.transcribe(caminho_audio)
    print("🗣️ Idioma detectado:", resultado["language"])

    texto = resultado["text"]
    salvar_transcricao_txt(texto, caminho_txt)
    salvar_transcricao_srt(resultado["segments"], caminho_srt)
    return texto
