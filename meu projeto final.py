import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


def conectar():
    return sqlite3.connect('controle_horas.db')


def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS registros_horas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            cliente TEXT NOT NULL,
            tarefa TEXT NOT NULL,
            horas_trabalhadas REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def inserir_horas():
    cliente = entry_cliente.get()
    tarefa = entry_tarefa.get()
    hora_inicio = entry_hora_inicio.get()
    hora_fim = entry_hora_fim.get()

    if cliente and tarefa and hora_inicio and hora_fim:
        try:
            
            inicio = datetime.strptime(hora_inicio, '%H:%M')
            fim = datetime.strptime(hora_fim, '%H:%M')

            
            horas_trabalhadas = (fim - inicio).seconds / 3600

          
            conn = conectar()
            c = conn.cursor()
            c.execute('INSERT INTO registros_horas (data, cliente, tarefa, horas_trabalhadas) VALUES (?, ?, ?, ?)',
                      (datetime.now().strftime('%Y-%m-%d'), cliente, tarefa, horas_trabalhadas))
            conn.commit()
            conn.close()

            messagebox.showinfo('Sucesso', 'Horas registradas com sucesso!')
            mostrar_registros()
        except ValueError:
            messagebox.showerror('Erro', 'Formato de hora inválido. Utilize HH:MM.')
    else:
        messagebox.showerror('Erro', 'Por favor, preencha todos os campos.')


def mostrar_registros():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM registros_horas')
    registros = c.fetchall()
    for registro in registros:
        tree.insert("", "end", values=(registro[0], registro[1], registro[2], registro[3], f'{registro[4]:.2f}'))
    conn.close()


janela = tk.Tk()
janela.title('Controle de Horas')


label_cliente = tk.Label(janela, text='Cliente:')
label_cliente.grid(row=0, column=0, padx=10, pady=10)
entry_cliente = tk.Entry(janela)
entry_cliente.grid(row=0, column=1, padx=10, pady=10)

label_tarefa = tk.Label(janela, text='Tarefa:')
label_tarefa.grid(row=1, column=0, padx=10, pady=10)
entry_tarefa = tk.Entry(janela)
entry_tarefa.grid(row=1, column=1, padx=10, pady=10)

label_hora_inicio = tk.Label(janela, text='Hora Início (HH:MM):')
label_hora_inicio.grid(row=2, column=0, padx=10, pady=10)
entry_hora_inicio = tk.Entry(janela)
entry_hora_inicio.grid(row=2, column=1, padx=10, pady=10)

label_hora_fim = tk.Label(janela, text='Hora Fim (HH:MM):')
label_hora_fim.grid(row=3, column=0, padx=10, pady=10)
entry_hora_fim = tk.Entry(janela)
entry_hora_fim.grid(row=3, column=1, padx=10, pady=10)


btn_salvar = tk.Button(janela, text='Salvar', command=inserir_horas)
btn_salvar.grid(row=4, column=0, padx=10, pady=10)


columns = ('ID', 'Data', 'Cliente', 'Tarefa', 'Horas Trabalhadas')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_registros()

janela.mainloop()
