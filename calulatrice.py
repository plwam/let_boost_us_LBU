import tkinter as tk
import ttkbootstrap as ttk
import math
import time
import os

# Création de la fenêtre principale
root = ttk.Window(themename="cyborg")  # Choix du thème initial (mode sombre)
root.title("Calculatrice Scientifique")
root.geometry("420x600")
root.resizable(False, False)

# Variables globales
expression = ""
history = []
history_file = "calc_history.txt"

# Chargement de l'historique et suppression après 12h
def load_history():
    global history
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                timestamp, expr, result = line.strip().split("|")
                if time.time() - float(timestamp) < 43200:  # 12h = 43200 secondes
                    history.append(f"{expr} = {result}")

def save_to_history(expr, result):
    global history
    timestamp = str(time.time())
    history.append(f"{expr} = {result}")
    with open(history_file, "a") as f:
        f.write(f"{timestamp}|{expr}|{result}\n")

# Mise à jour de l'affichage
def update_display():
    entry_var.set(expression)

# Ajout d'une touche au calcul
def on_button_click(value):
    global expression
    expression += str(value)
    update_display()

# Effacer l'affichage
def clear():
    global expression
    expression = ""
    update_display()

# Suppression d'un seul caractère
def backspace():
    global expression
    expression = expression[:-1]
    update_display()

# Évaluation de l'expression
def calculate():
    global expression
    try:
        result = eval(expression, {"math": math, "__builtins__": None})
        if isinstance(result, float) and abs(result) > 1e6:
            result = "{:.6e}".format(result)  # Notation scientifique
        expression = str(result)
        save_to_history(expression, result)
    except Exception as e:
        expression = "Erreur"
    update_display()

# Basculer entre mode clair et sombre
def toggle_theme():
    current_theme = root.style.theme_use()
    new_theme = "cyborg" if current_theme == "flatly" else "flatly"
    root.style.theme_use(new_theme)

# Interface de l'application
entry_var = tk.StringVar()
entry = ttk.Entry(root, textvariable=entry_var, font=("Arial", 20), justify="right", bootstyle="info")
entry.place(x=10, y=10, width=400, height=60)

# Boutons de la calculatrice
buttons = [
    ("7", 10, 80), ("8", 110, 80), ("9", 210, 80), ("/", 310, 80),
    ("4", 10, 140), ("5", 110, 140), ("6", 210, 140), ("*", 310, 140),
    ("1", 10, 200), ("2", 110, 200), ("3", 210, 200), ("-", 310, 200),
    ("0", 10, 260), (".", 110, 260), ("=", 210, 260), ("+", 310, 260),
    ("sin", 10, 320), ("cos", 110, 320), ("tan", 210, 320), ("log", 310, 320),
    ("sqrt", 10, 380), ("x²", 110, 380), ("1/x", 210, 380), ("%", 310, 380),
    ("(", 10, 440), (")", 110, 440), ("π", 210, 440), ("e", 310, 440),
    ("C", 10, 500), ("⌫", 110, 500), ("Hist.", 210, 500), ("Mode", 310, 500),
]

for (text, x, y) in buttons:
    if text == "=":
        btn = ttk.Button(root, text=text, bootstyle="success", command=calculate)
    elif text == "C":
        btn = ttk.Button(root, text=text, bootstyle="danger", command=clear)
    elif text == "⌫":
        btn = ttk.Button(root, text=text, bootstyle="warning", command=backspace)
    elif text == "Mode":
        btn = ttk.Button(root, text=text, bootstyle="secondary", command=toggle_theme)
    elif text == "Hist.":
        btn = ttk.Button(root, text=text, bootstyle="info", command=lambda: print("\n".join(history)))
    elif text == "π":
        btn = ttk.Button(root, text=text, bootstyle="primary", command=lambda: on_button_click(math.pi))
    elif text == "e":
        btn = ttk.Button(root, text=text, bootstyle="primary", command=lambda: on_button_click(math.e))
    elif text == "sqrt":
        btn = ttk.Button(root, text="√", bootstyle="primary", command=lambda: on_button_click("math.sqrt("))
    elif text == "x²":
        btn = ttk.Button(root, text="x²", bootstyle="primary", command=lambda: on_button_click("**2"))
    elif text == "1/x":
        btn = ttk.Button(root, text="1/x", bootstyle="primary", command=lambda: on_button_click("1/"))
    elif text in ["sin", "cos", "tan", "log"]:
        btn = ttk.Button(root, text=text, bootstyle="primary", command=lambda t=text: on_button_click(f"math.{t}("))
    else:
        btn = ttk.Button(root, text=text, bootstyle="light", command=lambda t=text: on_button_click(t))
    
    btn.place(x=x, y=y, width=90, height=50)

# Chargement de l'historique
load_history()

# Lancer l'application
root.mainloop()
