import json
import psycopg2
import psycopg2.extras

class DatabaseConnection:
    def __init__(self):
        self.config = self.get_config()
        self.host = self.config['database_host']
        self.username = self.config['database_username']
        self.schema = self.config['database_schema']
        self.password = self.config['database_password']
        self.etl_insert_batch_size_limit = self.config['etl_insert_batch_size_limit']
        self.insert_queue = ()

    def add_row_to_insert_queue(self, row_data):
        self.insert_queue += ((row_data), )

        if len(self.insert_queue) > self.etl_insert_batch_size_limit:
            self.process_insert_queue()

    def empty_queue(self):
        self.insert_queue = []

    def execute_sql(self, sql, use_schema=True, data=None):
        try:
            if use_schema:
                connection = self.get_connection_with_schema()
            else:
                connection = self.get_connection_schemaless()

            autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
            connection.set_isolation_level(autocommit)
            cursor = connection.cursor()    
            
            if data == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, data)

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

    def process_insert_queue(self):
        sql = "INSERT INTO form (return_s3_doc_id, return_version, ein,"\
            "return_filer_name, tax_year, total_assets, "\
            "return_header_timestamp, gross_receipts) "\
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        connection = self.get_connection_with_schema()
        autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        connection.set_isolation_level(autocommit)
        cursor = connection.cursor()
        psycopg2.extras.execute_batch(
            cur=cursor,
            sql=sql,
            argslist=self.insert_queue,
            page_size=self.etl_insert_batch_size_limit
        )
        self.empty_queue()

    def select(self, sql):
        connection = self.get_connection_with_schema()
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        
        return records

    def select_top_n_rows(self, table_name, n=100):
        sql = f"SELECT * from {table_name} limit {n};"
        rows = self.select(sql)

        return rows

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
                return_filer_name text NOT NULL,
                tax_year int NOT NULL,
                total_assets bigint,
                return_header_timestamp timestamp,
                gross_receipts bigint
            );
        """
        self.execute_sql(sql)

    def store_row_to_database(self, payload):
        self.add_row_to_insert_queue(payload)

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
