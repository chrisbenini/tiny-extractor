import tkinter as tk
from tkinter import messagebox
import threading
import os
from extractor import extrair_produtos_tiny

TOKEN = "SEU_TOKEN_AQUI"

# CORES
BG = "#0f172a"
FG = "#e5e7eb"
ACCENT = "#38bdf8"
BTN = "#1e293b"
BTN_HOVER = "#334155"
DANGER = "#ef4444"


def criar_janela():
    # ===== JANELA =====
    root = tk.Tk()
    root.title("Tiny Extractor")
    root.geometry("560x360")
    root.configure(bg=BG)
    root.resizable(False, False)

    # ÍCONE
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # ===== EVENTOS DE CONTROLE =====
    pause_event = threading.Event()
    cancel_event = threading.Event()
    pause_event.set()

    # ===== VARIÁVEIS =====
    status_var = tk.StringVar(value="Aguardando início")
    pagina_var = tk.StringVar(value="Páginas: -")
    total_var = tk.StringVar(value="Produtos: 0")

    # ===== CONTAINER =====
    container = tk.Frame(root, bg=BG)
    container.pack(expand=True)

    # ===== TÍTULO =====
    tk.Label(
        container,
        text="Tiny Extractor",
        font=("Segoe UI", 18, "bold"),
        fg=ACCENT,
        bg=BG
    ).pack(pady=(10, 20))

    # ===== STATUS =====
    tk.Label(container, textvariable=status_var, fg=FG, bg=BG, font=("Segoe UI", 12)).pack()
    tk.Label(container, textvariable=pagina_var, fg="#94a3b8", bg=BG).pack(pady=2)
    tk.Label(container, textvariable=total_var, fg="#94a3b8", bg=BG).pack(pady=(0, 20))

    # ===== CALLBACK THREAD-SAFE =====
    def callback_status(pagina, total, msg):
        root.after(0, lambda: (
            status_var.set(msg),
            pagina_var.set(f"Páginas: {pagina}"),
            total_var.set(f"Produtos: {total}")
        ))

    # ===== BOTÃO ARREDONDADO =====
    def _rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def botao_arredondado(parent, texto, cor, comando, width=160, height=48, radius=18):
        wrap = tk.Frame(parent, bg=BG)
        c = tk.Canvas(wrap, width=width, height=height, bg=BG, highlightthickness=0)
        c.pack()

        shape = _rounded_rect(c, 2, 2, width - 2, height - 2, radius, fill=cor, outline=cor)
        label = c.create_text(width // 2, height // 2, text=texto, fill=FG, font=("Segoe UI", 11, "bold"))

        def on_enter(_):
            c.itemconfig(shape, fill=BTN_HOVER, outline=BTN_HOVER)

        def on_leave(_):
            c.itemconfig(shape, fill=cor, outline=cor)

        def on_click(_):
            comando()

        c.bind("<Enter>", on_enter)
        c.bind("<Leave>", on_leave)
        c.bind("<Button-1>", on_click)

        c.tag_bind(label, "<Enter>", on_enter)
        c.tag_bind(label, "<Leave>", on_leave)
        c.tag_bind(label, "<Button-1>", on_click)

        return wrap

    # ===== FRAMES DE CONTROLE =====
    frame_iniciar = tk.Frame(container, bg=BG)
    frame_iniciar.pack(pady=20)

    frame_acoes = tk.Frame(container, bg=BG)

    # ===== AÇÕES =====
    def iniciar():
        frame_iniciar.pack_forget()
        frame_acoes.pack(pady=10)

        pause_event.set()
        cancel_event.clear()
        status_var.set("Iniciando...")

        def tarefa():
            try:
                total, pagina = extrair_produtos_tiny(
                    TOKEN,
                    callback_status,
                    pause_event,
                    cancel_event
                )
                root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Finalizado",
                        f"Processo encerrado\nTotal: {total}\nArquivo base.xlsx gerado"
                    )
                )
            except Exception as e:
                msg = str(e)
                root.after(0, lambda m=msg: messagebox.showerror("Erro", m))
            finally:
                root.after(0, resetar_interface)

        threading.Thread(target=tarefa, daemon=True).start()

    def pausar():
        pause_event.clear()
        status_var.set("Pausado")

    def continuar():
        pause_event.set()
        status_var.set("Continuando...")

    def cancelar():
        cancel_event.set()
        pause_event.set()
        status_var.set("Cancelando...")

    def resetar_interface():
        frame_acoes.pack_forget()
        frame_iniciar.pack(pady=20)

        status_var.set("Aguardando início")
        pagina_var.set("Páginas: -")
        total_var.set("Produtos: 0")

    # ===== BOTÃO INICIAR (ÚNICO VISÍVEL NO INÍCIO) =====
    btn_iniciar = botao_arredondado(frame_iniciar, "Iniciar", ACCENT, iniciar, width=180, height=52, radius=22)
    btn_iniciar.pack()

    # ===== BOTÕES DE AÇÃO (INVISÍVEIS NO INÍCIO) =====
    btn_pausar = botao_arredondado(frame_acoes, "Pausar", BTN, pausar, width=160, height=48, radius=18)
    btn_continuar = botao_arredondado(frame_acoes, "Continuar", BTN, continuar, width=160, height=48, radius=18)
    btn_cancelar = botao_arredondado(frame_acoes, "Cancelar", DANGER, cancelar, width=160, height=48, radius=18)

    btn_pausar.pack(side="left", padx=8)
    btn_continuar.pack(side="left", padx=8)
    btn_cancelar.pack(side="left", padx=8)

    # ===== LOOP PRINCIPAL =====
    root.mainloop()
