import return_filing

def main():
    directory = 'data/indices/'
    form_file_name = '201014493492009090_public.xml'
    form_full_path = directory + form_file_name
    single_return = return_filing.ReturnFiling(form_file_name, form_full_path)
    single_return.display_contents()

if __name__ == '__main__':
    main()
