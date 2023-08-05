"""Transports contains serialisation & de-serialiastion glue code.

You will typically find code related to serialising/de-serialising the transport framework
requests/responses to/from the business objects here. By transport framework, we mean HTTP,
gRPC, Thrift etc. However, in this project, we mainly work with HTTP!
"""

import http

from flask import Response, jsonify
from grpc_instance_pool import Dingman_grpc_cli
from utils import make_dingman_error_response, get_token_from_request
from werkzeug.datastructures import ImmutableMultiDict

from typing import Callable

from . import consts
from . import errors
from .endpoints import call_general_dingman_cmd, call_dingman_for_show_cmd
from openapi_server.models.dingman_error import DingmanError

OP_SHOW_CMDS = ["show"]
OP_WRITE_CMDS = ["add", "set", "delete"]
KEY_TOKEN = "token"

##########
# Common #
##########

def rbac_token_middleware(op: str):
    def common_inner(next: Callable):
        def endpoint(cli: Dingman_grpc_cli, req):
            token = get_token_from_request(req)
            if not token:
                return next(cli, req)

            if op in OP_SHOW_CMDS:
                params_dict = {k: v for k, v in req.args.items()}
                params_dict[KEY_TOKEN] = token
                req.args = ImmutableMultiDict(params_dict)
            elif op in OP_WRITE_CMDS:
                req.json[KEY_TOKEN] = token

            return next(cli, req)

        return endpoint
    return common_inner


def handle_general_dingman_cmd(cli: Dingman_grpc_cli, cmd: str, process_resp: callable = None):
    """handle_general_dingman_cmd sends gRPC command through dingman cli,
    and process response using given handle function.
    Args:
        cli: dingman grpc client
        cmd: dingman gRPC request command
        process_resp: a function that processes response from dingman
    """
    resp = call_general_dingman_cmd(cli, cmd)
    return encode_response(resp, process_resp)


def handle_show_dingman_cmd(cli: Dingman_grpc_cli, cmd: str, search_kv_pair=('', ''), process_resp: callable = None):
    """handle_show_dingman_cmd sends gRPC command through dingman cli,
    and process response using given handle function.
    Args:
        cli: dingman grpc client
        cmd: dingman gRPC request command
        search_kv_pair: search key val pairs
        process_resp: a function that processes response from dingman
    """

    resp = call_dingman_for_show_cmd(cli, cmd, search_kv_pair)
    return encode_response(resp, process_resp)


def encode_response(resp, process_resp=None) -> Response:
    """encode_response converts service group response to Flask Response.
    """
    if resp.error:
        dm_err = DingmanError(consts.GRPC_STATUS_ERROR, resp.error.err_type, resp.error.err_code, str(resp.error))
        return make_dingman_error_response(dm_err, resp.error.http_status_code)
    data = {}
    if isinstance(resp.data, list) and len(resp.data) > 0:
        data = resp.data[0]
    elif isinstance(resp.data, dict):
        data = resp.data
    if data:
        status = data.get(consts.GRPC_KEY_STATUS, '')
        # handle error status from dingman
        if status == consts.GRPC_STATUS_ERROR:
            return process_error_status(data)
    if process_resp:
        return process_resp(data)
    # Default handler: remove error field from valid response
    d = resp.to_dict()
    del d["error"]
    return jsonify(d)


def process_error_status(data) -> Response:
    err_type = data.get(consts.GRPC_KEY_ERROR_TYPE, '')
    err_code = data.get(consts.GRPC_KEY_ERROR_CODE, errors.DEFAULT_ERR_CODE)
    err_msg = data.get(consts.GRPC_KEY_ERROR_REASON, '')
    http_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    if err_type == errors.BAD_REQUEST:
        http_code = http.HTTPStatus.BAD_REQUEST
    elif err_type == errors.UNAUTHORIZED:
        http_code = http.HTTPStatus.UNAUTHORIZED
    elif err_type == errors.NOT_FOUND:
        http_code = http.HTTPStatus.NOT_FOUND
    elif err_type == errors.CONFLICT:
        http_code = http.HTTPStatus.CONFLICT
    return make_dingman_error_response(DingmanError(consts.GRPC_STATUS_ERROR, err_type, err_code, err_msg), http_code)
