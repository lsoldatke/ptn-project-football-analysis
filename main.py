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


def change_widget_visibility(widget, visibility):
    if visibility and not widget.winfo_viewable():
        widget.grid(padx=10, pady=10)
    if not visibility and widget.winfo_viewable():
        widget.grid_forget()


def update_by_combobox(event):
    match target_combobox.get():
        case "Players":
            by_combobox.config(values=list(players_df.columns))
        case "Clubs":
            by_combobox.config(values=list(clubs_df.columns))


def update_menu(event):
    match operation_combobox.get():
        case "Sort":
            # change_widget_visibility(order_label, True)
            # change_widget_visibility(order_combobox, True)
            # change_widget_visibility(value_label, False)
            # change_widget_visibility(value_entry, False)

            if not order_label.winfo_viewable():
                order_label.grid(row=3, column=0)
            if not order_combobox.winfo_viewable():
                order_combobox.grid(row=3, column=1, padx=10, pady=10)
            if value_label.winfo_viewable():
                value_label.grid_forget()
            if value_entry.winfo_viewable():
                value_entry.grid_forget()
        case "Filter":
            # change_widget_visibility(order_label, False)
            # change_widget_visibility(order_combobox, False)
            # change_widget_visibility(value_label, True)
            # change_widget_visibility(value_entry, True)

            order_label.grid_forget()
            order_combobox.grid_forget()
            value_label.grid(row=3, column=0)
            value_entry.grid(row=3, column=1, padx=10, pady=10)


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

operation_frame = tk.Frame(root)
operation_frame.pack(pady=5)
target_frame = tk.Frame(root)
target_frame.pack(pady=5)
by_frame = tk.Frame(root)
by_frame.pack(pady=5)
order_frame = tk.Frame(root)
order_frame.pack(pady=5)
value_frame = tk.Frame(root)
value_frame.pack(pady=5)
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=5)

operation_label = tk.Label(operation_frame, text="Operation:")
operation_label.pack(side="left")
operation_combobox = ttk.Combobox(operation_frame, values=["Sort", "Filter"])
operation_combobox.pack(side="left")
operation_combobox.current(0)
operation_combobox.bind("<<ComboboxSelected>>", update_menu)

target_label = tk.Label(target_frame, text="Target:")
target_label.pack(side="left")
target_combobox = ttk.Combobox(target_frame, values=["Players", "Clubs"])
target_combobox.pack(side="left")
target_combobox.current(0)
target_combobox.bind("<<ComboboxSelected>>", update_by_combobox)

by_label = tk.Label(by_frame, text="By:")
by_label.pack(side="left")
by_combobox = ttk.Combobox(by_frame, values=list(players_df.columns))
by_combobox.pack(side="left")
by_combobox.current(0)

order_label = tk.Label(order_frame, text="Order:")
order_label.pack(side="left")
order_combobox = ttk.Combobox(order_frame, values=["Ascending", "Descending"])
order_combobox.pack(side="left")
order_combobox.current(0)

value_label = tk.Label(value_frame, text="Value")
value_label.pack_forget()
value_entry = tk.Entry(value_frame)
value_entry.pack_forget()

analyze_button = tk.Button(buttons_frame, text="Analyze", command=show_results)
analyze_button.pack(side="left")

root.mainloop()
