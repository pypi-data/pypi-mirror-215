


class Domains(object):
    """
    The Domains APIs let you manage your domains.

    https://apidocs.securitycloud.symantec.com/#/doc?id=domains

    """
    def __init__(self, session):
        super(Domains, self).__init__()
        self._session = session


    def getDomains(self):
        """
        Gets a list of all accessible domains.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
            'tags':['domains'],
            'operation': 'Get Domains'
        }

        resource = f'/domains'

        return self._session.get(metadata, resource)


    def addDomain(self, **kwargs):
        """
        Creates a new domain.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
            'tags':['domains'],
            'operation': 'Add Domains'
        }

        resource = f'/domains'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getDomainName(self, id: str, **kwargs):
        """
        Gets the domain name for the specified domain ID.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	    path		Yes	string
        body	body		No	Request object details
        """
        metadata = {
            'tags':['domains', 'name'],
            'operation': 'Get Domain Name'
        }

        resource = f'/domains/name/{id}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def getDomain(self, id: str, **kwargs):
        """
        Gets the details for a specified domain.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	    path		Yes	string
        body	body		No	Request object details
        """
        metadata = {
            'tags':['domains', 'name'],
            'operation': 'Get Domain'
        }

        resource = f'/domains/{id}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def updateDomainEnabledStatus(self, id: str, action: str):
        """
        Updates the status of a specified domain as enabled or disabled.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path		Yes	string
        action	query		Yes	string
        """
        metadata = {
            'tags':['domains'],
            'operation': 'Update Domain Enabled Status'
        }

        resource = f'/domains/{id}'

        return self._session.post(metadata, resource)


    def updateDomain(self, id: str, **kwargs):
        """
        Updates an existing domain's information.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path		Yes	string
        body	body		No	Request object details
        """
        metadata = {
            'tags':['domains'],
            'operation': 'Update Domain Enabled Status'
        }

        resource = f'/domains/{id}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def deleteDomain(self, id: str, **kwargs):
        """
        Deletes a specified domain.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path		Yes	string
        body	body		No	Request object details
        """
        metadata = {
            'tags':['domains'],
            'operation': 'Delete Domain'
        }

        resource = f'/domains/{id}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)
