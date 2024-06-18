import pandas as pd
import tkinter as tk
from tkinter import ttk


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def show_results():
    clear_window()
    tk.Label(root, text="Not implemented yet").pack(padx=20, pady=20)


# Pandas view configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Datasource configuration
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'

root = tk.Tk()
root.title("Football data analysis project")

tk.Label(root, text="Operation:").grid(row=0, column=0)
operation_combobox = ttk.Combobox(root, values=["Sort", "Filter"])
operation_combobox.grid(row=0, column=1, padx=10, pady=10)
operation_combobox.current(0)

tk.Label(root, text="Target:").grid(row=1, column=0)
target_combobox = ttk.Combobox(root, values=["Players", "Clubs"])
target_combobox.grid(row=1, column=1, padx=10, pady=10)
target_combobox.current(0)

tk.Label(root, text="By:").grid(row=2, column=0)
target_combobox = ttk.Combobox(root, values=["Name"])
target_combobox.grid(row=2, column=1, padx=10, pady=10)
target_combobox.current(0)

tk.Label(root, text="Order:").grid(row=3, column=0)
target_combobox = ttk.Combobox(root, values=["Ascending", "Descending"])
target_combobox.grid(row=3, column=1, padx=10, pady=10)
target_combobox.current(0)

tk.Button(root, text="Analyze", command=show_results).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Clear window", command=clear_window).grid(row=4, column=1, padx=10, pady=10)

root.mainloop()

# def show_available_operations():
#     print()
#     print("Available operations:")
#     print("1d. Sort players by their market value - descending")
#     print("1a. Sort players by their market value - ascending")
#     print("2nm. Filter players by their name")
#     print("2c. Filter players by clubs")
#     print("2nt. Filter players by nationality")
#     print("0. Exit")
#     print()
#
# print()
# print("Football data analysis project")
# print("------------------------------")
#
# df = pd.read_csv(players_datasource)
#
# show_available_operations()
#
# selection = ''
#
# while True:
#     selection = input("Choose operation (L for list of available operations): ")
#
#     match selection:
#         case '1d':
#             print()
#             print(df.sort_values('market_value_in_eur', ascending=False))
#             show_available_operations()
#         case '1a':
#             print()
#             print(df.sort_values('market_value_in_eur', ascending=True))
#             show_available_operations()
#         case '2nm':
#             searched = input("Name: ")
#             print()
#             print(df.loc[df['name'] == searched])
#             show_available_operations()
#         case '2c':
#             searched = input("Club name: ")
#             print()
#             print(df.loc[df['current_club_name'] == searched])
#             show_available_operations()
#         case '2nt':
#             searched = input("Nationality: ")
#             print()
#             print(df.loc[df['country_of_citizenship'] == searched])
#             show_available_operations()
#         case '0':
#             exit(0)
#         case 'L' | 'l':
#             show_available_operations()
#         case _:
#             print("Invalid selection")
