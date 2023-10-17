import os
import tkinter as tk
from time import sleep
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
os.startfile("client.pyw", "open")


class MainWindow:
    def __init__(self):
        with open("data\\s_var", "r", encoding="utf-8") as r_start_var:
            self.start_var = r_start_var.read()
        self.list_consoles = ["console 1" + 10 * " " + self.start_var]
        self.command_list = ["cd", "md", "rmdir", "copy", "ren", "return", "mf", "del", "start", "exit",
                             "new_con", "paste", "mFTP", "oFTP"]
        self.num_consoles = 0
        self.last_console = 0
        self.directory_list = [[]]
        self.directory_list_ftp_f = [""]
        self.copy_list = []
        self.x, self.y = 0, 0
        # ------------------------------------------------------------------ data ^
        self.root = tk.Tk()
        self.root.geometry("602x395")
        self.root.resizable(False, False)
        self.root.title('Explorer')
        # ------------------------------------------------------------------ base win settings ^
        self.main_frame = tk.Frame(self.root, bg="gray")
        self.main_frame.grid(row=0, column=0, sticky='news')
        # ------------------------------------------------------------------ base frame settings ^
        self.ret_but = tk.Button(self.main_frame, text="Back", command=self.ret_but_f)
        self.ret_but.grid(row=0, column=0, sticky="news")
        # ------------------------------------------------------------------ ret but settings ^
        self.widget_list_consoles = ttk.Combobox(self.main_frame, textvariable=tk.StringVar(), width=70)
        self.widget_list_consoles["values"] = self.list_consoles
        self.widget_list_consoles['state'] = 'readonly'
        self.widget_list_consoles.current(0)
        self.widget_list_consoles.bind("<<ComboboxSelected>>", lambda e: self.select_con_f())
        self.widget_list_consoles.grid(row=0, column=1, sticky="news")
        # ------------------------------------------------------------------ select console widget settings ^
        self.set_but = tk.Button(self.main_frame, text="Settings", command=SettingWindow, width=16)
        self.set_but.grid(column=2, row=0, sticky="news")
        # ------------------------------------------------------------------ setting button ^
        self.command_list_widget = tk.Listbox(self.main_frame, height=11)
        for i in self.command_list:
            self.command_list_widget.insert(tk.END, i)
        self.command_list_widget.bind("<Double-Button-1>", lambda e: self.help_c())
        self.command_list_widget.grid(column=2, row=1, sticky="news")
        # ------------------------------------------------------------------ command list widget settings ^
        self.list_c_help = scrolledtext.ScrolledText(self.main_frame, width=13, height=10)
        self.list_c_help["state"] = "disabled"
        self.list_c_help.grid(row=2, column=2, sticky="news")
        # ------------------------------------------------------------------ help widget settings ^
        self.help_but = tk.Button(self.main_frame, text="help", command=self.help_c)
        self.help_but.grid(column=2, row=3, sticky="news")
        # ------------------------------------------------------------------ help but settings ^
        self.enter_command = tk.Entry(self.main_frame)
        self.enter_command.bind("<Return>", lambda e: self.analysis_command_f())
        self.enter_command.grid(row=3, column=0, sticky="news", columnspan=2)
        # ------------------------------------------------------------------ enter command widget settings ^
        self.out_ListBox = tk.Listbox(self.main_frame, cursor="hand2", fg="blue")
        self.out_ListBox.bind("<Double-Button-1>", lambda e: self.cd_command_f_0())
        self.out_ListBox.bind("<Button-3>", self.cursor_position_print)
        self.out_ListBox.grid(column=0, row=1, columnspan=2, rowspan=2, sticky="news")
        # ------------------------------------------------------------------ out ListBox settings ^
        self.data_create_f()
        # ------------------------------------------------------------------ start program ^

        self.root.mainloop()

    def fast_copy_command_f(self):
        data = self.out_ListBox.curselection()[0]
        data_1 = self.directory_list[self.num_consoles][data]
        if "|" not in self.list_consoles[self.num_consoles]:
            if data_1[:6] == "folder":
                data_1 = data_1.split(" " * 10)[1]
            else:
                data_1 = data_1.split(" " * 15)[1]
            if data_1 in self.copy_list:
                return
            data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data_1
            self.copy_list.append(data)
        else:
            file = self.directory_list_ftp_f[data].split("|")[data * 2 + 1].split("\\")[-1]
            self.copy_list.append(file + "|" + self.directory_list_ftp_f[data].split("|")[data * 2 + 2])

    def fast_delete_command_f(self):
        data = self.out_ListBox.curselection()[0]
        data_1 = self.directory_list[self.num_consoles][data]
        if data_1[:6] == "folder":
            data_1 = data_1.split(" " * 10)[1]
            os.system("rmdir /S /Q \"" + self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data_1 + "\"")
            self.data_create_f()
            return
        else:
            data_1 = data_1.split(" " * 15)[1]
        try:
            os.system("del \"" + self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data_1 + "\"")
            self.data_create_f()
        except OSError:
            return

    def cursor_position_print(self, event):
        self.x, self.y = event.x, event.y
        if "|" not in self.list_consoles[self.num_consoles]:
            if self.out_ListBox.curselection() == ():
                FastCommandsWin(self, self.x, self.y, self.root.geometry(), block=0)
                return
            FastCommandsWin(self, self.x, self.y, self.root.geometry())
        else:
            if self.out_ListBox.curselection() == ():
                FastCommandsWin(self, self.x, self.y, self.root.geometry(), block=2)
                return
            FastCommandsWin(self, self.x, self.y, self.root.geometry(), block=3)

    def data_create_f(self):
        directory_list_0 = []
        file_list = []
        way = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\"
        list_data_1 = os.listdir(path=way)
        # ------------------------------------- data ^
        if self.directory_list[0]:
            for _ in range(0, len(self.directory_list[self.last_console])):
                self.out_ListBox.delete(0)
            self.directory_list.pop(self.num_consoles)
        for i in list_data_1:
            if os.path.isdir(way + f"\\{i}"):
                directory_list_0.append("folder" + " " * 10 + i)
            else:
                file_list.append("file" + " " * 15 + i)
        for i in directory_list_0:
            self.out_ListBox.insert(tk.END, i)
        for i in file_list:
            self.out_ListBox.insert(tk.END, i)
        self.last_console = self.num_consoles
        self.directory_list.insert(self.num_consoles, directory_list_0 + file_list)

    def cd_command_f_0(self):
        select_dir = self.out_ListBox.curselection()
        # ------------------------------------- data ^
        if select_dir == ():
            return
        if "|" not in self.list_consoles[self.num_consoles]:
            if self.directory_list[self.num_consoles][select_dir[0]][:4] == "file":
                self.start_file_f_0(select_dir[0])
                return
            self.list_consoles[self.num_consoles] = self.list_consoles[self.num_consoles] + "\\" + self.directory_list[self.num_consoles][select_dir[0]].split(" " * 10)[1]
            self.widget_list_consoles["values"] = self.list_consoles
            self.widget_list_consoles.current(self.num_consoles)
            self.data_create_f()
        else:
            self.rFTP_file_read()

    def start_file_f_0(self, select_dir):
        os.startfile(self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" +
                     self.directory_list[self.num_consoles][select_dir].split(" " * 15)[1], "open")

    def cd_command_f_1(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.split(" ")[1]
            way = self.list_consoles[self.num_consoles].split(" " * 10)[1]
            data = data.lstrip(" ").rstrip(" ")
            if os.system(f"cd \"{way}\\{data}\"") == 1:
                return
            self.list_consoles[self.num_consoles] = self.list_consoles[self.num_consoles] + f"\\{data}"
            self.widget_list_consoles["values"] = self.list_consoles
            self.widget_list_consoles.current(self.num_consoles)
            del data
            self.data_create_f()
        else:
            self.error_win("Команду \"cd\" нельзя использовать в FTP директории.")

    def ret_but_f(self):
        if "|" not in self.list_consoles[self.num_consoles]:
            if self.list_consoles[self.num_consoles].split(" " * 10)[-4:] == "C:\\":
                return
            self.list_consoles[self.num_consoles] = self.list_consoles[self.num_consoles].split("\\" + self.list_consoles[self.num_consoles].split("\\")[-1])[0]
            # if self.list_consoles[self.num_consoles].split(" " * 10)[1] == "C:":
            #     self.list_consoles[self.num_consoles] += "\\"
            self.widget_list_consoles["values"] = self.list_consoles
            self.widget_list_consoles.current(self.num_consoles)
            self.data_create_f()
        else:
            self.list_consoles[self.num_consoles] = self.list_consoles[self.num_consoles].split("|")[0]
            self.widget_list_consoles["values"] = self.list_consoles
            self.widget_list_consoles.current(self.num_consoles)
            self.data_create_f()

    def select_con_f(self):
        self.num_consoles = self.list_consoles.index(self.widget_list_consoles.get())
        # ------------------------------------- data ^
        if "|" not in self.list_consoles[self.num_consoles]:
            if self.num_consoles == self.last_console:
                return
            self.data_create_f()
        else:
            if self.num_consoles == self.last_console:
                return
            self.rFTP_data_create()

    def new_con_f(self):
        num_con = int(self.list_consoles[-1].split(" ")[1])
        # ------------------------------------- data ^
        self.list_consoles.append("console " + str(num_con + 1) + " " * 10 + self.start_var)
        self.widget_list_consoles["values"] = self.list_consoles
        self.widget_list_consoles.current(num_con)
        self.num_consoles = num_con
        self.directory_list.append([])
        self.directory_list_ftp_f.append("")
        self.data_create_f()

    def help_c(self):
        help_info = ["CD - команда осуществляющая переход по директориям.\nCD [путь]",
                     "MD - команда осуществляющая создание директорий.\nMD [путь]\\[папка]\n MD [папка]",
                     "RMDIR - команда осуществляющая удаление директорий.\n RMDIR [путь]\\[папка]\nRMDIR [папка]",
                     "COPY - команда осуществляющая сохранение файла в участок памяти программы.\nCOPY [путь_1]",
                     "REN - команда для переименовывания файлов директорий.\nREN \"[файл\\директория]\" \"[файл\\директория]\"",
                     "RET - команда осуществляющая возвращение по директориям.\nRET\nRETURN",
                     "MF - команда осуществяющая создание файлов.\nMF [путь]\\[файл]\nMF [файл]",
                     "DEL - команда осуществляющая удаление файлов.\nDEL [путь]\\[файл]\nDEL [файл]",
                     "START - команда осуществляющая запуск приложений, открытие файлов.\nSTART [путь]\\[файл]\nSTART [файл]",
                     "EXIT - команда для закрытия консольной вкладки.\nEXIT\nEXIT console_n",
                     "NEW_CON - команда для запуска дополнительной консольной вкладки.\nNEW_CON",
                     "PASTE - команда осуществляющая создание файла с данными файла из участка памяти.\nPASTE",
                     "mFTP - команда для создания фтп папки. mFTP [путь]:[пороль]:[индекс], mFTP [папка]:[пороль]:[индекс]",
                     "rFTP - команда для чтения фтп папки на сторонем устройстве. rFTP [индекс]:[имя FTP директории]:[пороль]"]
        c = self.command_list_widget.curselection()
        # ------------------------------------- data ^
        if c == ():
            return
        else:
            self.list_c_help["state"] = "normal"
            self.list_c_help.delete("1.0", tk.END)
            self.list_c_help.insert(tk.INSERT, help_info[c[0]])
            self.list_c_help["state"] = "disabled"

    def exit_command_f(self):
        if len(self.list_consoles) == 1:
            self.root.destroy()
            quit()
        self.list_consoles.pop(self.num_consoles)
        if self.num_consoles == 1:
            self.num_consoles += 1
        else:
            self.num_consoles -= 1
        self.widget_list_consoles["values"] = self.list_consoles
        self.widget_list_consoles.current(self.num_consoles)
        self.data_create_f()

    def start_command_f(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.partition("start ")[-1]
            data = data.lstrip(" ").rstrip(" ")
            # ------------------------------------- data ^
            if "C:\\" not in data:
                data = "\"C:\\" + self.list_consoles[self.num_consoles].split("C:\\")[1] + f'\\{data}\"'
            # ------------------------------------- data ^
            os.startfile(data, "open")
            self.data_create_f()
            return
        else:
            self.rFTP_file_read()

    def md_command_f(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.partition("md ")[-1]
            data = data.lstrip(" ").rstrip(" ")
            # ------------------------------------- data ^
            if "C:\\" not in data:
                data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data
            try:
                os.system("md \"" + data + "\"")
                del data
                self.data_create_f()
            except OSError:
                del data
                return
        else:
            self.error_win("Нельзя создать директорию в FTP директории.\nМожно обновить фтп директорию путем повторного создания ее.")

    def rmdir_command_f(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.partition("rmdir ")[-1]
            data = data.lstrip(" ").rstrip(" ")
            # ------------------------------------- data ^
            if "C:\\" not in data:
                data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data
            try:
                os.system("rmdir \"" + data + "\"")
                del data
                self.data_create_f()
            except OSError:
                del data
                return
        else:
            self.error_win("Нельзя удалить директорию в FTP директории.")

    def ren_command_f(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.partition("ren ")[-1]
            data = data.lstrip(" ").rstrip(" ")
            data_1 = data.split("\"")[3]
            # ------------------------------------- data ^
            if "C:\\" not in data:
                data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data
            try:
                os.system(f"ren \"{data}\" \"{data_1}\"")
                self.answer_win(f"Файл \"{data}\" успешно переименован.")
                self.data_create_f()
            except OSError:
                self.error_win(f"Не удалось переименовать файл: \"{data}\" в \"{data_1}\".")
            del data, data_1
        else:
            self.error_win("Нельзя переименовать файл в FTP директории.")

    def copy_command_f(self, data):
        data = data.partition("copy ")[-1]
        data = data.rstrip(" ").lstrip(" ")
        if "|" not in self.list_consoles[self.num_consoles]:
            if "C:\\" not in data:
                data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data
            try:
                if data in self.copy_list:
                    self.answer_win(f"Файл \"{data}\" уже в буфере обмена.")
                if os.path.isfile(data):
                    self.copy_list.append(data)
            except OSError:
                self.error_win(f"Не удалось поместить файл: \"{data}\" в буфер обмена.")
            del data
        else:
            try:
                if "C:\\" in data:
                    self.error_win("FTP директория не имеет маршрута \"C:\\\".")
                    return
                list_outListbox = []
                for i in range(0, len(self.directory_list[self.num_consoles])):
                    list_outListbox.append(self.out_ListBox.get(i))
                file = self.directory_list_ftp_f[list_outListbox.index("file" + " " * 15 + data)].split("|")[list_outListbox.index("file" + " " * 15 + data) * 2 + 1].split("\\")[-1]
                self.copy_list.append(file + "|" + self.directory_list_ftp_f[list_outListbox.index("file" + " " * 15 + data)].split("|")[list_outListbox.index("file" + " " * 15 + data) * 2 + 2])
            except IndexError:
                self.error_win(f"Не удалось поместить файл: \"{data}\" в буфер обмена.")
                del data

    def paste_command_f(self):
        way = self.list_consoles[self.num_consoles].split(" " * 10)[1]
        if len(self.copy_list) > 0:
            for i in self.copy_list:
                if "|" not in i:
                    try:
                        os.system(f"copy \"{i}\" \"" + way + "\"")
                    except OSError:
                        self.error_win(f"Не удалось скопировать файл: \"{i}\" в директорию: \"{way}\".")
                else:
                    with open(way + "\\" + i.split("|")[0], "w", encoding="utf-8") as file_paste:
                        file_paste.write(i.partition("|")[-1])
        self.data_create_f()

    def mf_command_f(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.split("mf ")[1]
            data = data.lstrip(" ").rstrip(" ")
            if "C:\\" not in data:
                data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + "\\" + data
            try:
                if os.path.isfile(data) == 0:
                    with open(data, "w", encoding="utf-8") as _:
                        self.data_create_f()
            except OSError:
                self.error_win(f"Не удалось создать файл: \"{data}\".")
        else:
            self.error_win("Нельзя создать создать файл в FTP директории.")

    def del_command_f(self, data):
        if "|" not in self.list_consoles[self.num_consoles]:
            data = data.split("del ")[1]
            data = data.lstrip(" ").rstrip(" ")
            if "C:\\" not in data:
                data = self.list_consoles[self.num_consoles].split(" " * 10)[1] + f"\\{data}"
            list_data_1 = os.listdir(path=data)
            if list_data_1:
                return
            try:
                if os.path.isfile(path=data):
                    os.system(f"del \"{data}\"")
                    self.data_create_f()
                else:
                    os.system(f"mkdir \"{data}\"")
                    self.data_create_f()
            except OSError:
                self.error_win(f"Не удалось удалить файл: \"{data}\".")
        else:
            self.error_win("Нельзя удалить файл директорию в FTP директории.")

    @staticmethod
    def error_win(text):
        messagebox.showerror(title="Error", message=text)

    @staticmethod
    def answer_win(text):
        messagebox.showinfo(title="Answer", message=text)

    def mftp(self, data):
        way, data_out, n = self.list_consoles[self.num_consoles].split(" " * 10)[1], "", 0
        data = data.partition(" ")[-1]
        data_0 = data.split(":")[0]
        data_take_path = os.listdir(path=f"{way}\\{data_0}")
        for i in data_take_path:
            if not os.path.isdir(f"{way}\\{data_0}\\{i}"):
                with open(f"{way}\\{data_0}\\{i}", "r", encoding="utf-8") as take_data_f:
                    data_out += f"{way}\\{data_0}\\{i}|{take_data_f.read()}|"
                n += 1
        with open("data\\data_o", "w", encoding="utf-8") as out_data:
            out_data.write(f"{data}|{data_out}{n}\n")
        with open("data\\ind_0", "w", encoding="utf-8") as ind:
            ind.write("6")
        while True:
            sleep(0.1)
            with open("data\\ind_0", "r", encoding="utf-8") as check_answer:
                answer = check_answer.read()
                if answer == "1":
                    self.answer_win("FTP директория создана и сохранена в базе данных.")
                    break
                elif answer == "3":
                    self.error_win("Индекс FTP папки уже занят.\nmFTP [папка]:[пороль]:[индекс].")
                    break
                else:
                    continue

    def rFTP_file_read(self):
        select_f = self.out_ListBox.curselection()
        if select_f != ():
            file = self.directory_list_ftp_f[self.num_consoles].split("|")[select_f[0] * 2 + 1].split("\\")[-1]
            with open(f"data\\{file}", "w", encoding="utf-8") as FTP_file_c:
                FTP_file_c.write(self.directory_list_ftp_f[self.num_consoles].split("|")[select_f[0] * 2 + 2])
            os.startfile(f"data\\{file}", "open")
        else:
            self.error_win("Файл в FTP директории не выбран.")

    def rFTP_data_create(self):
        data_0 = self.directory_list_ftp_f[self.num_consoles].split("|")
        if self.directory_list[0]:
            for _ in range(0, len(self.directory_list[self.last_console])):
                self.out_ListBox.delete(0)
            self.directory_list.pop(self.num_consoles)
        self.directory_list.insert(self.num_consoles, [])
        for i in range(0, len(data_0) + 1):
            if i % 2 == 1:
                self.directory_list[self.num_consoles].append(data_0[i])
        self.directory_list[self.num_consoles].pop()
        for i in self.directory_list[self.num_consoles]:
            self.out_ListBox.insert(tk.END, "file" + " " * 15 + i.split("\\")[-1])
        self.last_console = self.num_consoles
        self.widget_list_consoles["values"] = self.list_consoles
        self.widget_list_consoles.current(self.num_consoles)

    def start_rFTP_data_create(self):
        with open("data\\data_i", "r", encoding="utf-8") as data:
            data = data.read()
        self.directory_list_ftp_f[self.num_consoles] = data
        self.list_consoles[self.num_consoles] += "|ftp " + self.directory_list_ftp_f[self.num_consoles].split("|")[0]
        self.rFTP_data_create()

    def rftp(self, data):
        with open("data\\data_o", "w", encoding="utf-8") as r_ftp_data:
            r_ftp_data.write(data)
        with open("data\\ind_0", "w", encoding="utf-8") as r_ftp_index:
            r_ftp_index.write("7")
        while True:
            sleep(0.05)
            with open("data\\ind_0", "r", encoding="utf-8") as read_ind:
                ind = read_ind.read()
                if ind == "2":
                    self.start_rFTP_data_create()
                    self.answer_win("FTP директория открыта.")
                    break
                elif ind == "4":
                    self.error_win("Не удалось открыть удаллённый FTP директорию.")
                    break
                else:
                    continue

    def analysis_command_f(self):
        data = self.enter_command.get()
        # ------------------------------------- data ^
        self.enter_command.delete(0, tk.END)
        if " " in data:
            if data.split(" ")[0].lower() == "cd":
                self.cd_command_f_1(data)
            elif data.split(" ")[0].lower() == "md":
                self.md_command_f(data)
            elif data.split(" ")[0].lower() == "rmdir":
                self.rmdir_command_f(data)
            elif data.split(" ")[0].lower() == "copy":
                self.copy_command_f(data)
            elif data.split(" ")[0].lower() == "ren":
                self.ren_command_f(data)
            elif data.split(" ")[0].lower() == "mf":
                self.mf_command_f(data)
            elif data.split(" ")[0].lower() == "del":
                self.del_command_f(data)
            elif data.split(" ")[0].lower() == "start":
                self.start_command_f(data)
            elif data.split(" ")[0].lower() == "mftp":
                self.mftp(data)
            elif data.split(" ")[0].lower() == "rftp":
                self.rftp(data)
            return
        elif data[:4].lower() == "exit":
            self.exit_command_f()
        elif data[:3].lower() == "ret":
            self.ret_but_f()
        elif data[:7].lower() == "new_con":
            self.new_con_f()
        elif data[:5].lower() == "paste":
            self.paste_command_f()


class SettingWindow:
    def __init__(self):
        self.root_2 = tk.Toplevel()
        self.root_2.geometry("300x70")
        self.root_2.resizable(False, False)
        self.root_2.title('Settings')
        # -------------------------------------------------- settings win setting ^
        text_1 = tk.Label(self.root_2, text="Start var: ")
        text_1.grid(row=0, column=0, pady=5)

        with open("data\\s_var", "r", encoding="utf-8") as start_var:
            self.start_var_entry = tk.Entry(self.root_2, width=31)
            self.start_var_entry.bind("<Return>", lambda e: self.root_2)
            self.start_var_entry.grid(row=0, column=1, columnspan=2, pady=5)
            self.start_var_entry.insert(0, start_var.read())

        self.check_but_1 = tk.Button(self.root_2, text="check", command=self.analis_var)
        self.check_but_1.grid(row=0, column=3, pady=5)

        self.message = tk.Label(self.root_2, text="No messages", anchor="w")
        self.message.grid(row=2, column=0, pady=5, columnspan=2)

        self.save_but = tk.Button(self.root_2, text="save", command=self.save_data, width=6)
        self.save_but.grid(row=2, column=2, pady=5)

        self.cancel_but = tk.Button(self.root_2, text="cancel", command=self.cancel, width=6)
        self.cancel_but.grid(row=2, column=3)

    def analis_var(self):
        var = self.start_var_entry.get()
        if var == "":
            self.message["text"] = "Системе не удаёться наити путь."
            return
        error = os.system(f"cd \"{var}\"")
        if error == 1:
            self.message["text"] = "Системе не удаёться наити путь."
            self.start_var_entry.delete(0, tk.END)
            self.start_var_entry.insert(0, var)
        else:
            self.message["text"] = "Путь обновлен. Сохраните."
            return

    def save_data(self):
        entry_data = self.start_var_entry.get()
        error = os.system("cd " + entry_data)
        if error == 1:
            self.message["text"] = "Неверно выбранная директория."
            return
        with open("data\\s_var", "w", encoding="utf-8") as data_s:
            data_s.write(entry_data)
        self.root_2.destroy()

    def cancel(self):
        self.root_2.destroy()


class FastCommandsWin:
    def __init__(self, main_window_self, x, y, geo, block=1):
        self.mainWindow_self = main_window_self
        geo = geo.split("+")
        self.root_3 = tk.Toplevel()
        self.root_3.geometry(f'199x100+{x + int(geo[1]) - 10}+{y + int(geo[2])}')
        self.root_3.resizable(False, False)
        self.root_3.title('Fast commands')

        self.open_but = tk.Button(self.root_3, text="Open", command=self.open_f, width=27)
        self.open_but.grid(row=0, column=0)

        self.copy_but = tk.Button(self.root_3, text="Copy", command=self.copy_f, width=27)
        self.copy_but.grid(row=1, column=0)

        self.paste_but = tk.Button(self.root_3, text="Paste", command=self.paste_f, width=27)
        self.paste_but.grid(row=2, column=0)

        self.del_but = tk.Button(self.root_3, text="Delete", command=self.del_f, width=27)
        self.del_but.grid(row=3, column=0)

        if block == 0:
            self.open_but["state"] = "disabled"
            self.copy_but["state"] = "disabled"
            self.del_but["state"] = "disabled"
        elif block == 2:
            self.open_but["state"], self.copy_but["state"], self.del_but["state"] = "disabled", "disabled", "disabled"
            self.paste_but["state"] = "disabled"
        elif block == 3:
            self.del_but["state"], self.paste_but["state"] = "disabled", "disabled"

    def open_f(self):
        MainWindow.cd_command_f_0(self.mainWindow_self)
        self.root_3.destroy()

    def copy_f(self):
        MainWindow.fast_copy_command_f(self.mainWindow_self)
        self.root_3.destroy()

    def paste_f(self):
        MainWindow.paste_command_f(self.mainWindow_self)
        self.root_3.destroy()

    def del_f(self):
        MainWindow.fast_delete_command_f(self.mainWindow_self)
        self.root_3.destroy()


with open("data\\ind_0", "w", encoding="utf-8") as w_i:
    w_i.write("0")
with open("data\\f_c", "w", encoding="utf-8") as up_f_c:
    up_f_c.write("0")
MainWindow()
