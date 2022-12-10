import os
from tkinter import *
from tkinter import ttk, filedialog

from converter import AudioConverter
from pdf_reader import PdfReader
from utils import get_user_desktop, invalid_pdf_messagebox, invalid_dir_messagebox, about_messagebox


class GUI(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master: Tk = master
        self.master.title('PDF to Audiobook Converter')
        self.master.resizable(width=False, height=False)
        self.grid(row=0, column=0, sticky=N + W + E + S)
        self.configure(padding=30)
        self.file_browse_button = None
        self.file_path = None
        self.destiny_button = None
        self.destiny_path = None
        self.convert_button = None
        self.warning_label = None
        self.create_widgets()

    def create_widgets(self):
        my_menu = Menu(self.master)
        self.master.config(menu=my_menu)
        self.master.option_add('*tearOff', False)
        file_menu = Menu(my_menu)
        my_menu.add_cascade(label='File', menu=file_menu)
        help_menu = Menu(my_menu)
        my_menu.add_cascade(label='Help', menu=help_menu)
        file_menu.add_command(label='Quit', command=self.master.quit)
        help_menu.add_command(label='About', command=about_messagebox)
        self.file_browse_button = ttk.Button(
            self,
            text='Choose a PDF',
            style='TButton',
            command=self.file_browse_event,
            width=20
        )
        self.file_browse_button.grid(row=0, column=0, sticky=W + E, padx=5, pady=5)
        self.file_path = StringVar(value='Choose a file')
        file_entry = ttk.Entry(self, textvariable=self.file_path, state='readonly', takefocus=0, width=55)
        file_entry.grid(row=0, column=1, sticky=N + W + S + E, padx=5, pady=5)
        self.destiny_button = ttk.Button(
            self,
            text='Choose destiny',
            style='TButton',
            command=self.destiny_folder_browse_event,
            width=20
        )
        self.destiny_button.grid(row=1, column=0, sticky=W + E, padx=5, pady=5)
        self.destiny_path = StringVar(value=get_user_desktop())
        destiny_entry = ttk.Entry(self, textvariable=self.destiny_path, state='readonly', takefocus=0, width=55)
        destiny_entry.grid(row=1, column=1, sticky=N + W + S + E, padx=5, pady=5)
        self.convert_button = ttk.Button(text="Convert", command=self.convert_action)
        self.convert_button.grid(row=2, column=0, pady=(0, 14))
        self.warning_label = ttk.Label(self, text="The window may freeze and not respond. Please, wait.")
        self.warning_label.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        self.warning_label.configure(justify='center')
        self.warning_label.grid_remove()

    def swap_loading_bar_and_button(self):
        loading_bar_is_visible = bool(self.warning_label.grid_info())
        if loading_bar_is_visible:
            self.warning_label.grid_remove()
            self.convert_button.grid()
        else:
            self.warning_label.grid()
            self.convert_button.grid_remove()

    def destiny_folder_browse_event(self):
        path = filedialog.askdirectory()
        if not path:
            return
        self.destiny_path.set(path)

    def file_browse_event(self):
        path = filedialog.askopenfilename()
        if path is None:
            return
        if not path.endswith('.pdf'):
            invalid_pdf_messagebox()
            return
        self.file_path.set(path)

    def convert_action(self):
        path = self.file_path.get()
        if not path.endswith('.pdf'):
            invalid_pdf_messagebox()
            return
        save_location = self.destiny_path.get()
        if not os.path.isdir(save_location):
            invalid_dir_messagebox()
            return
        self.swap_loading_bar_and_button()
        self.master.update_idletasks()
        audio_file_name = 'Converted ' + os.path.basename(path)[:-4] + '.mp3'
        audio_path = os.path.join(save_location, audio_file_name)
        pdf_string = PdfReader.convert_to_string(path=path)
        AudioConverter.convert_and_save(
            string=pdf_string,
            save_location=audio_path
        )
        self.swap_loading_bar_and_button()
        self.master.update_idletasks()
