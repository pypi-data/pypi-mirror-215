import json

from qingcloud_hpc.config import Config
from src.sdk_api.hpc import Hpc
import constants



def build_sdk():
    action_pair = {}
    with open("/pitrix/hpc/pitrix-hpc-ws/spec/swagger.json","r",encoding="utf-8") as f:
        api_dict = json.load(f)
        for path ,value in api_dict.get("paths").items():
            for method, param in value.items():
                action = "Hpc" + param.get("tags")[0].title()
                operation_handler = param.get("operationId")
                op_list = operation_handler.split("_")
                for o in op_list:
                    action = action + o.title()
            action_pair[action] = operation_handler
    with open("constants.py", "w") as f:
        f.write(json.dumps(action_pair))

    # config = Config()
    # # config.load_config_from_filepath(kwargs['config'])
    # config.connection_retries = 10
    # global api
    # api = Hpc(config)
    # print(dir(api))
    # print(constants)

build_sdk()