import boto3
import pandas
from json import dumps

list = []
s3_client = boto3.client(
    's3',
    region_name='us-west-2',
    aws_access_key_id='iam-key',
    aws_secret_access_key='iam-password'
)

def set_correct_values(next_marker):
  global list, s3_client
  if next_marker == '':
    response = s3_client.list_objects(
      Bucket='sigler-sivo',
      Prefix='siglercutsheet/',
      Delimiter='/'
    )
  else:
    response = s3_client.list_objects(
      Bucket='sigler-sivo',
      Prefix='siglercutsheet/',
      Delimiter='/',
      Marker=next_marker
    )
  for object in response['Contents']:
    list.append({
      'name': object['Key'].replace('siglercutsheet/', ''),
      'size': str(object['Size'] / 1024) + ' MB'
    })
  return response['NextMarker']

try:
  next_marker = set_correct_values('')
  while (True):
    next_marker = set_correct_values(next_marker)
except Exception as e:
  print(e)

sigler_cutsheets = pandas.read_json(dumps(list))
