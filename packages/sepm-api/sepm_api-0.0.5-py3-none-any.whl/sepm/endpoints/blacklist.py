


class Blacklist(object):
    """
    The Blacklist APIs let you manage your blacklist definitions.

    https://apidocs.securitycloud.symantec.com/#/doc?id=blacklist

    """
    def __init__(self, session):
        super(Blacklist, self).__init__()
        self._session = session


    def getFileFingerPrintListByName(self, name:str, domainId=None,  **kwargs):
        """
        Gets the file fingerprint list for a specified Name as a set of hash values. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        name	query	The Name of the file fingerprint list.	Yes	string
        domainId query	The domain for the file fingerprint list.	No	string
        body	body	Only used internally.	No	Request object details

        """
        metadata = {
            'tags':['blacklist', 'policy-objects', 'fingerprints'],
            'operation': 'Get File Finger Print List By Name'
        }

        domainIdParam = f'&domainId={domainId}' if domainId is not None else ''

        resource = f'/policy-objects/fingerprints?name={name}{domainIdParam}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def addBlackList(self, **kwargs):
        """
        Adds a blacklist as a file fingerprint list to Symantec Endpoint Protection Manager. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The blacklist to be added.	Yes	Request object details

        """
        metadata = {
            'tags':['blacklist', 'policy-objects', 'fingerprints'],
            'operation': 'Add Black List'
        }

        resource = f'/policy-objects/fingerprints'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getFileFingerPrintList(self, id:str, **kwargs):
        """
        Gets the file fingerprint list for a specified ID as a set of hash values. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the file fingerprint list.	Yes	string
        body	body	Only used internally.	No	Request object details

        """
        metadata = {
            'tags':['blacklist', 'policy-objects', 'fingerprints'],
            'operation': 'Get File Finger Print List'
        }

        resource = f'/policy-objects/fingerprints/{id}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def updateBlackList(self, id: str, **kwargs):
        """
        Updates an existing blacklist. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the file fingerprint list to update.	Yes	string
        body	body	The fingerprint list to update.	Yes	Request object details

        """
        metadata = {
            'tags':['blacklist', 'policy-objects', 'fingerprints'],
            'operation': 'Update BlackList'
        }

        resource = f'/policy-objects/fingerprints/{id}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def deleteBlackList(self, id: str):
        """
        Deletes an existing blacklist, and removes it from a group to which it applies. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the file fingerprint list to delete.	Yes	string

        """
        metadata = {
            'tags':['blacklist', 'policy-objects', 'fingerprints'],
            'operation': 'Delete BlackList'
        }

        resource = f'/policy-objects/fingerprints/{id}'

        return self._session.delete(metadata, resource)