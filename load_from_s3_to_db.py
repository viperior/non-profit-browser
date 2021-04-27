import boto3
import database_connection
import json
import progressbar
import return_filing

def main():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    limit = config_data['load_limit']
    s3_bucket_name = 'irs-form-990'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket_name)
    connection = database_connection.DatabaseConnection()
    record_insert_count = 0

    with progressbar.ProgressBar(max_value=limit) as bar:
        for index, bucket_object in enumerate(bucket.objects.all()):
            if index + 1 > limit:
                break

            form_file_name = bucket_object.key
            current_return = return_filing.ReturnFiling(form_file_name)
            connection.insert_single_record(current_return.get_database_payload())
            record_insert_count += 1
            bar.update(index)

    print(f"Rows inserted: {record_insert_count}")

if __name__ == '__main__':
    main()
