from tkinter import ttk, scrolledtext

from PIL._tkinter_finder import tk

from main import load_csv, show_graphs


data_frame = None
data_general_text_body = None

graphs_frame = None
graphs_tabs = None


def generate_body():
    global data_frame
    global data_general_text_body

    global graphs_frame
    global graphs_tabs

    # Main ===========

    root = tk.Tk()
    root.title('Cordell Space')
    root.geometry('600x600')
    root.resizable(width=False, height=False)

    # Tabs ===========

    tabs = []
    tab_control = ttk.Notebook(root)
    for i in ['Данные', 'Основное', 'Графики', 'Корреляция']:
        tabs.append(ttk.Frame(tab_control))
        tab_control.add(tabs[len(tabs) - 1], text=i)

    tab_control.pack(expand=1, fill='both')

    # ================

    # Вкладка "Данные"
    data_frame = tk.Frame(tabs[0])
    data_frame.pack(fill='both', expand=1)
    btn_load_csv = tk.Button(data_frame, text='Загрузить CSV', command=load_csv)
    btn_load_csv.pack(pady=10)

    data_general_text_body = scrolledtext.ScrolledText(data_frame, wrap=tk.WORD)
    data_general_text_body.pack(fill='both', expand=1)

    # Вкладка "Графики"
    graphs_frame = tk.Frame(tabs[2])
    graphs_frame.pack(fill='both', expand=1)

    graphs_tabs = ttk.Notebook(graphs_frame)
    graphs_tabs.pack(expand=1, fill='both')
    tab_control.bind("<<NotebookTabChanged>>", show_graphs)

    root.mainloop()
