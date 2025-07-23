import os

#KEYS
KEY_USERNAME = "USERNAME"
KEY_PASSWORD = "PASSWORD"
KEY_METRIC_NAME = "MetricName"
KEY_DIMENSIONS = "Dimensions"
KEY_TIMESTAMP = "Timestamp"
KEY_VALUE = "Value"
KEY_UNIT = "Unit"
KEY_NAME = "Name"
KEY_AUTH_RESULTS = "AuthenticationResult"
KEY_ID_TOKEN = "IdToken"
KEY_IDENTITY_ID = "IdentityId"
KEY_CREDENTIALS = "Credentials"

#CONSTANTS
UNIT_PERCENT = "Percent"
UNIT_SECONDS = "Seconds"
COGNITO_PROVIDER = "cognito-idp.us-west-2.amazonaws.com/"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "creds.json")
DEFAULT_ENCODING = "utf-8"
EXPIRATION = "Expiration"
USER_PASSWORD_AUTH="USER_PASSWORD_AUTH"
COGNITO_IDP = "cognito-idp"
COGNITO_IDENTITY = "cognito-identity"
CLOUDWATCH = "cloudwatch"
ACCESS_KEY_ID = "AccessKeyId"
SECRET_KEY = "SecretKey"
SESSION_TOKEN = "SessionToken"

#Names
metric_name_disk_usage = "DiskUsage"
root_name_value = "/"
metric_name_uptime = "Uptime"
