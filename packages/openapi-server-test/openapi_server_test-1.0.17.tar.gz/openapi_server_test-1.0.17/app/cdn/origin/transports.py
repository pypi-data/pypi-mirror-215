from flask import Request, Response
from grpc_instance_pool import Dingman_grpc_cli

import utils
from app import common
from . import endpoints

ENTITY_CDN_ORIGIN="cdn-origin"
PARAM_DATA_FORMAT="data-format"
PARAM_SERVER_LIST="server-list"
PARAM_KEEPALIVE_LIMIT="keepalive-limit"
PARAM_KEEPALIVE_NUMBER="keepalive-number"

@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for cdn-origin.
    """
    show_req = endpoints.ShowRequest(params=req.args)

    show_resp = endpoints.show(cli, show_req)
    return common.transports.encode_response(show_resp)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for cdn-origin.
    """
    params = req.json

    if PARAM_SERVER_LIST in params:
        params[PARAM_SERVER_LIST] = ",".join(params[PARAM_SERVER_LIST])

    add_req = endpoints.AddRequest(params=params)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for cdn-origin.
    """
    delete_req = endpoints.DeleteRequest(params=req.json)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for cdn-origin.
    """
    params = req.json

    if PARAM_SERVER_LIST in params:
        params[PARAM_SERVER_LIST] = ",".join(params[PARAM_SERVER_LIST])

    for p in [PARAM_KEEPALIVE_LIMIT, PARAM_KEEPALIVE_NUMBER]:
        try:
            int(params[p]) # this also checks for key existence
        except:
            params[p] = 0

    set_req = endpoints.SetRequest(params=params)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
