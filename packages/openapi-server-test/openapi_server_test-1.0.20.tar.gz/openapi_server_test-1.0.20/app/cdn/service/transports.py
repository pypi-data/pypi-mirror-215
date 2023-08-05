from flask import Request, Response
from grpc_instance_pool import Dingman_grpc_cli

import utils
from app import common
from . import endpoints

ENTITY_CDN_SERVICE="cdn-service"
PARAM_CDN_EDGE="cdn-edge"
PARAM_ORIGIN_DOMAIN="origin-domain"
PARAM_ORIGIN_HOST="origin-host"
PARAM_CDN_VENDOR="cdn-vendor"

@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for cdn-service.
    """
    params = {k:v for k,v in req.args.items()}
    if PARAM_CDN_VENDOR not in params:
        params[PARAM_CDN_VENDOR] = "bos_cdn"

    show_req = endpoints.ShowRequest(params=params)
    show_resp = endpoints.show(cli, show_req)
    return common.transports.encode_response(show_resp)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for cdn-service.
    """
    params = req.json

    if PARAM_CDN_EDGE in params:
        params[PARAM_CDN_EDGE] = ",".join(params[PARAM_CDN_EDGE])
    if PARAM_ORIGIN_DOMAIN in params:
        params[PARAM_ORIGIN_DOMAIN] = ",".join(params[PARAM_ORIGIN_DOMAIN])

    add_req = endpoints.AddRequest(params=params)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for cdn-service.
    """
    delete_req = endpoints.DeleteRequest(params=req.json)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for cdn-service.
    """
    params = req.json

    for p in [PARAM_CDN_EDGE, PARAM_ORIGIN_DOMAIN]:
        if p not in params:
            continue
        params[p] = ",".join(params[p])

    if PARAM_ORIGIN_HOST not in params:
        params[PARAM_ORIGIN_HOST] = "nO_ChANgE"


    set_req = endpoints.SetRequest(params=params)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
