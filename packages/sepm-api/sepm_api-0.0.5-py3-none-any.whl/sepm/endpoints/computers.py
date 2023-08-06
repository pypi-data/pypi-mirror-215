

class Computers(object):
    """
    The Computers APIs let you manage your computers in a specified domain.

    A system administrator account is required for this API.

    https://apidocs.securitycloud.symantec.com/#/doc?id=computers
    """

    def __init__(self, session):
        super(Computers, self).__init__()
        self._session = session

    def getComputers(self, **kwargs):
        """
        Gets the information about the computers in a specified domain. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        pageIndex		The index page used for returned results. The default page index is 1.	No	integer
        pageSize		The number of results to include on each page. The default is 20.	No	integer
        sort			The column by which the results are sorted. Possible values are COMPUTER_NAME (Default value), COMPUTER_ID, COMPUTER_DOMAIN_NAME, or DOMAIN_ID.	No	string
        order			Specifies whether the results are in ascending order (ASC) or descending order (DESC).	No	string
        lastUpdate		Indicates when a computer last updated its status. The default value of 0 gets all the results.	No	integer
        os				The list of OS to filter. Possible values are CentOs, Debian, Fedora, MacOSX, Oracle, OSX, RedHat, SUSE, Ubuntu, Win10, Win2K, Win7, Win8, Win81, WinEmb7, WinEmb8, WinEmb81, 				WinFundamental, WinNT, Win2K3, Win2K8, Win2K8R2, Win2K12, Win2K12R2, Win2K16, WinVista, WinXP, WinXPEmb, WinXPProf64	No	array
        domain			The domain from which to get computer information.	No	string
        computerName	The host name of computer. Wild card is supported as '*'.	No	string
        mac				The MAC address of computer. Wild card is supported as '*'.	No	string
        computer_id		The computer GUID. When computer_id is used the query will ignore all other query conditions except "domain", "feature" and "verbose" and return the current active one 				record.	No	string
        hardware_key	The computer hardware key. When hardware_key is used and computer_id is empty the query will ignore all other query conditions except "domain", "feature" and "verbose" and 				return the current active one record.	No	string
        feature			List of features to return opstate information in reduced mode.Possible values are av, mem, fw, ips, tdad	No	array
        verbose			Returns a reduced set of computer information if true.	No	boolean
        """

        metadata = {
            'tags':['computers', ],
            'operation': 'Get Computers'
        }

        resource = f'/computers'

        query_params = ['pageIndex', 'pageSize', 'sort', 'order', 'lastUpdate', 'os', 'domain', 'computerName', 'mac', 'computer_id', 'hardware_key', 'feature', 'verbose', ]

        params = {k.strip(): v for k, v in kwargs.items() if k.strip() in query_params}

        return self._session.get(metadata, resource, params)

    def moveClients(self, **kwargs):
        """
        checks and moves a client to the specified group. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	       	Information of a computer.	Yes
        """

        metadata = {
            'tags':['computers',],
            'operation': 'Move Clients'
        }

        resource = f'/computers'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)

    def deleteClients(self, **kwargs):
        """
        Deletes list of existing computers. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	       	Information of a computer.	Yes
        body	                            		No	                      Request object details
        """

        metadata = {
            'tags':['computers', 'delete',],
            'operation': 'Delete Clients'
        }

        resource = f'/computers/delete'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)

    def enrollComputer(self, **kwargs):
        """
        Updates the device ID and encrypted device password for a specified computer.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	    	The device ID and encrypted device password to upload to Symantec Endpoint Protection Manager for enrollment.	Yes
        """

        metadata = {
            'tags':['computers', 'enroll',],
            'operation': 'Enroll'
        }

        resource = f'/computers/enroll'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)

    def getEnrollmentStatus(self, id: str):
        """
        Gets the status of the enrollment job.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id		        The enrollment job for which the status is needed.	Yes	string
        """

        metadata = {
            'tags':['computers', 'enroll', ],
            'operation': 'Enroll'
        }

        id = urllib.parse.quote(str(id), safe='')

        resource = f'/computers/enroll/{id}'

        return self._session.get(metadata, resource)

    def deleteComputer(self, id: str, **kwargs):
        """
        Deletes an existing computer. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	        	The ID of the computer to delete.	Yes	string
        body			                            No	                      Request object details
        """

        metadata = {
            'tags':['computers',],
            'operation': 'Delete Computer'
        }

        id = urllib.parse.quote(str(id), safe='')

        resource = f'/computers/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)
