from dataclasses import dataclass
from typing import ClassVar
from grpc_instance_pool import Dingman_grpc_cli

from app import common
from app.common.endpoints import Response

@dataclass
class ShowRequest(common.endpoints.ShowRequest):
    directive: ClassVar[str] = 'service-group'

@common.endpoints.logging_middleware("show", "service-group")
def show(cli: Dingman_grpc_cli, req: ShowRequest) -> Response:
    return common.endpoints.call_dingman_for_show_cmd(cli, req.to_cmd(), req.get_search_kv())


@dataclass
class WriteRequest(common.endpoints.WriteRequest):
    directive: str = "service-group"

@dataclass
class AddRequest(WriteRequest):
    """AddRequest encapsulates fields adding a service-group
    """
    cmd_type: ClassVar[str] = "add"

@dataclass
class DeleteRequest(WriteRequest):
    """DeleteRequest encapsulates fields deleting a service-group
    """
    cmd_type: ClassVar[str] = "del"

@dataclass
class SetRequest(WriteRequest):
    """SetRequest encapsulates fields updating a service-group
    """
    cmd_type: ClassVar[str] = "set"


@common.endpoints.logging_middleware("add", "service-group")
def add(cli: Dingman_grpc_cli, req: AddRequest) -> Response:
    """Processes the user's request and adds a new service group
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())

@common.endpoints.logging_middleware("delete", "service-group")
def delete(cli: Dingman_grpc_cli, req: DeleteRequest) -> Response:
    """Process the user's request and deletes a new service group
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())

@common.endpoints.logging_middleware("set", "service-group")
def set(cli: Dingman_grpc_cli, req: SetRequest) -> Response:
    """Processes the user's request and sets a new service group
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())
