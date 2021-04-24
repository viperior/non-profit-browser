import database_connection
import os
import return_filing

def main():
    limit = 5
    directory = 'data\\indices'
    file_list = os.scandir(directory)
    connection = database_connection.DatabaseConnection()

    for index, form_path in enumerate(file_list):
        if index > limit:
            break
        else:
            full_form_path = directory + "\\" + form_path.name
            current_return = return_filing.ReturnFiling(form_path.name, full_form_path)
            connection.insert_single_record(current_return.get_database_payload())

main()
