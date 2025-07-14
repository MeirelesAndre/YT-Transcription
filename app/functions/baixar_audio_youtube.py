import yt_dlp
import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

URL = 'https://www.youtube.com/watch?v=QDLWghHmBJY'

def sanitize_nome(nome: str) -> str:
    return re.sub(r'[\\/*?:"<>|⧸]', "_", nome)

def baixar_audio_youtube(url: str, destino_base: str = "downloads") -> str:
    """
    Baixa o áudio de um vídeo do YouTube em formato MP3 usando yt-dlp.
    Cria uma subpasta com o nome da música e armazena lá os arquivos relacionados.
    Retorna o caminho do arquivo salvo.
    """
    if not os.path.exists(destino_base):
        os.makedirs(destino_base)
    print("🔗 Baixando do YouTube...")

    # Extrai informações do vídeo (sem baixar)
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        titulo = sanitize_nome(info.get('title', 'audio'))
        pasta_musica = os.path.join(destino_base, titulo)
        caminho_final = os.path.join(pasta_musica, "musica.mp3")

    # Cria a pasta da música, se não existir
    os.makedirs(pasta_musica, exist_ok=True)

    # Verifica se o arquivo já existe
    if os.path.exists(caminho_final):
        print(f"🎵 Áudio já existe: {caminho_final}")
        return caminho_final

    # Define opções de download com caminho ajustado
    nome_arquivo = os.path.join(pasta_musica, 'musica.%(ext)s')
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

    # Faz o download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"✅ Download realizado: {caminho_final}")
    return caminho_final

if __name__ == "__main__":
    link = URL
    caminho = baixar_audio_youtube(link)
    print("\n===== CONCLUÍDO =====\n")
