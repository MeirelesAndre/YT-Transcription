import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Defina essa variável no .env ou via terminal
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def verificar_com_ia(texto_transcrito: str, caminho_base: str) -> str:
    """
    Envia um texto transcrito com erros fonéticos para a IA revisar e traduzir.
    Salva a resposta como traducao.txt na mesma pasta do arquivo base.
    Retorna o conteúdo da resposta.
    """
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY não definido nas variáveis de ambiente.")

    prompt_base = (
        "Este é um texto transcrito automaticamente a partir de uma música do YouTube,\n"
        "mas com possíveis erros fonéticos e de transcrição. Reescreva o texto de forma\n"
        "natural e corrigida (preservando o estilo poético) e, em seguida,\n"
        "forneça uma tradução clara para o português.\n\n"
        "Texto original:\n\n"
    )
    prompt = prompt_base + texto_transcrito.strip()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Você é um revisor lingüístico especializado em corrigir transcrições automáticas de músicas."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Erro ao consultar a API Groq: {response.status_code}\n{response.text}")

    resultado = response.json()
    conteudo = resultado['choices'][0]['message']['content']

    print("\n===== CORREÇÃO IA =====\n")
    print(conteudo)

    caminho_arquivo = os.path.join(caminho_base, "traducao.txt")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return conteudo
