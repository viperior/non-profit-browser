import glob
import json

def main():
    file_list = glob.glob('data/npb-indices/npb_index_[0-9]*.json')
    full_index = ()

    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    for item in file_list:
        with open(item, 'r') as index_file:
            full_index_json = json.load(index_file)
        
        full_index += ((tuple(full_index_json), ))

    with open('data/npb-indices/npb_full_index.json', 'w') as output_file:
        json.dump(full_index, output_file)

if __name__ == '__main__':
    main()
