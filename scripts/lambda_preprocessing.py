import json
import re


def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        cleaned_data = preprocess_data(data)
        if cleaned_data:
            # Send cleaned data to another Kinesis Stream or store in S3
            pass
    return 'Processed'

def preprocess_data(data):
    sensor_id_pattern = re.compile(r'^[0-9]+$')
    if not sensor_id_pattern.match(str(data.get('sensor_id', ''))):
        return None
    return data
