
from functions.baixar_audio_youtube import baixar_audio_youtube
from functions.transcrever_com_whisper import transcrever_com_whisper

URL = "https://www.youtube.com/watch?v=SZJ4FhvzQGY"


if __name__ == "__main__":
    link = URL
    caminho = baixar_audio_youtube(link)
    texto = transcrever_com_whisper(caminho,'large', True)
    print("\n===== TRANSCRIÇÃO CONCLUÍDA =====\n")
    print(texto)
    print(" ")