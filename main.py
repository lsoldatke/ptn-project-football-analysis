import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def change_widget_visibility(widget, visibility):
    if visibility and not widget.winfo_viewable() and widget in grid_info:
        widget.grid(**grid_info[widget])
    if not visibility and widget.winfo_viewable():
        grid_info[widget] = widget.grid_info()
        widget.grid_forget()


def reorganize_dataframe(df, first_col):
    new_cols = [first_col] + [col for col in df.columns.tolist() if col != first_col]

    return df[new_cols]


def show_results():
    operation = operation_combobox.get()
    target = target_combobox.get()
    by = by_combobox.get()
    order = order_combobox.get()
    value = value_entry.get()

    if operation == "Wykres":
        plot_player_market_values()
    else:
        clear_window()

        results_frame = ttk.Frame(root)
        results_frame.pack(expand=True, fill='both')

        results_df = pd.DataFrame()

        match operation:
            case "Sortowanie":
                results_df = sort_data(target, by, order)
            case "Filtrowanie":
                results_df = filter_data(target, by, value)

        results_view = ttk.Treeview(results_frame)
        results_view['columns'] = list(results_df.columns)
        results_view['show'] = 'headings'

        for column in results_df.columns:
            results_view.heading(column, text=column)
            results_view.column(column, anchor="w")
        for index, row in results_df.iterrows():
            results_view.insert("", "end", values=list(row))

        h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=results_view.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_view.yview)
        v_scrollbar.pack(side="right", fill="y")
        results_view.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        results_view.pack(side="top", fill="both", expand=True)

        menu_button = tk.Button(root, text="Powrót do menu", command=show_main_menu)
        menu_button.pack(padx=10, pady=10)


def on_operation_combobox_change(event):
    match operation_combobox.get():
        case "Sort":
            change_widget_visibility(order_frame, True)
            change_widget_visibility(value_frame, False)
        case "Filter":
            change_widget_visibility(order_frame, False)
            change_widget_visibility(value_frame, True)
        case "Plot":
            change_widget_visibility(order_frame, False)
            change_widget_visibility(value_frame, True)
            by_combobox.config(values=["Wartość / Data"])
            value_label.config(text="Wartość (ID zawodnika)")


def on_target_combobox_change(event):
    match target_combobox.get():
        case "Zawodnicy":
            by_combobox.config(values=list(players_df.columns))
        case "Kluby":
            by_combobox.config(values=list(clubs_df.columns))


def sort_data(target, by, order):
    df_to_sort = pd.DataFrame()

    match target:
        case "Zawodnicy":
            df_to_sort = players_df
        case "Kluby":
            df_to_sort = clubs_df

    sorted_df = df_to_sort.sort_values(by, ascending=True if order == "Rosnąco" else False)

    return reorganize_dataframe(sorted_df, by)


def filter_data(target, by, value):
    df_to_filter = pd.DataFrame()

    match target:
        case "Zawodnicy":
            df_to_filter = players_df
        case "Kluby":
            df_to_filter = clubs_df

    filtered_df = df_to_filter.loc[df_to_filter[by].str.contains(value, case=False)]

    return reorganize_dataframe(filtered_df, by)


def plot_player_market_values():
    player_id = int(value_entry.get())
    player_name = players_df.loc[players_df['player_id'] == player_id, 'name'].values[0]
    player_values = player_valuations_df[player_valuations_df['player_id'] == player_id]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(player_values['date'], player_values['market_value_in_eur'], marker='o')
    ax.set_title("Zmiany wartości rynkowej zawodnika z ID: " + str(player_id) + " " + player_name)
    ax.set_xlabel("Data")
    ax.set_ylabel("Wartość")
    ax.tick_params(axis='x', labelsize=5)
    ax.grid()

    clear_window()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    menu_button = tk.Button(root, text="Back to menu", command=show_main_menu)
    menu_button.pack(padx=10, pady=10)


def show_main_menu():
    global grid_info
    global menu_frame, operation_frame, target_frame, by_frame, value_frame, order_frame, buttons_frame
    global operation_label, operation_combobox
    global target_label, target_combobox
    global by_label, by_combobox
    global value_label, value_entry
    global order_label, order_combobox
    global analyze_button

    clear_window()

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

    operation_label = tk.Label(operation_frame, text="Operacja:")
    operation_label.grid()
    operation_combobox = ttk.Combobox(operation_frame, values=["Sortowanie", "Filtrowanie", "Wykres"])
    operation_combobox.grid()
    operation_combobox.current(0)
    operation_combobox.bind("<<ComboboxSelected>>", on_operation_combobox_change)

    target_label = tk.Label(target_frame, text="Cel analizy:")
    target_label.grid()
    target_combobox = ttk.Combobox(target_frame, values=["Zawodnicy", "Kluby"])
    target_combobox.grid()
    target_combobox.current(0)
    target_combobox.bind("<<ComboboxSelected>>", on_target_combobox_change)

    by_label = tk.Label(by_frame, text="Według:")
    by_label.grid()
    by_combobox = ttk.Combobox(by_frame, values=list(players_df.columns))
    by_combobox.grid()
    by_combobox.current(0)

    value_label = tk.Label(value_frame, text="Wartość:")
    value_label.grid()
    value_entry = tk.Entry(value_frame)
    value_entry.grid()

    order_label = tk.Label(order_frame, text="Porządek:")
    order_label.grid()
    order_combobox = ttk.Combobox(order_frame, values=["Rosnąco", "Malejąco"])
    order_combobox.grid()
    order_combobox.current(0)

    analyze_button = tk.Button(buttons_frame, text="Analizuj", command=show_results)
    analyze_button.grid()


# Konfiguracja widoku Pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Konfiguracja źródła danych
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'
player_valuations_datasource = datasource_directory + 'player_valuations.csv'
clubs_datasource = datasource_directory + 'clubs.csv'

# Inicjalizacja dataframe
players_df = pd.read_csv(players_datasource)
player_valuations_df = pd.read_csv(player_valuations_datasource)
clubs_df = pd.read_csv(clubs_datasource)

root = tk.Tk()
root.title("Projekt do analizy danych piłkarskich")

show_main_menu()

root.mainloop()
