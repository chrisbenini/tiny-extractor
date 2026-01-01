import os
import pystray
from PIL import Image
from designer import criar_janela

def abrir_app(icon, item):
    criar_janela()

def sair(icon, item):
    icon.stop()

def iniciar_tray():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(BASE_DIR, "icon.ico")

    if os.path.exists(icon_path):
        image = Image.open(icon_path)
    else:
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

    menu = pystray.Menu(
        pystray.MenuItem("Abrir", abrir_app),
        pystray.MenuItem("Sair", sair)
    )

    icon = pystray.Icon("Tiny Extractor", image, "Tiny Extractor", menu)
    icon.run()
