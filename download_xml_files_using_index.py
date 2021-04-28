import json
import progressbar
import requests

def main():
    file_count_estimate = 4000000
    file_counter = 0

    with open('data/npb-indices/npb_full_index.json', 'r') as index_file:
        index = json.load(index_file)
    
    with progressbar.ProgressBar(max_value=file_count_estimate) as bar:
        for index_partition in index:
            for doc in index_partition:
                url = f"https://s3.amazonaws.com/irs-form-990/{doc}"
                r = requests.get(url)

                if r.status_code == 200:
                    with open(f"data/npb-xml/{doc}", 'w') as output_file:
                        output_file.write(r.text)
                else:
                    print(f"[ERROR] Error encountered while attempting to "\
                        "download {doc}")

                file_counter += 1

                if file_counter <= file_count_estimate:
                    bar.update(file_counter)
                else:
                    printf(f"[INFO] Estimated file count of "\
                        "{file_count_estimate} exceeded with a final count "\
                        "of: {file_counter}")

if __name__ == '__main__':
    main()
