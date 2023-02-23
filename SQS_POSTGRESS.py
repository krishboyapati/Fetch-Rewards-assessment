from datetime import date
import hashlib
import json
import boto3
import psycopg2

def connect_to_sqs(region_name, aws_access_key_id, aws_secret_access_key, endpoint_url):
    """
    Connects to an Amazon Simple Queue Service (SQS) queue.

    Args:
    - region_name (str): The name of the region where the queue is located.
    - aws_access_key_id (str): The AWS access key ID for the user's account.
    - aws_secret_access_key (str): The AWS secret access key for the user's account.
    - endpoint_url (str): The endpoint URL for the queue.

    Returns:
    - sqs_client (boto3.client): The SQS client object used to interact with the queue.

    """
    sqs_client = boto3.client(
        'sqs',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
    )

    return sqs_client


def retrieve_message_from_queue(sqs_client, queue_url):
    """
    Retrieves messages from an SQS queue.

    Args:
    - sqs_client (boto3.client): The SQS client object used to interact with the queue.
    - queue_url (str): The URL of the queue from which messages will be retrieved.

    Returns:
    - queue_messages (list): A list of messages retrieved from the queue.

    """
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=10,
        MessageAttributeNames=['All'],
        VisibilityTimeout=10,
        WaitTimeSeconds=4,
    )
    response_message = response['Messages']

    queue_messages = []
    for message in response_message:
        queue_messages.append(message['Body'])

    return queue_messages


def connect_to_postgresdb(user, host, port, password, database):
    """
    Connects to a PostgreSQL database.

    Args:
    - user (str): The name of the user used to connect to the database.
    - host (str): The hostname of the database server.
    - port (str): The port number used to connect to the database.
    - password (str): The password used to authenticate the user.
    - database (str): The name of the database to which to connect.

    Returns:
    - connection (psycopg2.extensions.connection): A connection object representing the database connection.

    """
    connection = psycopg2.connect(database=database, host=host, user=user, password=password, port=port)
    return connection


def insert_data_into_table(records_content, cursor):
    """
    Inserts records into a PostgreSQL database table.

    Args:
    - records_content (list): A list of records to be inserted into the table.
    - cursor (psycopg2.extensions.cursor): A cursor object used to execute SQL commands.

    """
    insert_records = []

    for record in records_content:
        record = json.loads(record)
        
        try:
            user_id = record['user_id']
            device_type = record['device_type']
            ip = record['ip']
            masked_ip = mask(ip)
            device_id = record['device_id']
            masked_device_id = mask(device_id)
            locale = record['locale']
            app_version = record["app_version"].split(".")[0]

            record_data = [device_type, masked_ip, masked_device_id, locale, app_version]
            insert_records.append(record_data)
            insert_into_table(user_id, cursor, record_data)
        except Exception as e:
            print(e)
            print("exception while processing the record")
            print(record)
            pass


def mask(value):
    """
    Hashes the given value using SHA-256 and returns the hashed value.
    
    Args:
        value (str): The value to be hashed.
    
    Returns:
        str: The hashed value.
    """
    hashed_value = hashlib.sha256(value.encode()).hexdigest()
    return hashed_value


def insert_into_table(new_user_id, cursor, data_record):
    """
    Inserts or updates a row in the `public.user_logins` table based on the given parameters.
    
    If a row with the specified `new_user_id` already exists in the table, the function updates the 
    existing row with the `data_record` values. Otherwise, it inserts a new row with the `new_user_id`
    and `data_record` values.
    
    Args:
        new_user_id (str): The ID of the user to be inserted or updated.
        cursor (cursor): The database cursor object.
        data_record (list): A list containing the device type, masked IP address, masked device ID,
            locale, and app version of the user.
    """
    cursor.execute("SELECT user_id FROM public.user_logins WHERE user_id = %s", [new_user_id])
    existing_user_ids = cursor.fetchall()

    if not existing_user_ids:
        # If the user ID doesn't already exist, insert a new row
        insert_stmt = "INSERT INTO public.user_logins(user_id,device_type, masked_ip, masked_device_id, locale, app_version, create_date) values (%s, %s, %s, %s, %s, %s, %s)"
        create_date = date.today()
        new_data_record = [new_user_id] + data_record + [create_date]
        cursor.execute(insert_stmt, new_data_record)
        print(f"New row with user ID {new_user_id} inserted.")
    else:
        # If the user ID already exists, update the existing row
        update_stmt = """UPDATE public.user_logins SET
                device_type = %s,
                masked_ip = %s,
                masked_device_id = %s,
                locale = %s,
                app_version = %s
                WHERE user_id = %s"""

        new_data_record = data_record + [new_user_id]
        cursor.execute(update_stmt, new_data_record)
        print(f"User ID {new_user_id} updated.")


def main():
    """
    Retrieves messages from an SQS queue and inserts them into a Postgres database table.
    """
    # Connect to the SQS queue
    sqs_client = connect_to_sqs(
        region_name='us-east-1',
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint_url='http://localhost:4566',
    )
    queue_messages = retrieve_message_from_queue(sqs_client, queue_url='http://localhost:4566/000000000000/login-queue')

    # Connect to the Postgres database
    connection = connect_to_postgresdb(
        user='postgres', host='localhost', port=7777, password='postgres', database="postgres"
    )
    cursor = connection.cursor()

    # Insert the queue messages into the database table
    insert_data_into_table(queue_messages, cursor)

    # Close the database connection
    cursor.close()
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()

