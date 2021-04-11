import json
import psycopg2

def main():
    try:
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)

        connection = psycopg2.connect(
            host = config_data['postgres_host'],
            database = config_data['postgres_database'],
            user = config_data['postgres_username'],
            password = config_data['postgres_password']
        )

        cursor = connection.cursor()    
        sql = """
            CREATE TABLE IF NOT EXISTS form (
                form_id bigserial PRIMARY KEY,
                irs_form_id bigint NOT NULL,
                return_version text NOT NULL,
                entity_name text NOT NULL
            );
        """
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
