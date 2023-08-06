

class Replication(object):
    """
    The Replication APIs let you retrieve partner replication status or initiate a replication for a specified replication partner.

    https://apidocs.securitycloud.symantec.com/#/doc?id=replication

    """
    def __init__(self, session):
        super(Replication, self).__init__()
        self._session = session



    def isSiteHasReplicationPartner(self):
        """
        Check whether site has replication partner.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
            'tags':['replication', 'is_replicated'],
            'operation': 'Is Site Has Replication Partner'
        }

        resource = f'/replication/is_replicated'

        return self._session.get(metadata, resource)



    def replicateNow(self, partnerSiteName: str, logs: False, content: False, **kwargs):
        """
        Initiates a replication for the specified replication partner. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        partnerSiteName	query	Replication partner site name.	Yes	string
        logs	query	Replicate Logs	Yes	boolean
        content	query	Replicate Content And Packages.	Yes	boolean
        body	body	Only used internally.	No	Request object details
        """

        metadata = {
            'tags':['replication', 'replicatenow'],
            'operation': 'Replicate Now'
        }

        resource = f'/replication/replicatenow?partnerSiteName={partnerSiteName}&logs={logs}&content={content}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)



    def getReplicationStatus(self):
        """
        Gets replication status.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
            'tags':['replication', 'is_replicated'],
            'operation': 'Get Replication Status'
        }

        resource = f'/replication/status'

        return self._session.get(metadata, resource)
