class DatabaseConnection:
    def __init__(self):
        self.config = get_config()
        self.host = self.config['database_host']
        self.username = self.config['database_username']
        self.schema = self.config['database_schema']
        self.password = self.config['database_password']

    def execute_sql(sql):
        try:
            connection = psycopg2.connect(
                host = self.host,
                user = self.username,
                password = self.password
            )

            autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
            connection.set_isolation_level(autocommit)
            cursor = connection.cursor()    
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as ex:
            print('Error occurred while attempting to connect to database host: ', self.host)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def get_config():
        with open('config.json', 'r') as input_file:
            config_data = json.load(input_file)

        return config_data

    def setup_database():
        setup_database_schema()
        setup_database_tables()

    def setup_database_schema()
        execute_sql(f"CREATE DATABASE {self.schema};")

    def setup_database_tables():
        sql = """
            CREATE TABLE IF NOT EXISTS form (
                form_id bigserial PRIMARY KEY,
                return_s3_doc_id bigint NOT NULL,
                return_version text NOT NULL,
                ein bigint NOT NULL,
                return_filer_name text NOT NULL
            );
        """
        execute_sql(sql)
