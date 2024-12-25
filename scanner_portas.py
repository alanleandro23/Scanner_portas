import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import socket
import csv
import json
import threading
import os
from time import sleep
from datetime import datetime
import subprocess
import re

# Função para detectar serviço com base na porta (exemplo simples)
def detectar_servico(porta):
    servicos = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS",
        110: "POP3",
        143: "IMAP",
        3306: "MySQL",
        5432: "PostgreSQL",
        8080: "HTTP Alternativo",
        161: "SNMP",
        162: "SNMP Trap",
        137: "NetBIOS - Name Service",
        138: "NetBIOS - Datagram Service",
        139: "NetBIOS - Session Service",
        3389: "RDP",
        514: "Syslog",
        119: "NNTP",
        6660: "IRC",
        6661: "IRC",
        6662: "IRC",
        6663: "IRC",
        6664: "IRC",
        6665: "IRC",
        6666: "IRC",
        6667: "IRC",
        6668: "IRC",
        6669: "IRC",
        5900: "VNC",
        27017: "MongoDB",
        6379: "Redis",
        11211: "Memcached"
    }
    return servicos.get(porta, "Desconhecido")

# Função para obter a data e hora atual
def obter_data_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Função para verificar o formato de IP (IPv4)
def verificar_ip(host):
    regex = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(regex, host):
        octetos = host.split('.')
        if all(0 <= int(octeto) <= 255 for octeto in octetos):
            return True
        else:
            return False
    return False

# Função para verificar se o hostname pode ser resolvido
def verificar_hostname(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False

# Função para verificar a porta
def verificar_porta(host, porta, barra_progresso, total_portas, tabela_resultados, arquivo_resultados, status_label):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        resultado = s.connect_ex((host, porta))
        servico = detectar_servico(porta)
        
        # Obter data e hora da verificação
        data_hora = obter_data_hora()

        if resultado == 0:
            status = "Aberta"
        else:
            status = "Fechada"
        
        # Adicionar os resultados na tabela
        tabela_resultados.insert("", "end", values=(porta, status, servico, data_hora))
        
        # Escrever no arquivo diretamente
        mensagem = f"[{data_hora}] Porta {porta} ({servico}) está {status}.\n"
        arquivo_resultados.write(mensagem)

        s.close()
    except socket.timeout:
        data_hora = obter_data_hora()
        mensagem = f"[{data_hora}] Timeout ao verificar a porta {porta}.\n"
        arquivo_resultados.write(mensagem)
        tabela_resultados.insert("", "end", values=(porta, "Erro", "Desconhecido", data_hora))
    except Exception as e:
        data_hora = obter_data_hora()
        mensagem = f"[{data_hora}] Erro ao verificar a porta {porta}: {e}\n"
        arquivo_resultados.write(mensagem)
        tabela_resultados.insert("", "end", values=(porta, "Erro", "Desconhecido", data_hora))

    # Atualizar a barra de progresso e o rótulo com informações detalhadas
    barra_progresso['value'] += (100 / total_portas)
    status_label.config(text=f"Escaneando porta {porta} de {total_portas}")
    root.update_idletasks()

# Função para salvar os resultados em CSV ou JSON
def salvar_resultados():
    formato = formato_var.get()  # Obter o formato selecionado (CSV ou JSON)

    if formato == "CSV":
        salvar_csv()
    elif formato == "JSON":
        salvar_json()

# Função para salvar os resultados em CSV
def salvar_csv():
    try:
        pasta_resultados = os.path.join("historico", obter_data_hora().replace(":", "-").replace(" ", "_"))
        os.makedirs(pasta_resultados, exist_ok=True)

        caminho_csv = os.path.join(pasta_resultados, "resultados_scan.csv")
        
        with open(caminho_csv, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Porta", "Status", "Serviço", "DataRegistro"])
            for linha in tabela_resultados.get_children():
                valores = tabela_resultados.item(linha)['values']
                writer.writerow(valores)

        messagebox.showinfo("Sucesso", f"Resultados salvos com sucesso em CSV em {caminho_csv}!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar os resultados em CSV: {e}")

# Função para salvar os resultados em JSON
def salvar_json():
    try:
        pasta_resultados = os.path.join("historico", obter_data_hora().replace(":", "-").replace(" ", "_"))
        os.makedirs(pasta_resultados, exist_ok=True)

        caminho_json = os.path.join(pasta_resultados, "resultados_scan.json")
        
        resultados = []
        for linha in tabela_resultados.get_children():
            valores = tabela_resultados.item(linha)['values']
            resultados.append({"Porta": valores[0], "Status": valores[1], "Serviço": valores[2], "DataRegistro": valores[3]})
        
        with open(caminho_json, "w") as jsonfile:
            json.dump(resultados, jsonfile, indent=4)

        messagebox.showinfo("Sucesso", f"Resultados salvos com sucesso em JSON em {caminho_json}!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar os resultados em JSON: {e}")

# Função para realizar o escaneamento
def escanear():
    host = entry_host.get()
    try:
        inicio = int(entry_inicio.get())
        fim = int(entry_fim.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos para as portas.")
        return

    if not host:
        messagebox.showerror("Erro", "Por favor, insira um IP ou hostname.")
        return
    
    if not (verificar_ip(host) or verificar_hostname(host)):
        messagebox.showerror("Erro", "Endereço IP ou hostname inválido.")
        return

    if inicio < 1 or fim > 65535 or inicio > fim:
        messagebox.showerror("Erro", "Intervalo de portas inválido.")
        return

    btn_escaneamento.config(state=tk.DISABLED, bg="gray")
    btn_salvar.config(state=tk.DISABLED)
    btn_abrir_pasta.config(state=tk.DISABLED)  
    btn_cancelar.config(state=tk.NORMAL, bg="red")

    tabela_resultados.delete(*tabela_resultados.get_children())  
    barra_progresso['value'] = 0

    global escaneando
    escaneando = True

    def iniciar_escaneamento():
        total_portas = fim - inicio + 1

        pasta_resultados = os.path.join("historico", obter_data_hora().replace(":", "-").replace(" ", "_"))
        os.makedirs(pasta_resultados, exist_ok=True)

        with open(os.path.join(pasta_resultados, "resultados_scan.txt"), "w") as arquivo_resultados:
            for porta in range(inicio, fim + 1):
                if not escaneando:
                    break
                verificar_porta(host, porta, barra_progresso, total_portas, tabela_resultados, arquivo_resultados, status_label)
            messagebox.showinfo("Concluído", "Escaneamento concluído!")

        btn_escaneamento.config(state=tk.NORMAL, bg="green")
        btn_salvar.config(state=tk.NORMAL)
        btn_abrir_pasta.config(state=tk.NORMAL)

    threading.Thread(target=iniciar_escaneamento).start()

# Função para cancelar o escaneamento
def cancelar_escaneamento():
    global escaneando
    escaneando = False
    messagebox.showinfo("Cancelado", "O escaneamento foi cancelado.")

def abrir_pasta():
    try:
        # Caminho do diretório onde o arquivo foi salvo
        pasta = os.path.dirname(os.path.abspath("resultados_scan.txt"))
        # Abrir a pasta no explorador de arquivos
        if os.name == 'nt':  # Para Windows
            subprocess.Popen(f'explorer {pasta}')
        elif os.name == 'posix':  # Para Linux/Mac
            subprocess.Popen(['xdg-open', pasta])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir a pasta: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Scanner de Portas")
root.geometry("800x600")

# Label e Entry para o IP/Hostname
tk.Label(root, text="Endereço IP/Hostname:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_host = tk.Entry(root, font=("Arial", 12))
entry_host.grid(row=0, column=1, padx=10, pady=10)

# Label e Entry para a Porta Inicial
tk.Label(root, text="Porta Inicial:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_inicio = tk.Entry(root, font=("Arial", 12))
entry_inicio.grid(row=1, column=1, padx=10, pady=10)

# Label e Entry para a Porta Final
tk.Label(root, text="Porta Final:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_fim = tk.Entry(root, font=("Arial", 12))
entry_fim.grid(row=2, column=1, padx=10, pady=10)

# Barra de Progresso
barra_progresso = ttk.Progressbar(root, length=400, mode="determinate", maximum=100)
barra_progresso.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

# Rótulo de status
status_label = tk.Label(root, text="Status: Pronto", font=("Arial", 12))
status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Tabela para exibir os resultados
tabela_resultados = ttk.Treeview(root, columns=("Porta", "Status", "Serviço", "DataRegistro"), show="headings")
tabela_resultados.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Definindo as colunas
tabela_resultados.heading("Porta", text="Porta")
tabela_resultados.heading("Status", text="Status")
tabela_resultados.heading("Serviço", text="Serviço")
tabela_resultados.heading("DataRegistro", text="DataRegistro")

# Botões
btn_escaneamento = tk.Button(root, text="Iniciar Escaneamento", font=("Arial", 14), bg="green", command=escanear)
btn_escaneamento.grid(row=6, column=0, padx=10, pady=10)

btn_cancelar = tk.Button(root, text="Cancelar", font=("Arial", 14), bg="red", command=cancelar_escaneamento, state=tk.DISABLED)
btn_cancelar.grid(row=6, column=1, padx=10, pady=10)

btn_salvar = tk.Button(root, text="Salvar Resultados", font=("Arial", 14), command=salvar_resultados, state=tk.DISABLED)
btn_salvar.grid(row=7, column=0, padx=10, pady=10)

btn_abrir_pasta = tk.Button(root, text="Abrir Pasta de Resultados", font=("Arial", 14), command=abrir_pasta, state=tk.DISABLED)
btn_abrir_pasta.grid(row=7, column=1, padx=10, pady=10)

# Formato de salvamento
formato_var = tk.StringVar(value="CSV")
tk.Label(root, text="Escolha o formato de salvamento:", font=("Arial", 12)).grid(row=8, column=0, padx=10, pady=10, sticky="w")
tk.Radiobutton(root, text="CSV", font=("Arial", 12), variable=formato_var, value="CSV").grid(row=8, column=1, padx=10, pady=10, sticky="w")
tk.Radiobutton(root, text="JSON", font=("Arial", 12), variable=formato_var, value="JSON").grid(row=8, column=1, padx=10, pady=10, sticky="e")

# Ajustar as colunas da tabela
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
