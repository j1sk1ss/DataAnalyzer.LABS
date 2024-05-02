import tkinter as tk
from tkinter import filedialog, scrolledtext
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import pandas as pd

from modules.data import Data


dataframe = None


def load_csv():
    global dataframe
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        dataframe = Data(pd.read_csv(file_path))
        print("CSV loaded:", file_path)

        text.delete(1.0, tk.END)
        text.insert(tk.END, dataframe.data_body)


def draw_graph(canvas, plot, column_name):
    x = dataframe.data_body.index
    y = dataframe.data_body[column_name]
    plot.plot(x, y)
    plot.set_xlabel('Index')
    plot.set_ylabel(column_name)
    plot.set_title(f'График для столбца "{column_name}"')


def show_graphs():
    for widget in tab_control_graphs.winfo_children():
        widget.destroy()

    for column_name in dataframe.data_body.columns:
        tab = ttk.Frame(tab_control_graphs)
        tab_control_graphs.add(tab, text=column_name)

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        draw_graph(FigureCanvasTkAgg(fig, master=tab), plot, column_name)


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
frame_main = tk.Frame(tabs[0])
frame_main.pack(fill='both', expand=1)
btn_load_csv = tk.Button(frame_main, text='Загрузить CSV', command=load_csv)
btn_load_csv.pack(pady=10)

text = scrolledtext.ScrolledText(frame_main, wrap=tk.WORD)
text.pack(fill='both', expand=1)

# Вкладка "Графики"
frame_graph = tk.Frame(tabs[2])
frame_graph.pack(fill='both', expand=1)

tab_control_graphs = ttk.Notebook(frame_graph)
tab_control_graphs.pack(expand=1, fill='both')


root.mainloop()
