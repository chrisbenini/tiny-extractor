import pandas as pd
import requests
import time

BASE_URL = "https://api.tiny.com.br/api2/"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

def extrair_produtos_tiny(
    token: str,
    callback_status,
    pause_event,
    cancel_event,
    sleep_seg=0.5,
    limite=100
):
    produtos_lista = []
    pagina = 1
    total_extraidos = 0

    pause_event.set()  # começa rodando

    while True:
        if cancel_event.is_set():
            break

        pause_event.wait()  # pausa aqui

        callback_status(pagina, total_extraidos, f"Baixando página {pagina}...")

        url_listar = f"{BASE_URL}produtos.pesquisa.php"
        params = {
            "token": token,
            "formato": "json",
            "pagina": pagina,
            "limite": limite
        }

        r = requests.get(url_listar, params=params)
        dados = r.json()

        if dados.get("retorno", {}).get("status") != "OK":
            erros = dados.get("retorno", {}).get("erros", [])
            if erros and "Bloqueada" in erros[0].get("erro", ""):
                callback_status(pagina, total_extraidos, "API bloqueada. Aguardando...")
                time.sleep(3)
                continue
            raise RuntimeError("Erro ao listar produtos")

        produtos = dados["retorno"].get("produtos")
        if not produtos:
            break

        for item in produtos:
            if cancel_event.is_set():
                break

            pause_event.wait()

            id_produto = item["produto"]["id"]

            payload = f"token={token}&formato=JSON&id={id_produto}"
            r2 = requests.post(f"{BASE_URL}produto.obter.php", headers=HEADERS, data=payload)
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

                total_extraidos += 1
                callback_status(pagina, total_extraidos, f"Extraídos {total_extraidos} produtos")

            time.sleep(sleep_seg)

        pagina += 1

    # salva mesmo se cancelar
    df = pd.DataFrame(produtos_lista)
    df.to_excel("base.xlsx", index=False)

    return total_extraidos, pagina
