from dataclasses import dataclass
from typing import ClassVar
from grpc_instance_pool import Dingman_grpc_cli

from app import common
from app.common.endpoints import Response

@dataclass
class ShowRequest(common.endpoints.ShowRequest):
    directive: ClassVar[str] = 'gts-view'

@common.endpoints.logging_middleware("show", "gts-view")
def show(cli: Dingman_grpc_cli, req: ShowRequest) -> Response:
    return common.endpoints.call_dingman_for_show_cmd(cli, req.to_cmd(), req.get_search_kv())


@dataclass
class WriteRequest(common.endpoints.WriteRequest):
    directive: str = "gts-view"

@dataclass
class AddRequest(WriteRequest):
    """AddRequest encapsulates fields adding a gts-view
    """
    cmd_type: ClassVar[str] = "add"

@dataclass
class DeleteRequest(WriteRequest):
    """DeleteRequest encapsulates fields deleting a gts-view
    """
    cmd_type: ClassVar[str] = "del"

@dataclass
class SetRequest(WriteRequest):
    """SetRequest encapsulates fields updating a gts-view
    """
    cmd_type: ClassVar[str] = "set"


@common.endpoints.logging_middleware("add", "gts-view")
def add(cli: Dingman_grpc_cli, req: AddRequest) -> Response:
    """Processes the user's request and adds a new gts view
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())

@common.endpoints.logging_middleware("delete", "gts-view")
def delete(cli: Dingman_grpc_cli, req: DeleteRequest) -> Response:
    """Process the user's request and deletes a new gts view
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())

@common.endpoints.logging_middleware("set", "gts-view")
def set(cli: Dingman_grpc_cli, req: SetRequest) -> Response:
    """Processes the user's request and sets a new gts view
    """
    return common.endpoints.call_general_dingman_cmd(cli, req.to_cmd())
