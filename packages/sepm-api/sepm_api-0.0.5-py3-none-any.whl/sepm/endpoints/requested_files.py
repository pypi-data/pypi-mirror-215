

class RequestedFiles(object):
    """
    The Requested Files API lets you get the binary file content for a given SHA value.

    A system administrator account is required for this REST API.

    https://apidocs.securitycloud.symantec.com/#/doc?id=requestedfiles

    """

    def __init__(self, session):
        super(RequestedFiles, self).__init__()
        self._session = session


    def getBinaryFileContentForSha256(self, sha256: str, **kwargs):
        """
        Gets the binary file content for a given SHA value. A system administrator account is required for this REST API.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        sha256	path	The SHA256 value which to get the binary content.	Yes	string
        body	body		No	Request object details

        """

        metadata = {
         'tags':['requested-file', 'sha256', 'content'],
         'operation': '	Get Binary File Content For Sha256'
        }

        resource = f'/requested-files/{sha256}/content'

        # TODO: add valid param lookup
        payload = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, payload)