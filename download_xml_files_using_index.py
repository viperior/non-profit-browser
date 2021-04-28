import json
import multiprocessing
import requests

def process_index_partition(index_partition):
    for doc in index_partition:
        url = f"https://s3.amazonaws.com/irs-form-990/{doc}"
        r = requests.get(url)

        if r.status_code == 200:
            with open(f"data/npb-xml/{doc}", 'w') as output_file:
                output_file.write(r.text)
        else:
            print(f"[ERROR] Error encountered while attempting to "\
                "download {doc}")

def main():
    with open('data/npb-indices/npb_full_index.json', 'r') as index_file:
        index = json.load(index_file)
    
    with multiprocessing.Pool() as pool:
        pool.map(process_index_partition, index)

if __name__ == '__main__':
    main()
