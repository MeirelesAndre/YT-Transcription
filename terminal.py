from app.functions.baixar_audio_youtube import baixar_audio_youtube
from app.functions.transcrever_com_whisper import transcrever_com_whisper

URL = "https://www.youtube.com/watch?v=me7Ae6d2jRg"


if __name__ == "__main__":
    link = URL
    caminho = baixar_audio_youtube(link)
    texto = transcrever_com_whisper(caminho,'small', False)
    print("\n===== TRANSCRIÇÃO CONCLUÍDA =====\n")
    print(texto)
    print(" ")