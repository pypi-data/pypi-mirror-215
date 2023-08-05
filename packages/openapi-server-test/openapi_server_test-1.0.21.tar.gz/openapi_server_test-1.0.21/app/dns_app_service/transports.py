from flask import Request, Response
from grpc_instance_pool import Dingman_grpc_cli

from app import common
from . import endpoints

ENTITY_DNS_APP_SERVICE="dns-app-service"

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for dns app service.
    """
    add_req = endpoints.AddRequest(params=req.json)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)


@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for dns app service.
    """
    set_req = endpoints.SetRequest(params=req.json)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
