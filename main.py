import pandas as pd

# Pandas view configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Datasource configuration
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'


def show_available_operations():
    print()
    print("Available operations:")
    print("1. Sort players by their market value - descending")
    print("0. Exit")
    print()


print()
print("Football data analysis project")
print("------------------------------")

df = pd.read_csv(players_datasource)

show_available_operations()

selection = ''

while selection != '0':
    selection = input("Choose operation (L for list of available operations): ")

    match selection:
        case '1':
            print()
            print(df.sort_values('market_value_in_eur', ascending=False))
            print()
        case '0':
            exit(0)
        case 'L' | 'l':
            show_available_operations()
        case _:
            print("Invalid selection")
