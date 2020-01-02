def get_token(event):
    # whole_auth_token should look like:
    # "Bearer SOME_CODE_GIBBERISH6r712fyasd.othergibberish.finalgibberish"
    whole_auth_token = event.get('authorizationToken')
    print('Client token: ' + whole_auth_token)
    print('Method ARN: ' + event['methodArn'])
    if not whole_auth_token:
        raise Exception('Unauthorized')
    token_parts = whole_auth_token.split(' ')
    auth_token = token_parts[1]
    token_method = token_parts[0]
    if not (token_method.lower() == 'bearer' and auth_token):
        print("Failing due to invalid token_method or missing auth_token")
        raise Exception('Unauthorized')
    # At this point we've confirmed the token format looks ok
    # So return the unverified token
    return auth_token
