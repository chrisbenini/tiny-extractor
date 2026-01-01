from PIL import Image
import pandas as pd
import threading
import requests
import pystray
import time
import os

# ================= CONFIG =================
TOKEN = "48fd2f4a545bdf71eff988b2b83c56237c1f3f5ba67f164de47d2a2edd174816"
BASE_URL = "https://api.tiny.com.br/api2/"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
OUTPUT_FILE = "Base.xlsx"

cancel_event = threading.Event()

def extrair_produtos():
    produtos_lista = []
    pagina = 1
    total = 0
    inicio = time.time()

    while True:
        if cancel_event.is_set():
            break

        print(f"[Tiny] Baixando página {pagina}...")

        params = {
            "token": TOKEN,
            "formato": "json",
            "pagina": pagina,
            "limite": 100
        }

        r = requests.get(f"{BASE_URL}produtos.pesquisa.php", params=params)
        dados = r.json()

        if dados.get("retorno", {}).get("status") != "OK":
            erros = dados.get("retorno", {}).get("erros", [])
            if erros and "Bloqueada" in erros[0].get("erro", ""):
                time.sleep(3)
                continue
            break

        produtos = dados["retorno"].get("produtos")
        if not produtos:
            break

        for item in produtos:
            if cancel_event.is_set():
                break

            id_produto = item["produto"]["id"]
            payload = f"token={TOKEN}&formato=JSON&id={id_produto}"

            r2 = requests.post(
                f"{BASE_URL}produto.obter.php",
                headers=HEADERS,
                data=payload
            )
            detalhes = r2.json()

            if "produto" in detalhes.get("retorno", {}):
                p = detalhes["retorno"]["produto"]
                produtos_lista.append({
                    "codigo": p.get("codigo"),
                    "nome": p.get("nome"),
                    "preco": p.get("preco"),
                    "preco_custo": p.get("preco_custo"),
                    "preco_custo_medio": p.get("preco_custo_medio"),
                    "gtin": p.get("gtin"),
                    "marca": p.get("marca"),
                    "peso_liquido": p.get("peso_liquido")
                })
                total += 1

            time.sleep(1)

        pagina += 1

    # salva mesmo se cancelar
    df = pd.DataFrame(produtos_lista)
    df.to_excel(OUTPUT_FILE, index=False)

    duracao = int(time.time() - inicio)
    print(f"[Tiny] Finalizado. Produtos: {total} | Tempo: {duracao}s")

    return total


def iniciar_extracao(icon):
    def task():
        total = extrair_produtos()
        icon.notify(
            f"Extração finalizada ({total} produtos)",
            "Tiny Extractor"
        )
        icon.stop()

    threading.Thread(target=task, daemon=True).start()


def cancelar(icon, item):
    cancel_event.set()
    icon.notify("Cancelando extração...", "Tiny Extractor")


def sair(icon, item):
    cancel_event.set()
    icon.stop()


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "icon.ico")

    image = Image.open(icon_path) if os.path.exists(icon_path) else Image.new("RGBA", (64, 64))

    menu = pystray.Menu(
        pystray.MenuItem("Cancelar", cancelar),
        pystray.MenuItem("Sair", sair)
    )

    icon = pystray.Icon(
        "TinyExtractorHeadless",
        image,
        "Tiny Extractor (Headless)",
        menu
    )

    iniciar_extracao(icon)
    icon.run()

if __name__ == "__main__":
    main()
