


class Groups(object):
    """
    The Groups APIs let you manage any aspect of your groups in a domain.

    A system administrator account is required for this API.

    https://apidocs.securitycloud.symantec.com/#/doc?id=groups

    """
    def __init__(self, session):
        super(Groups, self).__init__()
        self._session = session


    def syncDeleteGroups(self, domainId: str, **kwargs):
        """
        Delete groups. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainId query	The id of the domain for which the groups needs to be deleted.	No	string
        body	body	Group details	Yes	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'syncdelete'],
            'operation': 'Sync Delete Groups'
        }

        resource = f'/ext/groups/syncdelete?domainId={domainId}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def syncGroups(self, domainId=None, **kwargs):
        """
        Add/Update groups. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainId query	The id of the domain for which the groups needs to be deleted.	No	string
        body	body	Group details	Yes	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'synchronization'],
            'operation': 'Sync Groups'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/ext/groups/synchronization{domainIdParam}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def unsynchronizeGroups(self, domainId=None):
        """
        Changes the group node type back to its default value
        i.e Native for all the groups and temporary for default group and changes the external Reference Id back to null.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainId query	The id of the domain for which the groups needs to be deleted.	No	string

        """

        metadata = {
            'tags':['ext', 'groups', 'synchronization'],
            'operation': 'Unsynchronize Groups'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/ext/groups/synchronization{domainIdParam}'

        return self._session.delete(metadata, resource, payload)


    def getGroupCloudExternalCommunicationSettings(self, group_id: str):
        """
        Get cloud external communication settings for the given group

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path		Yes	string

        """

        metadata = {
            'tags':['ext', 'groups', 'policies', 'external-communication'],
            'operation': 'Get Group Cloud External Communication Settings'
        }

        resource = f'/ext/groups/{group_id}/policies/external-communication'

        return self._session.get(metadata, resource)


    def updateGroupExternalCommunication(self, group_id: str, **kwargs):
        """
        Update lowbandwidth external communication settings to a given group.
        The values that are not specified are set to defaults

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id path	The ID of the group	Yes	string
        body	body	The Settings to be used.	Yes	Request object details
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'policies', 'external-communication'],
            'operation': 'Update Group External Communication'
        }

        resource = f'/ext/groups/{group_id}/policies/external-communication'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)



    def withdrawSettingFromGroup(self, group_id: str, **kwargs):
        """
        Withdraw a cloud setting from a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id path	The ID of the group	Yes	string
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'policies', 'external-communication'],
            'operation': 'Withdraw Setting From Group'
        }

        resource = f'/ext/groups/{group_id}/policies/external-communication'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)



    def getPolicyIDFromGroup(self, group_id: str, policy_type: str, **kwargs):
        """
        Get a cloud Policy from a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the Policy to get.	Yes	string
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'policies'],
            'operation': 'Get Policy ID From Group'
        }

        resource = f'/ext/groups/{group_id}/policies/{policy_type}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def assignPolicyToGroup(self, group_id: str, policy_type: str, **kwargs):
        """
        Assign a cloud policy to a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the policy to assign.	Yes	string
        body	body	JSON object containing ID of the policy to be assigned. e.g. {"id":"Policy ID"}	Yes	Request object details
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'policies'],
            'operation': 'Assign Policy To Group'
        }

        resource = f'/ext/groups/{group_id}/policies/{policy_type}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)



    def withdrawPolicyFromGroup(self, group_id: str, policy_type: str, **kwargs):
        """
        Withdraw a cloud policy from a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the policy to assign.	Yes	string
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
            'tags':['ext', 'groups', 'policies'],
            'operation': 'Withdraw Policy From Group'
        }

        resource = f'/ext/groups/{group_id}/policies/{policy_type}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)



    def getPolicyIDFromGroup(self, group_id: str, policy_type: str, sub_type: str, **kwargs):
        """
        Get a cloud Policy from a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the policy to get.	Yes	string
        sub_type	path	The type of the sub policy to get.	Yes	string
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
         'tags':['ext', 'groups', 'policies'],
         'operation': 'Get Policy ID From Group'
        }

        resource = f'/ext/groups/{group_id}/policies/{policy_type}/{sub_type}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def assignPolicyToGroup(self, group_id: str, policy_type: str, sub_type: str, **kwargs):
        """
        Assign a cloud policy with sub type to a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the policy to get.	Yes	string
        sub_type	path	The type of the sub policy to get.	Yes	string
        body	body	Only used internally.	No	Request object details


        """

        metadata = {
         'tags':['ext', 'groups', 'policies'],
         'operation': 'Assign Policy To Group'
        }

        resource = f'/ext/groups/{group_id}/policies/{policy_type}/{sub_type}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)



    def withdrawPolicyWithSubTypeFromGroup(self, group_id: str, policy_type: str, sub_type: str, **kwargs):
        """
        Withdraw a cloud policy with sub type from a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the policy to get.	Yes	string
        sub_type	path	The type of the sub policy to get.	Yes	string
        body	body	Only used internally.	No	Request object details


        """

        metadata = {
         'tags':['ext', 'groups', 'policies'],
         'operation': 'Withdraw Policy From Group'
        }

        resource = f'/ext/groups/{group_id}/policies/{policy_type}/{sub_type}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)



    def getGroupDetailFromMyCompany(self, source: str, domainId=None, **kwargs):
        """
        Get the 'My Company' group details..

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        source	path	External source	Yes	string
        domainId	query		No	string

        """

        metadata = {
         'tags':['ext', 'groups', 'policies'],
         'operation': 'Get Group Detail From My Company'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/ext/{source}/groups/mycompany{domainIdParam}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def getGroupDetailFromSAEPGroupID(self, source: str, group_id: str, domainId=None, **kwargs):
        """
        Get the group information from its SAEP group ID,
        this is the equavalance of /api/v1/groups/{groupId} but this api takes external source group ID

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        source	path	External source	Yes	string
        groupId	path	The SAEP group Id, it has different than the sepm group ID	Yes	string
        domainId	query		No	string

        """

        metadata = {
         'tags':['ext', 'groups'],
         'operation': 'Get Group Detail From SAEP Group ID'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/ext/{source}/groups/{groupId}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def getGroups(self, **kwargs):
        """
        Gets a group list. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domain	query		No	string
        pageIndex	query	The index page used for returned results. The default page index is 1.	No	integer
        pageSize	query	The number of results to include on each page. The default is 25.	No	integer
        sort	query	The column by which the results are sorted. The default is by name.	No	string
        order	query	Specifies whether the results are in ascending order (ASC) or descending order (DESC).	No	string
        mode	query	The presentation mode for the results, as a list (default) or as a tree.	No	string
        fullPathName	query	The full path name of the group.	No	string

        """

        metadata = {
        'tags':['groups'],
        'operation': 'Get Groups'
        }

        resource = f'/groups'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def getGroupDetail(self, groupId: str, domainId=None, **kwargs):
        """
        Get SEPM group detail information.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group from which to query group detail	Yes	string
        domainId query	The ID of the group's domain	No	string

        """

        metadata = {
        'tags':['groups'],
        'operation': 'Get Group Detail'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}{domainIdParam}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def createGroup(self, groupId: str, domainId=None, **kwargs):
        """
        Create a group.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the parent group. A system administrator account is required for this REST API.	Yes	string
        domainId query	The ID of the group's domain	No	string
        body	body	The group configuration to be created.	Yes	Request object details
        body	body		No	Request object details

        """

        metadata = {
        'tags':['groups'],
        'operation': 'Create Group'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}{domainIdParam}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)



    def deleteGroup(self, groupId: str, domainId=None):
        """
        Delete a specific group.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the parent group. A system administrator account is required for this REST API.	Yes	string
        domainId query	The ID of the group's domain	No	string

        """

        metadata = {
        'tags':['groups'],
        'operation': 'Delete Group'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}{domainIdParam}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.delete(metadata, resource, payload)



    def patchGroup(self, groupId: str, domainId=None, **kwargs):
        """
        Update group configuration.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the parent group. A system administrator account is required for this REST API.	Yes	string
        domainId query	The ID of the group's domain	No	string
        body	body	The group configurations to be updated.	Yes	Request object details
        """

        metadata = {
        'tags':['groups'],
        'operation': 'Patch Group'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}{domainIdParam}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)



    def getComputersByGroupID(self, groupId: str, **kwargs):
        """
        Gets the information about the computers in a specified domain and group.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group where the clients are communicating	Yes	string
        pageIndex query	The index page used for returned results. The default page index is 1.	No	integer
        pageSize query	The number of results to include on each page. The default is 20.	No	integer
        sort	query	The column by which the results are sorted. Possible values are COMPUTER_NAME (Default value), COMPUTER_ID, COMPUTER_DOMAIN_NAME, or DOMAIN_ID.	No	string
        order	query	Specifies whether the results are in ascending order (ASC) or descending order (DESC).	No	string
        lastUpdate query	Indicates when a computer last updated its status. The default value of 0 gets all the results.	No	integer
        os	query	    The list of OS to filter. Possible values are CentOs, Debian, Fedora, MacOSX, Oracle, OSX, RedHat, SUSE, Ubuntu, Win10, Win2K, Win7, Win8, WinEmb7, WinEmb8, WinEmb81, WinFundamental, WinNT, Win2K3, Win2K8, Win2K8R2, WinVista, WinXP, WinXPEmb, WinXPProf64	No	array
        domain	query	The domain from which to get computer information.	No	string
        feature	query	List of features to return opstate information in reduced mode.Possible values are av, mem, fw, ips, tdad	No	array
        verbose	query	Returns a reduced set of computer information if true.	No	boolean

        """

        metadata = {
        'tags':['groups','computers'],
        'operation': 'Get Computers By Group ID'
        }

        resource = f'/groups/{groupId}/computers'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def getGroupExternalCommunicationSettings(self, groupId:str):
        """
        Get external communication settings of a location in the given group.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group where the clients are communicating	Yes	string

        """

        metadata = {
        'tags':['groups','computers'],
        'operation': 'Get Group External Communication Settings'
        }

        resource = f'/groups/{groupId}/external-communication'

        return self._session.get(metadata, resource)



    def putGroupExternalCommunicationSettings(self, groupId:str, **kwargs):
        """
        Add or replace external communication settings to a given group.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        body	body	The Settings to be used.	Yes	Request object details
        body	body	Only used internally.	No	Request object details
        """

        metadata = {
        'tags':['groups', 'external-communication'],
        'operation': 'Put Group External Communication'
        }

        resource = f'/groups/{groupId}/external-communication'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)



    def patchGroupExternalCommunicationSettings(self, groupId: str, **kwargs):
        """
        Patch external communication settings to a given group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        body	body	The Settings to be used.	Yes	Request object details
        body	body	Only used internally.	No	Request object details
        """

        metadata = {
        'tags':['groups', 'external-communication'],
        'operation': 'Patch Group External Communication'
        }

        resource = f'/groups/{groupId}/external-communication'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)



    def getLocationIdsForGroups(self, groupId:str, **kwargs):
        """
        Get SEPM locations information for specific group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group from which to query locations	Yes	string
        domainId	query	The ID of the group's domain	No	string
        hasName	query	If the return list contains location name.	No	boolean
        """

        metadata = {
        'tags':['groups', 'locations'],
        'operation': 'Get Location IDs For Group'
        }

        resource = f'/groups/{groupId}/locations'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)



    def getGroupLocationExternalCommunicationSettings(self, groupId: str, locationId: str):
        """
        Get external communication settings of a location in the given group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId	path	The ID of the location to which the policy is being retrieved.	Yes	string

        """

        metadata = {
        'tags':['groups', 'locations', 'external-communication'],
        'operation': 'Get Group Location External Communication Settings'
        }

        resource = f'/groups/{groupId}/locations/{locationId}/external-communication'

        return self._session.get(metadata, resource)



    def putGroupLocationExternalCommunication(self, groupId:str, locationId: str, **kwargs):
        """
        Update external communication settings to a location in the given group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being updated.	Yes	string
        body	body	The Settings to be used.	Yes	Request object details
        body	body	Only used internally.	No	Request object details
        """

        metadata = {
        'tags':['groups', 'locations', 'external-communication'],
        'operation': 'Put Group Location External Communication'
        }

        resource = f'/groups/{groupId}/locations/{locationId}/external-communication'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)



    def patchGroupLocationExternalCommunication(self, groupId: str, locationId: str, **kwargs):
        """
        Patch external communication settings to a location in the given group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being updated.	Yes	string
        body	body	The Settings to be used.	Yes	Request object details
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
        'tags':['groups', 'locations', 'external-communication'],
        'operation': 'Patch Group Location External Communication'
        }

        resource = f'/groups/{groupId}/locations/{locationId}/external-communication'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)



    def getPolicyTypeForLocation(self, groupId: str, locationId: str, domainId=None, **kwargs):
        """
        Get policies type list which are supported by SEPM for the specific group,
        it will always return av, fw, lu, hi, hid adc, ips, tdad and exceptions as of now.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being retrieved.	Yes	string
        domainId query	The ID of the group's domain	No	string

        """

        metadata = {
        'tags':['groups', 'locations', 'policies'],
        'operation': 'Get Policy Type For Location'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}/locations/{locationId}/policies{domainIdParam}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getPolicyIDForType(self, groupId: str, locationId: str, policyType: str, domainId=None, **kwargs):
        """
        Get the ID of a specific policy type that is assigned to a specific location in a specific group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being retrieved.	Yes	string
        policyType	path	The policy type, which can be av, fw, ips, adc, hi, hid, mem, lu, or exceptions.	Yes	string
        domainId query	The ID of the group's domain	No	string

        """

        metadata = {
        'tags':['groups', 'locations', 'policies'],
        'operation': 'Get Policy Type For Location'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}/locations/{locationId}/policies/{policyType}{domainIdParam}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getPolicyTypeForQuarantine(self, groupId: str, locationId: str, domainId=None, **kwargs):
         """
         Get quarantine policies type list which are supported by SEPM for group location's,
         it will always return av, fw, lu, hid, adc, ips, tdad and exceptions as of now.

         parameter       description                 required                  type
         ---------       -----------                 --------                  ----
         groupId	path	The ID of the group	Yes	string
         locationId path	The ID of the location to which the policy is being retrieved.	Yes	string
         domainId query	The ID of the group's domain	No	string

         """

         metadata = {
         'tags':['groups', 'locations', 'quarantine'],
         'operation': 'Get Policy Type For Quarantine'
         }

         domainIdParam = f'?domainId={domain}' if domainId is not None else ''

         resource = f'/groups/{groupId}/locations/{locationId}/quarantine'

         # TODO: add valid param lookup
         params = {k.strip(): v for k, v in kwargs.items()}

         return self._session.get(metadata, resource, params)


    def getQuarantinePolicyIDForType(self, groupId: str, locationId: str, policyType: str, domainId=None, **kwargs):
        """
        Get quarantine policies type list which are assigned to the specific location in specific group,
        the policy type can be av, fw, ips, adc, hid, lu, exceptions.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being retrieved.	Yes	string
        policyType path	The policy types, it can be av, fw, ips, adc, hi, lu, exceptions	Yes	string
        domainId query	The ID of the group's domain	No	string

        """

        metadata = {
        'tags':['groups', 'locations', 'policies'],
        'operation': 'Get Quarantine Policy ID For Type'
        }

        domainIdParam = f'?domainId={domainId}' if domainId is not None else ''

        resource = f'/groups/{groupId}/locations/{locationId}/quarantine/{policyType}{domainIdParam}'

        # TODO: add valid param lookup
        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getGroupSettings(self, groupId: str, locationId: str):
        """
        Get settings of a location in the given group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being retrieved.	Yes	string
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
        'tags':['groups', 'locations', 'settings'],
        'operation': 'Get Group Settings'
        }

        resource = f'/groups/{groupId}/locations/{locationId}/settings'

        return self._session.get(metadata, resource)


    def patchGroupSettings(self, groupId: str, locationId: str, **kwargs):
        """
        Patch all the communication settings to a given group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being updated.	Yes	string
        body	body	The Settings to be used.	Yes	Request object details
        body	body	Only used internally.	No	Request object details

        """

        metadata = {
        'tags':['groups', 'locations', 'settings'],
        'operation': 'Patch Group Settings'
        }

        resource = f'/groups/{groupId}/locations/{locationId}/settings'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.patch(metadata, resource, payload)


    def getLocationXML(self, groupId: str, locationId:str, **kwargs):
        """
        Get Location XML for specified location id.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        groupId	path	The ID of the group	Yes	string
        locationId path	The ID of the location to which the policy is being updated.	Yes	string

        """

        metadata = {
        'tags':['groups', 'locations', 'xml'],
        'operation': 'Get Location XML'
        }

        resource = f'/groups/{groupId}/locations/{locationId}/xml'

        return self._session.get(metadata, resource)


    def assignPolicyToLocation(self, group_id: str, location_id: str, policy_type: str, **kwargs):
        """
        Assign a Policy to a given location with in a group.
        Only location specific policies can be assigned to a location.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        location_id	path	The ID of the location to which the policy is being assigned. To assign policy to default location, 'default' can also be used instead of location ID.	Yes	string
        policy_type	path	The type of the Policy to assign.	Yes	string
        body	body	JSON object containing ID of the policy to be assigned. e.g. {"id":"some GUID"}	Yes	Request object details

        """

        metadata = {
        'tags':['groups', 'locations', 'policies'],
        'operation': 'Assign Policy To Location'
        }

        resource = f'/groups/{group_id}/locations/{location_id}/policies/{policy_type}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def getPolicyAssignedToGroup(self, group_id: str, policy_type: str, **kwargs):
        """
        Get Policy Assigned To Group

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id path	The ID of the group from which to query policies.	Yes	string
        policy_type path	The policy type, which can be lucontent or customips.	Yes	string

        """

        metadata = {
        'tags':['groups', 'policies',],
        'operation': 'Get Policy Assigned To Group'
        }

        resource = f'/groups/{group_id}/policies/{policy_type}'

        return self._session.get(metadata, resource)


    def assignPolicyToGroup(self, group_id: str, policy_type: str, **kwargs):
        """
        Assign a location independent Policy to a group.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id	path	The ID of the group to which the policy is being assigned.	Yes	string
        policy_type	path	The type of the Policy to assign.	Yes	string
        body	body	JSON object containing ID of the policy to be assigned. e.g. {"id":"some GUID"}	Yes	Request object details

        """

        metadata = {
        'tags':['groups', 'policies'],
        'operation': 'Assign Policy To Group'
        }

        resource = f'/groups/{group_id}/policies/{policy_type}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)


    def assignFingerprintToGroup(self, group_id: str, fingerprint_id: str, **kwargs):
        """
        Assign a fingerprint list to a group for system lockdown.
        A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        group_id path	The ID of the group to which a fingerprint list is being assigned.	Yes	string
        fingerprint_id	path	The ID of the fingerprint list to assign.	Yes	string
        """

        metadata = {
        'tags':['groups', 'policies'],
        'operation': 'Assign Policy To Group'
        }

        resource = f'/groups/{group_id}/system-lockdown/fingerprints/{fingerprint_id}'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.put(metadata, resource, payload)