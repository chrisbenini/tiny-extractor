<div align="center">

# 🖥️ Tiny Extractor — Extração de Produtos (Tiny ERP)

**Aplicação em Python para automação de extração de dados do Tiny ERP**,  

- 🖥️ **Interface gráfica (Desktop App)**
- ⚙️ **Modo headless (background / servidor / agendador)**
Projeto focado em **automação para varejo**, resolvendo tarefas que normalmente são manuais, lentas e repetitivas.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Desktop App](https://img.shields.io/badge/Desktop%20App-Tkinter-blueviolet)
![Automation](https://img.shields.io/badge/Automation-Varejo-success)
![ERP](https://img.shields.io/badge/ERP-Tiny-orange)

</div>

---

## 🎯 Objetivo do projeto

Automatizar a extração de dados de produtos do Tiny ERP, gerando uma base estruturada em Excel com informações como:

- Código
- Nome do produto
- Preço
- Preço de custo
- Preço de custo médio
- GTIN
- Marca
- Peso líquido

O projeto foi pensado para atender **dois cenários reais**:
- Usuário final (desktop)
- Servidores, VMs e rotinas agendadas

---

## 🖥️ Modo 1 — Aplicação Desktop (GUI)

Aplicação com **interface gráfica em Tkinter**, voltada para uso diário por usuários.

### Funcionalidades

- Interface gráfica simples e intuitiva
- Execução em segundo plano via **System Tray**
- Controles de execução:
  - ▶️ Iniciar
  - ⏸️ Pausar
  - ▶️ Continuar
  - ❌ Cancelar
- Feedback visual de progresso (páginas e total de produtos)
- Exportação automática para Excel (`.xlsx`)

📂 Código localizado em:

automacao_1/

Rodar em modo desenvolvimento:
```bash
python automacao_1/main.py
```

⚙️ Modo 2 — Headless (Background / Servidor)

Versão sem interface gráfica, ideal para:
- Servidores
- Máquinas virtuais
- Agendador de Tarefas do Windows
- Execuções automáticas

### Características

- Nenhuma janela é exibida
- Aplicação roda diretamente em segundo plano
- Ícone aparece apenas no System Tray
- Menu de contexto:
  - ❌ Cancelar execução
  - ❌ Encerrar aplicação
- Geração do Excel mesmo em caso de cancelamento

📂 Código localizado em:

automacao_2/

Rodar em modo desenvolvimento:
```bash
python automacao_2/headless_tiny.py
```

📦 Geração do executável (.exe)

O projeto não versiona arquivos .exe, mas o README explica como gerar localmente.

### Requisitos
```bash
pip install pyinstaller
```

🖥️ Gerar .exe da versão com interface gráfica

## PowerShell
```bash
pyinstaller --onefile --windowed `
  --icon automacao_1\icon.ico `
  --add-data "automacao_1\icon.ico;." `
  automacao_1\main.py
```
## CMD
```bash
pyinstaller --onefile --windowed ^
  --icon automacao_1\icon.ico ^
  --add-data "automacao_1\icon.ico;." ^
  automacao_1\main.py
```
⚙️ Gerar .exe da versão headless (background)
```bash
pyinstaller --onefile --windowed `
  --icon automacao_2\icon.ico `
  --add-data "automacao_2\icon.ico;." `
  automacao_2/headless_tiny.py
```
📌 O executável final será gerado na pasta:

```bash
dist/
```
🧰 Stack utilizada
- Python 3.10+
- requests
- pandas
- openpyxl
- Tkinter
- pystray
- Pillow
- PyInstaller

💡 Contexto de uso real

Este projeto foi desenvolvido com foco em automação de rotinas no varejo, reduzindo tarefas manuais e garantindo:
- Padronização dos dados
- Ganho de tempo
- Menos erros operacionais
- Facilidade de uso por usuários não técnicos

📌 Observação final

O Tiny Extractor foi pensado como um projeto de produto, não apenas como script:
- Interface para usuário final
- Versão técnica para servidores
- Código organizado e reutilizável
- Documentação clara para reprodução
