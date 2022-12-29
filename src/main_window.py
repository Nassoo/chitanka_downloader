import tkinter as tk
from tkinter import ttk
import webbrowser
from functools import partial
from idlelib.tooltip import Hovertip
from threading import Thread
from sys import exit
import os
import importlib.util

from utilities.path_handler import resource_path
from utilities.tkHyperlinkManager import HyperlinkManager
from src.database_connection import ConnectDatabase
from src.download_from_server import DownloadFiles
from src.get_urls import GetContent
from src.select_dir_location import GetDirectory
from src.set_series import SetSeries


class UserInterface:

    def __init__(self):
        self.filenames = 'кирилица'
        self.file_type = '.fb2.zip'
        self.output_dir = "../Читанка" if self.filenames == 'кирилица' else 'Chitanka'
        self.window = tk.Tk()
        self.frame_params = None
        self.db_output_text = tk.StringVar()
        self.files_dir_output_text = tk.StringVar()
        self.file_types_option_var = tk.StringVar()
        self.file_type_output_text = tk.StringVar(value=f"Избраният файлов формат е {self.file_type}.")
        self.ft_warning_message = tk.StringVar()
        self.filenames_option_var = tk.StringVar()
        self.filenames_output_text = tk.StringVar(value=f"Имената на файловете ще са на {self.filenames}.")
        self.progress_label_text = tk.StringVar()
        self.process_finished_text = tk.StringVar()
        self.ft_warning = None
        self.ft_warning_btn = None
        self.error_message = None
        self.t = Thread()

        self.df = DownloadFiles(output_dir=self.output_dir, file_type=self.file_type)
        self.gc = GetContent(filenames=self.filenames)
        self.ss = SetSeries(output_dir=self.output_dir)

    def run_main_window(self):

        if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
            import pyi_splash
            pyi_splash.update_text('UI Loaded ...')
            pyi_splash.close()

        self.window.title("Chitanka Downloader")
        self.window.geometry("600x400")
        self.window.configure(bg="black")

        frame_logo = tk.Frame(self.window, height=70, bg="black", name="frame_logo")
        frame_logo.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.window.grid_columnconfigure(0, weight=1)

        logo_file = tk.PhotoImage(file=resource_path("img/logo.png"))
        self.window.wm_iconphoto(False, logo_file)
        logo = tk.Label(frame_logo, image=logo_file, bg="black")
        logo.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=10)
        logo.place(anchor=tk.CENTER, relx=0.5, rely=0.5)

        exit_btn = tk.Button(self.window, text="Изход", width=14, command=self.end_program, name="exit_btn")
        exit_btn.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
        exit_btn.place(anchor=tk.CENTER, relx=0.5, rely=0.95)

        self.intro_screen()

        self.window.mainloop()

    def intro_screen(self):
        self.clear_screen()
        intro_text = tk.Text(self.window, bg="black", fg="white", height=5, border=0, font=12, wrap=tk.WORD)
        intro_text.tag_configure("center", justify='center')
        intro_text.insert(tk.END, "Преди да започне обработката, е необходимо да сте изтеглили и стартирали ")
        hyperlink = HyperlinkManager(intro_text)
        intro_text.insert(tk.END,
                          "преносимата версия на Моята библиотека",
                          hyperlink.add(partial(webbrowser.open,
                                                "https://forum.chitanka.info/chitanka-standalone-edition-t6309.html")))
        intro_text.insert(tk.END, '. След това натиснете бутона "База данни" и изберете основната директория на '
                                  'преносимата версия на Моята библиотека '
                                  '(в която се намира изпълнимият файл chitanka), за да се зареди базата данни.')
        intro_text.tag_add("center", "1.0", "end")
        intro_text.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        db_btn = tk.Button(self.window, text="База данни", width=14, command=self.connect_database)
        db_btn.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        db_btn.place(anchor=tk.CENTER, relx=0.5, rely=0.5)

        db_output = tk.Label(self.window, textvariable=self.db_output_text, bg="black", fg="red", font="none 12 bold")
        db_output.grid(row=4, column=0, columnspan=4, sticky=tk.W)
        db_output.place(anchor=tk.CENTER, relx=0.5, rely=0.66)

    def params_screen(self, cur):
        self.clear_screen()
        db_txt = tk.Label(self.window, text="Базата данни е заредена успешно!",
                          bg="black", fg="green", font="none 12 bold")
        db_txt.grid(row=1, column=0, columnspan=4, sticky="nsew")
        db_txt.bind('<Configure>', lambda e: db_txt.config(wraplength=db_txt.winfo_width()))

        params_txt = tk.Label(self.window, text="Въведете желаните параметри за изтеглянето на книгите.",
                              bg="black", fg="white", font="none 12")
        params_txt.grid(row=2, column=0, columnspan=4, sticky="nsew")
        params_txt.bind('<Configure>', lambda e: params_txt.config(wraplength=params_txt.winfo_width()))

        self.frame_params = tk.Frame(self.window, height=70, bg="black", name="frame_params")
        self.frame_params.grid(row=3, column=0, columnspan=4, sticky='nsew')

        files_dir_btn = tk.Button(self.frame_params, text="Директория", width=14, command=self.select_files_dir)
        files_dir_btn.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=10)
        self.files_dir_output_text = tk.StringVar()
        self.files_dir_output_text.set("Файловете ще се изтеглят в " + os.path.abspath(self.output_dir))
        files_dir_output = tk.Label(self.frame_params, textvariable=self.files_dir_output_text, bg="black", fg="white",
                                    font="none 12")
        files_dir_output.grid(row=0, column=2, sticky=tk.W)
        self.frame_params.bind('<Configure>', lambda e: files_dir_output.config(
            wraplength=self.window.winfo_width() - 150))

        file_types = [".fb2.zip", ".epub"]
        ft = ttk.OptionMenu(self.frame_params, self.file_types_option_var, file_types[0], *file_types,
                            command=self.set_file_type)
        ft.config(width=12)
        ft.grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)
        ft_output = tk.Label(self.frame_params, textvariable=self.file_type_output_text, bg="black", fg="white",
                             font="none 12")
        ft_output.grid(row=1, column=2, sticky=tk.W)
        ft_output.bind('<Configure>', lambda e: ft_output.config(wraplength=self.window.winfo_width() - 150))

        filenames = ["кирилица", "латиница"]
        fn = ttk.OptionMenu(self.frame_params, self.filenames_option_var, filenames[0], *filenames,
                            command=self.set_filenames)
        fn.config(width=12)
        fn.grid(row=3, column=0, sticky=tk.NW, padx=10, pady=10)
        fn_output = tk.Label(self.frame_params, textvariable=self.filenames_output_text, bg="black", fg="white",
                             font="none 12")
        fn_output.grid(row=3, column=2, sticky=tk.W)
        fn_output.bind('<Configure>', lambda e: fn_output.config(wraplength=self.window.winfo_width() - 150))

        download_btn = tk.Button(self.window, text="Изтегли всичко", width=14,
                                 command=lambda: self.download_content(False, cur))
        download_btn.grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        download_btn.place(anchor=tk.CENTER, relx=0.5, rely=0.75)

        update_btn = tk.Button(self.window, text="Само обнови", width=14,
                               command=lambda: self.download_content(True, cur))
        update_btn.grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        update_btn.place(anchor=tk.CENTER, relx=0.5, rely=0.85)

    def connect_database(self):
        db = ConnectDatabase()
        cur, database_message = db.connect_db()
        if cur is not None:
            self.params_screen(cur)
        else:
            self.db_output_text.set(database_message)

    def clear_screen(self):
        for el in self.window.winfo_children():
            if el.winfo_name() != "frame_logo" and el.winfo_name() != "exit_btn":
                el.destroy()

    def end_program(self):
        # TODO: save series too (check which process is running)
        if self.t.is_alive():
            if self.t.name == 'download':
                self.df.save_urls()
            elif self.t.name == 'set_series':
                self.ss.save_series()
        self.window.destroy()
        exit()

    def select_files_dir(self):
        gd = GetDirectory()
        self.output_dir = gd.get_directory()
        self.window.update_idletasks()
        self.files_dir_output_text.set(self.output_dir)

    def set_file_type(self, value):
        self.file_type = value
        self.file_type_output_text.set(f"Избраният файлов формат е {value}.")
        if value == ".fb2.zip":
            self.ft_warning.destroy()
            self.ft_warning_btn.destroy()
        elif self.ft_warning not in self.frame_params.winfo_children():
            self.ft_warning = tk.Label(self.frame_params,
                                       text="Внимание! Поредиците ще могат да бъдат импортирани в книгите "
                                            "единствено ако форматът е .fb2.zip.",
                                       bg="black", fg="red",
                                       font="none 12")
            self.ft_warning.grid(row=2, column=2, sticky=tk.W)
            self.ft_warning.bind('<Configure>',
                                 lambda e: self.ft_warning.config(wraplength=self.window.winfo_width() - 150))
            self.ft_warning_btn = tk.Label(self.frame_params, text="?")
            self.ft_warning_btn.grid(row=2, column=0, sticky=tk.E, padx=10, pady=10)
            Hovertip(self.ft_warning_btn,
                     "В базата данни на chitanka.info информацията за поредиците \n"
                     "е налична само за произведенията, но не и за книгите. \n"
                     "Ако желаете да импортирате поредиците и номерата им в книгите, \n"
                     "трябва да изберете формат .fb2.zip. \n"
                     "Това не засяга имената на файловете, \n"
                     "а единствено метаданните вътре във файловете, \n"
                     "за да могат програмите за четене на книги да ги разпознават. \n"
                     "Поредиците и номерата им ще бъдат отразени в имената на файловете, \n"
                     "независимо от файловия формат.", 0)

    def set_filenames(self, value):
        self.filenames = value
        self.filenames_output_text.set(f"Имената на файловете ще са на {value}.")

    def download_content(self, update, cur):
        # TODO: error handling if server is down
        if self.output_dir is None:
            self.error_message = tk.Label(self.window, text="Не сте избрали папка за изтегляне!", bg="black", fg="red",
                                          font="none 12 bold")
            self.error_message.grid(row=5, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
            self.error_message.place(anchor=tk.CENTER, relx=0.5, rely=0.7)
        else:
            self.clear_screen()
            self.gc.filenames = self.filenames
            self.gc.cur = cur
            self.gc.get_content()
            self.df.update = update
            self.df.urls = self.gc.urls
            self.df.get_new_urls()

            self.t = Thread(target=self.df.download, name='download')
            self.t.daemon = True
            self.t.start()

            self.progress_label_text.set("Файловете се изтеглят. Процесът е бавен - моля, изчакайте!")
            # TODO: add description of the process
            self.process_finished_text.set(f"Изтеглянето приключи!")
            self.progress_bar(self.df)

    def progress_bar(self, process):
        all_files = len(process.entries_to_process)
        progress_label = tk.Label(self.window,
                                  textvariable=self.progress_label_text,
                                  bg="black",
                                  fg="white",
                                  font="none 12 bold",
                                  name="progress_label")
        progress_label.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        progress_label.place(anchor=tk.CENTER, relx=0.5, rely=0.4)
        progress_value = tk.StringVar()
        progress_value.set("0")
        s = ttk.Style()
        s.layout("LabeledProgressbar",
                 [('LabeledProgressbar.trough',
                   {'children': [('LabeledProgressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'}),
                                 ("LabeledProgressbar.label",  # label inside the bar
                                  {"sticky": ""})],
                    'sticky': 'nswe'})])
        s.configure("LabeledProgressbar", text=f"{progress_value.get()} %      ")
        p = ttk.Progressbar(self.window, orient="horizontal", length=400, mode='determinate',
                            style="LabeledProgressbar", name="progress_bar")
        p.daemon = True
        p.grid(row=2, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        p.place(anchor=tk.CENTER, relx=0.5, rely=0.3)

        def update_progress_bar():
            if self.t.is_alive():
                if all_files > 0:
                    progress_value.set(str(round(process.download_progress / all_files * 100, 2)))
                s.configure("LabeledProgressbar", text=f"{progress_value.get()} %      ")
                p["value"] = progress_value.get()
                p.after(5000, update_progress_bar)
            else:
                s.configure("LabeledProgressbar", text=f"{progress_value.get()} %      ")
                p["value"] = progress_value.get()
                p.destroy()
                progress_label.destroy()
                process_finished = tk.Label(self.window, textvariable=self.process_finished_text, bg="black",
                                            fg="green",
                                            font="none 12 bold", name="process_finished")
                process_finished.grid(row=5, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
                process_finished.place(anchor=tk.CENTER, relx=0.5, rely=0.4)
                if self.file_type == ".fb2.zip" and self.process_finished_text.get() == "Изтеглянето приключи!":
                    self.series()

        update_progress_bar()

    def series(self):
        # TODO: run the process without downloading the files again
        series_label = tk.Label(self.window,
                                text="Желаете ли да бъдат импортирани номерата на поредиците в книгите?\n"
                                     "Процесът е изключително бавен и може да отнеме няколко часа.",
                                bg="black",
                                fg="white",
                                font="none 12 bold")
        series_label.grid(row=6, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        series_label.place(anchor=tk.CENTER, relx=0.5, rely=0.5)

        series_button = tk.Button(self.window, text="Импортирай", width=14, command=self.insert_series,
                                  name="series_button")
        series_button.grid(row=7, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        series_button.place(anchor=tk.CENTER, relx=0.5, rely=0.6)

    def insert_series(self):
        self.clear_screen()
        self.ss.output_dir = self.output_dir
        self.ss.update = self.df.update
        self.ss.urls = self.df.urls
        self.ss.user_series = self.df.user_series
        self.ss.book_series_ids = self.gc.book_series_ids
        self.ss.get_new_series()
        self.ss.download_progress = 0

        # TODO: add an option insert all series or update only the missing ones
        self.t = Thread(target=self.ss.set_series, name='set_series')
        self.t.daemon = True
        self.t.start()

        self.progress_label_text.set("Поредиците се вмъкват във файловете, в които е необходимо.\n"
                                     "Процесът е бавен - моля, изчакайте!")
        self.process_finished_text.set(f"Процесът приключи! Можете да затворите програмата.")
        self.progress_bar(self.ss)
