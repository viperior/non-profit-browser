import database_connection
import json
import os
import return_filing

def main():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    limit = config_data['load_limit']
    directory = config_data['local_xml_storage_directory']
    file_list = os.scandir(directory)
    connection = database_connection.DatabaseConnection()
    record_insert_count = 0

    for index, form_path in enumerate(file_list):
        if index > limit:
            break
        else:
            full_form_path = directory + "\\" + form_path.name
            current_return = return_filing.ReturnFiling(form_path.name, full_form_path)
            connection.insert_single_record(current_return.get_database_payload())
            record_insert_count += 1

    print(f"Rows inserted: {record_insert_count}")

if __name__ == '__main__':
    main()
