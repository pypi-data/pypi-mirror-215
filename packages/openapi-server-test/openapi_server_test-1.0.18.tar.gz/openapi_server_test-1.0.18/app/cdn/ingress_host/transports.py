import copy
from flask import Request, Response
from grpc_instance_pool import Dingman_grpc_cli
from typing import Dict

import consts, utils
from app import common
from . import endpoints

ENTITY_CDN_INGRESS_HOST="cdn-ingress-host"
PARAM_SERVER_NAME="server-name"
PARAM_CDN_VENDOR="cdn-vendor"
PARAM_TOKEN="token"
PARAM_QUEUE="queue"
PARAM_LABELS="labels"

IGNORE_ARGS = set([
    ENTITY_CDN_INGRESS_HOST,
    PARAM_SERVER_NAME,
    PARAM_CDN_VENDOR,
    PARAM_TOKEN,
    PARAM_QUEUE,
    PARAM_LABELS,
])

def remove_invalid_write_params(params: Dict) -> Dict:
    filtered = copy.deepcopy(params)
    for k in params.keys():
        if k in IGNORE_ARGS or k.startswith("label."):
            continue
        if k not in consts.DM_ALLOWED_ARGS:
            del filtered[k]
    return filtered

@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for cdn-ingress-host.
    """
    params = req.args
    params_dict = {k: v for k, v in params.items()}
    if PARAM_SERVER_NAME in params_dict:
        params_dict[PARAM_SERVER_NAME] = utils.base64_encode_string(params_dict[PARAM_SERVER_NAME])
    show_req = endpoints.ShowRequest(params=params_dict)
    show_resp = endpoints.show(cli, show_req)
    return common.transports.encode_response(show_resp)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for cdn-ingress-host.
    """
    params = req.json
    if PARAM_SERVER_NAME in params:
        params[PARAM_SERVER_NAME] = utils.base64_encode_string(params[PARAM_SERVER_NAME])

    filtered = remove_invalid_write_params(params)

    add_req = endpoints.AddRequest(params=filtered)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for cdn-ingress-host.
    """
    delete_req = endpoints.DeleteRequest(params=req.json)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for cdn-ingress-host.
    """
    params = req.json

    if PARAM_SERVER_NAME in params:
        params[PARAM_SERVER_NAME] = utils.base64_encode_string(params[PARAM_SERVER_NAME])

    filtered = remove_invalid_write_params(params)

    set_req = endpoints.SetRequest(params=filtered)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
