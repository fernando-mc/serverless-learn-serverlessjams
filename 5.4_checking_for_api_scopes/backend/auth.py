from get_token import get_token
from verify_token import verify_token

def handler(event, context):
    print(event)
    print(context)
    token = get_token(event)
    id_token = verify_token(token)
    print(id_token)
    if id_token and id_token.get('permissions'):
        scopes = '|'.join(id_token['permissions'])
        policy = generate_policy(
            id_token['sub'], 
            'Allow', 
            event['methodArn'],
            scopes=scopes
        )
        return policy
    else:
        policy = generate_policy(
            id_token['sub'],
            "Deny",
            event['methodArn']
        )
        return policy

def generate_policy(principal_id, effect, resource, scopes=None):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
    if scopes:
        policy['context'] = {'scopes': scopes}
    return policy
