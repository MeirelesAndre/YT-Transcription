import os
import subprocess
import shutil

def extrair_vocal_com_demucs(caminho_mp3: str) -> str:
    """
    Utiliza Demucs para separar o vocal do instrumental de um arquivo MP3.
    Salva o vocal como 'vocal.wav' na mesma pasta do arquivo original.
    Retorna o caminho do arquivo de voz (ex: downloads/HOME/vocal.wav).
    """
    pasta_destino = os.path.dirname(caminho_mp3)
    vocal_path_destino = os.path.join(pasta_destino, "vocal.wav")

    # Verifica se o arquivo de voz já existe
    if os.path.exists(vocal_path_destino):
        print(f"✅ Voz já extraída: {vocal_path_destino}")
        return vocal_path_destino

    print("🎧 Separando vocal com Demucs...")

    comando = [
        "demucs",
        caminho_mp3,
        "--two-stems", "vocals",
        "-o", pasta_destino
    ]

    resultado = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8")

    if resultado.returncode != 0:
        print("❌ Erro ao executar Demucs:")
        print(resultado.stderr)
        raise RuntimeError("Falha na separação de voz com Demucs")

    # Caminho de origem do vocals.wav
    nome_base = os.path.splitext(os.path.basename(caminho_mp3))[0]
    pasta_temporaria = os.path.join(pasta_destino, "htdemucs", nome_base)
    vocal_path_origem = os.path.join(pasta_temporaria, "vocals.wav")

    if not os.path.exists(vocal_path_origem):
        raise FileNotFoundError(f"Voz não encontrada em {vocal_path_origem}")

    # Move o vocals.wav para a pasta principal com o nome padronizado
    shutil.move(vocal_path_origem, vocal_path_destino)

    # Remove o accompaniment.wav se existir
    accompaniment_path = os.path.join(pasta_temporaria, "accompaniment.wav")
    if os.path.exists(accompaniment_path):
        os.remove(accompaniment_path)

    # Remove pasta temporária criada pelo Demucs
    shutil.rmtree(os.path.join(pasta_destino, "htdemucs"), ignore_errors=True)

    print(f"✅ Voz salva como: {vocal_path_destino}")
    return vocal_path_destino


if __name__ == "__main__":
    teste = "downloads/HOME/musica.mp3"
    caminho_vocal = extrair_vocal_com_demucs(teste)
    print("Vocal extraído para:", caminho_vocal)