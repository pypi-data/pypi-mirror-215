

class Administrators(object):
    """
    The Administrators APIs lets you perform the following administrative functions:

        Manage your administrator accounts.
        Access information about your servers and databases.
        Manage your Threat Defense for Active Directory (TDAD) server information.
        Manage your licenses.
        Retrieve the current bearer token.

    https://apidocs.securitycloud.symantec.com/#/doc?id=admin
    """

    def __init__(self, session):
        super(Administrators, self).__init__()
        self._session = session

    def getAllAdminUserDetails(self, domain=None):
        """
        Gets the list of administrators for a particular domain.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domain	query	The domain in which to look for administrators.	No	string
        """

        metadata = {
            'tags':['admin-users',],
            'operation': 'Get All Admin User Details'
        }

        # TODO - check if params parsing required
        #domain = urllib.parse.quote(str(domain), safe='')

        domainParam = f'?domain={domain}' if domain is not None else ''

        resource = f'/admin-users{domainParam}'

        return self._session.get(metadata, resource)


    def createAdminUser(self, domain=None, **kwargs):
        """
        Create a new administrator with the details that are provided.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domain	query	The domain in which to look for administrators.	No	string
        body	body	The information used to create the administrator.	Yes	Request object details
        """

        metadata = {
            'tags':['admin-users', ],
            'operation': 'Create Admin User'
        }

        domain = urllib.parse.quote(str(domain), safe='')

        domainParam = f'?domainId={domain}' if domain is not None else ''

        resource = f'/admin-users{domainParam}'

        # TODO: add valid payload lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getAdminUserDetails(self, id: str, domainId=None):
        """
        Gets the details of a single administrator.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	     path	The administrator's ID.	Yes	string
        domainId query	The domain in which to look for the administrator.	No	string
        body	 body	Only used internally.
        """

        metadata = {
            'tags':['admin-users',],
            'operation': 'Get Admin User Details'
        }

        #domainId = urllib.parse.quote(str(domainId), safe='')

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/admin-users/{id}{domainIdParam}'

        return self._session.get(metadata, resource)


    def updateAdminUser(self, id: str, domainId=None):
        """
        Updates the details for a specified administrator.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	     path	The administrator's ID.	Yes	string
        domainId query	The domain in which to look for the administrator.	No	string
        body	 body	Only used internally.
        """

        metadata = {
            'tags':['admin-users',],
            'operation': 'Update Admin User'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/admin-users/{id}{domainIdParam}'

        return self._session.put(metadata, resource)


    def getLocalDatabase(self):
        """
        Gets the database information of local site.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	 body	Only used internally.
        """

        metadata = {
            'tags':['admin', 'database',],
            'operation': 'Get Local Database'
        }

        resource = f'/admin/database'

        return self._session.get(metadata, resource)


    def getServers(self, **kwargs):
        """
        Gets the list of servers present in SEPM. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	 body	Only used internally.
        """
        metadata = {
            'tags':['admin', 'servers'],
            'operation': 'Get Servers'
        }

        resource = f'/admin/servers'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def getTDADServerDetails(self, **kwargs):
        """
        Retrieve TDAD server information.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	 body	Only used internally.
        """
        metadata = {
            'tags':['administrators', 'admin', 'tdadserver', 'get'],
            'operation': 'Get TDAD Server Details'
        }

        resource = f'/admin/tdadserver'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def updateTDADServerDetails(self, **kwargs):
        """
        Update TDAD server information.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	Object containing TDAD server details.	Yes	Request object details
        body	body		No	Request object details
        """

        metadata = {
            'tags':['administrators', 'admin', 'tdadserver','update'],
            'operation': 'Update TDAD Server Details'
        }

        resource = f'/admin/tdadserver'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def deleteTDADServerDetails(self, **kwargs):
        """
        Delete TDAD server information.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		No	Request object details
        """

        metadata = {
         'tags':['administrators', 'admin', 'tdadserver', 'delete'],
         'operation': 'Delete TDAD Server Details'
        }

        resource = f'/admin/tdadserver'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)


    def getAllLicenses(self):
        """
        Retrieves all license-related information.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
         'tags':['administrators', 'licenses', 'get'],
         'operation': 'Get All Licenses'
        }

        resource = f'/licenses'

        return self._session.get(metadata, resource)


    def addNewLicenses(self, **kwargs):
        """
        Imports a license file into Symantec Endpoint Protection Manager.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The license file to import into Symantec Endpoint Protection Manager.	Yes	Request object details
        body	body	Only used internally.	No
        """

        metadata = {
         'tags':['administrators', 'licenses', 'add'],
         'operation': 'Add New Licenses'
        }

        resource = f'/licenses/add'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getLicensesConfig(self):
        """
        Gets the license configuration. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """

        metadata = {
         'tags':['administrators', 'licenses', 'config'],
         'operation': 'Get License Config'
        }

        resource = f'/licenses/config'

        return self._session.get(metadata, resource)


    def getEntitlements(self, serialNumbers: str, **kwargs):
        """
        Retrieves specified licenses from the licensing server, given a list of serial numbers.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        serialNumbers	query	The serial numbers used to retrieve the licenses.	Yes	array
        body	body	Only used internally.	No	Request object details
        """

        metadata = {
         'tags':['administrators', 'licenses', 'entitlements'],
         'operation': 'Get Entitlements'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/licenses/entitlements?serialNumbers={serialNumbers}'

        return self._session.get(metadata, resource, payload)


    def getSEPMLicenseSummary(self, domainId=None):
        """
        Returns LicenseSummary object, which contains information about license type and expiration state.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainId	query		No	string

        """

        metadata = {
         'tags':['administrators', 'licenses', 'summary'],
         'operation': 'Get Entitlements'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/licenses/summary{domainIdParam}'

        return self._session.get(metadata, resource)


    def getCurrentUserToken(self, **kwargs):
        """
        Gets the current usertoken object

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		No	Request object details

        """

        metadata = {
         'tags':['administrators', 'sessions', 'currentuser'],
         'operation': 'Get Current User Token'
        }

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        resource = f'/sessions/currentuser'

        return self._session.get(metadata, resource, payload)