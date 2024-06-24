import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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


def reorganize_dataframe(df, first_col):
    new_cols = [first_col] + [col for col in df.columns.tolist() if col != first_col]

    return df[new_cols]


def show_results():
    operation = operation_combobox.get()
    target = target_combobox.get()
    by = by_combobox.get()
    order = order_combobox.get()
    value = value_entry.get()

    clear_window()

    results_frame = ttk.Frame(root)
    results_frame.pack(expand=True, fill='both')

    results_df = pd.DataFrame()

    match operation:
        case "Sort":
            results_df = sort_data(target, by, order)
        case "Filter":
            results_df = filter_data(target, by, value)

    results_view = ttk.Treeview(root)
    results_view['columns'] = list(results_df.columns)
    results_view['show'] = 'headings'

    for column in results_df.columns:
        results_view.heading(column, text=column)
        results_view.column(column, anchor="w")
    for index, row in results_df.iterrows():
        results_view.insert("", "end", values=list(row))

    h_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=results_view.xview)
    h_scrollbar.pack(side="bottom", fill="x")
    results_view.configure(xscrollcommand=h_scrollbar.set)
    results_view.pack(side="top", fill="both", expand=True)


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
def sort_data(target, by, order):
    df_to_sort = pd.DataFrame()

    match target:
        case "Players":
            df_to_sort = players_df
        case "Clubs":
            df_to_sort = clubs_df

    sorted_df = df_to_sort.sort_values(by, ascending=True if order == "Ascending" else False)

    return reorganize_dataframe(sorted_df, by)


def filter_data(target, by, value):
    df_to_filter = pd.DataFrame()

    match target:
        case "Players":
            df_to_filter = players_df
        case "Clubs":
            df_to_filter = clubs_df

    filtered_df = df_to_filter.loc[df_to_filter[by].str.contains(value, case=False)]

    return reorganize_dataframe(filtered_df, by)


def create_dependency_chart():
    merged_df = pd.merge(player_valuations_df, players_df, on='player_id')
    merged_df = merged_df.drop(columns=['market_value_in_eur_x', 'market_value_in_eur_y'])

    print(merged_df.head())
    print(merged_df.columns)

    fig = plt.figure(figsize=(10, 6))

    for player_id in merged_df['player_id'].unique():
        player_data = merged_df[merged_df['player_id'] == player_id]
        plt.plot(player_data['date'], player_data['market_value_in_eur'], marker='o', label=player_data['name'].iloc[0])

    plt.title("Chart of players' values")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Pandas view configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Datasource configuration
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'
player_valuations_datasource = datasource_directory + 'player_valuations.csv'
clubs_datasource = datasource_directory + 'clubs.csv'

# Dataframe initialization
players_df = pd.read_csv(players_datasource)
player_valuations_df = pd.read_csv(player_valuations_datasource)
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
dependency_chart_button = tk.Button(buttons_frame, text="Values", command=create_dependency_chart)
dependency_chart_button.grid()

root.mainloop()
