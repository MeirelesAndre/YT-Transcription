import whisper
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.util.transcrições import salvar_transcricao_txt, salvar_transcricao_srt 


URL = ""

def transcrever_com_whisper(caminho_audio, modelo="base", forcar=False):
    """
    Transcreve o áudio com Whisper e salva a transcrição 
    como um arquivo .txt e .srt no mesmo diretório do áudio.
    """
    print("Carregando modelo Whisper...")
    model = whisper.load_model(modelo)
    
    # Gera caminho do .txt com mesmo nome do áudio
    nome_base = os.path.splitext(os.path.basename(caminho_audio))[0]
    pasta = os.path.dirname(caminho_audio)
    caminho_txt = os.path.join(pasta, f"{nome_base}.txt")
    caminho_srt = os.path.join(pasta, f"{nome_base}.srt")

    texto = None
    resultado = None
    if not forcar:
        # Se apenas SRT faltando
        if os.path.exists(caminho_txt) and not os.path.exists(caminho_srt):
            print(f"Transcrição texto já existe: {caminho_txt}")
            with open(caminho_txt, "r", encoding="utf-8") as f:
                texto = f.read()
            print("Gerando apenas o .srt...")
            resultado = model.transcribe(caminho_audio)
            salvar_transcricao_srt(resultado["segments"], caminho_srt)
            return texto

        # Se apenas TXT faltando
        if not os.path.exists(caminho_txt) and os.path.exists(caminho_srt):
            print(f"Transcrição SRT já existe: {caminho_srt}")
            print("Gerando apenas o .txt...")
            resultado = model.transcribe(caminho_audio)
            texto = resultado["text"]
            salvar_transcricao_txt(texto, caminho_txt)
            return texto

        # Se ambos já existirem
        if os.path.exists(caminho_txt) and os.path.exists(caminho_srt):
            print(f"Transcrição já existente: {caminho_txt} e {caminho_srt}")
            with open(caminho_txt, "r", encoding="utf-8") as f:
                return f.read()

    # Nenhum existe (ou forçando) → processa normalmente
    print("Forçando transcrição" if forcar else "Transcrevendo...")
    resultado = model.transcribe(caminho_audio)
    print("Idioma detectado:", resultado["language"])
    
    texto = resultado["text"]
    salvar_transcricao_txt(texto, caminho_txt)
    salvar_transcricao_srt(resultado["segments"], caminho_srt)
    return texto

if __name__ == "__main__":
    link = URL
    
    texto = transcrever_com_whisper(caminho)
    print("\n--- TRANSCRIÇÃO CONCLUÍDA ---\n")
    print(texto)
    print(" ")