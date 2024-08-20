import boto3
from boto3.dynamodb.conditions import Key
import json

def lambda_handler(event, context):
    """
    This AWS Lambda function is responsible for scheduling a request to a worker
    node. It uses a simple scheduling algorithm: it chooses the node with the
    least CPU usage.

    The function takes in an event containing the request ID, and returns a
    response with a JSON body that contains the request ID and the worker node
    that was chosen.
    """

    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')

    # Get references to the tables we need
    node_metrics_table = dynamodb.Table('node-metrics')
    requests_table = dynamodb.Table('test-table')

    # Get all node metrics
    response = node_metrics_table.scan()
    nodes = response['Items']

    # Simple scheduling algorithm: choose the node with the least CPU usage
    # We use the min() function with a lambda function as the key parameter.
    # This lambda function takes a node as input and returns its CPU usage.
    # The min() function then returns the node with the lowest CPU usage.
    selected_node = min(nodes, key=lambda x: x['cpu'])
    print(f"Selected node: {selected_node['node-id']}")

    # Update the request with the selected worker
    # We use the update_item() method to update the 'worker' field of the
    # request with the ID of the selected node.
    requests_table.update_item(
        Key={'id':  event['requestid']},
        UpdateExpression="set worker = :w",
        ExpressionAttributeValues={':w': selected_node['node-id']}
    )
    
    # Invoke the writeToWorker Lambda function
    # We use the boto3 client to invoke the Lambda function.
    # We pass the request ID as the payload.
    lda = boto3.client('lambda')
    payload = {"requestid" :  event['requestid']}
    invokeLambda_response = lda.invoke(
        FunctionName = 'arn:aws:lambda:eu-central-1:975050134966:function:writeRequestToWorker:concurrency_test',
        InvocationType='Event',
        Payload = json.dumps(payload)
    )

    # Return a response with the request ID and the worker node that was chosen
    return {
        'statusCode': 200,
        'body': f"Request {event['requestid']} scheduled to node {selected_node['node-id']}"
    }
