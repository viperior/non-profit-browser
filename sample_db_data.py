import database_connection

def main():
    connection = database_connection.DatabaseConnection()
    sample_data = connection.select_top_n_rows(table_name='form', n=3)

    for row in sample_data:
        print(row)

if __name__ == '__main__':
    main()
