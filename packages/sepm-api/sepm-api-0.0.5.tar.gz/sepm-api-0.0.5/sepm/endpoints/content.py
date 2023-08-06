


class Content(object):
    """
    The Content API lets you retrieve the latest revision information for antivirus definitions from Symantec Security Response.

    https://apidocs.securitycloud.symantec.com/#/doc?id=content

    """
    def __init__(self, session):
        super(Content, self).__init__()
        self._session = session

    def getAVDefLatestInfo(self):
        """
        Gets the latest revision information for antivirus definitions from Symantec Security Response.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
            'tags':['content', 'avdef', 'latest'],
            'operation': 'Get AV Def Latest Info'
        }

        resource = f'/content/avdef/latest'

        return self._session.get(metadata, resource)
