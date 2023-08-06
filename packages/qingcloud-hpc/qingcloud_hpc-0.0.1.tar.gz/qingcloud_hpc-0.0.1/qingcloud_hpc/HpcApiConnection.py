import time

from qingcloud_hpc.sdk_api.constants import enable_action_pair
from qingcloud_hpc.sdk_api.hpc import Hpc

def get_timestamp():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
class Config:
    def __init__(self, access_key_id="", secret_access_key=""):
        self.access_key_id = access_key_id
        self.qy_access_key_id = secret_access_key
        self.qy_secret_access_key = secret_access_key
        self.connection_retries = 1
        self.protocol="http"
        self.port = 9889
        self.timeout = 60
class HpcApiConnection(object):
    def __init__(self,
                 access_key_id=None,
                 secret_access_key=None,
                 host=None,
                 port=None,
                 zone=None,
                 protocol=None,
                 **kwargs):
        self.config = Config()
        self.config.qy_access_key_id = access_key_id
        self.config.qy_secret_access_key = secret_access_key
        self.config.host = host
        self.api = Hpc(self.config)
        self.enable_action_pair = enable_action_pair
        self.config.zone = zone
        self.config.port = port
        self.config.protocol=protocol


    def send_request(self, action=None, zone=None, **kwargs):
        if action not in self.enable_action_pair:
            return {"ret_code":-1,
                    "message":"action [%s] not support" % action}
        if hasattr(self.api, self.enable_action_pair[action]):
            if not zone:
                zone = self.config.zone
            handler = self.enable_action_pair[action]
            return getattr(self.api, handler)(zone=zone,timestamp=get_timestamp(),
                                              **kwargs)


