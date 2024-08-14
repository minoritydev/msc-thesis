import yaml
import boto3
import json
import decimal
# import timeit

def lambda_handler(event, context):
    database = boto3.resource('dynamodb')
    table = database.Table('test-table') 
    req_id = event['requestid']
    # start_time = timeit.default_timer()
    response = table.get_item(
        Key = {
            'id' : req_id
        }
    )
    # elapsed = timeit.default_timer() - start_time
    # print('Time to GET request from DB: ', elapsed)
    # start_time = timeit.default_timer()
    class DecimalEncoder(json.JSONEncoder):
        """
        Helper class to convert a DynamoDB item to JSON.
        """
        def default(self, o):  # pylint: disable=E0202
            if isinstance(o, decimal.Decimal):
                if abs(o) % 1 > 0:
                    return float(o)
                return int(o)
            return super(DecimalEncoder, self).default(o)

    requestJSON = json.dumps(response['Item'], ensure_ascii=False, indent=4, cls=DecimalEncoder)
    requestDict = json.loads(requestJSON)
    # elapsed = timeit.default_timer() - start_time
    # print('Time to convert DynamoDB json to yaml: ', elapsed)
    
    # start_time = timeit.default_timer()
    with open('/mnt/lambda/' + req_id +'.yaml', 'w') as f:
        yaml.dump(requestDict, f)
    # elapsed = timeit.default_timer() - start_time
    # print('Time to write to EFS: ', elapsed)
    return {
        'statusCode': 200,
        'body': json.dumps('Sent request file to worker!')
    }
