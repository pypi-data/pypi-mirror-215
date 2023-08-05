from flask import Request, Response
from grpc_instance_pool import Dingman_grpc_cli

from app import common
from . import endpoints

ENTITY_REGION="region"

@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for region.
    """
    show_req = endpoints.ShowRequest(params=req.args)
    show_resp = endpoints.show(cli, show_req)
    return common.transports.encode_response(show_resp)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for region.
    """
    add_req = endpoints.AddRequest(params=req.json)
    add_req.merge_labels()
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for region.
    """
    delete_req = endpoints.DeleteRequest(params=req.json)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for region.
    """
    set_req = endpoints.SetRequest(params=req.json)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
