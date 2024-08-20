import json


def lambda_handler(event, context):
    """
    This is an AWS Lambda function that is used to handle authorization for
    an AWS API Gateway. The function takes in an event which contains the
    authorization token sent by the client, and the route ARN of the API
    Gateway.

    The function returns an object that contains the following:
    - principalId: The principal user identification associated with the token
        sent by the client.
    - policyDocument: A policy document that describes the permissions that
        the principal has on the API.
    - context: A dictionary of key-value pairs that are passed to the API
        Gateway.

    The function checks if the authorization token is valid, and if so,
    updates the policy document to allow the principal to invoke the API.
    """

    response = {
        # The principal user identification associated with the token sent by
        # the client.
        "principalId": "abcdef",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": "Deny",
                "Resource": event["routeArn"]
            }]
        },
        "context": {
            "stringKey": "value",
            "numberKey": 1,
            "booleanKey": True,
            "arrayKey": ["value1", "value2"],
            "mapKey": {"value1": "value2"}
        }
    }

    try:
        if (event["headers"]["authorization"] == "allow"):
            response = {
                # The principal user identification associated with the token
                # sent by the client.
                "principalId": "abcdef",
                "policyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event["routeArn"]
                    }]
                },
                "context": {
                    "stringKey": "value",
                    "numberKey": 1,
                    "booleanKey": True,
                    "arrayKey": ["value1", "value2"],
                    "mapKey": {"value1": "value2"}
                }
            }
            print('allowed')
            return response
        else:
            print('denied')
            return response
    except BaseException:
        print('denied')
        return response
