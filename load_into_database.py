import os
import return_filing

def store_form_to_db(payload):
    print(payload)

def main():
    directory = 'data\\indices'
    file_list = os.scandir(directory)
    
    for index, form in enumerate(file_list):
        if index > 50:
            break
        else:
            current_return = return_filing.ReturnFiling(form.name, form.path)
            print(f"entity_name: {current_return.get_return_filer_name_full()}")
            store_form_to_db(current_return.get_database_payload())

main()
