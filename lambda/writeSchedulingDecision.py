import boto3
from boto3.dynamodb.conditions import Key
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    node_metrics_table = dynamodb.Table('node-metrics')
    requests_table = dynamodb.Table('test-table')

    # Get all node metrics
    response = node_metrics_table.scan()
    nodes = response['Items']
  
    # Simple scheduling algorithm: choose the node with the least CPU usage
    selected_node = min(nodes, key=lambda x: x['cpu'])

    # Update the request with the selected worker
    requests_table.update_item(
        Key={'id':  event['requestid']},
        UpdateExpression="set worker = :w",
        ExpressionAttributeValues={':w': selected_node['node-id']}
    )
    print(selected_node)
    
    #invoke writeToWorker lambda
    lda = boto3.client('lambda')
    payload = {"requestid" :  event['requestid']}
    invokeLambda_response = lda.invoke(
        FunctionName = 'arn:aws:lambda:eu-central-1:975050134966:function:writeRequestToWorker:concurrency_test',
        InvocationType='Event',
        Payload = json.dumps(payload)
    )
    return {
        'statusCode': 200,
        'body': f"Request {event['requestid']} scheduled to node {selected_node['node-id']}"
    }