import json
import boto3
from decimal import Decimal



def lambda_handler(event,context): 
    # First, we connect to the DynamoDB service
    dynamodb = boto3.resource('dynamodb') 
    # We also connect to the lambda service so that we can invoke the lambda
    # writeSchedulingDecision:concurrency_test
    lda = boto3.client('lambda') 
    
    # The event is a JSON string that we parse into a python dictionary
    # We use the Decimal type to avoid losing precision
    data = json.loads(event, parse_float=Decimal)
    # We add two fields to the data dictionary: id and worker
    # id is the AWS request ID, which we use to identify the request
    # worker is set to -1, which means that the request hasn't been scheduled
    # to a worker yet
    data['id'] = context.aws_request_id
    data['worker'] = -1
   
    # We get the table 'test-table' i.e the table where requests are stored, from the DynamoDB database
    table = dynamodb.Table('test-table') 
    
    # We write the data to the DynamoDB table
    response = table.put_item(Item = data) 
   
    # We create a payload to pass to the writeSchedulingDecision lambda
    # We pass the AWS request ID as the requestid
    payload = {"requestid" : context.aws_request_id}
    # We invoke the writeSchedulingDecision lambda in an event-driven manner
    # This means that we don't wait for the result of the lambda, but instead
    # return immediately after invoking the lambda
    invokeLambda_response = lda.invoke(
      
        FunctionName = 'arn:aws:lambda:eu-central-1:975050134966:function:writeSchedulingDecision:concurrency_test',
        InvocationType='Event',
        Payload = json.dumps(payload)
        )
    
    # We return a response to the caller
    # The response is a JSON object with a status code and content type
    return {
        'statusCode': 200,
        "content-type":"application/json",
        
    }
