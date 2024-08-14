import json
import boto3
from decimal import Decimal



def lambda_handler(event,context): 
    dynamodb = boto3.resource('dynamodb') 
    lda = boto3.client('lambda') 
    
    data = json.loads(event, parse_float=Decimal)
    data['id'] = context.aws_request_id
    data['worker'] = -1
   
    
    table = dynamodb.Table('test-table') 
    
    response = table.put_item(Item = data) 
   
    payload = {"requestid" : context.aws_request_id}
    invokeLambda_response = lda.invoke(
      
        FunctionName = 'arn:aws:lambda:eu-central-1:975050134966:function:writeSchedulingDecision:concurrency_test',
        InvocationType='Event',
        Payload = json.dumps(payload)
        )
    
    return {
        'statusCode': 200,
        "content-type":"application/json",
        
    }