import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors")
        self.root.geometry("600x400")

        # menu bar
        self.menubar = tk.Menu(self.root)

        self.action_menu = tk.Menu(self.menubar, tearoff=0)
        self.action_menu.add_command(label="Close", command=self.on_closing)
        self.action_menu.add_command(label="Close without question", command=self.root.destroy)
        self.action_menu.add_separator()
        self.action_menu.add_command(label="Reset", command=self.reset)

        # ABOUT AND LICENSE - IGNORE
        
        self.about_menu = tk.Menu(self.menubar, tearoff=0)
        self.about_menu.add_command(label="About", command=lambda: messagebox.showinfo("About",
"""
Rock Paper Scissors made by a university student from Data Science & Artificial Intelligence major.
Created for a university project.
"""))
        self.about_menu.add_separator()
        self.about_menu.add_command(label="License", command=lambda: messagebox.showinfo("License",
"""
Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

SPDX-License-Identifier: MIT
"""))

        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Settings", command=self.open_settings)

        self.menubar.add_cascade(menu=self.about_menu, label="About")
        self.menubar.add_cascade(menu=self.action_menu, label="Action")
        self.menubar.add_cascade(menu=self.settings_menu, label="Settings")

        self.root.config(menu=self.menubar)

        # label
        self.label = tk.Label(self.root, text="Rock Paper Scissors!", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)
        self.difficulty_display = tk.Label(self.root, text="", font=('Arial', 18))
        self.difficulty_display.pack(padx=5, pady=5)

        self.ai_state = tk.IntVar()

        self.difficulty = tk.StringVar(value="Normal")

        self.hint = tk.Label(self.root, text="You can press 1, 2, 3 respectively!", font=('Arial', 14))
        self.hint.pack(padx=10, pady=10)


        # button (grid format) plus shortcuts
        self.button_frame = tk.Frame(self.root)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.rock = tk.Button(self.button_frame, text = "Rock", font = ('Arial', 16, 'bold'), command=lambda: self.played(self.rock))
        self.rock.grid(row = 0, column = 0, sticky=tk.W+tk.E)

        self.paper = tk.Button(self.button_frame, text="Paper", font=('Arial', 16, 'bold'), command=lambda: self.played(self.paper))
        self.paper.grid(row=0, column=1, sticky=tk.W + tk.E)

        self.scissors = tk.Button(self.button_frame, text="Scissors", font=('Arial', 16, 'bold'), command=lambda: self.played(self.scissors))
        self.scissors.grid(row=0, column=2, sticky=tk.W + tk.E)

        self.button_frame.pack(fill = 'x')

        self.root.bind("<KeyPress>", self.shortcut)
        
        # data (i/o)
        self.previous_inputs = []
        self.all_moves = ['Rock', 'Paper', 'Scissors']
        self.winning_moves = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper"
        }

        self.counter = {
            "Rock": "Paper",
            "Paper": "Scissors",
            "Scissors": "Rock"
        }

        self.transitions = {} # for Markov AI

        self.text = tk.Label(self.root, text=" ", font=('Arial', 16, 'bold'))
        self.text.pack(padx=10, pady=10)

        self.computer_score = self.user_score = self.tie_score = 0

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=('Arial', 12, 'bold'))
        self.score_label.pack(padx=10, pady=10)
        # closing confirm prompt
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    # Settings pop-up
    def open_settings(self):
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("400x400")

        difficulty_label = tk.Label(settings, text="Difficulty", font=('Arial', 16, 'bold'))
        difficulty_menu = ttk.OptionMenu(settings, self.difficulty, self.difficulty.get(), "Easy", "Normal", "Hard", command=self.changed_difficulty)
        difficulty_menu.config(state="disabled" if self.ai_state.get() == 0 else "normal")

        toggle_ai = tk.Checkbutton(settings, text="Enable AI", font=('Arial', 16), variable=self.ai_state, command= lambda: self.enable_difficulty(difficulty_menu))
        toggle_ai.pack(padx=10, pady=10)


        difficulty_label.pack(padx=10, pady=10)
        difficulty_menu.pack(padx=10, pady=10)


    def on_closing(self):
        if messagebox.askyesno("Quit?", message = "Are you sure you want to quit?"):
            self.root.destroy()

    # shortcut handler
    def shortcut(self, event=None):
        if event.keysym == "1":
            self.played(self.rock)
        elif event.keysym == "2":
            self.played(self.paper)
        elif event.keysym == "3":
            self.played(self.scissors)

    handle_button_object = lambda self, btn: btn.cget('text')

    get_button_by_choice = lambda self, choice: {"Rock": self.rock, "Paper": self.paper, "Scissors": self.scissors}[choice]

    def get_score_text(self):
        return f"Computer: {self.computer_score}  |  You: {self.user_score} | Tie: {self.tie_score}"

    def enable_difficulty(self, diff_menu):
        if self.ai_state.get() == 1:
            diff_menu.config(state="normal")
            self.difficulty_display.config(text="Difficulty: Normal")
        else:
            diff_menu.config(state="disabled")
            self.difficulty_display.config(text="")

    def changed_difficulty(self, difficulty):
        return self.difficulty_display.config(text="Difficulty: " + difficulty)

    def played(self, btn):
        msg, color = self.decide_win(btn)
        self.print_output(msg, color)

    def highlight_button(self, btn, color):
        btn.config(bg=color)
        self.root.after(500, btn.config, {"bg": "SystemButtonFace"})

    # AI

    def markov_ai(self):
        last_move = self.previous_inputs[-1]
        next_move_counts = self.transitions.get(last_move, {"Rock": 1, "Paper": 1, "Scissors": 1})
        predicted_move = max(next_move_counts, key=next_move_counts.get)

        return self.counter[predicted_move]

    def predict_last_moves(self, last_move, second_last_move): # so that you can't just hold a button and win
        if last_move == second_last_move:
            possible_moves = [move for move in self.all_moves if move != self.winning_moves[last_move]]
            if len(self.previous_inputs) > 2:
                third_last_move = self.previous_inputs[-3]
                if third_last_move == last_move:
                    possible_moves.remove(last_move)
                    computer_choice = possible_moves[0]
            else:
                computer_choice = random.choice(possible_moves)
        else:
            computer_choice = self.markov_ai()
        return computer_choice


    def hard_ai(self, _btn=None): # very "easy", sarcasm
        last_move = (self.previous_inputs and self.previous_inputs[-1]) or random.choice(self.all_moves)
        computer_choice = self.counter[last_move]
        if len(self.previous_inputs) > 1 and self.previous_inputs[-1] == self.previous_inputs[-2]:
            computer_choice = self.predict_last_moves(self.previous_inputs[-1], self.previous_inputs[-2])
        return computer_choice

    def normal_ai(self, _btn=None):
        if random.random() < 0.2 or not self.previous_inputs:
            return random.choice(self.all_moves)

        if len(self.previous_inputs) > 1:
            last, second_last = self.previous_inputs[-1], self.previous_inputs[-2]
            return self.predict_last_moves(last, second_last) if last == second_last else self.markov_ai()

        return random.choice(self.all_moves)

    easy_ai = lambda self, btn: self.winning_moves[self.handle_button_object(btn)]

    # predictive + randomized AI (KEYWORD: PREDICTIVE)
    def computer_ai(self, move):
        if not self.ai_state.get():
            return random.choice(self.all_moves)

        strategies = {
            "Hard": self.hard_ai,
            "Normal": self.normal_ai,
            "Easy": self.easy_ai
        }

        selected_strategy = strategies.get(self.difficulty.get(), lambda: random.choice(self.all_moves))

        return selected_strategy(move)


    # decides who would win
    def decide_win(self, btn):
        computer_choice = self.computer_ai(btn)
        user_choice = self.handle_button_object(btn)

        if user_choice == computer_choice:
            result = "Tie"
            color = "black"
            self.tie_score += 1
        elif self.winning_moves.get(user_choice) == computer_choice:
            result = "Won"
            color = "blue"
            self.user_score += 1
        else:
            result = "Lost"
            color = "red"
            self.computer_score += 1
        self.previous_inputs.append(user_choice)

        # Provides training to Markovian AI
        if len(self.previous_inputs) >= 2:
            last_move = self.previous_inputs[-2]  # Second-to-last move
            next_move = self.previous_inputs[-1]  # Last move (current move)
            if last_move not in self.transitions:
                self.transitions[last_move] = {"Rock": 1, "Paper": 1, "Scissors": 1}
            self.transitions[last_move][next_move] += 1

        self.score_label.config(text=self.get_score_text())
        self.highlight_button(btn, color)
        self.highlight_button(self.get_button_by_choice(computer_choice), "yellow")
        return f"Your choice: {user_choice}\nComputer choice: {computer_choice}\nResult: {result}", color

    print_output = lambda self, msg, color: self.text.config(text=msg, fg=color)

    def reset(self):
        if self.computer_score == self.user_score == self.tie_score:
            self.print_output("As cleared as it gets", "black")
        else:
            self.print_output(f"All history cleared.", "black")
            self.previous_inputs = []
            self.computer_score = self.user_score = self.tie_score = 0
            self.score_label.config(text=self.get_score_text())
            self.transitions = {}

if __name__ == "__main__":
    app = GUI()
    app.root.mainloop()
