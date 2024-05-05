import tkinter as tk
from tkinter import filedialog, scrolledtext
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import pandas as pd

from modules.data import Data
from ui import data_general_text_body, graphs_tabs, generate_body


dataframe = None


def load_csv():
    global dataframe
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        dataframe = Data(pd.read_csv(file_path))
        print("CSV loaded:", file_path)

        data_general_text_body.delete(1.0, tk.END)
        data_general_text_body.insert(tk.END, dataframe.data_body)


def draw_graph(canvas, plot, column_name):
    x = dataframe.data_body.index
    y = dataframe.data_body[column_name]
    plot.plot(x, y)
    plot.set_xlabel('Index')
    plot.set_ylabel(column_name)
    plot.set_title(f'График для столбца "{column_name}"')


def show_graphs(data):
    if dataframe == None:
        return

    for widget in graphs_tabs.winfo_children():
        widget.destroy()

    for column_name in dataframe.data_body.columns:
        tab = ttk.Frame(graphs_tabs)
        graphs_tabs.add(tab, text=column_name)

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        draw_graph(FigureCanvasTkAgg(fig, master=tab), plot, column_name)


generate_body()
