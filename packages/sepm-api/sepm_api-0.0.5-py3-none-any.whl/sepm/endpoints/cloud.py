


class Cloud(object):
    """
    The Cloud APIs let you manage your cloud connection and domain enrollment status.

    https://apidocs.securitycloud.symantec.com/#/doc?id=cloud

    """
    def __init__(self, session):
        super(Cloud, self).__init__()
        self._session = session


    def getCloudEnrollment(self, customerId: str, domainId: str, clientId: str, clientSecret: str):
        """
        Retrieve the Cloud's domain enrollment status. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        x-epmp-customer-id	header	EPMP Customer ID	Yes	string
        x-epmp-domain-id	header	EPMP Domain ID	Yes	string
        x-epmp-client-id	header	EPMP Client ID	Yes	string
        x-epmp-client-secret	header	EPMP Client Secret	Yes	string
        """

        pass


    def enableAutoPolicySync(self):
        """
        Enable auto policy sync flag

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
            'tags':['cloud', 'epmp', 'enableAutoPolicySync'],
            'operation': 'Enable Auto Policy Sync'
        }

        resource = f'/cloud/epmp/enableAutoPolicySync'

        return self._session.post(metadata, resource)


    def getEnrollmentStatus(self, domainId: str):
        """
        Gets the enrollment status.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainid	query	The ID of the domain for which you want to check the enrollment status.	Yes	string

        """
        metadata = {
                'tags':['administrators', 'admin-users', 'create'],
                'operation': 'Get Enrollment Status'
        }

        resource = f'/cloud/epmp/enroll?domainid={domainId}'

        return self._session.get(metadata, resource)


    def doCloudEnroll(self, domainId: str, **kwargs):
        """
        Enrolls Symantec Cloud Bridge with the cloud.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainid query	The ID of the domain that you want to enroll.	Yes	string
        body	body	The enrollment details to register in the cloud.	Yes	Request object details
        body	body	Only used internally.	No	Request object details

        """
        metadata = {
                'tags':['cloud', 'epmp', 'enroll'],
                'operation': 'Do Cloud Enroll'
        }

        resource = f'/cloud/epmp/enroll?domainid={domainId}'

        # TODO: add valid params lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.post(metadata, resource, payload)


    def doCloudUnEnroll(self, domainId: str):
        """
        Un-Enroll Symantec DHub with cloud. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainid query	Un-Enrollment based on domain	Yes	string

        """

        metadata = {
                'tags':['cloud', 'epmp', 'enroll'],
                'operation': 'Do Cloud UnEnroll'
        }

        resource = f'/cloud/epmp/enroll/?domainid={domainId}'

        return self._session.delete(metadata, resource)


    def getHubStatus(self):
        """
        Get reporting hub's status

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
                'tags':['cloud', 'epmp', 'hubstatus'],
                'operation': 'Get Hub Status'
        }

        resource = f'/cloud/epmp/hubstatus'

        return self._session.get(metadata, resource)


    def isEnrolled(self, domainId: str):
        """
        Check if the hub on the specified server is reporting hub

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        domainid query	Domain Id	Yes	string
        """
        metadata = {
                'tags':['cloud', 'epmp', 'isEnrolled'],
                'operation': 'Is Enrolled'
        }

        resource = f'/cloud/epmp/isEnrolled?domainid={domainId}'

        return self._session.get(metadata, resource)