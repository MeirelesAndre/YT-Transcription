import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.functions.baixar_audio_youtube import baixar_audio_youtube
from app.functions.transcrever_com_whisper import transcrever_com_whisper

URL = "https://www.youtube.com/watch?v=SZJ4FhvzQGY"


if __name__ == "__main__":
    link = URL
    caminho = baixar_audio_youtube(link)
    texto = transcrever_com_whisper(caminho,'base', False)
    print("\n===== TRANSCRIÇÃO CONCLUÍDA =====\n")
    print(texto)
    print(" ")