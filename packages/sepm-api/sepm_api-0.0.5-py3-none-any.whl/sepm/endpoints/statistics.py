

class Statistics(object):
    """
    The Statistics APIs let you retrieve the following statistical data:
    Threats that were automatically resolved.
    Clients for a group by content version.
    Count of client groups by content download sources.
    Count for a specified time range of infected clients.
    Specified time range of clients reporting malware events.
    Count of the online and offline clients.
    Specified time range the risk distribution by protection technology information for the given time range.
    Count of clients by client product version.
    Threat statistical data.

    https://apidocs.securitycloud.symantec.com/#/doc?id=stats

    """

    def __init__(self, session):
        super(Statistics, self).__init__()
        self._session = session


    def getAutoResolvedAttacksCount(self, reportType: str, startTime: str, endTime: str, **kwargs):
        """
        Gets a list of threats that were automatically resolved.
        Threats include viruses, spyware, and risks.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        reportType	path	The type of report. Report types are Hour, Day, Week, and Month.	Yes	string
        startTime	path	The start time for gathering these statistics.	Yes	integer
        endTime	path	The end time for gathering these statistics.	Yes	integer
        timeZone	query	The time zone of the returned events. The default is UTC.	No	string

        """
        metadata = {
            'tags':['stats', 'autoresolved', 'reportType', 'startTime', 'endTime'],
            'operation': 'Get Auto Resolved Attacks Count'
        }

        resource = f'/stats/autoresolved/{reportType}/{startTime}/to/{endTime}'

        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getClientDefStatus(self):
        """
        Gets a list of clients for a group by content version.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
            'tags':['stats', 'client', 'content', 'startTime', 'endTime'],
            'operation': 'Get Client Def Status'
        }

        resource = f'/stats/client/content'

        return self._session.get(metadata, resource)


    def getClientContentDownloadSources(self, **kwargs):
        """
        Gets a list and count of client groups by content download sources.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        locale	query	The locale specified and the language in which to return results. The default is en-US.	No	string
        Responses

        """
        metadata = {
            'tags':['stats', 'autoresolved', 'reportType', 'startTime', 'endTime'],
            'operation': 'Get Client Content Download Sources'
        }

        resource = f'/stats/client/sources'

        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getInfectedClient(self, reportType: str, startTime: str, endTime: str, **kwargs):
        """
        Gets a list and count for a specified time range of infected clients.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        reportType	path	The type of report. Report types are Hour, Day, Week, and Month.	Yes	string
        startTime	path	The start time for gathering these statistics.	Yes	integer
        endTime	path	The end time for gathering these statistics.	Yes	integer
        timeZone	query	The time zone of the returned events. The default is UTC.	No	string

        """
        metadata = {
            'tags':['stats', 'client', 'infection', 'reportType', 'startTime', 'endTime'],
            'operation': 'Get Infected Client'
        }

        resource = f'/stats/client/infection/{reportType}/{startTime}/to/{endTime}'

        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getMalwareClient(self, reportType: str, startTime: str, endTime: str, **kwargs):
        """
        Gets a list and count for a specified time range of infected clients.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        reportType	path	The type of report. Report types are Hour, Day, Week, and Month.	Yes	string
        startTime	path	The start time for gathering these statistics.	Yes	integer
        endTime	path	The end time for gathering these statistics.	Yes	integer
        timeZone	query	The time zone of the returned events. The default is UTC.	No	string

        """
        metadata = {
            'tags':['stats', 'client', 'malware', 'reportType', 'startTime', 'endTime'],
            'operation': 'Get Malware Client Stats'
        }

        resource = f'/stats/client/malware/{reportType}/{startTime}/to/{endTime}'

        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getClientOfflineOnlineCountStats(self, **kwargs):
        """
        Gets a list and count of the online and offline clients.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----

        """
        metadata = {
            'tags':['stats', 'client', 'onlinestatus'],
            'operation': 'Get Clients On-line Off-line Count Stats'
        }

        resource = f'/stats/client/onlinestatus'

        return self._session.get(metadata, resource)


    def getRiskDistributionStats(self, startTime: str, endTime: str, **kwargs):
        """
        Gets a list for a specified time range the risk distribution
        by protection technology information for the given time range.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----
        startTime	path	The start time for gathering these statistics.	Yes	integer
        endTime	path	The end time for gathering these statistics.	Yes	integer
        timeZone	query	The time zone of the returned events. The default is UTC.	No	string

        """
        metadata = {
            'tags':['stats', 'client', 'malware', 'startTime', 'endTime'],
            'operation': 'Get Risk Distribution Stats'
        }

        resource = f'/stats/client/risk/{startTime}/to/{endTime}'

        params = {k.strip(): v for k, v in kwargs.items()}

        return self._session.get(metadata, resource, params)


    def getClientVersion(self):
        """
        Gets a list and count of clients by client product version.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----


        """
        metadata = {
            'tags':['stats', 'client', 'version'],
            'operation': 'Get Client Version'
        }

        resource = f'/stats/client/version'

        return self._session.get(metadata, resource)


    def getThreatStatus(self, **kwargs):
        """
        Gets threat statistics.

        parameter       description                 required                  type
        ---------       -----------                 --------                  ----


        """
        metadata = {
            'tags':['stats', 'client', 'version'],
            'operation': 'Get Threat Stats'
        }

        resource = f'/stats/threat'

        return self._session.get(metadata, resource)
