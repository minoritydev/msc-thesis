import json
import  boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    """
    This function is responsible for authorizing a request.
    """
    decision = 'deny'
   
    token = 'allow'
    namespace = 'mynamespace'
    database = boto3.resource('dynamodb')
    lda = boto3.client('lambda')
    users_table = database.Table('users') 
    rolebindings_table = database.Table('rolebindings')
    roles_table = database.Table('roles')
    
    
    users_response = users_table.get_item(
        Key = {
            'token' : token
        }
    )
    user =  users_response["Item"]['user']
   
    rolebindings_response = rolebindings_table.query(
        IndexName = 'username-index',
        KeyConditionExpression = Key('username').eq(user) ,
        FilterExpression = Key('namespace').eq(namespace)
    )
    
    roles_response = roles_table.get_item(
        Key = {
            'name' : rolebindings_response["Items"][0]["roleRef"]["name"],
            'namespace' : rolebindings_response["Items"][0]["namespace"],
        }
    )
    request = json.loads(event['body'])
    
    request_kind = request['kind'].lower() + 's'
    response = "User {} is not allowed to access resource type '{}'".format(user, request_kind)
    #if request.kind == role.kind then allow
    if request_kind in roles_response["Item"]["rules"][0]["resources"]:
        decision = 'allow'
        response = 'Request submitted!'
    print(decision)
    if decision == 'allow':
        #invoke initiateRequest lambda
        invokeLambda_response = lda.invoke(
            FunctionName = 'initiateRequest',
            InvocationType='Event',
            Payload = json.dumps(event['body'])
        )
   
   # print(event)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
