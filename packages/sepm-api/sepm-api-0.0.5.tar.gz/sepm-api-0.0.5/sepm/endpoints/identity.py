


class Identity(object):
    """
    The Identity APIs lets you manage token authentication.

    https://apidocs.securitycloud.symantec.com/#/doc?id=identity

    """
    def __init__(self, session):
        super(Identity, self).__init__()
        self._session = session



    def authenticate(self, banner: None, appName: None, **kwargs):
        """
        Authenticates and returns an access token for a valid user.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The credentials used to log on to Symantec Endpoint Protection Manager.	Yes	Request object details
        getBanner query	Displays a logon banner, if configured. The possible values are TRUE or FALSE.	No	string
        appName	query	Specify an application name to receive a token unique for that app	No	string
        body	body		No	Request object details

        """
        metadata = {
            'tags':['identity', 'authenticate'],
            'operation': 'Authenticate User'
        }

        queryParam = ''
        if (banner):
            queryParam = f'?getBanner={banner}'
            if(appName):
                queryParam = f'?getBanner={banner}&appName={appName}'

        if (appName):
            queryParam = f'?appName={appName}'

        resource = f'/identity/authenticate{queryParam}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)



    def logout(self, **kwargs):
        """
        Logs off the user that is associated with a specified token.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		No	Request object details

        """
        metadata = {
            'tags':['identity', 'logout'],
            'operation': 'Logout'
        }

        resource = f'/identity/logout'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)
