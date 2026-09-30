import tkinter as tk
from tkinter import messagebox
import json
import os


# ==========================================
# CONFIGURAÇÕES
# ==========================================

NOME_APP = "Atarefado"

PASTA_DADOS = os.path.join(
    os.getenv("APPDATA") or os.path.expanduser("~"),
    NOME_APP
)

os.makedirs(PASTA_DADOS, exist_ok=True)

ARQUIVO_TAREFAS = os.path.join(
    PASTA_DADOS,
    "tarefas.json"
)


# ==========================================
# CARREGAR TAREFAS
# ==========================================

def carregar_tarefas():
    if os.path.exists(ARQUIVO_TAREFAS):
        try:
            with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except:
            return []

    return []


# ==========================================
# SALVAR TAREFAS
# ==========================================

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=4)


# ==========================================
# ATUALIZAR CONTADOR
# ==========================================

def atualizar_contador():
    total = len(tarefas)
    concluidas = sum(1 for tarefa in tarefas if tarefa["concluida"])
    pendentes = total - concluidas

    contador.config(
        text=f"{concluidas} concluída(s)  •  {pendentes} pendente(s)"
    )


# ==========================================
# MARCAR/DESMARCAR TAREFA
# ==========================================

def alterar_tarefa(indice):
    tarefas[indice]["concluida"] = not tarefas[indice]["concluida"]

    salvar_tarefas()
    atualizar_lista()


# ==========================================
# EXCLUIR TAREFA
# ==========================================

def excluir_tarefa(indice):
    resposta = messagebox.askyesno(
        "Excluir tarefa",
        "Tem certeza que deseja excluir esta tarefa?"
    )

    if resposta:
        tarefas.pop(indice)

        salvar_tarefas()
        atualizar_lista()


# ==========================================
# LIMPAR TAREFAS CONCLUÍDAS
# ==========================================

def limpar_concluidas():
    global tarefas

    concluidas = sum(1 for tarefa in tarefas if tarefa["concluida"])

    if concluidas == 0:
        messagebox.showinfo(
            "Atarefado",
            "Não existem tarefas concluídas para limpar."
        )
        return

    resposta = messagebox.askyesno(
        "Limpar concluídas",
        f"Excluir as {concluidas} tarefa(s) concluída(s)?"
    )

    if resposta:
        tarefas = [
            tarefa for tarefa in tarefas
            if not tarefa["concluida"]
        ]

        salvar_tarefas()
        atualizar_lista()


# ==========================================
# ADICIONAR TAREFA
# ==========================================

def adicionar_tarefa():
    texto = entrada_tarefa.get().strip()

    if texto == "":
        messagebox.showwarning(
            "Atarefado",
            "Digite uma tarefa antes de adicionar."
        )
        return

    nova_tarefa = {
        "texto": texto,
        "concluida": False
    }

    tarefas.append(nova_tarefa)

    entrada_tarefa.delete(0, tk.END)

    salvar_tarefas()
    atualizar_lista()

    entrada_tarefa.focus()


# ==========================================
# ATUALIZAR LISTA NA TELA
# ==========================================

def atualizar_lista():

    for widget in lista_frame.winfo_children():
        widget.destroy()

    if len(tarefas) == 0:

        mensagem = tk.Label(
            lista_frame,
            text="Nenhuma tarefa adicionada ainda.",
            font=("Segoe UI", 12),
            fg="#777777",
            bg="#f5f5f5"
        )

        mensagem.pack(pady=40)

    else:

        for indice, tarefa in enumerate(tarefas):

            linha = tk.Frame(
                lista_frame,
                bg="white",
                bd=1,
                relief="solid"
            )

            linha.pack(
                fill="x",
                padx=5,
                pady=5
            )

            # Checkbox visual
            if tarefa["concluida"]:
                simbolo = "☑"
            else:
                simbolo = "☐"

            checkbox = tk.Button(
                linha,
                text=simbolo,
                command=lambda i=indice: alterar_tarefa(i),
                font=("Segoe UI Symbol", 18),
                fg="#222222",
                bg="white",
                activebackground="white",
                relief="flat",
                bd=0,
                cursor="hand2"
            )

            checkbox.pack(
                side="left",
                padx=(8, 2)
            )

            # Texto da tarefa
            if tarefa["concluida"]:
                texto_cor = "#888888"
                fonte = ("Segoe UI", 11, "overstrike")
            else:
                texto_cor = "#222222"
                fonte = ("Segoe UI", 11)

            texto = tk.Label(
                linha,
                text=tarefa["texto"],
                font=fonte,
                fg=texto_cor,
                bg="white",
                anchor="w"
            )

            texto.pack(
                side="left",
                fill="x",
                expand=True,
                pady=12
            )

            # Botão excluir
            botao_excluir = tk.Button(
                linha,
                text="✕",
                command=lambda i=indice: excluir_tarefa(i),
                font=("Segoe UI", 10, "bold"),
                fg="#cc3333",
                bg="white",
                activebackground="#ffeeee",
                relief="flat",
                bd=0,
                cursor="hand2"
            )

            botao_excluir.pack(
                side="right",
                padx=10
            )

    atualizar_contador()


# ==========================================
# JANELA PRINCIPAL
# ==========================================

janela = tk.Tk()

janela.title(NOME_APP)

janela.geometry("650x650")

janela.minsize(550, 500)

janela.configure(bg="#f5f5f5")


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    janela,
    text="📚 Atarefado",
    font=("Segoe UI", 26, "bold"),
    fg="#222222",
    bg="#f5f5f5"
)

titulo.pack(
    pady=(25, 5)
)


subtitulo = tk.Label(
    janela,
    text="Organize suas tarefas e não esqueça de nada.",
    font=("Segoe UI", 11),
    fg="#777777",
    bg="#f5f5f5"
)

subtitulo.pack(
    pady=(0, 20)
)


# ==========================================
# ÁREA PARA ADICIONAR TAREFA
# ==========================================

area_adicionar = tk.Frame(
    janela,
    bg="#f5f5f5"
)

area_adicionar.pack(
    fill="x",
    padx=30
)


entrada_tarefa = tk.Entry(
    area_adicionar,
    font=("Segoe UI", 12),
    relief="solid",
    bd=1
)

entrada_tarefa.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8,
    padx=(0, 10)
)


botao_adicionar = tk.Button(
    area_adicionar,
    text="+ Adicionar",
    command=adicionar_tarefa,
    font=("Segoe UI", 11, "bold"),
    bg="#222222",
    fg="white",
    activebackground="#444444",
    activeforeground="white",
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
)

botao_adicionar.pack(
    side="right"
)


# Permitir adicionar usando ENTER
entrada_tarefa.bind(
    "<Return>",
    lambda evento: adicionar_tarefa()
)


# ==========================================
# CONTADOR
# ==========================================

contador = tk.Label(
    janela,
    text="0 concluída(s)  •  0 pendente(s)",
    font=("Segoe UI", 10),
    fg="#777777",
    bg="#f5f5f5"
)

contador.pack(
    pady=15
)


# ==========================================
# LISTA DE TAREFAS
# ==========================================

container_lista = tk.Frame(
    janela,
    bg="#f5f5f5"
)

container_lista.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 10)
)


canvas = tk.Canvas(
    container_lista,
    bg="#f5f5f5",
    highlightthickness=0
)

barra_rolagem = tk.Scrollbar(
    container_lista,
    orient="vertical",
    command=canvas.yview
)

lista_frame = tk.Frame(
    canvas,
    bg="#f5f5f5"
)


lista_frame.bind(
    "<Configure>",
    lambda evento: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas.create_window(
    (0, 0),
    window=lista_frame,
    anchor="nw"
)


canvas.configure(
    yscrollcommand=barra_rolagem.set
)


canvas.pack(
    side="left",
    fill="both",
    expand=True
)


barra_rolagem.pack(
    side="right",
    fill="y"
)


# ==========================================
# BOTÃO LIMPAR CONCLUÍDAS
# ==========================================

botao_limpar = tk.Button(
    janela,
    text="🧹 Limpar tarefas concluídas",
    command=limpar_concluidas,
    font=("Segoe UI", 10),
    fg="#555555",
    bg="#f5f5f5",
    activebackground="#eeeeee",
    relief="flat",
    cursor="hand2"
)

botao_limpar.pack(
    pady=(0, 20)
)


# ==========================================
# INICIALIZAÇÃO
# ==========================================

tarefas = carregar_tarefas()

atualizar_lista()

entrada_tarefa.focus()

janela.mainloop()