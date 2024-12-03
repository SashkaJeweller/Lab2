import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class VideoPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Видеоплеер")
        self.window.configure(bg='black')  # Установка черного фона

        self.video_source = None
        self.vid = None

        self.is_paused = False
        self.current_frame = 0

        self.canvas = tk.Canvas(window, width=640, height=480, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Кнопка настроек в верхнем левом углу
        self.btn_settings = ttk.Button(window, text="Настройки окна", command=self.open_settings)
        self.btn_settings.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

        self.btn_load = ttk.Button(window, text="Загрузить видео", command=self.load_video)
        self.btn_load.pack(side=tk.TOP, fill=tk.X)

        # Загрузка изображений для кнопок
        self.play_image = ImageTk.PhotoImage(
            Image.open("play.png").resize((30, 30)))  # Изображение кнопки воспроизведения
        self.pause_image = ImageTk.PhotoImage(Image.open("pause.png").resize((30, 30)))  # Изображение кнопки паузы
        self.restart_image = ImageTk.PhotoImage(Image.open("restart_icon.png").resize((30, 30)))  # Иконка кнопки "Воспроизвести заново"

        self.btn_pause = ttk.Button(window, image=self.play_image, command=self.toggle_pause)
        self.btn_pause.pack(side=tk.TOP, fill=tk.X)

        self.btn_restart = ttk.Button(window, image=self.restart_image, command=self.restart_video)  # Используем изображение для кнопки
        self.btn_restart.pack(side=tk.TOP, fill=tk.X)
        self.btn_restart.config(state=tk.DISABLED)  # Изначально отключена

        self.lbl_time = ttk.Label(window, text="00:00", background='black', foreground='white')
        self.lbl_time.pack(side=tk.TOP)

        self.window.geometry("800x600")  # Начальный размер окна

    def load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_path:
            self.video_source = file_path
            self.vid = cv2.VideoCapture(self.video_source)
            self.current_frame = 0
            self.btn_restart.config(state=tk.DISABLED)  # Отключаем кнопку воспроизведения заново
            self.update()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.config(image=self.play_image)  # Меняем изображение на кнопку воспроизведения
        else:
            self.btn_pause.config(image=self.pause_image)  # Меняем изображение на кнопку паузы
            self.update()

    def restart_video(self):
        if self.vid is not None:
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Сбрасываем на начало видео
            self.current_frame = 0
            self.btn_restart.config(state=tk.DISABLED)  # Отключаем кнопку воспроизведения заново
            self.update()

    def update(self):
        if not self.is_paused and self.vid is not None:
            ret, frame = self.vid.read()
            if ret:
                self.current_frame += 1
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Масштабирование кадра под размер канваса
                frame = self.resize_frame(frame)

                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk
                self.canvas.after(10, self.update)

                # Обновление хронометража
                self.update_time()
            else:
                # Видео закончилось
                self.btn_restart.config(state=tk.NORMAL)  # Включаем кнопку воспроизведения заново

    def resize_frame(self, frame):
        # Получаем размеры канваса
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Масштабируем кадр
        return cv2.resize(frame, (canvas_width, canvas_height))

    def update_time(self):
        if self.vid is not None:
            total_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(self.vid.get(cv2.CAP_PROP_FPS))
            current_time = self.current_frame / fps
            minutes, seconds = divmod(int(current_time), 60)
            self.lbl_time.config(text=f"{minutes:02}:{seconds:02}")

    def __del__(self):
        if self.vid is not None and self.vid.isOpened():
            self.vid.release()

    def open_settings(self):
        SettingsWindow(self.window)


class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.settings_window = tk.Toplevel(master)
        self.settings_window.title("Настройки")

        # Ползунки для изменения размера окна
        self.width_scale = tk.Scale(self.settings_window, from_=400, to=1600, orient=tk.HORIZONTAL, label="Ширина",
                                    command=self.update_window_size)
        self.width_scale.set(master.winfo_width())
        self.width_scale.pack(fill=tk.X)

        self.height_scale = tk.Scale(self.settings_window, from_=300, to=900, orient=tk.VERTICAL, label="Высота",
                                     command=self.update_window_size)
        self.height_scale.set(master.winfo_height())
        self.height_scale.pack(fill=tk.Y)

    def update_window_size(self, event):
        new_width = self.width_scale.get()
        new_height = self.height_scale.get()
        self.master.geometry(f"{new_width}x{new_height}")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
