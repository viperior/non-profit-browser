import database_connection

def main():
    npb_db_connection = database_connection.DatabaseConnection()
    npb_db_connection.setup_database()

main()
