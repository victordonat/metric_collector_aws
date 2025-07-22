import json
from datetime import datetime, timezone
from typing import Callable, Dict, Any

import boto3
import psutil
import pytz

import constants as ct
from config import Config


class CognitoCredentialError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class CreateCognitoclientError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class GetDiskUsageError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class BuildMetricError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class SendMetricError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class SaveCredentialsError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def get_disk_usage(vol: str) -> float:
    """
    Get the disk usage percentage of the root directory vol.

    Returns:
        float: Disk usage as a percentage.
    """
    try:
        return psutil.disk_usage(vol).percent
    except Exception as e:
        raise GetDiskUsageError(f"Failed to retrieve disk usage: {str(e)}")


def build_metric_data(
    metric_name: str, 
    value: float,
    unit: str
) -> Dict[str, Any]:
    """
    Build a dictionary with metric data formatted for CloudWatch.

    Args:
        metric_name (str): Name of the metric.
        value (float): Metric value.
        unit (str): Unit of the metric.

    Returns:
        Dict[str, Any]: Metric data dictionary.
    """
    try:
        return {
            ct.KEY_METRIC_NAME: metric_name,
            ct.KEY_TIMESTAMP: datetime.now(pytz.UTC),
            ct.KEY_VALUE: value,
            ct.KEY_UNIT: unit
        }
    except Exception as e:
        raise BuildMetricError(f"Failed to build metric: {str(e)}")


def put_metrics(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: str,
    metric_collector: Callable[[], float],
    cw_namespace: str,
    region_name: str
) -> None:
    """
    Collect metric using a callable and send it to CloudWatch.

    Args:
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        aws_session_token (str): AWS session token.
        metric_collector (Callable[[], float]): Function to collect metric.
        instance_name (str): Name of the instance sending metrics.
        region_name (str): AWS region name.
    """
    try:
        cw = boto3.client(
            ct.CLOUDWATCH,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name
        )
    except Exception as e:
        raise CreateCognitoclientError(f"Failed to create CloudWatch client: {str(e)}")
    metric_data_value = metric_collector()
    metric_data = build_metric_data(
        metric_name=ct.metric_name_disk_usage,
        value=metric_data_value,
        unit=ct.UNIT_PERCENT,
    )
    try:
        cw.put_metric_data(
            Namespace=cw_namespace,
            MetricData=[metric_data]
        )
    except Exception as e:
        raise SendMetricError(f"Failed to send metric: {str(e)}")


def get_cognito_credentials(
    email: str,
    password: str,
    user_pool_id: str,
    identity_pool_id: str,
    client_id: str,
    region: str
) -> Dict[str, str]:
    """
    Authenticate against Cognito and get temporary AWS credentials.

    Args:
        username (str): Cognito user name.
        password (str): Cognito user password.
        user_pool_id (str): Cognito user pool ID.
        identity_pool_id (str): Cognito identity pool ID.
        client_id (str): Cognito client app ID.
        region (str): AWS region.

    Returns:
        Dict[str, str]: Dictionary with AWS temporary credentials
        and expiration of credentials.
    """
    try:
        idp = boto3.client(ct.COGNITO_IDP, region_name=region)
        resp = idp.initiate_auth(
            AuthFlow=ct.USER_PASSWORD_AUTH,
            AuthParameters={
                ct.KEY_USERNAME: email,
                ct.KEY_PASSWORD: password,
            },
            ClientId=client_id
        )
        id_token = resp[ct.KEY_AUTH_RESULTS][ct.KEY_ID_TOKEN]
        identity = boto3.client(ct.COGNITO_IDENTITY, region_name=region)
        identity_id = identity.get_id(
            IdentityPoolId=identity_pool_id,
            Logins={ct.COGNITO_PROVIDER + user_pool_id: id_token}
        )[ct.KEY_IDENTITY_ID]
        creds = identity.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={ct.COGNITO_PROVIDER + user_pool_id: id_token}
        )[ct.KEY_CREDENTIALS]
        expiration_dt = creds[ct.EXPIRATION].astimezone(timezone.utc)
        expiration_iso = expiration_dt.isoformat()
        return {
            ct.ACCESS_KEY_ID: creds[ct.ACCESS_KEY_ID],
            ct.SECRET_KEY: creds[ct.SECRET_KEY],
            ct.SESSION_TOKEN: creds[ct.SESSION_TOKEN],
            ct.EXPIRATION: expiration_iso
        }
    except Exception as e:
        raise CognitoCredentialError(f"Failed to get Cognito credentials: {str(e)}")


def save_credentials(
    creds: Dict[str, str],
    credentials_file: str,
    encoding: str
) -> None:
    """
    Save credentials dictionary as JSON to a file.

    Args:
        creds (Dict[str, str]): Credentials data to save.
        credentials_file (str): File path to save credentials.
        encoding (str): File encoding.
    """
    try:
        with open(credentials_file, "w", encoding=encoding) as f:
            json.dump(creds, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise SaveCredentialsError(f"Failed to save new credentials: {str(e)}")


def load_credentials(now_utc: datetime):
    try:
        with open(ct.CREDENTIALS_FILE, "r", encoding=ct.DEFAULT_ENCODING) as f:
            creds = json.load(f)
            expiration_str = creds[ct.EXPIRATION]
            expiration_dt = datetime.fromisoformat(expiration_str)
            if now_utc < expiration_dt:
                return creds
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
        pass
    return None


def main():
    """
    Main entry point.

    Checks if saved credentials exist, are valid and not expired; 
    if so, sends metrics using them, otherwise authenticates to Cognito,
    sends metrics and saves new creds.
    """
    now_utc = datetime.now(timezone.utc)
    creds = load_credentials(now_utc=now_utc)
    config = Config()
    if creds is not None:
        put_metrics(
            aws_access_key_id=creds[ct.ACCESS_KEY_ID],
            aws_secret_access_key=creds[ct.SECRET_KEY],
            aws_session_token=creds[ct.SESSION_TOKEN],
            metric_collector=(lambda:get_disk_usage(vol = config.vol)),
            cw_namespace=config.cw_namespace,
            region_name=config.region
        )
    else:
        creds = get_cognito_credentials(
            email=config.email,
            password=config.password,
            user_pool_id=config.user_pool_id,
            identity_pool_id=config.identity_pool_id,
            client_id=config.client_id,
            region=config.region
        )
        save_credentials(
            creds=creds,
            credentials_file=ct.CREDENTIALS_FILE,
            encoding=ct.DEFAULT_ENCODING
        )
        put_metrics(
            aws_access_key_id=creds[ct.ACCESS_KEY_ID],
            aws_secret_access_key=creds[ct.SECRET_KEY],
            aws_session_token=creds[ct.SESSION_TOKEN],
            metric_collector=(lambda:get_disk_usage(vol = config.vol)),
            cw_namespace=config.cw_namespace,
            region_name=config.region
        )
