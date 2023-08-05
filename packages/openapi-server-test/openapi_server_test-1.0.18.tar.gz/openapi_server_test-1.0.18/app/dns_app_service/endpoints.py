from dataclasses import dataclass
from typing import ClassVar
from app.authdns_zone.endpoints import SetRequest
from grpc_instance_pool import Dingman_grpc_cli

from app import common
from app.common.endpoints import Response


@dataclass
class WriteRequest(common.endpoints.WriteRequest):
    directive: str = "dns-app-service"

@dataclass
class AddRequest(WriteRequest):
    """AddRequest encapsulates fields adding a dns-app-service
    """
    cmd_type: ClassVar[str] = "add"

@common.endpoints.logging_middleware("add", "dns-app-service")
def add(cli: Dingman_grpc_cli, req: AddRequest) -> Response:
    """Processes the user's request and adds a new dns-app-service
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())


@dataclass
class SetRequest(WriteRequest):
    """AddRequest encapsulates fields updating a dns-app-service
    """
    cmd_type: ClassVar[str] = "set"

@common.endpoints.logging_middleware("set", "dns-app-service")
def set(cli: Dingman_grpc_cli, req: SetRequest) -> Response:
    """Processes the user's request and sets a new dns-app-service
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())
