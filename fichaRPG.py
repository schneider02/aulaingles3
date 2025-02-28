import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Função para conectar ao banco de dados
def conectar_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",      # Altere para seu usuário do MySQL
            password="",      # Altere para sua senha do MySQL
            database="rpg"    # Altere para o nome do seu banco de dados
        )
        return db
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

# Função para adicionar uma ficha no banco
def adicionar_ficha(db):
    nome = entry_nome.get()
    classe = entry_classe.get()
    try:
        nivel = int(entry_nivel.get())
        forca = int(entry_forca.get())
        destreza = int(entry_destreza.get())
        inteligencia = int(entry_inteligencia.get())
        sabedoria = int(entry_sabedoria.get())
        carisma = int(entry_carisma.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos nos campos de nível e atributos.")
        return

    cursor = db.cursor()
    sql = ("INSERT INTO ficha (nome, classe, nivel, forca, destreza, "
           "inteligencia, sabedoria, carisma) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    valores = (nome, classe, nivel, forca, destreza, inteligencia, sabedoria, carisma)

    try:
        cursor.execute(sql, valores)
        db.commit()
        messagebox.showinfo("Sucesso", "Ficha adicionada com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao adicionar ficha: {err}")

# Função para visualizar as fichas no banco
def visualizar_fichas(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ficha")
    result = cursor.fetchall()

    # Limpar a área de texto para nova exibição
    text_fichas.delete(1.0, tk.END)

    if result:
        for row in result:
            text_fichas.insert(tk.END, f"ID: {row[0]} | Nome: {row[1]} | Classe: {row[2]} | Nível: {row[3]}\n")
    else:
        text_fichas.insert(tk.END, "Nenhuma ficha encontrada.\n")

# Função para atualizar uma ficha existente
def atualizar_ficha(db):
    try:
        ficha_id = int(entry_id_atualizar.get())
        nome = entry_nome_atualizar.get()
        classe = entry_classe_atualizar.get()
        nivel = entry_nivel_atualizar.get()
        forca = entry_forca_atualizar.get()
        destreza = entry_destreza_atualizar.get()
        inteligencia = entry_inteligencia_atualizar.get()
        sabedoria = entry_sabedoria_atualizar.get()
        carisma = entry_carisma_atualizar.get()

        cursor = db.cursor()

        sql = "UPDATE ficha SET "
        valores = []
        if nome:
            sql += "nome = %s, "
            valores.append(nome)
        if classe:
            sql += "classe = %s, "
            valores.append(classe)
        if nivel:
            sql += "nivel = %s, "
            valores.append(int(nivel))
        if forca:
            sql += "forca = %s, "
            valores.append(int(forca))
        if destreza:
            sql += "destreza = %s, "
            valores.append(int(destreza))
        if inteligencia:
            sql += "inteligencia = %s, "
            valores.append(int(inteligencia))
        if sabedoria:
            sql += "sabedoria = %s, "
            valores.append(int(sabedoria))
        if carisma:
            sql += "carisma = %s, "
            valores.append(int(carisma))

        sql = sql.rstrip(', ')
        sql += " WHERE id = %s"
        valores.append(ficha_id)

        cursor.execute(sql, tuple(valores))
        db.commit()
        messagebox.showinfo("Sucesso", "Ficha atualizada com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao atualizar ficha: {err}")

# Função para deletar uma ficha
def deletar_ficha(db):
    try:
        ficha_id = int(entry_id_deletar.get())
        cursor = db.cursor()
        cursor.execute("DELETE FROM ficha WHERE id = %s", (ficha_id,))
        db.commit()
        messagebox.showinfo("Sucesso", "Ficha deletada com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um ID válido.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao deletar ficha: {err}")

# Função principal para criar a interface
def criar_interface():
    global entry_nome, entry_classe, entry_nivel, entry_forca, entry_destreza, entry_inteligencia, entry_sabedoria, entry_carisma
    global entry_id_atualizar, entry_nome_atualizar, entry_classe_atualizar, entry_nivel_atualizar, entry_forca_atualizar
    global entry_destreza_atualizar, entry_inteligencia_atualizar, entry_sabedoria_atualizar, entry_carisma_atualizar
    global entry_id_deletar, text_fichas
    
    # Criação da janela principal
    janela = tk.Tk()
    janela.title("Sistema de Fichas de RPG")
    
    # Tela de Adicionar Ficha
    tk.Label(janela, text="Nome do Personagem:").grid(row=0, column=0)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=0, column=1)
    
    tk.Label(janela, text="Classe:").grid(row=1, column=0)
    entry_classe = tk.Entry(janela)
    entry_classe.grid(row=1, column=1)

    tk.Label(janela, text="Nível:").grid(row=2, column=0)
    entry_nivel = tk.Entry(janela)
    entry_nivel.grid(row=2, column=1)

    tk.Label(janela, text="Força:").grid(row=3, column=0)
    entry_forca = tk.Entry(janela)
    entry_forca.grid(row=3, column=1)

    tk.Label(janela, text="Destreza:").grid(row=4, column=0)
    entry_destreza = tk.Entry(janela)
    entry_destreza.grid(row=4, column=1)

    tk.Label(janela, text="Inteligência:").grid(row=5, column=0)
    entry_inteligencia = tk.Entry(janela)
    entry_inteligencia.grid(row=5, column=1)

    tk.Label(janela, text="Sabedoria:").grid(row=6, column=0)
    entry_sabedoria = tk.Entry(janela)
    entry_sabedoria.grid(row=6, column=1)

    tk.Label(janela, text="Carisma:").grid(row=7, column=0)
    entry_carisma = tk.Entry(janela)
    entry_carisma.grid(row=7, column=1)

    tk.Button(janela, text="Adicionar Ficha", command=lambda: adicionar_ficha(db)).grid(row=8, column=0, columnspan=2)
    
    # Tela de Visualizar Fichas
    text_fichas = tk.Text(janela, height=10, width=50)
    text_fichas.grid(row=9, column=0, columnspan=2)

    tk.Button(janela, text="Visualizar Fichas", command=lambda: visualizar_fichas(db)).grid(row=10, column=0, columnspan=2)

    # Tela de Atualizar Ficha
    tk.Label(janela, text="ID da ficha a ser atualizada:").grid(row=11, column=0)
    entry_id_atualizar = tk.Entry(janela)
    entry_id_atualizar.grid(row=11, column=1)

    tk.Label(janela, text="Novo Nome:").grid(row=12, column=0)
    entry_nome_atualizar = tk.Entry(janela)
    entry_nome_atualizar.grid(row=12, column=1)

    tk.Label(janela, text="Nova Classe:").grid(row=13, column=0)
    entry_classe_atualizar = tk.Entry(janela)
    entry_classe_atualizar.grid(row=13, column=1)

    tk.Button(janela, text="Atualizar Ficha", command=lambda: atualizar_ficha(db)).grid(row=14, column=0, columnspan=2)

    # Tela de Deletar Ficha
    tk.Label(janela, text="ID da ficha a ser deletada:").grid(row=15, column=0)
    entry_id_deletar = tk.Entry(janela)
    entry_id_deletar.grid(row=15, column=1)

    tk.Button(janela, text="Deletar Ficha", command=lambda: deletar_ficha(db)).grid(row=16, column=0, columnspan=2)

    janela.mainloop()

if __name__ == "__main__":
    db = conectar_db()
    if db:
        criar_interface()

