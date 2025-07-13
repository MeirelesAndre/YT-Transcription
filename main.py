import uvicorn
import webbrowser
import time
import threading

url = 'https://www.youtube.com/watch?v=y79eFeGM6zM'  # Cole aqui o link do YouTube se quiser fixar
if not url:
    url = input("🔗 Cole o link do YouTube para transcrição: ")

if not url.startswith("http"):
    print("❌ URL inválida. Certifique-se de colar um link completo do YouTube.")
    exit()

localhost = 'http://localhost:8000/docs'
curl = f'http://localhost:8000/transcrever?url={url}'


def abrir_api():
    # Espera o servidor subir e abre no navegador
    time.sleep(2)
    print("🌐 Abrindo navegador em:", curl)
    webbrowser.open(curl)

# Iniciar o servidor FastAPI
if __name__ == "__main__":
    print("🚀 Iniciando FastAPI...")
    threading.Thread(target=abrir_api).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)