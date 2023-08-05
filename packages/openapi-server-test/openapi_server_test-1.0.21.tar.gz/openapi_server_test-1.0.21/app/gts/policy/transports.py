from flask import Request, Response, jsonify
from typing import Dict
from grpc_instance_pool import Dingman_grpc_cli
from utils import get_labels_dic

from app import common
from . import endpoints

ENTITY_GTS_POLICY='gts-policy'
QUERY_PARAM_SUB_OP='sub-op'
QUERY_PARAM_QUEUE = "queue"
QUERY_PARAM_TOKEN = "token"
QUERY_PARAM_BEST_IPDB_FIRST="best_ipdb_first"
QUERY_PARAM_BEST_ONLY="best_only"
QUERY_PARAM_ECS_SCOPE="ecs_scope"
QUERY_PARAM_ECS_SCOPE_IPV6="ecs_scope_ipv6"
QUERY_PARAM_HIGH_WEIGHT_FIRST="high_weight_first"
QUERY_PARAM_IPV6_PREFIX="ipv6_prefix"
QUERY_PARAM_IPV6_TRANSLATE="ipv6_translate"
QUERY_PARAM_MAX_ANSWER="max_answer"
QUERY_PARAM_PARTIAL_MATCH="partial_match"
QUERY_PARAM_REGION_MAP="region_map"
QUERY_PARAM_REGION_WITH_CONTINENT="region_with_continent"
QUERY_PARAM_REGION_WITH_ISP="region_with_isp"
QUERY_PARAM_STICKY_SERVER="sticky_server"
QUERY_PARAM_TTL="ttl"
QUERY_PARAM_UNMATCH_ECS_SCOPE="unmatch_ecs_scope"
QUERY_PARAM_UNMATCH_ECS_SCOPE_IPV6="unmatch_ecs_scope_ipv6"
QUERY_PARAM_USE_ISO_CODE="use_iso_code"
QUERY_PARAM_SELECTORS="selectors"
QUERY_PARAM_PARA_DICT="para_dict"


@common.transports.rbac_token_middleware("show")
def show(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /show endpoint for gts policies.

    /show?gts-policy=my-gts-policy,queue=optional
    """
    show_req = endpoints.ShowRequest(params=req.args)
    show_resp = endpoints.show(cli, show_req)
    return common.transports.encode_response(show_resp)

def decode_req_body_to_params_dict(req: Request) -> Dict:
    body = req.json

    labels = get_labels_dic(body)
    if not labels:
        labels = body.get('labels', None)

    return dict(
        name=body.get(ENTITY_GTS_POLICY, ''),
        sub_op=body.get(QUERY_PARAM_SUB_OP, None),
        queue=body.get(QUERY_PARAM_QUEUE, None),
        token=body.get(QUERY_PARAM_TOKEN, None),
        best_ipdb_first=body.get(QUERY_PARAM_BEST_IPDB_FIRST, None),
        best_only=body.get(QUERY_PARAM_BEST_ONLY, None),
        ecs_scope=body.get(QUERY_PARAM_ECS_SCOPE, None),
        ecs_scope_ipv6=body.get(QUERY_PARAM_ECS_SCOPE_IPV6, None),
        high_weight_first=body.get(QUERY_PARAM_HIGH_WEIGHT_FIRST, None),
        ipv6_prefix=body.get(QUERY_PARAM_IPV6_PREFIX, None),
        ipv6_translate=body.get(QUERY_PARAM_IPV6_TRANSLATE, None),
        max_answer=body.get(QUERY_PARAM_MAX_ANSWER, None),
        partial_match=body.get(QUERY_PARAM_PARTIAL_MATCH, None),
        region_map=body.get(QUERY_PARAM_REGION_MAP, None),
        region_with_continent=body.get(QUERY_PARAM_REGION_WITH_CONTINENT, None),
        region_with_isp=body.get(QUERY_PARAM_REGION_WITH_ISP, None),
        sticky_server=body.get(QUERY_PARAM_STICKY_SERVER, None),
        ttl=body.get(QUERY_PARAM_TTL, None),
        unmatch_ecs_scope=body.get(QUERY_PARAM_UNMATCH_ECS_SCOPE, None),
        unmatch_ecs_scope_ipv6=body.get(QUERY_PARAM_UNMATCH_ECS_SCOPE_IPV6, None),
        use_iso_code=body.get(QUERY_PARAM_USE_ISO_CODE, None),
        selectors=body.get(QUERY_PARAM_SELECTORS, None),
        labels=labels,
        para_dict=body.get(QUERY_PARAM_PARA_DICT, None)
    )


def decode_add_request(req: Request) -> endpoints.AddRequest:
    params = decode_req_body_to_params_dict(req)
    return endpoints.AddRequest(**params)

@common.transports.rbac_token_middleware("add")
def add(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /add endpoint for gts policies.
    """
    add_req = decode_add_request(req)
    add_resp = endpoints.add(cli, add_req)
    return common.transports.encode_response(add_resp)

def decode_delete_request(req: Request) -> endpoints.DeleteRequest:
    body = req.json
    params = dict(
        name=body.get(ENTITY_GTS_POLICY, ''),
        sub_op=body.get(QUERY_PARAM_SUB_OP, None),
        queue=body.get(QUERY_PARAM_QUEUE, None),
        token=body.get(QUERY_PARAM_TOKEN, None),
        selectors=body.get(QUERY_PARAM_SELECTORS, None),
    )
    return endpoints.DeleteRequest(**params)


@common.transports.rbac_token_middleware("delete")
def delete(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /delete endpoint for gts policies.
    """
    delete_req = decode_delete_request(req)
    delete_resp = endpoints.delete(cli, delete_req)
    return common.transports.encode_response(delete_resp)

def decode_set_request(req: Request) -> endpoints.SetRequest:
    params = decode_req_body_to_params_dict(req)
    return endpoints.SetRequest(**params)

@common.transports.rbac_token_middleware("set")
def set(cli: Dingman_grpc_cli, req: Request) -> Response:
    """Processes a request on the /set endpoint for gts policies.
    """

    set_req = decode_set_request(req)
    set_resp = endpoints.set(cli, set_req)
    return common.transports.encode_response(set_resp)
