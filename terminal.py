from app.functions.baixar_audio_youtube import baixar_audio_youtube
from app.functions.transcrever_com_whisper import transcrever_com_whisper
from app.functions.separar_vocal_demucs import extrair_vocal_com_demucs 
from app.functions.agents import verificar_com_ia
import os

URL = "https://www.youtube.com/watch?v=me7Ae6d2jRg"

if __name__ == "__main__":
    link = URL
    caminho_mp3 = baixar_audio_youtube(link)
    caminho_wav = extrair_vocal_com_demucs(caminho_mp3)  # novo passo
    texto = transcrever_com_whisper(caminho_wav, modelo='small', forcar=False)
    resposta = verificar_com_ia(texto, caminho_base=os.path.dirname(caminho_wav))
    
    print("\n===== TRANSCRIÇÃO CONCLUÍDA =====\n")
    print(" ")