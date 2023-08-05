from flask import Request, Response
from grpc_instance_pool import Dingman_grpc_cli

import utils
from app import common
from . import endpoints

ENTITY_CDN_POLICY="cdn-policy"
PARAM_VALUE="value"
PARAM_BLOCK_LIST="block-list"
PARAM_ALLOW_LIST="allow-list"
PARAM_HOSTS="hosts"

@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for cdn-policy.
    """
    show_req = endpoints.ShowRequest(params=req.args)
    show_resp = endpoints.show(cli, show_req)
    return common.transports.encode_response(show_resp)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for cdn-policy.
    """
    add_req = endpoints.AddRequest(params=req.json)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for cdn-policy.
    """
    delete_req = endpoints.DeleteRequest(params=req.json)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for cdn-policy.
    """
    params = req.json

    for p in [PARAM_VALUE, PARAM_ALLOW_LIST, PARAM_BLOCK_LIST, PARAM_HOSTS]:
        if p not in params:
            continue
        params[p] = ",".join(params[p])

    set_req = endpoints.SetRequest(params=params)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
