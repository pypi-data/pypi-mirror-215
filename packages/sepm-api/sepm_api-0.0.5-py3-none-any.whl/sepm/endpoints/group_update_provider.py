


class GroupUpdateProvider(object):
    """
    The Group Update Provider API lets you retrieve a list of group update providers.

    https://apidocs.securitycloud.symantec.com/#/doc?id=gup

    """
    def __init__(self, session):
        super(GroupUpdateProvider, self).__init__()
        self._session = session



    def getGupData(self):
        """
        Gets a list of group update providers.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
            'tags':['gup', 'status'],
            'operation': 'Get GUP Data'
        }

        resource = f'/gup/status'

        return self._session.get(metadata, resource)