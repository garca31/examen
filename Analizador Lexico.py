import ply.lex as lex
import tkinter as tk
from tkinter import ttk

# Definición de tokens y palabras reservadas
tokens = (
    'RESERVADO',
    'IDENTIFICADOR',
    'OPERADOR',
    'NUMERO_ENTERO',
    'PUNTO',
    'FINAL',
    'DELIMITADOR',
    'NODEFINIDO'
)

palabra_reservada = ['programa', 'suma', 'int', 'read', 'print', 'end']
identificador = ['a', 'b', 'c']
operador = ['=']
delimitador = ['(', ')', '{', '}', ';', ',', '.']

t_ignore = ' \t'

# Inicializar contador de tokens por tipo
contadores = {token: 0 for token in tokens}

def t_IDENTIFICADOR(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in palabra_reservada:
        t.type = 'RESERVADO'
    elif t.value in identificador:
        t.type = 'IDENTIFICADOR'
    else:
        t.type = 'NODEFINIDO'
    contadores[t.type] += 1
    return t

def t_OPERADOR(t):
    r'='
    t.type = 'OPERADOR'
    contadores[t.type] += 1
    return t

def t_NUMERO_ENTERO(t):
    r'\d+'
    t.type = 'NUMERO_ENTERO'
    contadores[t.type] += 1
    return t

def t_PUNTO(t):
    r'\.'
    t.type = 'PUNTO'
    contadores[t.type] += 1
    return t

def t_FINAL(t):
    r'end'
    t.type = 'FINAL'
    contadores[t.type] += 1
    return t

def t_DELIMITADOR(t):
    r'[\(\)\{\};,.]'
    t.type = 'DELIMITADOR'
    contadores[t.type] += 1
    return t

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()


def analizar_codigo():
    codigo = entrada_texto.get('1.0', tk.END)
    lexer.input(codigo)
    tokens = []
    lexemas = []
    lineas = []

    for tok in lexer:
        tokens.append(tok.type)
        lexemas.append(tok.value)
        lineas.append(tok.lineno)

    resultado_texto.delete(*resultado_texto.get_children())

    for token, lexema, linea in zip(tokens, lexemas, lineas):
        resultado_texto.insert("", tk.END, values=(token, lexema, linea))

    total_tokens_label.config(text=f"Total de Tokens: {sum(contadores.values())}\n" +
                                  f"Total de RESERVADO: {contadores['RESERVADO']}\n" +
                                  f"Total de IDENTIFICADOR: {contadores['IDENTIFICADOR']}\n" +
                                  f"Total de OPERADOR: {contadores['OPERADOR']}\n" +
                                  f"Total de NUMERO_ENTERO: {contadores['NUMERO_ENTERO']}\n" +
                                  f"Total de PUNTO: {contadores['PUNTO']}\n" +
                                  f"Total de FINAL: {contadores['FINAL']}\n" +
                                  f"Total de DELIMITADOR: {contadores['DELIMITADOR']}\n" +
                                  f"Total de NODEFINIDO: {contadores['NODEFINIDO']}")

def borrar_codigo():
    entrada_texto.delete('1.0', tk.END)

ventana = tk.Tk()
ventana.title("Analizador")
ventana.config(bg="#2DFFB0")

tk.Label(ventana, text="Escribe un texto:").pack()
boton_borrar = tk.Button(ventana, text="Borrar",font=("Arial",12),bg="#121b29",fg="white", command=borrar_codigo)
boton_borrar.pack()

entrada_texto = tk.Text(ventana, height=10, width=50)
entrada_texto.pack()

boton_analizar = tk.Button(ventana, text="Analizar", font=("Arial",12),bg="#121b29",fg="white", command=analizar_codigo)
boton_analizar.pack()

resultado_texto = ttk.Treeview(ventana, columns=("Token", "Lexema", "Línea"))
resultado_texto.heading("Token", text="Token")
resultado_texto.heading("Lexema", text="Lexema")
resultado_texto.heading("Línea", text="Línea")
resultado_texto.pack()

total_tokens_label = tk.Label(ventana, text="")
total_tokens_label.pack()

ventana.mainloop()