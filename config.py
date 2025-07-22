import os
from dotenv import load_dotenv

load_dotenv()

#class Config:
#    INSTANCE_NAME = "INSTANCE_NAME"
#    USERNAME = "USERNAME"
#    PASSWORD = "PASSWORD"
#    USER_POOL_ID = "USER_POOL_ID"
#    IDENTITY_POOL_ID = "IDENTITY_POOL_ID"
#    CLIENT_ID = "CLIENT_ID"
#    REGION = "REGION"
#    DIMENSION_NAME_MACHINE = "DIMENSION_NAME_MACHINE"
#    CW_NAMESPACE = "CW_NAMESPACE"
#    VOL = "VOL"
#    def __init__(self):
#        self.instance_name = os.getenv(Config.INSTANCE_NAME)
#        self.username = os.getenv(Config.USERNAME)
#        self.password = os.getenv(Config.PASSWORD)
#        self.user_pool_id = os.getenv(Config.USER_POOL_ID)
#        self.identity_pool_id = os.getenv(Config.IDENTITY_POOL_ID)
#        self.client_id = os.getenv(Config.CLIENT_ID)
#        self.region = os.getenv(Config.REGION)
#        self.dimension_name_machine = os.getenv(Config.DIMENSION_NAME_MACHINE)
#        self.cw_namespace = os.getenv(Config.CW_NAMESPACE)
#        self.vol = os.getenv(Config.VOL)
#        missing = [k for k, v in self.__dict__.items() if v is None]
#        if missing:
#            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
        
class Config:
    EMAIL = "EMAIL"
    PASSWORD = "PASSWORD"
    USER_POOL_ID = "USER_POOL_ID"
    IDENTITY_POOL_ID = "IDENTITY_POOL_ID"
    CLIENT_ID="CLIENT_ID"
    REGION = "REGION"
    CW_NAMESPACE = "CW_NAMESPACE"
    VOL = "VOL"
    def __init__(self):
        self.email = os.getenv(Config.EMAIL)
        self.password = os.getenv(Config.PASSWORD)
        self.user_pool_id = os.getenv(Config.USER_POOL_ID)
        self.identity_pool_id = os.getenv(Config.IDENTITY_POOL_ID)
        self.client_id = os.getenv(Config.CLIENT_ID)
        self.region = os.getenv(Config.REGION)
        self.cw_namespace = os.getenv(Config.CW_NAMESPACE)
        self.vol = os.getenv(Config.VOL)
        missing = [k for k, v in self.__dict__.items() if v is None]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
