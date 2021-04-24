import json
import psycopg2

class DatabaseConnection:
    def __init__(self):
        self.config = self.get_config()
        self.host = self.config['database_host']
        self.username = self.config['database_username']
        self.schema = self.config['database_schema']
        self.password = self.config['database_password']

    def execute_sql(self, sql, use_schema=True):
        try:
            if use_schema:
                connection = self.get_connection_with_schema()
            else:
                connection = self.get_connection_schemaless()

            autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
            connection.set_isolation_level(autocommit)
            cursor = connection.cursor()    
            cursor.execute(sql)
            connection.commit()
            cursor.close()
        except SyntaxError as ex:
            print('[ERROR] Syntax error occurred while attempting to execute '\
                'sql statement')
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        except Exception as ex:
            print(
                'Error occurred while attempting to connect to database host: ',
                self.host
            )
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        finally:
            connection.close()

    def get_connection_schemaless(self):
        connection = psycopg2.connect(
            host = self.host,
            user = self.username,
            password = self.password
        )
        return connection

    def get_connection_with_schema(self):
        connection = psycopg2.connect(
            host = self.host,
            dbname = self.schema,
            user = self.username,
            password = self.password
        )
        return connection

    def get_config(self):
        with open('config.json', 'r') as input_file:
            config_data = json.load(input_file)

        return config_data

    def insert_single_record(self, payload):
        keys = [
            'return_s3_doc_id',
            'return_version',
            'ein',
            'return_filer_name'
        ]
        sql = 'INSERT INTO form ('

        for i, key in enumerate(keys):
            sql += key

            if i < len(keys) - 1:
                sql += ','

        sql += ") VALUES ("
        sql += str(payload['return_s3_doc_id']) + ','
        sql += "'" + payload['return_version'] + "',"
        sql += str(payload['ein']) + ','
        sql += "'" + payload['return_filer_name'] + "'"
        sql += ");"
        self.execute_sql(sql)

    def setup_database(self):
        self.uninstall_database()
        self.setup_database_schema()
        self.setup_database_tables()
        print('[SUCCESS] Non-Profit Browser database installation complete!')

    def setup_database_schema(self):
        self.execute_sql(
            sql = f"CREATE DATABASE {self.schema};",
            use_schema = False
        )

    def setup_database_tables(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS form (
                form_id bigserial PRIMARY KEY,
                return_s3_doc_id bigint NOT NULL,
                return_version text NOT NULL,
                ein bigint NOT NULL,
                return_filer_name text NOT NULL
            );
        """
        self.execute_sql(sql)

    def uninstall_database(self):
        self.uninstall_table_form()
        self.uninstall_database_schema()

    def uninstall_database_schema(self):
        self.execute_sql(
            sql = f"DROP DATABASE IF EXISTS {self.schema};",
            use_schema = False
        )

    def uninstall_table_form(self):
        self.execute_sql(f"DROP TABLE IF EXISTS form;")
