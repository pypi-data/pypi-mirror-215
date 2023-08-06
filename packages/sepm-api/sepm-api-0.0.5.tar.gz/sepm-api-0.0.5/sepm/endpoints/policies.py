


class Policies(object):
    """
    The Policies APIs let you create, delete, modify any of your Symantec Endpoint Protection policies.
    You can also retrieve your policy payloads or settings.

    https://apidocs.securitycloud.symantec.com/#/doc?id=policies

    """
    def __init__(self, session):
        super(Policies, self).__init__()
        self._session = session


    def createExceptionsPolicy(self, **kwargs):
        """
        Creates a new exceptions policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Create Exceptions Policy'
        }

        resource = f'/policies/exceptions'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getExceptionsPolicy(self, id: str):
        """
        Get the exceptions policy for specified policy id.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	The ID of the exceptions policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Get Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'

        return self._session.get(metadata, resource)


    def editExceptionsPolicy(self, id: str, **kwargs):
        """
        Modify existing policy values with PUT request.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be modified.	Yes	Request object details
        id	    path	The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Edit Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def deleteExceptionsPolicy(self, id: str):
        """
        Deletes an existing Exceptions policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	    path	The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Delete Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'

        return self._session.delete(metadata, resource)



    def updateExceptionsPolicy(self, id: str, **kwargs):
        """
        Update existing policy values with PUT request.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be modified.	Yes	Request object details
        id	    path	The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Update Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)


    def getFirewallPolicy(self, id: str):
        """
        Get the firewall policy for specified policy id.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	    path	The ID of the firewall policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Get Firewall Policy'
        }

        resource = f'/policies/firewall/{id}'

        return self._session.get(metadata, resource)


    def deleteFirewallPolicy(self, id: str):
        """
        Deletes an existing Firewall policy
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	    path	The ID of the firewall policy to delete.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Delete Firewall Policy'
        }

        resource = f'/policies/firewall/{id}'

        return self._session.delete(metadata, resource)


    def createHIDPolicy(self, **kwargs):
        """
        Creates a new High Intensity Detection policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'hid'],
            'operation': 'Create HID Policy'
        }

        resource = f'/policies/hid'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getHIDPolicy(self, id: str):
        """
        Get Hid Policy payload for specified policy id
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	The ID of the HID policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'hid'],
            'operation': 'Get HID Policy'
        }

        resource = f'/policies/hid/{id}'

        return self._session.get(metadata, resource)


    def editHIDPolicy(self, id: str, **kwargs):
        """
        Modify existing policy values.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        id	    path	The ID of the HID policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'hid'],
            'operation': 'Edit HID Policy'
        }

        resource = f'/policies/hid/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def deleteHIDPolicy(self, id: str):
        """
        Delete HID policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	    path	The ID of the HID policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'hid'],
            'operation': 'Delete HID Policy'
        }

        resource = f'/policies/hid/{id}'

        return self._session.delete(metadata, resource)


    def updateHIDPolicy(self, id: str, **kwargs):
        """
        Update HID policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        id	    path	The ID of the HID policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'hid'],
            'operation': 'Update HID Policy'
        }

        resource = f'/policies/hid/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)


    def getIPSPolicy(self, id: str):
        """
        Get IPS Policy payload for specified policy id
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	The ID of the HID policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'ips'],
            'operation': 'Get IPS Policy'
        }

        resource = f'/policies/ips/{id}'

        return self._session.get(metadata, resource)


    def createLicensingPolicy(self, **kwargs):
        """
        Creates a new SAEP licensing setting.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body		                        No	Request object details
        body	body		                        No	Request object details
        """

        metadata = {
            'tags':['policies', 'licensing'],
            'operation': 'Create Licensing Policy'
        }

        resource = f'/policies/licensing'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getLiveUpdatePolicy(self, id: str):
        """
        Creates a new SAEP licensing setting.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	The ID of the LiveUpdate settings policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'licensing'],
            'operation': 'Get Live Update Policy'
        }

        resource = f'/policies/lu/{id}'

        return self._session.get(metadata, resource)


    def createMEMPolicy(self, **kwargs):
        """
        Creates a new Memory Exploit Mitigation policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'mem'],
            'operation': 'Create MEM Policy'
        }

        resource = f'/policies/mem'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getMEMPolicy(self, id: str):
        """
        Get Mem Policy payload for specified policy id.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	The ID of the MEM policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'mem'],
            'operation': 'Get MEM Policy'
        }

        resource = f'/policies/mem/{id}'

        return self._session.get(metadata, resource)


    def editMEMPolicy(self, id: str, **kwargs):
        """
        Modify existing policy values
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body body	    The Memory Exploit Mitigation policy to be modified.	Yes	Request object details
        id	path	    The ID of the MEM policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'mem'],
            'operation': 'Edit MEM Policy'
        }

        resource = f'/policies/mem/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def deleteMEMPolicy(self, id: str):
        """
        Delete existing policy values
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the MEM policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'mem'],
            'operation': 'Delete MEM Policy'
        }

        resource = f'/policies/mem/{id}'

        return self._session.delete(metadata, resource)


    def updateMEMPolicy(self, id: str, **kwargs):
        """
        Update policy patch.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body body	    The Memory Exploit Mitigation policy to be modified.	Yes	Request object details
        id	path	    The ID of the MEM policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'mem'],
            'operation': 'Update MEM Policy'
        }

        resource = f'/policies/mem/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)


    def getPolicyXML(self, policy_type: str, id: str):
        """
        Get Policy XML for specified policy id.
        A system administrator account is required for this REST API.

        parameter           description                 required                  type
        ---------           -----------                 --------                  ----
        id	path	        The ID of the policy to get.	Yes	string
        policy_type	path	The type of the policy to get.	Yes	string
        """

        metadata = {
            'tags':['policies', 'raw'],
            'operation': 'Get XML Policy'
        }

        resource = f'/policies/raw/{policy_type}/{id}'

        return self._session.get(metadata, resource)


    def getPolicySummary(self, domainId=None):
        """
        Get the policy summary for specified policy type.
        A system administrator account is required for this REST API.

        parameter           description                 required                  type
        ---------           -----------                 --------                  ----
        domainId	query	If present, get policies from this domain.
                            Else get policies from logged in domain.	No	string

        """

        metadata = {
            'tags':['policies', 'summary'],
            'operation': 'Get Policy Summary'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/policies/summary{domainIdParam}'

        return self._session.get(metadata, resource)


    def getPolicySummaryWithType(self, policy_type:str, domainIdParam=None):
        """
        Get the policy summary for specified policy type.
        Also gets the list of groups to which the policies are assigned.

        parameter           description                 required                  type
        ---------           -----------                 --------                  ----
        policy_type	path	Get summary for all the policies of this type.	Yes	string
        domainId	query	If present, get policies from this domain.
                            Else get policies from logged in domain.	No	string

        """

        metadata = {
            'tags':['policies', 'summary'],
            'operation': 'Get Policy Summary with Policy Type'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/policies/summary/policy_type{domainIdParam}'

        return self._session.get(metadata, resource)


    def createTDADPolicy(self, **kwargs):
        """
        Creates a new Threat Defense for Active Directory policy
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'tdad'],
            'operation': 'Create TDAD Policy'
        }

        resource = f'/policies/tdad'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getTDADPolicy(self, id: str):
        """
        Get TDAD Policy payload for specified policy id.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the TDAD policy to get.	Yes	string
        body	body	No	Request object details
        """

        metadata = {
            'tags':['policies', 'tdad'],
            'operation': 'Get TDAD Policy'
        }

        resource = f'/policies/tdad/{id}'

        return self._session.get(metadata, resource)


    def editTDADPolicy(self, id: str, **kwargs):
        """
        Modify existing policy values.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The Threat Defense for Active Directory policy to be modified.	Yes	Request object details
        id	path	    The ID of the TDAD policy to edit.	Yes	string
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'tdad'],
            'operation': 'Edit TDAD Policy'
        }

        resource = f'/policies/tdad/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def deleteTDADPolicy(self, id: str):
        """
        Delete existing TDAD policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the TDAD policy to edit.	Yes	string
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'tdad'],
            'operation': 'Delete TDAD Policy'
        }

        resource = f'/policies/tdad/{id}'

        return self._session.delete(metadata, resource)


    def updateTDADPolicy(self, id: str, **kwargs):
        """
        Update existing policy values.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The Threat Defense for Active Directory policy to be modified.	Yes	Request object details
        id	path	    The ID of the TDAD policy to edit.	Yes	string
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'tdad'],
            'operation': 'Update TDAD Policy'
        }

        resource = f'/policies/tdad/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)


    def createExceptionsPolicy(self, **kwargs):
        """
        Creates a new Exceptions policy
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be created.	Yes	Request object details
        body	body		No	Request object details
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Create Exceptions Policy'
        }

        resource = f'/policies/exceptions'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def getExceptionsPolicy(self, id: str):
        """
        Get an existing Exceptions policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Get Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'


        return self._session.get(metadata, resource)


    def editExceptionsPolicy(self, id: str, **kwargs):
        """
        Modify existing policy values with PUT request.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be modified.	Yes	Request object details
        id	path	The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Edit Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def deleteExceptionsPolicy(self, id: str):
        """
        Deletes an existing Exceptions policy.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        id	path	    The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Delete Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'


        return self._session.delete(metadata, resource)


    def updateExceptionsPolicy(self, **kwargs):
        """
        Update exceptions policies by patch.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        body	body	The exceptions policy to be modified.	Yes	Request object details
        id	path	The ID of the exceptions policy to edit.	Yes	string
        """

        metadata = {
            'tags':['policies', 'exceptions'],
            'operation': 'Update Exceptions Policy'
        }

        resource = f'/policies/exceptions/{id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)

