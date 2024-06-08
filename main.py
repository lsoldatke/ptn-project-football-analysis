import pandas as pd

# Pandas view configuration
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# Datasource configuration
datasource_directory = './data/'
players_datasource = datasource_directory + 'players.csv'

current_menu = 'main'


def show_available_operations():
    print()
    print("Available operations:")

    match current_menu:
        case 'main':
            print("1. Market values")
            print("0. Exit")
        case 'market_values':
            print("1. Descending")
            print("2. Ascending")
            print("0. Back")

    print()


print()
print("Football data analysis project")
print("------------------------------")

df = pd.read_csv(players_datasource)

show_available_operations()

selection = ''

while True:
    selection = input("Choose operation (L for list of available operations): ")

    match selection:
        case '1':
            current_menu = 'market_values'
            show_available_operations()

            while True:
                selection = input("Choose operation (L for list of available operations): ")

                match selection:
                    case '1':
                        print()
                        print(df.sort_values('market_value_in_eur', ascending=False))
                        show_available_operations()
                    case '2':
                        print()
                        print(df.sort_values('market_value_in_eur', ascending=True))
                        show_available_operations()
                    case '0':
                        current_menu = 'main'
                        show_available_operations()
        case '0':
            exit(0)
        case 'L' | 'l':
            show_available_operations()
        case _:
            print("Invalid selection")
