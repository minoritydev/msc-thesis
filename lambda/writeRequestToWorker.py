import yaml
import boto3
import json
import decimal
# import timeit

def lambda_handler(event, context):
    # Initialize connection to DynamoDB
    database = boto3.resource('dynamodb')
    # Get reference to DynamoDB table 'test-table'
    table = database.Table('test-table') 
    # Get request ID from event
    req_id = event['requestid']
    
    # Get item from DynamoDB table with key 'id' = req_id
    response = table.get_item(
        Key = {
            'id' : req_id
        }
    )
    
    # Define a helper class to convert a DynamoDB item to JSON
    # This is necessary because DynamoDB stores decimal numbers as Decimal objects
    class DecimalEncoder(json.JSONEncoder):
        """
        Helper class to convert a DynamoDB item to JSON.
        """
        def default(self, o):  # pylint: disable=E0202
            if isinstance(o, decimal.Decimal):
                # If the Decimal object is not an integer, convert it to a float
                if abs(o) % 1 > 0:
                    return float(o)
                # Otherwise, convert it to an integer
                return int(o)
            # If the object is not a Decimal, use the default JSON serializer
            return super(DecimalEncoder, self).default(o)

    # Convert the DynamoDB item to JSON using the helper class
    requestJSON = json.dumps(response['Item'], ensure_ascii=False, indent=4, cls=DecimalEncoder)
    # Convert the JSON to a Python dictionary
    requestDict = json.loads(requestJSON)
    
    # Write the Python dictionary to a YAML file in the /mnt/lambda directory
    with open('/mnt/lambda/' + req_id +'.yaml', 'w') as f:
        yaml.dump(requestDict, f)
    
    # Return a success response with a JSON body
    return {
        'statusCode': 200,
        'body': json.dumps('Sent request file to worker!')
    }
