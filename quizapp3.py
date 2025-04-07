import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
import time
import os

# -----------------------
# Fonctions utilitaires
# -----------------------
def is_prime(n):
    if n < 2:
        return False
    for j in range(2, int(n**0.5) + 1):
        if n % j == 0:
            return False
    return True

# -----------------------
# Génération des questions
# -----------------------
questions_data = []

# 50 questions de type QCM sur des additions simples (catégorie Maths)
for i in range(1, 51):
    questions_data.append({
        "question": f"Combien font {i} + {i} ?",
        "type": "MCQ",
        "options": [str(i*2 - 1), str(i*2), str(i*2 + 1), str(i*2 + 2)],
        "answer": str(i*2),
        "explanation": f"{i} + {i} = {i*2}",
        "category": "Maths",
        "difficulty": 1
    })

# 50 questions de type Vrai/Faux sur la primalité (catégorie Maths)
for i in range(51, 101):
    prime = is_prime(i)
    questions_data.append({
        "question": f"Vrai ou Faux : {i} est un nombre premier ?",
        "type": "TrueFalse",
        "options": ["Vrai", "Faux"],
        "answer": "Vrai" if prime else "Faux",
        "explanation": f"{i} est {'premier' if prime else 'non premier'}.",
        "category": "Maths",
        "difficulty": 2
    })

# 10 questions de programmation (catégorie Programmation)
programming_questions = [
    {
        "question": "Quel est le langage de programmation principalement utilisé pour le développement web côté serveur ?",
        "type": "MCQ",
        "options": ["PHP", "JavaScript", "Python", "Ruby"],
        "answer": "PHP",
        "explanation": "PHP est largement utilisé pour le développement web côté serveur.",
        "category": "Programmation",
        "difficulty": 2
    },
    {
        "question": "En Python, comment déclare-t-on une fonction ?",
        "type": "MCQ",
        "options": ["function myFunc():", "def myFunc():", "fun myFunc():", "declare myFunc():"],
        "answer": "def myFunc():",
        "explanation": "La syntaxe correcte en Python est 'def myFunc():' pour définir une fonction.",
        "category": "Programmation",
        "difficulty": 1
    },
    {
        "question": "Que signifie HTML ?",
        "type": "MCQ",
        "options": ["HyperText Markup Language", "Hyper Trainer Marking Language", "HyperText Makeup Language", "Hyperlink Markup Language"],
        "answer": "HyperText Markup Language",
        "explanation": "HTML signifie HyperText Markup Language.",
        "category": "Programmation",
        "difficulty": 1
    },
    {
        "question": "Quel langage de programmation est utilisé pour le développement d'applications Android ?",
        "type": "MCQ",
        "options": ["Java", "Swift", "C#", "Ruby"],
        "answer": "Java",
        "explanation": "Java est historiquement le langage principal pour le développement d'applications Android.",
        "category": "Programmation",
        "difficulty": 2
    },
    {
        "question": "Que signifie CSS ?",
        "type": "MCQ",
        "options": ["Cascading Style Sheets", "Creative Style System", "Computer Style Sheets", "Cascading Simple Sheets"],
        "answer": "Cascading Style Sheets",
        "explanation": "CSS signifie Cascading Style Sheets.",
        "category": "Programmation",
        "difficulty": 1
    },
    {
        "question": "Quelle commande Git permet de cloner un dépôt ?",
        "type": "MCQ",
        "options": ["git clone", "git copy", "git fetch", "git pull"],
        "answer": "git clone",
        "explanation": "La commande 'git clone' permet de cloner un dépôt distant.",
        "category": "Programmation",
        "difficulty": 1
    },
    {
        "question": "En JavaScript, quel symbole est utilisé pour terminer une instruction ?",
        "type": "MCQ",
        "options": ["Point-virgule (;)", "Deux-points (:)", "Virgule (,)", "Point (.)"],
        "answer": "Point-virgule (;)",
        "explanation": "En JavaScript, le point-virgule (;) termine généralement une instruction.",
        "category": "Programmation",
        "difficulty": 1
    },
    {
        "question": "Quel est le principal framework pour le développement d'applications web en Python ?",
        "type": "MCQ",
        "options": ["Django", "Laravel", "Rails", "Spring"],
        "answer": "Django",
        "explanation": "Django est l'un des frameworks web les plus populaires pour Python.",
        "category": "Programmation",
        "difficulty": 2
    },
    {
        "question": "Que permet de faire SQL ?",
        "type": "MCQ",
        "options": ["Gérer des bases de données relationnelles", "Créer des applications mobiles", "Concevoir des sites web", "Analyser des images"],
        "answer": "Gérer des bases de données relationnelles",
        "explanation": "SQL est utilisé pour interagir avec des bases de données relationnelles.",
        "category": "Programmation",
        "difficulty": 2
    },
    {
        "question": "Que signifie l'acronyme API ?",
        "type": "MCQ",
        "options": ["Application Programming Interface", "Applied Program Interface", "Advanced Programming Internet", "Application Program Internet"],
        "answer": "Application Programming Interface",
        "explanation": "API signifie Application Programming Interface.",
        "category": "Programmation",
        "difficulty": 2
    }
]

# Intégrer les questions de programmation
questions_data.extend(programming_questions)

# -----------------------
# Gestion de l'historique
# -----------------------
history_file = "quiz_history.txt"

def save_history_entry(entry):
    with open(history_file, "a") as f:
        f.write(entry + "\n")

def load_history_entries():
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return f.readlines()
    return []

def clear_history_file():
    if os.path.exists(history_file):
        os.remove(history_file)

# -----------------------
# Classe principale de l'application
# -----------------------
class QuizApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")  # Thème sombre par défaut
        self.title("Quiz App 🎓")
        self.geometry("600x600")
        self.resizable(False, False)
        
        # Variables du quiz
        self.all_questions = questions_data
        self.selected_questions = []
        self.current_question_index = 0
        self.score = 0
        self.total_time = 0
        self.question_start_time = None
        self.lives = 3
        self.multiplayer = False
        self.current_player = 1
        self.player_scores = {1: 0, 2: 0}
        self.exam_mode = False      # Ne révèle pas les réponses correctes avant la fin
        self.challenge_mode = False # En mode Challenge, une erreur coûte une vie supplémentaire
        
        # Paramètres personnalisables
        self.num_questions = 5
        self.selected_category = "Tous"
        self.selected_difficulty = "Tous"
        
        # Conteneur pour les frames
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        for F in (MainMenuFrame, QuizFrame, ResultFrame, HistoryFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(MainMenuFrame)
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
    
    def start_quiz(self):
        # Filtrer les questions en fonction des options
        filtered = self.all_questions
        if self.selected_category != "Tous":
            filtered = [q for q in filtered if q["category"] == self.selected_category]
        if self.selected_difficulty != "Tous":
            try:
                diff = int(self.selected_difficulty)
                filtered = [q for q in filtered if q["difficulty"] == diff]
            except:
                pass
        # Sélection aléatoire selon le nombre de questions demandé
        if len(filtered) < self.num_questions:
            self.selected_questions = filtered
        else:
            self.selected_questions = random.sample(filtered, self.num_questions)
        
        self.current_question_index = 0
        self.score = 0
        self.total_time = 0
        self.lives = 3
        self.current_player = 1
        self.player_scores = {1: 0, 2: 0} if self.multiplayer else {1: 0}
        # Mise à jour de la progress bar dans le QuizFrame
        self.frames[QuizFrame].progress["maximum"] = self.num_questions
        self.show_frame(QuizFrame)
        self.frames[QuizFrame].load_question()
    
    def finish_quiz(self):
        avg_time = self.total_time / self.num_questions if self.num_questions > 0 else 0
        entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Score: {self.score} - Temps moyen: {avg_time:.2f}s"
        save_history_entry(entry)
        self.frames[ResultFrame].update_results(self.score, avg_time, self.player_scores)
        self.show_frame(ResultFrame)
    
    def toggle_theme(self):
        current = self.style.theme_use()
        new_theme = "flatly" if current == "cyborg" else "cyborg"
        self.style.theme_use(new_theme)
    
    def toggle_fullscreen(self):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

# -----------------------
# Frame du menu principal
# -----------------------
class MainMenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        title = ttk.Label(self, text="Bienvenue sur Quiz App 🎓", font=("Arial", 24))
        title.pack(pady=20)
        
        # Options de configuration
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=10)
        
        ttk.Label(options_frame, text="Nombre de questions:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.num_questions_var = tk.StringVar(value="5")
        num_entry = ttk.Entry(options_frame, textvariable=self.num_questions_var, width=5)
        num_entry.grid(row=0, column=1, padx=5, pady=3)
        
        ttk.Label(options_frame, text="Catégorie:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.category_var = tk.StringVar(value="Tous")
        category_options = ["Tous", "Culture générale", "Maths", "Science", "Programmation"]
        ttk.OptionMenu(options_frame, self.category_var, self.category_var.get(), *category_options).grid(row=1, column=1, padx=5, pady=3)
        
        ttk.Label(options_frame, text="Difficulté:").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        self.difficulty_var = tk.StringVar(value="Tous")
        difficulty_options = ["Tous", "1", "2", "3"]
        ttk.OptionMenu(options_frame, self.difficulty_var, self.difficulty_var.get(), *difficulty_options).grid(row=2, column=1, padx=5, pady=3)
        
        self.exam_mode_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Mode Examen 🔒", variable=self.exam_mode_var).grid(row=3, column=0, columnspan=2, pady=5)
        
        self.challenge_mode_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Mode Challenge ⚡", variable=self.challenge_mode_var).grid(row=4, column=0, columnspan=2, pady=5)
        
        self.multiplayer_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Multijoueur 👥", variable=self.multiplayer_var).grid(row=5, column=0, columnspan=2, pady=5)
        
        start_btn = ttk.Button(self, text="Démarrer le Quiz 🚀", command=self.start_quiz, bootstyle="success")
        start_btn.pack(pady=20)
        
        history_btn = ttk.Button(self, text="Voir l'Historique 📜", command=lambda: controller.show_frame(HistoryFrame), bootstyle="info")
        history_btn.pack(pady=10)
        
        theme_btn = ttk.Button(self, text="Basculer Thème 🌗", command=controller.toggle_theme, bootstyle="secondary")
        theme_btn.pack(pady=5)
    
    def start_quiz(self):
        try:
            self.controller.num_questions = int(self.num_questions_var.get())
        except:
            self.controller.num_questions = 5
        self.controller.selected_category = self.category_var.get()
        self.controller.selected_difficulty = self.difficulty_var.get()
        self.controller.exam_mode = self.exam_mode_var.get()
        self.controller.challenge_mode = self.challenge_mode_var.get()
        self.controller.multiplayer = self.multiplayer_var.get()
        self.controller.start_quiz()

# -----------------------
# Frame du quiz
# -----------------------
class QuizFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.timer_seconds = 15
        self.remaining_time = self.timer_seconds
        
        # Timer et Progress Bar
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=5, fill="x")
        self.timer_label = ttk.Label(top_frame, text="⏱️ 15", font=("Arial", 16))
        self.timer_label.pack(side="left", padx=10)
        self.progress = ttk.Progressbar(top_frame, mode="determinate")
        self.progress.pack(side="right", fill="x", expand=True, padx=10)
        
        self.question_label = ttk.Label(self, text="", font=("Arial", 18), wraplength=500)
        self.question_label.pack(pady=10)
        
        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(pady=10)
        
        self.answer_entry = ttk.Entry(self, font=("Arial", 16))
        
        self.next_btn = ttk.Button(self, text="Suivant ➡️", command=self.submit_answer, bootstyle="success")
        self.next_btn.pack(pady=20)
        
        self.info_label = ttk.Label(self, text="", font=("Arial", 14))
        self.info_label.pack(pady=5)
    
    def load_question(self):
        self.remaining_time = self.timer_seconds
        self.update_timer()
        # Mise à jour de la progress bar
        self.progress["maximum"] = self.controller.num_questions
        self.progress["value"] = self.controller.current_question_index
        if self.controller.current_question_index < len(self.controller.selected_questions):
            q = self.controller.selected_questions[self.controller.current_question_index]
            if self.controller.multiplayer:
                self.info_label.config(text=f"Joueur {self.controller.current_player} - Vies: {self.controller.lives} ❤️")
            else:
                self.info_label.config(text=f"Vies: {self.controller.lives} ❤️")
            self.question_label.config(text=q["question"])
            for widget in self.options_frame.winfo_children():
                widget.destroy()
            # Affichage selon le type de question
            if q["type"] in ["MCQ", "TrueFalse"]:
                for option in q["options"]:
                    btn = ttk.Button(self.options_frame, text=option, command=lambda opt=option: self.select_option(opt), bootstyle="primary")
                    btn.pack(fill="x", pady=5)
                self.answer_entry.pack_forget()
            elif q["type"] == "Short":
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.pack(fill="x", pady=5)
            else:
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.pack(fill="x", pady=5)
            self.controller.question_start_time = time.time()
        else:
            self.controller.finish_quiz()
    
    def update_timer(self):
        self.timer_label.config(text=f"⏱️ {self.remaining_time}")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.after(1000, self.update_timer)
        else:
            self.process_answer(None)
    
    def select_option(self, selected):
        self.process_answer(selected)
    
    def submit_answer(self):
        q = self.controller.selected_questions[self.controller.current_question_index]
        if q["type"] == "Short":
            answer = self.answer_entry.get()
            self.process_answer(answer)
    
    def process_answer(self, answer):
        self.remaining_time = 0
        q = self.controller.selected_questions[self.controller.current_question_index]
        correct = False
        if answer is None:
            correct = False
        else:
            if q["type"] in ["MCQ", "TrueFalse"]:
                correct = (answer == q["answer"])
            elif q["type"] == "Short":
                correct = (answer.strip().lower() == q["answer"].strip().lower())
        time_taken = time.time() - self.controller.question_start_time
        self.controller.total_time += time_taken
        # Mise à jour du score
        if correct:
            bonus = max(0, self.timer_seconds - int(time_taken))
            if self.controller.multiplayer:
                self.controller.player_scores[self.controller.current_player] += 10 + bonus
            else:
                self.controller.score += 10 + bonus
        else:
            self.controller.lives -= 1
        if self.controller.challenge_mode and not correct:
            self.controller.lives -= 1
        # Affichage de l'explication (sauf en mode examen)
        if not self.controller.exam_mode:
            messagebox("Explication 📚", q.get("explanation", ""))
        # En mode multijoueur, alterner le joueur
        if self.controller.multiplayer:
            self.controller.current_player = 2 if self.controller.current_player == 1 else 1
        self.controller.current_question_index += 1
        if self.controller.lives <= 0:
            self.controller.finish_quiz()
        else:
            self.load_question()

# -----------------------
# Frame des résultats
# -----------------------
class ResultFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.results_label = ttk.Label(self, text="", font=("Arial", 18))
        self.results_label.pack(pady=20)
        self.stats_label = ttk.Label(self, text="", font=("Arial", 14))
        self.stats_label.pack(pady=10)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        self.restart_btn = ttk.Button(btn_frame, text="Rejouer 🔄", command=lambda: controller.show_frame(MainMenuFrame), bootstyle="success")
        self.restart_btn.grid(row=0, column=0, padx=10)
        self.quit_btn = ttk.Button(btn_frame, text="Quitter ❌", command=self.controller.destroy, bootstyle="danger")
        self.quit_btn.grid(row=0, column=1, padx=10)
    
    def update_results(self, score, avg_time, player_scores):
        if self.controller.multiplayer:
            text = "Scores:\n"
            for player, sc in player_scores.items():
                text += f"Joueur {player}: {sc} 🏆\n"
        else:
            text = f"Score Final: {score} 🎉"
        self.results_label.config(text=text)
        stats = f"Temps moyen par question: {avg_time:.2f} s\nQuestions: {self.controller.num_questions}"
        self.stats_label.config(text=stats)

# -----------------------
# Frame de l'historique
# -----------------------
class HistoryFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        title = ttk.Label(self, text="Historique des Scores 📜", font=("Arial", 20))
        title.pack(pady=20)
        self.history_listbox = tk.Listbox(self, font=("Arial", 14))
        self.history_listbox.pack(fill="both", expand=True, padx=20, pady=10)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        back_btn = ttk.Button(btn_frame, text="Retour 🔙", command=lambda: controller.show_frame(MainMenuFrame), bootstyle="secondary")
        back_btn.grid(row=0, column=0, padx=10)
        clear_btn = ttk.Button(btn_frame, text="Vider Historique 🗑️", command=self.clear_history, bootstyle="danger")
        clear_btn.grid(row=0, column=1, padx=10)
        self.load_history()
    
    def load_history(self):
        self.history_listbox.delete(0, tk.END)
        entries = load_history_entries()
        for entry in entries:
            self.history_listbox.insert(tk.END, entry.strip())
    
    def clear_history(self):
        clear_history_file()
        self.history_listbox.delete(0, tk.END)

# -----------------------
# Lancement de l'application
# -----------------------
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
