import json
import time
import random
import boto3

kinesis_client = boto3.client('kinesis', region_name='YOUR_REGION')

def generate_sensor_data():
    sensor_data = {
        'sensor_id': random.randint(1, 100),
        'timestamp': int(time.time() * 1000),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 70.0), 2),
        'pressure': round(random.uniform(1.0, 1.5), 2)
    }
    return sensor_data

while True:
    data = generate_sensor_data()
    kinesis_client.put_record(
        StreamName='YOUR_KINESIS_STREAM_NAME',
        Data=json.dumps(data),
        PartitionKey=str(data['sensor_id'])
    )
    print(f"Sent data: {data}")
    time.sleep(1)
