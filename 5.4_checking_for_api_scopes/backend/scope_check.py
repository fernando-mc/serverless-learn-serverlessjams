
def scope_check(event, required_scopes=None):
    print(event)
    if not required_scopes:
        raise Exception('No expected scopes specified')
    if not event['requestContext']['authorizer']['scopes']:
        raise Exception('No scopes provided')
    provided_scopes = event['requestContext']['authorizer']['scopes'] 
    if isinstance(required_scopes, str):
        # There is only one required_scopes scope to check
        if required_scopes in provided_scopes:
            print('Scope check passed for: ' + required_scopes)
        else: 
            raise Exception('Scope check failed for: ' + required_scopes)
    if isinstance(required_scopes, list):
        # There are one or more scopes to check in an array
        # If there is more than one provided scope it should 
        # be separated with a pipe character.
        provided_scopes = provided_scopes.split('|')
        if set(required_scopes).issubset(provided_scopes):
            # If the required scopes are all included in the provided scopes
            print('Scope check passed for: ' + required_scopes)
        else:
            raise Exception('Scope check failed for: ' + required_scopes)

