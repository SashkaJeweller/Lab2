import tkinter as tk
from tkinter import ttk
import videoplayer  # Импортируем видеоплеер


class Menu:
    def __init__(self, window):
        self.window = window
        self.window.title("Меню")
        self.window.geometry("400x300")
        self.window.configure(bg='lightgray')

        self.label = ttk.Label(window, text="Меню", font=("Arial", 24), background='lightgray')
        self.label.pack(pady=20)

        self.btn_play = ttk.Button(window, text="Перейти в видеоплеер", command=self.open_videoplayer)
        self.btn_play.pack(pady=10)

    def open_videoplayer(self):
        self.window.destroy()  # Закрываем меню
        videoplayer.VideoPlayer(tk.Tk())  # Открываем видеоплеер


if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
