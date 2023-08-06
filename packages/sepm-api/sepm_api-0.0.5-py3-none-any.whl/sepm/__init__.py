"""sepm - Symantec Endpoint Protection Manager API"""

from datetime import datetime
import logging
import os

from sepm.rest_api_session import *
from sepm.endpoints.administrators import Administrators
from sepm.endpoints.blacklist import Blacklist
from sepm.endpoints.cloud import Cloud
from sepm.endpoints.commands import Commands
from sepm.endpoints.computers import Computers
from sepm.endpoints.content import Content
from sepm.endpoints.domains import Domains
from sepm.endpoints.events import Events
from sepm.endpoints.group_update_provider import GroupUpdateProvider
from sepm.endpoints.groups import Groups
from sepm.endpoints.identity import Identity
from sepm.endpoints.notifications import Notifications
from sepm.endpoints.policies import Policies
from sepm.endpoints.replication import Replication
from sepm.endpoints.reporting import Reporting
from sepm.endpoints.requested_files import RequestedFiles
from sepm.endpoints.statistics import Statistics
from sepm.endpoints.threat_defense_for_active_directory import ThreatDefenseForActiveDirectory
from sepm.endpoints.version import Version

#config import
from sepm.config import (
    API_USERNAME_ENV,
    API_PASSWORD_ENV,
    API_DOMAIN_ENV,
    DEFAULT_BASE_URL,
    AUTH_URL,
    OUTPUT_LOG,
    LOG_PATH,
    LOG_FILE_PREFIX,
    PRINT_TO_CONSOLE,
    SUPPRESS_LOGGING,
    INHERIT_LOGGING_CONFIG,
    SIMULATE_API,
)

__version__ = '0.0.5'
__author__ = 'Alex Almero <aalmero@gmail.com>'
__all__ = []

class SymantecEndpointProtectionManagerAPI(object):
    """
    create a persistent Symantec Endpoint Protection Manager API session
    ....
    """

    def __init__(self,
                 username=None,
                 password=None,
                 domain=None,
                 base_url=DEFAULT_BASE_URL,
                 auth_url=AUTH_URL,
                 output_log=OUTPUT_LOG,
                 log_path=LOG_PATH,
                 log_file_prefix=LOG_FILE_PREFIX,
                 print_console=PRINT_TO_CONSOLE,
                 suppress_logging=SUPPRESS_LOGGING,
                 simulate=SIMULATE_API,
                 inherit_logging_config=INHERIT_LOGGING_CONFIG,
                 ):

        # check API credentials
        username = username or os.environ.get(API_USERNAME_ENV)
        password = password or os.environ.get(API_PASSWORD_ENV)
        domain = domain or os.environ.get(API_DOMAIN_ENV)
        base_url = os.environ.get(API_BASE_URL_ENV) or base_url
        auth_url = '{0}{1}'.format(base_url, auth_url)

        print('base_url={3}, username={0}, password={1}, domain={2}'.format(username, password, domain, base_url))

        if not username or not password:
            raise APIError()

        inherit_logging_config = inherit_logging_config

        # configure logging
        if not suppress_logging:
            self._logger = logging.getLogger(__name__)

            if not inherit_logging_config:
                self._logger.setLevel(logging.DEBUG)

                formatter = logging.Formatter(
                    fmt='%(asctime)s %(name)12s: %(levelname)8s > %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler_console = logging.StreamHandler()
                handler_console.setFormatter(formatter)

                if output_log:
                    if log_path and log_path[-1] != '/':
                        log_path += '/'
                    self._log_file = f'{log_path}{log_file_prefix}_log__{datetime.now():%Y-%m-%d_%H-%M-%S}.log'
                    handler_log = logging.FileHandler(
                        filename=self._log_file
                    )
                    handler_log.setFormatter(formatter)

                if output_log and not self._logger.hasHandlers():
                    self._logger.addHandler(handler_log)
                    if print_console:
                        handler_console.setLevel(logging.INFO)
                        self._logger.addHandler(handler_console)
                elif print_console and not self._logger.hasHandlers():
                    self._logger.addHandler(handler_console)
        else:
            self._logger = None

        # create the API session
        self._session = RestApiSession(
            logger = self._logger,
            username = username,
            password = password,
            domain = domain,
            base_url = base_url,
            auth_url = auth_url,
            simulate = simulate,
        )

        # API endpoints definition
        self.administrators = Administrators(self._session)
        self.blacklist = Blacklist(self._session)
        self.cloud = Cloud(self._session)
        self.commands = Commands(self._session)
        self.computers = Computers(self._session)
        self.content = Content(self._session)
        self.domains = Domains(self._session)
        self.events = Events(self._session)
        self.group_update_provider = GroupUpdateProvider(self._session)
        self.groups = Groups(self._session)
        self.identity = Identity(self._session)
        self.notifications = Notifications(self._session)
        self.policies = Policies(self._session)
        self.replication = Replication(self._session)
        self.reporting = Reporting(self._session)
        self.requested_files = RequestedFiles(self._session)
        self.statistics = Statistics(self._session)
        self.threat_defense_for_active_directory = ThreatDefenseForActiveDirectory(self._session)
        self.version = Version(self._session)

