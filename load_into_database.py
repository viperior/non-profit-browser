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
            payload = {
                "form_file_name": form.name,
                "return_s3_doc_id": current_return.return_s3_doc_id,
                "return_version": current_return.get_return_version(),
                "ein": current_return.get_return_filer_ein(),
                "return_filer_name": current_return.get_return_filer_name_full()
            }
            store_form_to_db(payload)

main()
