import json

from dataclasses import dataclass, field, asdict
from grpc_instance_pool import Dingman_grpc_cli
from typing import Dict, Callable, ClassVar
from utils import checking_review, adding_labels, get_labels_dic, show_search_handler

from . import consts
from . import errors

KEY_SUB_OP = "sub-op"
KEY_LABELS = "labels"
SEARCH_KEY = 'search-key'
SEARCH_VAL = 'search-val'


def logging_middleware(op: str, directive: str):
    def common_inner(next: Callable):
        def endpoint(cli: Dingman_grpc_cli, req):
            resp = next(cli, req)
            if resp.error is not None:
                print(f"op: {op}, directive: {directive}, error: {str(resp.error)}, data: {resp.data}")
            return resp
        return endpoint
    return common_inner

@dataclass
class ShowRequest:
    directive: ClassVar[str] = ''
    params: Dict[str, str] = field(default_factory=lambda: {})

    def merge_labels(self):
        prefixed_labels = get_labels_dic(self.params)
        self.params['labels'] = prefixed_labels
        for k in prefixed_labels.keys():
            del self.params[f"label.{k}"]

    def to_cmd(self) -> str:
        self.params = {k: v for k, v in self.params.items()}
        self.merge_labels()

        tokens = ["show", f'{self.directive}:{self.params.get(self.directive)}']
        tokens += [
            f"{k}:{v}" for k, v in self.params.items()
            if k not in [self.directive, KEY_LABELS, SEARCH_KEY, SEARCH_VAL]]

        if self.params.get(KEY_LABELS):
            tokens.append(adding_labels("", self.params.get(KEY_LABELS)))
        cmd = " ".join(tokens)
        return cmd

    def get_search_kv(self) -> (str, str):
        search_key = self.params.get(SEARCH_KEY, '')
        search_val = self.params.get(SEARCH_VAL, '')
        return search_key, search_val


@dataclass
class WriteRequest:
    cmd_type: ClassVar[str] = ""
    directive: str = ""
    params: Dict[str, str] = field(default_factory=lambda: {})

    def merge_labels(self):
        prefixed_labels = get_labels_dic(self.params)
        if 'labels' in self.params:
            self.params['labels'] = {**self.params['labels'], **prefixed_labels}
        else:
            self.params['labels'] = prefixed_labels
        for k in prefixed_labels.keys():
            del self.params[f"label.{k}"]

    def to_cmd(self) -> str:
        self.merge_labels()

        tokens = [self.cmd_type, f'{self.directive}:{self.params.get(self.directive)}']
        tokens += [
            f"{k}:{v}" for k, v in self.params.items()
            if k not in [self.directive, KEY_LABELS]]

        if self.params.get(KEY_LABELS):
            tokens.append(adding_labels("", self.params.get(KEY_LABELS)))

        cmd = " ".join(tokens)

        # If sub-op is present, do not checking_review
        if KEY_SUB_OP not in self.params:
            cmd = checking_review(None, cmd)
        return cmd

@dataclass
class Response:
    data: Dict = field(default_factory=lambda: {})
    error: Exception = None

    def to_dict(self) -> Dict:
        return asdict(self)


def run_dingman_cmd(cli: Dingman_grpc_cli, cmd: str) -> Dict:
    """Executes the dingman command by sending it to upstream gRPC server.

    Raises GRPCUpstreamError if network connection cannot be made to upstream gRPC server
    Raises InvalidGRPCResponseError if returned data is not valid JSON
    """
    print(f'dingman cmd: {cmd}')
    try:
        grpc_resp = cli.run(cmd)
    except Exception as e:
        raise errors.GRPCUpstreamError(str(e))

    # JSON should be valid
    try:
        grpc_resp = json.loads(grpc_resp)
    except Exception as e:
        raise errors.InvalidGRPCResponseError('invalid JSON returned from grpc')
    return grpc_resp


def call_dingman_for_show_cmd(cli: Dingman_grpc_cli, cmd: str, search_kv_pair=('', '')) -> Response:
    try:
        grpc_resp = run_dingman_cmd(cli, cmd)
    except Exception as e:
        return Response(error=e)
    # Not all responses contain `data` key, so we immediately return those
    if consts.GRPC_KEY_DATA not in grpc_resp:
        data = grpc_resp
    else:
        data = grpc_resp.get(consts.GRPC_KEY_DATA)
    search_key, search_val = search_kv_pair
    return Response(show_search_handler(data, search_key, search_val))


def call_general_dingman_cmd(cli: Dingman_grpc_cli, cmd: str) -> Response:
    try:
        grpc_resp = run_dingman_cmd(cli, cmd)
    except errors.DingmanGRPCError as e:
        return Response(error=e)

    # Not all responses contain `data` key, so we immediately return those
    if consts.GRPC_KEY_DATA not in grpc_resp:
        return Response(data=grpc_resp)

    # If it has data, it cannot be empty
    try:
        raise_if_resp_empty_data(grpc_resp)
    except errors.InvalidGRPCResponseError as e:
        return Response(error=e)
    return Response(data=grpc_resp.get(consts.GRPC_KEY_DATA))


def raise_if_resp_empty_data(grpc_resp: Dict):
    """Raises InvalidGRPCResponseError if grpc_dict has an empty data array element.
    """
    if len(grpc_resp.get(consts.GRPC_KEY_DATA, [])) == 0:
        raise errors.InvalidGRPCResponseError('empty data returned from grpc')
