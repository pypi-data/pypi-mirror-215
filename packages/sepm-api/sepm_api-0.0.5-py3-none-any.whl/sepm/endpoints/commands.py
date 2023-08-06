

class Commands(object):
    """
    The Commands APIs lets you manage your endpoints.
    Use the Commands APIs to send commands from your Symantec Endpoint Protection Manager to your endpoints.

    A system administrator account is required for this API.

    https://apidocs.securitycloud.symantec.com/#/doc?id=commands

    """
    def __init__(self, session):
        super(Commands, self).__init__()
        self._session = session


    def activeScan(self, group_ids: str, computer_ids: str, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager
        to Symantec Endpoint Protection endpoints to request an active scan on the endpoint.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        body	body	No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'activescan'],
            'operation': 'Active Scan'
        }

        resource = f'/command-queue/activescan?group_ids={group_ids}&computer_ids{computer_ids}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getBaselineCommand(self, group_ids: str, computer_ids: str, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager
        to Symantec Endpoint Protection endpoints to request
        that baseline application information be uploaded back to Symantec Endpoint Protection Manager.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        body	body	No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'baseline'],
            'operation': 'Get Base Line Command'
        }

        resource = f'/command-queue/baseline?group_ids={group_ids}&computer_ids{computer_ids}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def becomeCloudManaged(self, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager
        to Symantec Endpoint Protection endpoints to request
        that those endpoints communicate directly with the cloud instead of Symantec Endpoint Protection Manager.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The target groups or computers to which this command should be applied.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'cloudmanaged'],
            'operation': 'Become Cloud Managed'
        }

        resource = f'/command-queue/cloudmanaged'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def eocCommand(self, group_ids: str, computer_ids: str, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager
        to Symantec Endpoint Protection endpoints to request an "Evidence of Compromise" scan on the endpoint.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        body	body	The target groups or computers to which this command should be applied.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'eoc'],
            'operation': 'EOC Command'
        }

        resource = f'/command-queue/eoc?group_ids={group_ids}&computer_ids{computer_ids}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getBinaryFileContent(self, file_id: str, **kwargs):
        """
        Gets the binary file content for a given file ID.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        file_id	path	The file ID from which to get the binary content.	Yes	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'file', 'file_id', 'content'],
            'operation': 'Get Binary File Contents'
        }

        resource = f'/command-queue/file/{file_id}/content'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def getBinaryFileDetails(self, file_id: str):
        """
        Gets the details of a binary file, such as the checksum and the file size.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        file_id	path	The file ID from which to get the binary content.	Yes	string

        """

        metadata = {
            'tags':['command-queue', 'file', 'file_id', 'details'],
            'operation': 'Get Binary File Details'
        }

        resource = f'/command-queue/file/{file_id}/details'

        return self._session.get(metadata, resource)


    def getFileCommand(self, file_path: str, computer_ids: str, sha256=None, md5=None, sha1=None, source='FILESYSTEM', **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager
        to Symantec Endpoint Protection endpoints to request
        a suspicious file be uploaded back to Symantec Endpoint Protection Manager.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        file_path query	The file path of the suspicious file.	Yes	string
        computer_ids	query	The list of computers on which to search for the suspicious file.	Yes	string
        sha256	query	The SHA256 hash value of the suspicious file.	No	string
        md5	query	The MD5 hash value of the suspicious file.	No	string
        sha1	query	The SHA1 hash value of the suspicious file.	No	string
        source	query	The source to search for the suspicious file. Possible values are: FILESYSTEM (default), QUARANTINE, or BOTH. 12.1.x clients only use FILESYSTEM.	No	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'file', 'file_id', 'content'],
            'operation': 'Get File Command'
        }

        sha256Param = f'&sha256={sha256}' if sha256 is not None else ''
        md5Param = f'&md5={md5}' if md5 is not None else ''
        sha1Param = f'&sha1={sha1}' if sha1 is not None else ''

        resource = f'/command-queue/files?file_path={file_path}&computer_ids={computer_ids}&source={source}{sha256Param}{md5Param}{sha1Param}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def fullScan(self, group_ids: str, computer_ids: str, **kwargs) :
        """
        Sends a command from Symantec Endpoint Protection Manager
        to Symantec Endpoint Protection endpoints to request a full scan on the endpoint.

        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'fullscan'],
            'operation': 'Full Scan'
        }

        resource = f'/command-queue/fullscan?group_ids={group_ids}&computer_ids{computer_ids}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def invalidateIronCacheEntries(self, group_ids: str, computer_ids: str, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager to Symantec Endpoint Protection endpoints to invalidate IRON cache entries on the endpoint.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        body	body	The hashType and hash list to be applied to endpoints.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'ironcache'],
            'operation': 'Invalidate IRON Cache Entries'
        }

        resource = f'/command-queue/ironcache?group_ids={group_ids}&computer_ids{computer_ids}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def applyLicenseOverride(self, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager to Symantec Endpoint Protection endpoints to override the default license policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The hashType and hash list to be applied to endpoints.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'license', 'override'],
            'operation': 'Apply License Override'
        }

        resource = f'/command-queue/license/override'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def resetLicenseOverride(self, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager to Symantec Endpoint Protection endpoints to reset license policy to default instance.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The hashType and hash list to be applied to endpoints.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'license', 'resetoverride'],
            'operation': 'Reset License Override'
        }

        resource = f'/command-queue/license/resetoverride'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def quarantineCommand(self, group_ids: str, computer_ids: str, hardware_ids: str, undo: False, **kwargs):
        """
        Sends a command from Symantec Endpoint Protection Manager to (un)quarantine Symantec Endpoint Protection endpoints.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        undo	query	If set to true, will undo quarantine.	No	boolean
        hardware_ids	query	The list of computer hardware keys	Yes	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'quarantine'],
            'operation': 'Quarantine Command'
        }

        resource = f'/command-queue/quarantine?group_ids={group_ids}&computer_ids={computer_ids}&hardware_ids={hardware_ids}&undo={undo}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def updateContentCommand(self, group_ids: str, computer_ids: str, **kwargs):
        """
        Sends a command from SEPM to SEP endpoints to update content.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_ids query	The list of groups on which to run the command.	Yes	string
        computer_ids query	The list of computers on which to run the command.	Yes	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'updatecontent'],
            'operation': 'Update Content Command'
        }

        resource = f'/command-queue/updatecontent?group_ids={group_ids}&computer_ids={computer_ids}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getCommandStatusDetails(self, command_id: str, pageIndex=1, pageSize=20, sort=None, order=None, **kwargs):
        """
        Gets the details of a command status.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        command_id	path	The command ID for which details are needed.	Yes	string
        pageIndex	query	The index page for returned results. The default page index is 1.	No	integer
        pageSize	query	The number of results to include on each page. The default is 20.	No	integer
        sort	query	The column by which the results are sorted. The default is by command's start time.	No	string
        order	query	Specifies whether the results are in ascending order (ASC) or descending order (DESC).	No	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'command_id'],
            'operation': 'Get Command Status Details'
        }

        sortParam = f'&sort={sort}' if sort is not None else ''
        orderParam = f'&order={order}' if order is not None else ''

        resource = f'/command-queue/{command_id}?pageIndex={pageIndex}&pageSize={pageSize}{sortParam}{orderParam}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)


    def cancelCommand(self, command_id: str, **kwargs):
        """
        Cancels an existing command by creating a new cancel command for clients for which the command is still pending.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        command_id	path	The command ID for which details are needed.	Yes	string
        body	body		No	Request object details

        """

        metadata = {
            'tags':['command-queue', 'command_id', 'cancel'],
            'operation': 'Cancel Command'
        }

        resource = f'/command-queue/{command_id}/cancel'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)




