<h1 align="center">🖥️ Tiny Extractor — Extração de Produtos (Tiny ERP)</h1>

<p align="center">
  Aplicação em Python para automação da extração de dados de produtos do Tiny ERP,
  com suporte a interface gráfica (Desktop) e execução em segundo plano (Headless).
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python">
  <img alt="desktop" src="https://img.shields.io/badge/Desktop%20App-Tkinter-informational?style=flat-square">
  <img src="https://img.shields.io/badge/ERP-Tiny-orange">
  <img src="https://img.shields.io/badge/status-Projeto%20Real-success">
</p>

---  

## 🎯 Objetivo do projeto

Automatizar a extração de dados de produtos do **Tiny ERP**, eliminando processos manuais,
lentos e sujeitos a erro, e entregando uma **base estruturada em Excel** pronta para análise.

### Dados extraídos:

- Código
- Nome do produto
- Preço
- Preço de custo
- Preço de custo médio
- GTIN
- Marca
- Peso líquido

O projeto foi pensado para **uso real em ambiente corporativo**, atendendo tanto usuários finais quanto servidores.

---

### 🧠 Visão geral da solução

O Tiny Extractor possui **dois modos de operação**, atendendo diferentes cenários:

### 🖥️ Modo 1 — Aplicação Desktop (GUI)
Interface gráfica simples e intuitiva para uso diário.

**Funcionalidades:**
- Interface amigável (Tkinter)
- Execução em segundo plano via **System Tray**
- Controles de execução:
  - ▶ Iniciar
  - ⏸ Pausar
  - ▶ Continuar
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
- Máquinas virtuais (VMs)
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

🧾 Dependências do projeto

Adicione esta seção:

## 📦 Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`.

Para instalar todas de uma vez:

```bash
pip install -r requirements.txt
```
Principais bibliotecas utilizadas:

- requests – Comunicação com a API do Tiny ERP
- pandas – Manipulação e estruturação dos dados
- openpyxl – Geração de planilhas Excel
- Tkinter – Interface gráfica (Desktop)
- pystray – Integração com System Tray
- Pillow – Manipulação de imagens (ícones)
- PyInstaller – Geração de executável (.exe)

📦 Geração do executável (.exe)

O projeto não versiona arquivos .exe, mas o processo de geração está documentado.

### Requisitos
```bash
pip install pyinstaller
```

🔹 Versão Desktop (GUI)

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
🔹 Versão Headless (Background)
```bash
pyinstaller --onefile --windowed `
  --icon automacao_2\icon.ico `
  --add-data "automacao_2\icon.ico;." `
  automacao_2/headless_tiny.py
```
📁 O executável final será gerado na pasta:
```bash
dist/
```
## 🚫 Arquivos ignorados (.gitignore)

O projeto utiliza um arquivo `.gitignore` para evitar versionar arquivos desnecessários, como:

- Ambientes virtuais (`.venv/`)
- Arquivos temporários do Python (`__pycache__/`)
- Builds e executáveis gerados (`dist/`, `build/`, `.exe`)
- Arquivos de saída (Excel, logs)

🧰 Stack utilizada
- Python 3.10+
- requests
- pandas
- openpyxl
- Tkinter
- pystray
- Pillow
- PyInstaller

🏢 Contexto de uso real

Projeto desenvolvido com foco em automação de rotinas no varejo, resultando em:
- Padronização dos dados
- Redução de erros operacionais
- Ganho significativo de tempo
- Facilidade de uso por usuários não técnicos

📌 Observação final

O Tiny Extractor foi pensado como um projeto de produto, não apenas como script:
- Interface para usuário final
- Versão técnica para servidores
- Código organizado e reutilizável
- Documentação clara para reprodução
