import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Видеоплеер")
        self.window.configure(bg='black')

        self.video_source = None
        self.vid = None

        self.is_paused = False
        self.current_frame = 0

        self.canvas = tk.Canvas(window, width=640, height=480, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.btn_load = ttk.Button(window, text="Загрузить видео", command=self.load_video)
        self.btn_load.pack(side=tk.TOP, fill=tk.X)

        self.play_image = ImageTk.PhotoImage(Image.open("play.png").resize((30, 30)))
        self.pause_image = ImageTk.PhotoImage(Image.open("pause.png").resize((30, 30)))
        self.restart_image = ImageTk.PhotoImage(Image.open("restart_icon.png").resize((30, 30)))

        self.btn_pause = ttk.Button(window, image=self.play_image, command=self.toggle_pause)
        self.btn_pause.pack(side=tk.TOP, fill=tk.X)

        self.btn_restart = ttk.Button(window, image=self.restart_image, command=self.restart_video)
        self.btn_restart.pack(side=tk.TOP, fill=tk.X)
        self.btn_restart.config(state=tk.DISABLED)

        self.lbl_time = ttk.Label(window, text="00:00", background='black', foreground='white')
        self.lbl_time.pack(side=tk.TOP)

        self.window.geometry("800x600")

        self.menu_button = ttk.Button(window, text="Назад в меню", command=self.go_to_menu)
        self.menu_button.pack(side=tk.TOP, fill=tk.X)

    def load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_path:
            self.video_source = file_path
            self.vid = cv2.VideoCapture(self.video_source)
            if not self.vid.isOpened():
                raise ValueError("Не удалось открыть видеофайл.")

            self.current_frame = 0
            self.btn_restart.config(state=tk.DISABLED)
            self.update()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.config(image=self.play_image)
        else:
            self.btn_pause.config(image=self.pause_image)
            self.update()

    def restart_video(self):
        if self.vid is not None:
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.current_frame = 0
            self.btn_restart.config(state=tk.DISABLED)
            self.update()

    def update(self):
        if not self.is_paused and self.vid is not None:
            ret, frame = self.vid.read()
            if ret:
                self.current_frame += 1
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = self.resize_frame(frame)

                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk
                self.canvas.after(10, self.update)

                self.update_time()
            else:
                self.btn_restart.config(state=tk.NORMAL)

    def resize_frame(self, frame):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return cv2.resize(frame, (canvas_width, canvas_height))

    def update_time(self):
        if self.vid is not None:
            total_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(self.vid.get(cv2.CAP_PROP_FPS))
            current_time = self.current_frame / fps
            minutes, seconds = divmod(int(current_time), 60)
            self.lbl_time.config(text=f"{minutes:02}:{seconds:02}")

    def go_to_menu(self):
        self.window.destroy()  # Закрываем окно видеоплеера
        import menu  # Импортируем и запускаем меню


if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
