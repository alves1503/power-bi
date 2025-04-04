import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup

def extrair_ops_de_arquivo(caminho_arquivo):
    """Lê um arquivo HTML/MHTML e extrai as ordens de produção (OPs) que possuem exatamente 7 dígitos."""
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        content = file.read()
    
    soup = BeautifulSoup(content, "html.parser")
    text_content = soup.get_text()
    
    # Procurar apenas números com exatamente 7 dígitos
    op_pattern = re.findall(r"\b\d{7}\b", text_content)
    return set(op_pattern)  # Remove duplicatas

def verificar_ordens(novo_arquivo, pasta_antiga):
    """Verifica se as ordens de produção do novo arquivo já foram enviadas antes."""
    ops_novas = extrair_ops_de_arquivo(novo_arquivo)
    ops_ja_enviadas = {}
    
    for arquivo in os.listdir(pasta_antiga):
        if arquivo.endswith(".html") or arquivo.endswith(".mhtml"):
            caminho_arquivo = os.path.join(pasta_antiga, arquivo)
            ops_encontradas = extrair_ops_de_arquivo(caminho_arquivo)
            
            for op in ops_novas:
                if op in ops_encontradas:
                    if op not in ops_ja_enviadas:
                        ops_ja_enviadas[op] = []
                    ops_ja_enviadas[op].append(arquivo)
    
    resultado = ""
    for op in ops_novas:
        if op in ops_ja_enviadas:
            resultado += f"A OP {op} já foi enviada nos arquivos: {', '.join(ops_ja_enviadas[op])}.\n"
        else:
            resultado += f"A OP {op} ainda não foi enviada.\n"
    
    return resultado.strip()

def executar_verificacao():
    novo_arquivo = filedialog.askopenfilename(title="Selecione o novo arquivo", filetypes=[("Arquivos HTML", "*.html;*.mhtml")])
    pasta_antiga = filedialog.askdirectory(title="Selecione a pasta com os relatórios antigos")
    
    if not novo_arquivo or not pasta_antiga:
        messagebox.showwarning("Aviso", "Novo arquivo ou pasta antiga não selecionados.")
        return
    
    resultado = verificar_ordens(novo_arquivo, pasta_antiga)
    text_resultado.config(state=tk.NORMAL)
    text_resultado.delete("1.0", tk.END)
    text_resultado.insert(tk.END, resultado)
    text_resultado.config(state=tk.DISABLED)

def criar_interface():
    """Cria a interface gráfica do aplicativo."""
    root = tk.Tk()
    root.title("Verificar OPs")
    root.geometry("500x400")
    
    tk.Label(root, text="Selecione o arquivo do novo dia e a pasta com arquivos antigos:").pack(pady=5)
    
    btn_verificar = tk.Button(root, text="Selecionar Arquivos e Verificar", command=executar_verificacao)
    btn_verificar.pack(pady=10)
    
    global text_resultado
    text_resultado = tk.Text(root, height=15, width=60, state=tk.DISABLED)
    text_resultado.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    criar_interface()
