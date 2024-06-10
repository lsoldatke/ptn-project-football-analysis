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
    print("1d. Sort players by their market value - descending")
    print("1a. Sort players by their market value - ascending")
    print("2nm. Filter players by their name")
    print("2c. Filter players by clubs")
    print("2nt. Filter players by nationality")
    print("0. Exit")
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
        case '1d':
            print()
            print(df.sort_values('market_value_in_eur', ascending=False))
            show_available_operations()
        case '1a':
            print()
            print(df.sort_values('market_value_in_eur', ascending=True))
            show_available_operations()
        case '2nm':
            searched = input("Name: ")
            print()
            print(df.loc[df['name'] == searched])
            show_available_operations()
        case '2c':
            searched = input("Club name: ")
            print()
            print(df.loc[df['current_club_name'] == searched])
            show_available_operations()
        case '2nt':
            searched = input("Nationality: ")
            print()
            print(df.loc[df['country_of_citizenship'] == searched])
            show_available_operations()
        case '0':
            exit(0)
        case 'L' | 'l':
            show_available_operations()
        case _:
            print("Invalid selection")
