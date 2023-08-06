


class ThreatDefenseForActiveDirectory(object):
    """
    The Threat Defense for Active Directory APIs let you manage your TDAD data and policies.

    A system administrator account is required for this API.

    https://apidocs.securitycloud.symantec.com/#/doc?id=computers

    """

    def __init__(self, session):
        super(ThreatDefenseForActiveDirectory, self).__init__()
        self._session = session


    def getPolicy(self, **kwargs):
        """
        Gets all Threat Defense for Active Directory policies.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		                        No	Request object details
        """

        metadata = {
            'tags':['tdad'],
            'operation': 'Get Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad'

        return self._session.get(metadata, resource, payload)


    def postPolicy(self, **kwargs):
        """
        Creates a new TDAD Global.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		                        No	Request object details
        body	body		                        No	Request object details
        """

        metadata = {
            'tags':['tdad'],
            'operation': 'Post Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad'

        return self._session.post(metadata, resource, payload)


    def putPolicy(self, **kwargs):
        """
        Updates an existing Threat Defense for Active Directory policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		                        No	Request object details
        body	body		                        No	Request object details
        """

        metadata = {
            'tags':['tdad'],
            'operation': 'Put Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad'

        return self._session.put(metadata, resource, payload)


    def deletePolicy(self, **kwargs):
        """
        Deletes all Threat Defense for Active Directory data.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		                        No	Request object details
        """

        metadata = {
            'tags':['tdad'],
            'operation': 'Delete Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad'

        return self._session.delete(metadata, resource, payload)


    def patchPolicy(self, **kwargs):
        """
        Updates an existing Threat Defense for Active Directory policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		                        No	Request object details
        body	body		                        No	Request object details
        """

        metadata = {
            'tags':['tdad'],
            'operation': 'Patch Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad'

        return self._session.patch(metadata, resource, payload)


    def getPolicyByADDomainIdAndPolicyId(self, domainId: str, policyId: str, **kwargs):
        """
        Gets a Threat Defense for Active Directory policy
        for the specified Active Directory domain UID and policy UID.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        adDomainUid	path	The Active Directory domain UID.	Yes	string
        policyUid	path	The policy uid for the given AD domain	Yes	string
        body	body		No	Request object details
        """

        metadata = {
          'tags':['tdad'],
          'operation': 'Get Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad/{domainId}/{policyId}'

        return self._session.get(metadata, resource, payload)


    def deletePolicyByADDomainIdAndPolicyId(self, domainId:str, policyId:str, **kwargs):
        """
        Delete a Threat Defense for Active Directory policy
        for the specified Active Directory domain UID and policy UID.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        adDomainUid	path	The Active Directory domain UID.	Yes	string
        policyUid	path	The policy uid for the given AD domain	Yes	string
        body	body		No	Request object details
        """

        metadata = {
          'tags':['tdad'],
          'operation': 'Delete Policy'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/tdad/{domainId}/{policyId}'

        return self._session.delete(metadata, resource, payload)