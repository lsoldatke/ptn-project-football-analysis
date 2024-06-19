import pandas as pd
import tkinter as tk
from tkinter import ttk


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def show_results():
    operation = operation_combobox.get()
    target = target_combobox.get()
    by = by_combobox.get()
    order = order_combobox.get()

    clear_window()

    frame = ttk.Frame(root)
    frame.pack(expand=True, fill='both')

    results_df = pd.DataFrame()

    match operation:
        case "Sort":
            results_df = sort(target, by, order)

    results_view = ttk.Treeview(root)
    results_view['columns'] = list(results_df.columns)
    results_view['show'] = 'headings'

    for column in results_df.columns:
        results_view.heading(column, text=column)
        results_view.column(column, anchor="w")
    for index, row in results_df.iterrows():
        results_view.insert("", "end", values=list(row))

    h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=results_view.xview)
    h_scrollbar.pack(side="bottom", fill="x")
    results_view.configure(xscrollcommand=h_scrollbar.set)
    results_view.pack(side="top", fill="both", expand=True)

    print(results_df)


def sort(target, by, order):
    match target:
        case "Players":
            match by:
                case "Name":
                    match order:
                        case "Ascending":
                            return players_df.sort_values('name', ascending=True)
                        case "Descending":
                            return players_df.sort_values('name', ascending=False)


def match_options_for_operations(event):
    selected_operation = operation_combobox.get()

    match selected_operation:
        case "Filter":
            order_label.grid_forget()
            order_combobox.grid_forget()
            value_label.grid(row=3, column=0)
            value_entry.grid(row=3, column=1, padx=10, pady=10)
        case "Sort":
            if not order_label.winfo_viewable():
                order_label.grid(row=3, column=0)
            if not order_combobox.winfo_viewable():
                order_combobox.grid(row=3, column=1, padx=10, pady=10)
            if value_label.winfo_viewable():
                value_label.grid_forget()
            if value_entry.winfo_viewable():
                value_entry.grid_forget()


# Pandas view configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Datasource configuration
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'

players_df = pd.read_csv(players_datasource)

root = tk.Tk()
root.title("Football data analysis project")

operation_label = tk.Label(root, text="Operation:")
operation_label.grid(row=0, column=0)
operation_combobox = ttk.Combobox(root, values=["Sort", "Filter"])
operation_combobox.grid(row=0, column=1, padx=10, pady=10)
operation_combobox.current(0)

operation_combobox.bind("<<ComboboxSelected>>", match_options_for_operations)

target_label = tk.Label(root, text="Target:")
target_label.grid(row=1, column=0)
target_combobox = ttk.Combobox(root, values=["Players", "Clubs"])
target_combobox.grid(row=1, column=1, padx=10, pady=10)
target_combobox.current(0)

by_label = tk.Label(root, text="By:")
by_label.grid(row=2, column=0)
by_combobox = ttk.Combobox(root, values=["Name"])
by_combobox.grid(row=2, column=1, padx=10, pady=10)
by_combobox.current(0)

order_label = tk.Label(root, text="Order:")
order_label.grid(row=3, column=0)
order_combobox = ttk.Combobox(root, values=["Ascending", "Descending"])
order_combobox.grid(row=3, column=1, padx=10, pady=10)
order_combobox.current(0)

value_label = tk.Label(root, text="Value")
value_label.grid_forget()
value_entry = tk.Entry(root)
value_entry.grid_forget()

tk.Button(root, text="Analyze", command=show_results).grid(row=4, column=0, padx=10, pady=10)

root.mainloop()
