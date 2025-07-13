import yt_dlp
import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

URL = 'https://www.youtube.com/watch?v=QDLWghHmBJY'

def sanitize_nome(nome: str) -> str:
    return re.sub(r'[\\/*?:"<>|⧸]', "_", nome)

def baixar_audio_youtube(url: str, destino: str = "downloads") -> str:
    """
    Baixa o áudio de um vídeo do YouTube em formato MP3 usando yt-dlp.
    Se o arquivo já existir, não realiza novo download.
    Retorna o caminho do arquivo salvo.
    """
    if not os.path.exists(destino):
        os.makedirs(destino)
    print("🔗 Baixando do YouTube...")

    # Primeiro, extrai informações do vídeo (sem baixar)
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        titulo = re.sub(r'[\\/*?:"<>|⧸]', "_", info.get('title', 'audio'))
        caminho_final = os.path.join(destino, f"{titulo}.mp3")

    # Verifica se o arquivo já existe
    if os.path.exists(caminho_final):
        print(f"🎵 Áudio já existe: {caminho_final}")
        return caminho_final

    # Define opções de download
    nome_arquivo = os.path.join(destino, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': nome_arquivo,
        'quiet': False,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Faz o download se necessário
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print (f"✅Download relizado : {caminho_final}")
    return caminho_final

if __name__ == "__main__":
    link = URL
    caminho = baixar_audio_youtube(link)
    print(" ")
    print("\n===== CONCLUÍDO =====\n")
    print(" ")