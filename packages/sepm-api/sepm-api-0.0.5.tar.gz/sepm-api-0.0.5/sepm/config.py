#libary constants

# API username and password configure either at instantiation or as an environment variable
API_USERNAME_ENV = 'API_USERNAME'
API_PASSWORD_ENV = 'API_PASSWORD'
API_DOMAIN_ENV = 'API_DOMAIN'
API_BASE_URL_ENV = 'API_BASE_URL'

# Base URL preceding all endpoint resources
DEFAULT_BASE_URL = 'https://localhost:8446/sepm/api/v1'

# Authentication URL
AUTH_URL = '/identity/authenticate'

# create output log file
OUTPUT_LOG = False

# Path to output log; by default, working directory of script if not specified
LOG_PATH = ''

# Log file name appended with date and timestamp
LOG_FILE_PREFIX = 'sepm_api_'

# Print output logging to console?
PRINT_TO_CONSOLE = True

# Enable/Disable Logging
SUPPRESS_LOGGING = False

#inherit an external logger instance.
INHERIT_LOGGING_CONFIG = False

# Simulate POST/PUT/DELETE calls
SIMULATE_API = True

# Retry if encountering other 4XX error (besides 429)?
RETRY_4XX_ERROR = False

# Other 4XX error retry wait time
RETRY_4XX_ERROR_WAIT_TIME = 60

# Retry n times when encountering 429s or other server-side errors
MAXIMUM_RETRIES = 2
