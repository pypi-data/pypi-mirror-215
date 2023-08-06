

class Version(object):
    """
    The Version API lets you retrieve the current version of your Symantec Endpoint Protection Manager.

    https://apidocs.securitycloud.symantec.com/#/doc?id=version

    """

    def __init__(self, session):
        super(Version, self).__init__()
        self._session = session


    def getVersion(self):
        """
        Gets the current version of Symantec Endpoint Protection Manager.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
            'tags':['version'],
            'operation': 'Get Version'
        }

        resource = f'/version'

        return self._session.get(metadata, resource)
