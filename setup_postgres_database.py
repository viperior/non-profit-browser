import json
import psycopg2

def main():
    try:
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)

        connection = psycopg2.connect(
            host = config_data['postgres_host'],
            user = config_data['postgres_username'],
            password = config_data['postgres_password']
        )

        autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        connection.set_isolation_level(autocommit)
        cursor = connection.cursor()    
        sql = """CREATE DATABASE npb;"""
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as ex:
        print('Error occurred while attempting to connect to postgres database.')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

main()
