

class Notifications(object):
    """
    The Notifications API lets you post an external notification.

    https://apidocs.securitycloud.symantec.com/#/doc?id=notifications

    """
    def __init__(self, session):
        super(Notifications, self).__init__()
        self._session = session


    def postExternalNotification(self, **kwargs):
        """
        Posts an External Notification.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The external Notification to be added.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
            'tags':['events', 'notifications'],
            'operation': '	Post External Notification'
        }

        resource = f'/events/notifications'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)