import pandas as pd
import tkinter as tk
from tkinter import ttk


# Utility functions
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def change_widget_visibility(widget, visibility):
    if visibility and not widget.winfo_viewable() and widget in grid_info:
        widget.grid(**grid_info[widget])
    if not visibility and widget.winfo_viewable():
        grid_info[widget] = widget.grid_info()
        widget.grid_forget()


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


# Combobox change handlers
def on_operation_combobox_change(event):
    match operation_combobox.get():
        case "Sort":
            change_widget_visibility(order_frame, True)
            change_widget_visibility(value_frame, False)
        case "Filter":
            change_widget_visibility(order_frame, False)
            change_widget_visibility(value_frame, True)


def on_target_combobox_change(event):
    match target_combobox.get():
        case "Players":
            by_combobox.config(values=list(players_df.columns))
        case "Clubs":
            by_combobox.config(values=list(clubs_df.columns))


# Main functionalities
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


# Pandas view configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Datasource configuration
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'
clubs_datasource = datasource_directory + 'clubs.csv'

# Dataframe initialization
players_df = pd.read_csv(players_datasource)
clubs_df = pd.read_csv(clubs_datasource)

root = tk.Tk()
root.title("Football data analysis project")

grid_info = {}

menu_frame = tk.Frame(root)
menu_frame.grid(row=0, column=0, padx=15, pady=15, sticky='w')
operation_frame = tk.Frame(menu_frame)
operation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
target_frame = tk.Frame(menu_frame)
target_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")
by_frame = tk.Frame(menu_frame)
by_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")
value_frame = tk.Frame(menu_frame)
value_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
order_frame = tk.Frame(menu_frame)
order_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")
buttons_frame = tk.Frame(menu_frame)
buttons_frame.grid(row=4, column=0, padx=10, pady=10, sticky="w")

operation_label = tk.Label(operation_frame, text="Operation:")
operation_label.grid()
operation_combobox = ttk.Combobox(operation_frame, values=["Sort", "Filter"])
operation_combobox.grid()
operation_combobox.current(0)
operation_combobox.bind("<<ComboboxSelected>>", on_operation_combobox_change)

target_label = tk.Label(target_frame, text="Target:")
target_label.grid()
target_combobox = ttk.Combobox(target_frame, values=["Players", "Clubs"])
target_combobox.grid()
target_combobox.current(0)
target_combobox.bind("<<ComboboxSelected>>", on_target_combobox_change)

by_label = tk.Label(by_frame, text="By:")
by_label.grid()
by_combobox = ttk.Combobox(by_frame, values=list(players_df.columns))
by_combobox.grid()
by_combobox.current(0)

value_label = tk.Label(value_frame, text="Value")
value_label.grid()
value_entry = tk.Entry(value_frame)
value_entry.grid()

order_label = tk.Label(order_frame, text="Order:")
order_label.grid()
order_combobox = ttk.Combobox(order_frame, values=["Ascending", "Descending"])
order_combobox.grid()
order_combobox.current(0)

analyze_button = tk.Button(buttons_frame, text="Analyze", command=show_results)
analyze_button.grid()

root.mainloop()
