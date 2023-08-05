from flask import Request, Response, jsonify
from grpc_instance_pool import Dingman_grpc_cli

import utils
from app import common
from . import endpoints

ENTITY_APP_SERVICE="app-service"
PARAM_DNS_DOMAIN="dns-domain"
PARAM_TEMPLATES="templates"
PARAM_IS_BASE64="isbase64"
PARAM_ENCODING="encoding"

@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for app-service.
    """
    show_req = endpoints.ShowRequest(params=req.args)
    show_resp = endpoints.show(cli, show_req)
    if "format" in show_req.params:
        return jsonify(show_resp.data)
    return common.transports.encode_response(show_resp)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for app-service.
    """
    params = req.json
    if PARAM_DNS_DOMAIN in params:
        params[PARAM_DNS_DOMAIN] = ",".join(params[PARAM_DNS_DOMAIN])

    add_req = endpoints.AddRequest(params=req.json)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for app-service.
    """
    delete_req = endpoints.DeleteRequest(params=req.json)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for app-service.
    """
    params = req.json
    if PARAM_DNS_DOMAIN in params:
        params[PARAM_DNS_DOMAIN] = ",".join(params[PARAM_DNS_DOMAIN])

    if PARAM_TEMPLATES in params and len(params[PARAM_TEMPLATES].keys()) > 0:
        tmpl_tks = []
        is_base64 = params.get(PARAM_IS_BASE64, "")
        encoding = params.get(PARAM_ENCODING, 'utf-8')
        if PARAM_ENCODING not in params:
            params[PARAM_ENCODING] = encoding

        for key in params[PARAM_TEMPLATES]:
            val = params[PARAM_TEMPLATES][key]
            if is_base64 == "True":
                tmpl_tks.append(f"{key}={val}")
            else:
                tmpl_tks.append(f"{key}={utils.base64_encode_string(val, encoding)}")
        params[PARAM_TEMPLATES] = ",".join(tmpl_tks)

    set_req = endpoints.SetRequest(params=params)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
