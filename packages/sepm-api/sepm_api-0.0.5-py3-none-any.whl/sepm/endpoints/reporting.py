

class Reporting(object):
    """
    The Reporting API lets you authenticates and return a PHP session token for a valid user.

    https://apidocs.securitycloud.symantec.com/#/doc?id=reporting

    """

    def __init__(self, session):
        super(Reporting, self).__init__()
        self._session = session


    def authenticateUser(self, **kwargs):
        """
        Authenticates and returns a PHP session token for a valid user.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The credentials used to log on to Symantec Endpoint Protection Manager.	Yes	Request object details
        body	body	Provided by default.	Yes	Request object details

        """

        metadata = {
         'tags':['reporting', 'authenticate'],
         'operation': 'Authenticate User'
        }

        resource = f'/reporting/authenticate'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)