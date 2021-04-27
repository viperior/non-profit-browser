import boto3
import datetime
import json
import progressbar

def process_batch(batch, batch_number):
    output_file_path = f"data/npb-indices/npb_index_{batch_number}.json"

    with open(output_file_path, 'w') as output_file:
        json.dump(batch, output_file)

def main():
    s3_bucket_name = 'irs-form-990'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket_name)
    bucket_object_list = bucket.objects.all()
    object_count_estimate = 4000000
    total_batch_count = 0
    batch_size_limit = 10000
    current_batch_counter = 0
    current_batch = ()

    with progressbar.ProgressBar(max_value=object_count_estimate) as bar:
        for i, item in enumerate(bucket_object_list):
            current_batch += ((item.key, ))
            
            if i <= object_count_estimate:
                bar.update(i)
            else:
                print(f"[INFO] Operation has exceeded {object_count_estimate} "\
                    "items")

            if current_batch_counter >= batch_size_limit:
                total_batch_count += 1
                process_batch(current_batch, total_batch_count)
                current_batch = ()
                current_batch_counter = 0

            current_batch_counter += 1

        total_batch_count += 1
        process_batch(current_batch, total_batch_count)
        print('[INFO] Program complete')

if __name__ == "__main__":
    main()
