import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from util.tempo import formatar_tempo

def salvar_transcricao_txt(texto: str, caminho_txt: str):
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(texto)

def salvar_transcricao_srt(segments, caminho_srt: str):
    with open(caminho_srt, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            f.write(f"{i}\n")
            f.write(f"{formatar_tempo(segment['start'])} --> {formatar_tempo(segment['end'])}\n")
            f.write(f"{segment['text'].strip()}\n\n")