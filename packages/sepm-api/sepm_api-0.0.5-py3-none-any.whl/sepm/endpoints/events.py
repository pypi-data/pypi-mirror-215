


class Events(object):
    """
    The Events APIs let you retrieve information for critical events or acknowledge any event.

    https://apidocs.securitycloud.symantec.com/#/doc?id=sepm_events

    """
    def __init__(self, session):
        super(Events, self).__init__()
        self._session = session


    def postAcknowledgementForNotification(self, eventID: str):
        """
        Acknowledges a specified event for a given event ID.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        eventID	path	The event ID to acknowledge.	Yes	string

        """

        metadata = {
            'tags':['events', 'acknowledge'],
            'operation': 'Post Acknowledgement For Notification'
        }

        resource = f'/events/acknowledge/{eventID}'

        return self._session.post(metadata, resource)


    def getCriticalEventsInfo(self):
        """
        Gets information related to critical events.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
            'tags':['events', 'acknowledge'],
            'operation': 'Get Critical Events Info'
        }

        resource = f'/events/critical'

        return self._session.get(metadata, resource)