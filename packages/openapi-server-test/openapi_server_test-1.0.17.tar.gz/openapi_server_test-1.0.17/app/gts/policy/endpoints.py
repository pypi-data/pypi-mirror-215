from dataclasses import dataclass
from typing import ClassVar, Dict, List
from grpc_instance_pool import Dingman_grpc_cli
from utils import checking_review, adding_labels

from app import common
from app.common.endpoints import Response

@dataclass
class ShowRequest(common.endpoints.ShowRequest):
    directive: ClassVar[str] = 'gts-policy'

@common.endpoints.logging_middleware("show", "gts-policy")
def show(cli: Dingman_grpc_cli, req: ShowRequest) -> Response:
    """Processes the user's request and returns a list of gts-policies.
    """
    return common.endpoints.call_dingman_for_show_cmd(cli, req.to_cmd(), req.get_search_kv())


@dataclass
class WriteRequest:
    cmd_type: ClassVar[str] = ""

    sub_op: str = None
    name: str = ""

    best_ipdb_first: bool = None
    best_only: bool = None
    high_weight_first: bool = None
    ipv6_translate: bool = None
    partial_match: bool = None
    region_with_continent: bool = None
    region_with_isp: bool = None
    use_iso_code: bool = None

    ecs_scope: int = None
    ecs_scope_ipv6: int = None
    ttl: int = None
    unmatch_ecs_scope: int = None
    unmatch_ecs_scope_ipv6: int = None
    max_answer: int = None

    region_map: str = None
    ipv6_prefix: str = None
    sticky_server: str = None

    selectors: List[Dict] = None
    labels: Dict = None

    para_dict: Dict = None  # To deprecate this field

    queue: str = None
    token: str = None

    def to_cmd(self) -> str:
        tokens = [self.cmd_type, f"gts-policy:{self.name}"]

        for key in [
            "best_ipdb_first", "best_only", "high_weight_first", "partial_match",
            "ipv6_translate", "region_with_continent", "region_with_isp",
            "use_iso_code", "ecs_scope", "ecs_scope_ipv6",
            "ttl", "unmatch_ecs_scope", "unmatch_ecs_scope_ipv6", "max_answer"]:
            if self.__getattribute__(key) is not None:
                tokens.append(f'{key.replace("_", "-")}:{str(self.__getattribute__(key)).lower()}')

        for key in ["region_map", "ipv6_prefix", "sticky_server", "sub_op", "queue", "token"]:
            if self.__getattribute__(key) is not None:
                tokens.append(f'{key.replace("_", "-")}:{str(self.__getattribute__(key))}')

        if self.selectors:
            selectors = [",".join([f"{k}={v}" for k, v in s.items()]) for s in self.selectors]
            selectors = "|".join(selectors)
            if selectors:
                tokens.append(f"selectors:{selectors}")

        if self.labels:
            tokens.append(adding_labels("", self.labels))

        if self.para_dict:
            arg = adding_labels("", self.para_dict).replace("labels:", "para_dict:")
            tokens.append(arg)

        cmd = " ".join(tokens)
        if not self.sub_op:  # only check review if handling main directive
            cmd = checking_review(None, cmd)

        return cmd

@dataclass
class AddRequest(WriteRequest):
    """AddRequest encapsulates fields adding a gts-policy or selectors
    """
    cmd_type: ClassVar[str] = "add"


@common.endpoints.logging_middleware("add", "gts-policy")
def add(cli: Dingman_grpc_cli, req: AddRequest) -> Response:
    """Processes the user's request and adds a new service group
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())

@dataclass
class DeleteRequest(WriteRequest):
    """DeleteRequest encapsulates fields deleting a gts-policy or selectors
    """
    cmd_type: ClassVar[str] = "del"

@common.endpoints.logging_middleware("delete", "gts-policy")
def delete(cli: Dingman_grpc_cli, req: DeleteRequest) -> Response:
    """Process the user's request and deletes a new service group
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())

@dataclass
class SetRequest(WriteRequest):
    """SetRequest encapsulates fields updating a gts-policy or selectors
    """
    cmd_type: ClassVar[str] = "set"

@common.endpoints.logging_middleware("set", "gts-policy")
def set(cli: Dingman_grpc_cli, req: SetRequest) -> Response:
    """Processes the user's request and sets a new service group
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())
